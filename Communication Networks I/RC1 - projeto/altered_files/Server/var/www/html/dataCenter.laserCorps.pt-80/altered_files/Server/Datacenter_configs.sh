#!/bin/bash

#sudo ip addr del 172.26.5.10/24 dev enp0s3
sudo ip addr add 198.137.170.196/29 dev enp0s3
sudo ip route add default via 198.137.170.193

