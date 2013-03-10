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
#cd ~/mininet_mptcp
for k in 4 6 8 10
do
  for workload in one_to_one one_to_several all_to_all
  do
      # run experiment
      python mptcp_test.py \
          --bw 1 \
          --queue 100 \
          --workload $workload \
          --topology ft$k \
          --time 20 \
          --iperf $iperf
  
       # plot RTT
       python plot_ping.py -k $k -f results/ft$k/$workload/*/client_ping* -o plots/ft$k-$workload-rtt.png
       # plot throughput
       python plot_hist.py -k $k -f results/ft$k/$workload/*/client_iperf* results/ft$k/$workload/max_throughput.txt -o plots/ft$k-$workload-throughput.png
       # plot link util
       python plot_link_util.py -k $k -f results/ft$k/$workload/*/link_util* -o plots/ft$k-$workload-link_util.png
       # plot queue size
       for f in {1..8}
       do
           python plot_queue.py -k $k -f results/ft$k/$workload/flows$f/queue_size* -o plots/ft$k-$workload-flows$f-queue_size.png
       done
  done
done

# plot cpu utilization
python plot_cpu.py -f results/ft*/one_to_one/flows*/cpu_utilization.txt -o plots/cpu_util.png


# Kills POX processes, remaining python processes
#killall -9 python
#kill $pox_pid 
