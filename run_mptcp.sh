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
topo_to_run=4
wl_to_run="one_to_one"

# ----- Sanity checks -----
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

# ----- Get arguments ------
#get topo
if [ "$1" = "all" ]
then
  topo_to_run=(4 6 8 10 12)
else
  if [ -n "$1" ] && [ $1 -ge 4 ]
  then
    topo_to_run=$1
  fi
fi

# get workload
if [ -n "$2" ]
then
  wl_to_run=$2
fi
if [ "$2" = "all" ]
then
  wl_to_run=('one_to_one' 'one_to_several' 'all_to_all')
fi

echo "Experiments to run..."
print_topo=''
for i in ${topo_to_run[*]}
do
  print_topo="$print_topo $i"
done
echo "Fat Tree topologies: k = $print_topo"

print_wl=''
for i in ${wl_to_run[*]}
do
  print_wl="$print_wl $i"
done
echo "Workloads: $print_wl"
echo

# create directory for plot output
mkdir -p plots



# ----- Run Mininet tests ------
for k in ${topo_to_run[*]} #4 6 8 10
do
  for workload in ${wl_to_run[*]} #one_to_one one_to_several all_to_all
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
python plot_cpu.py -f results/ft*/one_to_one/flows*/cpu_utilization.txt -o plots/cpu_util.png


