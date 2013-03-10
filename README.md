datacenter_mptcp
================

CS244 Win 2013 - MPTCP

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
sudo apt-get install sysstat

### Starting with our image on EC2
We have made the following image available on EC2 [US West (Oregon)]:
`fooo`

### Starting with the CS244 image on EC2
Follow the insructions here:
`https://github.com/bocon13/mptcp_setup`

### Starting with a fresh Ubuntu 12.10 image on EC2
You will need to install Mininet, Matplotlib, TermColor, and sysstat. We have made the following scripts 
to install MPTCP and RiplPox (+ dependencies).

Follow the instructions here:
`https://github.com/bocon13/mptcp_setup`

Setting up the Test
-------------------

`git clone`

`git submodule init`

`git submodule update`


Running the test
----------------
sudo ./run_mptcp.sh
