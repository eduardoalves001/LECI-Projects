#!/bin/bash
sudo ip link set up dev enp0s3
sudo ip addr add 120.100.20.29/24 dev enp0s3
sudo ip route add default via 120.100.20.1

sudo ip -6 addr add 2312:100:a199:aaee::29/64 dev enp0s3

