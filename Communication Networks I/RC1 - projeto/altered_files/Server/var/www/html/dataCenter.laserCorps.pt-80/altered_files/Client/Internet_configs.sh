#!/bin/bash

sudo ip addr add 120.100.20.29/24 dev enp0s3
sudo ip route add default via 120.100.20.1