#!/bin/bash

# Exit on any failure
set -e

ctrlc() {
    killall -9 python
    mn -c
    exit
}

trap ctrlc SIGINT

iperf=~/iperf-patched/src/iperf

# Start POX controller with ECMP routing on FatTree-4
#echo "python ~/pox/pox.py --no-cli riplpox.riplpox --topo=ft,$k --routing=hashed --mode=reactive &> controller.out &"
#python ~/pox/pox.py --no-cli riplpox.riplpox --topo=ft,$k --routing=hashed --mode=reactive &> controller.out &
#pox_pid=$!

# Run Mininet tests
cd ~/mininet_mptcp
for k in 4 6 8 10 12
do
  for workload in one_to_one
  do
      python mptcp_test.py \
          --bw 1 \
          --queue 10 \
          --workload $workload \
          --topology ft$k \
          --time 10 \
          --iperf $iperf  
  done
done

# Kills POX processes, remaining python processes
#killall -9 python
#kill $pox_pid 
