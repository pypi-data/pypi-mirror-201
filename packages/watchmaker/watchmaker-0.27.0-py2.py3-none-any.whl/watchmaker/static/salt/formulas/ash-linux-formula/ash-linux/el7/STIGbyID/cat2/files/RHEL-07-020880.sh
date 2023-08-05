#!/bin/sh
# Finding ID:	RHEL-07-020880
# Version:	RHEL-07-020880_rule
# SRG ID:	SRG-OS-000480-GPOS-00227
# Finding Level:	medium
# 
# Rule Summary:
#	Local initialization files must not execute world-writable programs.
#
# CCI-000366 
#    NIST SP 800-53 :: CM-6 b 
#    NIST SP 800-53A :: CM-6.1 (iv) 
#    NIST SP 800-53 Revision 4 :: CM-6 b 
#
#################################################################
# Standard outputter function
diag_out() {
   echo "${1}"
}

diag_out "----------------------------------------"
diag_out "STIG Finding ID: RHEL-07-020880"
diag_out "   Local initialization files must not"
diag_out "   execute world-writable programs."
diag_out "----------------------------------------"
