#!/bin/bash

# Exit on any failure
set -e

ctrlc() {
    killall -9 python
    mn -c
    exit
}

trap ctrlc SIGINT

iperf=iperf

# Start POX controller with ECMP routing on FatTree-4
cd ~
screen -d -m python ~/pox/pox.py riplpox.riplpox --topo=ft,4 --routing=hashed --mode=proactive

# Run Mininet tests
cd ~/mininet_mptcp
for workload in one_to_one
do
    python mptcp_test.py --bw 100 \
        --delay 1 \
        --workload $workload \
        --topology ft4 \
        --iperf $iperf
done

# Kills POX processes, remaining python processes
killall -9 python
