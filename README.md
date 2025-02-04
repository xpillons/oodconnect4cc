# CycleCloud OpenOnDemand Connection App

## Introduction

This Open OnDemand application allows users to connect to a CycleCloud cluster through the Open OnDemand GUI. It is designed to be used with the CycleCloud-OpenOnDemand project [INSERT GIT URL].

The application uses a Flask-based web app to run Ansible on the OOD server and configure the cluster connection.

## Prerequisites

Ensure you have a cluster deployed with NFS home directories mountable by the OOD server. Note that per-cluster home directories are currently not supported <https://github.com/OSC/ondemand/issues/2492>

The CycleCloud-OpenOnDemand project will configure all other prerequisites for you.

This app is compatible with:

- SLURM clusters
- AlmaLinux 8
- Ubuntu 22.04

If you are running this outside of the project, ensure the following:

- Python is installed
- Flask, PyYAML, and Ansible are installed
- A user account with passwordless sudo on the OOD server
- SELinux is disabled (as it runs from within httpd/Apache and makes local changes, SELinux prevents this)
- Open OnDemand is installed and configured with authentication

For production environments, it is recommended to change the Flask secret key in `app.py`. Refer to the Flask Secret Key documentation.
    [Flask Secret key documentation](https://flask.palletsprojects.com/en/2.3.x/config/)

## Customisation

The cluster configuration is minimal and based on the Open OnDemand installation guide.

Modifications to the `cluster.yml` file generated with Ansible can be made in `Ansible/Cluster_setup.yml`. Refer to the OOD Documentation.

To accommodate multi-cluster environments, connections to the SLURM clusters are managed through wrapper scripts. These scripts are run instead of the standard SLURM commands:

- `SBATCH`
- `SCANCEL`
- `SCONTROL`
- `SQUEUE`
- `SINFO`
- `SACCTMGR`

Wrapper scripts are per cluster and can be customized once copied into their respective folder: `/usr/local/bin/{{ cluster_name }}_wrapper_scripts/`. Wrapper scripts can contain any valid shell commands that will be run before SSH to the login node and running `SBATCH`.

[OOD Documentation on wrapper scripts](https://osc.github.io/ood-documentation/latest/installation/resource-manager/bin-override-example.html)

The wrapper scripts are based on this discussion on the OOD discourse link and modify the scripts at GitHub link.
 <https://discourse.openondemand.org/t/ood-portal-with-slurm-as-a-resource-manager-two-clusters/692> and modify the scripts at  <https://github.com/puneet336/OOD-1.5_wrappers/tree/42011d75963986aca5e9e34173e2ae565358f6a6/openondemand/1.5/wrappers/slurm/bin>
