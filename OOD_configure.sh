#!/bin/bash
echo "$@"
PATH=$PATH:/usr/local/bin

export ANSIBLE_VERBOSITY=2

if [ "$1" == "Home" ]; then
    ansible-playbook Ansible/homedir.yml
    exit_code=$?
fi

if [ "$1" == "Cluster" ]; then
    ansible-playbook Ansible/cluster.yml
    exit_code=$?
fi

exit $exit_code