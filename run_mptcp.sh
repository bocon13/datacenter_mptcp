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

mkdir -p plots

# Run Mininet tests
cd ~/mininet_mptcp
for k in 4 #6 8 10 12
do
  for workload in one_to_one
  do
      # run experiment
      python mptcp_test.py \
          --bw 1 \
          --queue 10 \
          --workload $workload \
          --topology ft$k \
          --time 10 \
          --iperf $iperf
  
       # plot RTT
       python plot_ping.py -k $k -f results/ft$k/$workload/*/client_ping* -o plots/ft$k-$workload-rtt.png
       # plot throughput
       python plot_hist.py -k $k -f results/ft$k/$workload/*/client_iperf* results/ft$k/$workload/max_throughput.txt -o plots/ft$k-$workload-throughput.png
       # plot link util
       # TODO

  done
done

# plot cpu utilization
python plot_cpu.py -f results/ft*/one_to_one/flows*/cpu_utilization.txt -o plots/cpu_util.png


# Kills POX processes, remaining python processes
#killall -9 python
#kill $pox_pid 
