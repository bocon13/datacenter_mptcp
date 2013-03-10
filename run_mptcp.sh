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
time=40
bw=1
queue_size=100
# Start POX controller with ECMP routing on FatTree-4
#echo "python ~/pox/pox.py --no-cli riplpox.riplpox --topo=ft,$k --routing=hashed --mode=reactive &> controller.out &"
#python ~/pox/pox.py --no-cli riplpox.riplpox --topo=ft,$k --routing=hashed --mode=reactive &> controller.out &
#pox_pid=$!


# Sanity checks
if [ ! -f $iperf ]
then
  echo "Patched iperf not installed! ... using regular iperf"
  echo "Install patched iperf using: ./iperf_patch/build-patched-iperf.sh"
  iperf='iperf'
  sleep 10
fi

if [ ! "$(ls -A util)" ]
then
  echo "You forgot initialize submodules"
  echo "Run: git submodule init && git submodule update"
  exit 1
fi

mkdir -p plots

# Run Mininet tests
#cd ~/mininet_mptcp
for k in 4 6 8 10
do
  for workload in one_to_one #one_to_several all_to_all
  do
      # run experiment
      python mptcp_test.py \
          --bw $bw \
          --queue $queue_size \
          --workload $workload \
          --topology ft$k \
          --time $time \
          --iperf $iperf
  
       # plot RTT
       python plot_ping.py -k $k -w $workload -f results/ft$k/$workload/*/client_ping* -o plots/ft$k-$workload-rtt.png
       # plot throughput
       python plot_hist.py -k $k -w $workload -t $time -f results/ft$k/$workload/*/client_iperf* results/ft$k/$workload/max_throughput.txt -o plots/ft$k-$workload-throughput.png
       # plot link util
       python plot_link_util.py -k $k -w $workload -f results/ft$k/$workload/*/link_util* -o plots/ft$k-$workload-link_util.png
       # plot queue size
       for f in {1..8}
       do
           python plot_queue.py -k $k -w $workload -f results/ft$k/$workload/flows$f/queue_size* -o plots/ft$k-$workload-flows$f-queue_size.png
       done
  done
done

# plot cpu utilization
python plot_cpu.py -w one_to_one -f results/ft*/one_to_one/flows*/cpu_utilization.txt -o plots/cpu_util.png


# Kills POX processes, remaining python processes
#killall -9 python
#kill $pox_pid 
