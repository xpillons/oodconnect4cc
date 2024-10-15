#!/bin/bash
# This script is based on the repository: https://github.com/puneet336/OOD-1.5_wrappers/tree/42011d75963986aca5e9e34173e2ae565358f6a6/openondemand/1.5/wrappers/slurm/bin
# This is replaced by Ansible
SERVER_IP=LOGIN_IP
#echo $(pwd) >> ${USER}_logs.txt


ssh $SERVER_IP "squeue $@"
EXIT_CODE=$(echo $?)

exit $EXIT_CODE
