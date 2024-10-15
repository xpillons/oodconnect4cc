#!/bin/bash
# This script is based on the repository: https://github.com/puneet336/OOD-1.5_wrappers/tree/42011d75963986aca5e9e34173e2ae565358f6a6/openondemand/1.5/wrappers/slurm/bin
# This is replaced by Ansible
SERVER_IP=LOGIN_IP
#echo $(pwd) >> ${USER}_logs.txt

# Define the home directory paths for Open OnDemand and the shared home directory
home_dir_OOD=/home/${USER}
shared_home_dir=/shared/home/${USER}

# Get the current working directory
current_dir=$(pwd)

# Check if the current directory is within the OOD home directory but not the shared home directory
if [[ $current_dir == *$home_dir_OOD* ]] && [[ $current_dir != *$shared_home_dir* ]]; then
        actual_home="${current_dir/"$home_dir_OOD"/$shared_home_dir}"
        # Replace the OOD home directory path with the shared home directory path
fi


#echo $(pwd) >> ${USER}
# Execute the sbatch command on the server with the actual home directory as the working directory
ssh $SERVER_IP "sbatch --chdir $actual_home $@"
# Exit the script with the captured exit code
EXIT_CODE=$(echo $?)
exit $EXIT_CODE

