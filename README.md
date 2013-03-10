Improving Datacenter Performance using MPTCP
============================================
CS244: Win 2013

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

### Starting with our image on EC2
**This is the easiest way to get started.**

We have made the following image available on EC2 [US West (Oregon)]:
`CS244-Mininet-MPTCP`

TODO: size recommendations


### Starting with the CS244 image on EC2
TODO:

Follow the insructions here:
`https://github.com/bocon13/mptcp_setup`

### Starting with a fresh Ubuntu 12.10 image on EC2
You will need to install Mininet, Matplotlib, TermColor, and sysstat. We have made the following scripts 
to install MPTCP and RiplPox (+ dependencies).

Then, follow the instructions here to install MPTCP, RiplPox, and sysstat:
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

The results are in the **plots** directory.
