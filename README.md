Improving Datacenter Performance using MPTCP
============================================
*CS244: Win 2013*

The goal of this project is to use Mininet to reproduce the results of: 
_Improving Datacenter Performance and Robustness with Multipath TCP_
by Raiciu et al. which appeared in SIGCOMM'11.

Authors: Brian O'Connor & Ryan Wilson

Preliminaries
-------------
This project has the following dependencies:
* Mininet 2.0
http://mininet.github.com/
* An MPTCP-enabled Linux kernel
http://mptcp.info.ucl.ac.be/
* RiplPox (and its dependencies)
https://github.com/brandonheller/riplpox
* Matplotlib
http://matplotlib.org/index.html
* TermColor
https://pypi.python.org/pypi/termcolor
* Sysstat
`sudo apt-get install sysstat`

### Starting with our image on EC2 (Recommended)
**This is the easiest way to get started.**

We have made the following image available on EC2 [US West (Oregon)]:
`CS244-Mininet-MPTCP`

You should use a `c1.xlarge` instance for the experiments.

If you use a `c1.medium` instance, make sure to turn off queue monitoring
and don't use a Fat Tree topology with greater than 6, unless your goal
is to max out the CPU.

### Starting with the CS244 image on EC2
Start will the following EC2 image: `CS244-Win13-Mininet`

Then, follow the instructions here:
`https://github.com/bocon13/mptcp_setup`

### Starting with a fresh Ubuntu 12.10 image on EC2
You will need to install Mininet, Matplotlib, TermColor, and sysstat on your own. 

We have made the following scripts to install MPTCP and RiplPox (+ dependencies):
`https://github.com/bocon13/mptcp_setup`

Setting up the Test
-------------------

Clone the code repository

`git clone https://github.com/bocon13/datacenter_mptcp.git`

Initialize the *util* submodule and clone it

`cd datacenter_mptcp`

`git submodule init`

`git submodule update`

If not using "CS244-Mininet-MPTCP" image, patch and install iperf:

`./iperf_patch/build-patched-iperf.sh`

Running the test
----------------
Use the following command to run the experiments:

`sudo ./run_mptcp.sh`

This will run the one-to-one workload (used in the paper) on a Fat Tree topology (k=4) with queue monitoring disabled.

#### Test options

Our test is capable of running various sized FatTree topologies and workloads.

You can specify them in the run command:
`sudo ./run_mptcp.sh <size of fat tree> <workload> <queue monitoring enabled>`

For `<size of fat tree>`, valid values are even integers >= 4. (default = 4)

For `<workload>`, valid values are: 
* one_to_one (default)
* one_to_several
* all_to_all

For `<queue monitoring enabled>`, valid values are `True` or `False` (default).

Examples:
* Run a Fat Tree topology (k=6) with one_to_one workload with queue monitoring disabled:
`sudo ./run_mptcp.sh 6`
* Run a Fat Tree topology (k=8) with all_to_all workload with queue monitoring disabled:
`sudo ./run_mptcp.sh 8 all_to_all`
* Run all workloads on various Fat Tree topologies: k = {4, 6, 8, 10, 12} with queue monitoring disabled:
`sudo ./run_mptcp.sh all all`
* Run a Fat Tree topology (k=4) with one_to_one workload with queue monitoring disabled:
`sudo ./run_mptcp.sh 4 one_to_one False`
* Run a Fat Tree topology (k=4) with one_to_one workload with queue monitoring enabled:
`sudo ./run_mptcp.sh 4 one_to_one True`


#### Observing your results
The results are graphs that are saved to the **plots** sub-directory.

Start a webserver on your EC2 instance (ensure that port 8000 is open):

`python -m SimpleHTTPServer &> /dev/null &`

Navigate to your server in your favorite web browser:

`http://<your ec2 instance name>:8000/`
