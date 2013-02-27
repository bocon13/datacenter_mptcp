# Kill any POX processes running
for p in $(ps aux | grep 'pox.py' | awk '{print $2}')
do
    kill $p
done

# Start POX controller with ECMP routing on FatTree-4
cd ~
screen -d -m python ~/pox/pox.py riplpox.riplpox --topo=ft,4 --routing=hashed --mode=reactive

# Run Mininet tests
cd mininet_mptcp
python mptcp_test.py

# Kill POX processes
for p in $(ps aux | grep 'pox.py' | awk '{print $2}')
do
    kill $p
done