#!/bin/bash
docker exec $1 -ti bash
# inside container
echo "LAB SECRET" > /var/secret_demo.txt
# or on host create a file and mount it under a path you can reach using fewer .. segments
