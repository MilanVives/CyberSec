# Advanced Shodan IoT Search Strings

## 1. Cameras & DVR Systems

    port:554 has_screenshot:true
    "Server: SQ-WEBCAM"
    "GoAhead-Webs" "webcam"
    "NETSurveillance Web"

## 2. Industrial IoT (SCADA / ICS)

    "Rockwell" "Automation" port:44818
    "Siemens" "S7" port:102
    "Modbus" port:502
    "BACnet" port:47808
    "ICS" "RTU" country:US

## 3. Smart Home Devices

    "Nest" port:443
    "Server: Boa" "webcam"
    port:80 "RV110W"
    "JetDirect" "printer"

## 4. IoT Devices With Default Credentials

    port:23 "default password"
    "root:root" port:23,2323
    "Telnet" "BusyBox" "Welcome"
    "Login:" "Password:" "admin"

## 5. Medical IoT Devices (OSINT Only)

    port:5900 "VNC" "Medical"
    "Infusion Pump" -test
    "medical imaging" port:104

## 6. Vehicle / Transportation IoT

    "AVTech" "Speed Dome"
    "gps" "tracker" port:8080
    "vehicle tracking" "login"

## 7. Smart Cities / Municipal IoT

    "Traffic Control" "SCADA"
    "Solar Inverter" port:502
    "Water Pump" port:502
    "City" "Weather Station" "login"

## 8. Consumer IoT Devices

    "Boa/0.93.15"
    "lighttpd/1.4" "IoT"
    "Server: mini_httpd"
    "HP Printer" "web server"

## 9. Zigbee / Z-Wave Gateways

    "Zigbee" port:1883
    "MQTT" "Home Assistant" -test
    "zwave" "controller"

## 10. Exposed MQTT Brokers

    port:1883 "MQTT"
    port:1883 "home"
    port:1883 "sensor"

## Fun / Unique Searches

    "Smart Refrigerator" OR "Fridge"
    "Jacuzzi" OR "spa" "control panel"
    "aquarium" port:80
    "irrigation" "controller"
    "pet feeder" "web"
