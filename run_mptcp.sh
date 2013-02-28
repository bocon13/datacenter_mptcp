#!/bin/bash

# Exit on any failure
set -e

kill_pox() {
    for p in $(ps aux | grep 'pox.py' | awk '{print $2}')
    do
        kill $p
    done
}

ctrlc() {
    killall -9 python
    mn -c
    exit
}

trap ctrlc SIGINT

iperf=~/iperf-patched/src/iperf

# Start POX controller with ECMP routing on FatTree-4
cd ~
screen -d -m python ~/pox/pox.py riplpox.riplpox --topo=ft,4 --routing=hashed --mode=reactive

# Run Mininet tests
cd ~/mininet_mptcp
for workload in one_to_one
do
    for num_subflows in {1..8}
    do
        python mptcp_test.py --bw 100 \
            --delay 1 \
            --nflows $num_subflows \
            --workload $workload \
            --topology ft4 \
            --iperf $iperf
    done
done

# Kill POX processes
kill_pox