#!/usr/bin/env python3
"""
Build chapter1_reference.pcap -- the fallback capture for the Chapter 1
Wireshark lab (Cybersecurity Architecture / ACS).

The file is SYNTHETIC: every frame is assembled here, not sniffed off a real
wire. Checksums, sequence numbers and timings are all valid, so Wireshark
dissects, reassembles and "Follow TCP Stream"s it exactly like a real capture.
Students who cannot generate their own traffic (no lab network, no root) use
this file instead.

Scenario, in capture order:
  1. ARP    who-has the gateway, and the reply
  2. DNS    A? neverssl.com  ->  34.223.124.45
  3. ICMP   4x echo request / echo reply to that address
  4. HTTP   GET /            ->  200 OK  (page fetch)
  5. HTTP   POST /login.php  ->  302     (credentials in cleartext)

Usage:  python3 make_reference_capture.py [output.pcap]
"""

import struct
import sys

# --- lab topology -----------------------------------------------------------
CLIENT_MAC = bytes.fromhex("080027aabbcc")   # Kali VM
ROUTER_MAC = bytes.fromhex("0a0027000001")   # gateway / DNS forwarder
CLIENT_IP  = "192.168.56.101"
ROUTER_IP  = "192.168.56.1"
SERVER_IP  = "34.223.124.45"                 # neverssl.com (plain HTTP on purpose)

START_TS = 1771232400.0                      # 2026-02-16 09:00:00 UTC


# --- checksum helpers -------------------------------------------------------
def checksum(data: bytes) -> int:
    """Standard RFC 1071 one's-complement sum, used by IP, ICMP, UDP and TCP."""
    if len(data) % 2:
        data += b"\x00"
    total = 0
    for i in range(0, len(data), 2):
        total += (data[i] << 8) + data[i + 1]
    while total >> 16:
        total = (total & 0xFFFF) + (total >> 16)
    return (~total) & 0xFFFF


def ip4(addr: str) -> bytes:
    return bytes(int(o) for o in addr.split("."))


# --- layer builders ---------------------------------------------------------
def ethernet(dst: bytes, src: bytes, ethertype: int, payload: bytes) -> bytes:
    frame = dst + src + struct.pack("!H", ethertype) + payload
    # NICs pad anything under the 60-byte minimum frame size (FCS excluded).
    if len(frame) < 60:
        frame += b"\x00" * (60 - len(frame))
    return frame


def ip_packet(src: str, dst: str, proto: int, payload: bytes, ident: int, ttl: int = 64) -> bytes:
    total_len = 20 + len(payload)
    header = struct.pack(
        "!BBHHHBBH4s4s",
        0x45, 0x00, total_len, ident, 0x4000, ttl, proto, 0, ip4(src), ip4(dst),
    )
    csum = checksum(header)
    header = header[:10] + struct.pack("!H", csum) + header[12:]
    return header + payload


def udp_datagram(src: str, dst: str, sport: int, dport: int, payload: bytes) -> bytes:
    length = 8 + len(payload)
    header = struct.pack("!HHHH", sport, dport, length, 0)
    pseudo = ip4(src) + ip4(dst) + struct.pack("!BBH", 0, 17, length)
    csum = checksum(pseudo + header + payload) or 0xFFFF
    return struct.pack("!HHHH", sport, dport, length, csum) + payload


def tcp_segment(src: str, dst: str, sport: int, dport: int,
                seq: int, ack: int, flags: int, payload: bytes = b"",
                window: int = 64240, options: bytes = b"") -> bytes:
    if len(options) % 4:
        options += b"\x00" * (4 - len(options) % 4)
    offset = (20 + len(options)) // 4
    header = struct.pack(
        "!HHIIBBHHH",
        sport, dport, seq, ack, offset << 4, flags, window, 0, 0,
    ) + options
    seg_len = len(header) + len(payload)
    pseudo = ip4(src) + ip4(dst) + struct.pack("!BBH", 0, 6, seg_len)
    csum = checksum(pseudo + header + payload)
    header = header[:16] + struct.pack("!H", csum) + header[18:]
    return header + payload


def dns_name(name: str) -> bytes:
    out = b""
    for label in name.split("."):
        out += bytes([len(label)]) + label.encode()
    return out + b"\x00"


# --- capture assembly -------------------------------------------------------
class Capture:
    def __init__(self):
        self.frames = []          # (timestamp, bytes)
        self.clock = START_TS
        self.ip_id = 0x1a00

    def tick(self, seconds: float) -> float:
        self.clock += seconds
        return self.clock

    def add(self, frame: bytes, gap: float = 0.0005):
        self.frames.append((self.tick(gap), frame))

    def next_id(self) -> int:
        self.ip_id = (self.ip_id + 1) & 0xFFFF
        return self.ip_id

    def from_client(self, proto: int, payload: bytes, dst: str, gap: float = 0.0005):
        pkt = ip_packet(CLIENT_IP, dst, proto, payload, self.next_id())
        self.add(ethernet(ROUTER_MAC, CLIENT_MAC, 0x0800, pkt), gap)

    def to_client(self, proto: int, payload: bytes, src: str, ttl: int = 64, gap: float = 0.0005):
        pkt = ip_packet(src, CLIENT_IP, proto, payload, self.next_id(), ttl=ttl)
        self.add(ethernet(CLIENT_MAC, ROUTER_MAC, 0x0800, pkt), gap)

    def write(self, path: str):
        with open(path, "wb") as fh:
            # pcap global header: magic, v2.4, no tz correction, snaplen, Ethernet
            fh.write(struct.pack("!IHHiIII", 0xA1B2C3D4, 2, 4, 0, 0, 65535, 1))
            for ts, frame in self.frames:
                fh.write(struct.pack("!IIII", int(ts), int(round((ts % 1) * 1e6)),
                                     len(frame), len(frame)))
                fh.write(frame)


def build_arp(cap: Capture):
    """Frames 1-2: the client resolves the gateway's MAC before sending anything."""
    request = struct.pack("!HHBBH", 1, 0x0800, 6, 4, 1) + \
        CLIENT_MAC + ip4(CLIENT_IP) + b"\x00" * 6 + ip4(ROUTER_IP)
    cap.add(ethernet(b"\xff" * 6, CLIENT_MAC, 0x0806, request), 0.0)

    reply = struct.pack("!HHBBH", 1, 0x0800, 6, 4, 2) + \
        ROUTER_MAC + ip4(ROUTER_IP) + CLIENT_MAC + ip4(CLIENT_IP)
    cap.add(ethernet(CLIENT_MAC, ROUTER_MAC, 0x0806, reply), 0.00031)


def build_dns(cap: Capture):
    """Frames 3-4: A? neverssl.com and the answer that drives everything after."""
    qname = dns_name("neverssl.com")
    question = qname + struct.pack("!HH", 1, 1)          # QTYPE A, QCLASS IN

    query = struct.pack("!HHHHHH", 0x1A2B, 0x0100, 1, 0, 0, 0) + question
    cap.from_client(17, udp_datagram(CLIENT_IP, ROUTER_IP, 51514, 53, query),
                    ROUTER_IP, gap=0.0412)

    answer = struct.pack("!HHHHHH", 0x1A2B, 0x8180, 1, 1, 0, 0) + question + \
        struct.pack("!HHHIH", 0xC00C, 1, 1, 60, 4) + ip4(SERVER_IP)
    cap.to_client(17, udp_datagram(ROUTER_IP, CLIENT_IP, 53, 51514, answer),
                  ROUTER_IP, gap=0.0186)


def build_icmp(cap: Capture):
    """Frames 5-12: ping -c 4, request and reply interleaved one second apart."""
    ident = 0x2F01
    # Linux ping: 56 data bytes -> 64-byte ICMP message.
    data = bytes(range(0x10, 0x10 + 40)) + b"\x00" * 16

    for seq in range(1, 5):
        echo = struct.pack("!BBHHH", 8, 0, 0, ident, seq) + data
        echo = echo[:2] + struct.pack("!H", checksum(echo)) + echo[4:]
        cap.from_client(1, echo, SERVER_IP, gap=1.0 if seq > 1 else 0.2)

        reply = struct.pack("!BBHHH", 0, 0, 0, ident, seq) + data
        reply = reply[:2] + struct.pack("!H", checksum(reply)) + reply[4:]
        cap.to_client(1, reply, SERVER_IP, ttl=52, gap=0.0238)


def http_exchange(cap: Capture, sport: int, request: bytes, response: bytes,
                  client_isn: int, server_isn: int, first_gap: float):
    """Full TCP conversation: handshake, one request, one response, teardown."""
    SYN, ACK, FIN, PSH = 0x02, 0x10, 0x01, 0x08
    mss = struct.pack("!BBH", 2, 4, 1460) + b"\x01\x01\x04\x02"   # MSS + SACK-permitted

    cseq, sseq = client_isn, server_isn

    def c2s(flags, payload=b"", gap=0.0005, opts=b""):
        cap.from_client(6, tcp_segment(CLIENT_IP, SERVER_IP, sport, 80,
                                       cseq, sseq if flags & ACK else 0,
                                       flags, payload, options=opts),
                        SERVER_IP, gap=gap)

    def s2c(flags, payload=b"", gap=0.0005, opts=b""):
        cap.to_client(6, tcp_segment(SERVER_IP, CLIENT_IP, 80, sport,
                                     sseq, cseq, flags, payload,
                                     window=65535, options=opts),
                      SERVER_IP, ttl=52, gap=gap)

    c2s(SYN, opts=mss, gap=first_gap)
    cseq += 1
    s2c(SYN | ACK, opts=mss, gap=0.0241)
    sseq += 1
    c2s(ACK, gap=0.0002)

    c2s(PSH | ACK, request, gap=0.0009)
    cseq += len(request)
    s2c(ACK, gap=0.0244)

    s2c(PSH | ACK, response, gap=0.0715)
    sseq += len(response)
    c2s(ACK, gap=0.0003)

    c2s(FIN | ACK, gap=0.0121)
    cseq += 1
    s2c(FIN | ACK, gap=0.0239)
    sseq += 1
    c2s(ACK, gap=0.0002)


def build_http_get(cap: Capture):
    """A plain page fetch -- the 'Follow HTTP Stream' exercise."""
    request = (
        b"GET / HTTP/1.1\r\n"
        b"Host: neverssl.com\r\n"
        b"User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0\r\n"
        b"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n"
        b"Accept-Language: en-US,en;q=0.5\r\n"
        b"Accept-Encoding: identity\r\n"
        b"Connection: keep-alive\r\n"
        b"Upgrade-Insecure-Requests: 1\r\n"
        b"\r\n"
    )
    body = (
        b"<!DOCTYPE html>\n<html>\n<head>\n<title>NeverSSL - Chapter 1 lab page</title>\n"
        b"<meta charset=\"utf-8\">\n</head>\n<body>\n"
        b"<h1>This page is served over plain HTTP.</h1>\n"
        b"<p>Everything you see here crossed the network in cleartext. "
        b"Anyone on the path could read it, and change it.</p>\n"
        b"<form action=\"/login.php\" method=\"post\">\n"
        b"  <input type=\"text\" name=\"username\">\n"
        b"  <input type=\"password\" name=\"password\">\n"
        b"  <input type=\"submit\" value=\"Log in\">\n"
        b"</form>\n</body>\n</html>\n"
    )
    response = (
        b"HTTP/1.1 200 OK\r\n"
        b"Date: Mon, 16 Feb 2026 09:00:02 GMT\r\n"
        b"Server: Apache/2.4.58 (Ubuntu)\r\n"
        b"Content-Type: text/html; charset=UTF-8\r\n"
        b"Content-Length: " + str(len(body)).encode() + b"\r\n"
        b"Cache-Control: no-store\r\n"
        b"\r\n"
    ) + body
    http_exchange(cap, 43518, request, response, 0x5C2A1000, 0x91B33000, first_gap=0.6)


def build_http_post(cap: Capture):
    """The payoff: a login posted in cleartext, recoverable with one filter."""
    form = b"username=student&password=Vives2026!&submit=Log+in"
    request = (
        b"POST /login.php HTTP/1.1\r\n"
        b"Host: neverssl.com\r\n"
        b"User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0\r\n"
        b"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n"
        b"Content-Type: application/x-www-form-urlencoded\r\n"
        b"Content-Length: " + str(len(form)).encode() + b"\r\n"
        b"Origin: http://neverssl.com\r\n"
        b"Referer: http://neverssl.com/\r\n"
        b"Connection: keep-alive\r\n"
        b"\r\n"
    ) + form
    response = (
        b"HTTP/1.1 302 Found\r\n"
        b"Date: Mon, 16 Feb 2026 09:00:04 GMT\r\n"
        b"Server: Apache/2.4.58 (Ubuntu)\r\n"
        b"Location: http://neverssl.com/welcome.php\r\n"
        b"Set-Cookie: PHPSESSID=8f14e45fceea167a5a36dedd4bea2543; path=/\r\n"
        b"Content-Length: 0\r\n"
        b"\r\n"
    )
    http_exchange(cap, 43520, request, response, 0x7D0E4000, 0xA4F12000, first_gap=1.4)


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "chapter1_reference.pcap"
    cap = Capture()
    build_arp(cap)
    build_dns(cap)
    build_icmp(cap)
    build_http_get(cap)
    build_http_post(cap)
    cap.write(out)
    print(f"Wrote {out}: {len(cap.frames)} frames, "
          f"{sum(len(f) for _, f in cap.frames)} bytes on the wire.")


if __name__ == "__main__":
    main()
