#!/bin/bash

# Exit on any failure
set -e

ctrlc() {
    killall -9 python
    mn -c
    exit
}

trap ctrlc SIGINT

k=8
iperf=~/iperf-patched/src/iperf

# Start POX controller with ECMP routing on FatTree-4
echo "python ~/pox/pox.py --no-cli riplpox.riplpox --topo=ft,$k --routing=hashed --mode=reactive &> controller.out &"
python ~/pox/pox.py --no-cli riplpox.riplpox --topo=ft,$k --routing=hashed --mode=reactive &> controller.out &

# Run Mininet tests
cd ~/mininet_mptcp
for workload in one_to_one
do
    python mptcp_test.py --bw 2 \
        --delay 1 \
        --workload $workload \
        --topology ft$k \
        --iperf $iperf
done

# Kills POX processes, remaining python processes
killall -9 python
