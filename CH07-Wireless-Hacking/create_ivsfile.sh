#!/bin/bash
# Instructor utility — regenerates weplab.ivs (part of Aircrack-ng).
# The resulting WEP key is 12:34:56:78:9A:BC:DE:F1:23:45:67:89:AB
# (that is the hex key 123456789ABCDEF123456789AB passed to -k).
# Running this OVERWRITES the committed weplab.ivs — the key stays the same,
# so the lab's expected output does not change.
makeivs-ng -b de:ad:be:ef:ca:fe -k 123456789ABCDEF123456789AB -w weplab.ivs
echo "IVS file 'weplab.ivs' created. WEP key = 12:34:56:78:9A:BC:DE:F1:23:45:67:89:AB"
