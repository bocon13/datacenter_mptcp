#!/usr/bin/python
"""
This util file defines some helper functions for MPTCP
It is adapted from the Mininet MPTCP test file (mininet-tests/mptcp/mptcp_2hNs.py)
"""

import sys
from subprocess import Popen, PIPE
from time import sleep
import termcolor as T
import argparse

def sysctl_set(key, value):
    """Issue systcl for given param to given value and check for error."""
    p = Popen("sysctl -w %s=%s" % (key, value), shell=True, stdout=PIPE,
              stderr=PIPE)
    # Output should be empty; otherwise, we have an issue.  
    stdout, stderr = p.communicate()
    stdout_expected = "%s = %s\n" % (key, value)
    if stdout != stdout_expected:
        raise Exception("Popen returned unexpected stdout: %s != %s" %
                        (stdout, stdout_expected))
    if stderr:
        raise Exception("Popen returned unexpected stderr: %s" % stderr)


def set_enabled(enabled):
    """Enable MPTCP if true, disable if false"""
    e = 1 if enabled else 0
    lg.info("setting MPTCP enabled to %s\n" % e)
    sysctl_set('net.mptcp.mptcp_enabled', e)


def set_ndiffports(ports):
    """Set ndiffports, the number of subflows to instantiate"""
    lg.info("setting MPTCP ndiffports to %s\n" % ports)
    sysctl_set("net.mptcp.mptcp_ndiffports", ports)

''' 
Disables MPTCP and resets the number of ports to 1
'''
def reset():
    set_enabled(False)
    set_ndiffports(1)
