#!/bin/bash

# Author: Alexander La Barge 
# Group: A
# Date: Nov 23'
# Project: Secure Chat Server
# Platform: Debian Linux GitLab
#
# Description:
# This script automates the installation of GitLab Enterprise Edition on a Debian-based system.
# It performs system updates, installs necessary dependencies, sets up the GitLab repository,
# and installs GitLab EE. After installation, it displays the initial root password for GitLab.
#
# Usage:
# Run this script as a root privileges. This requires internet access for package manager 
# installations. Modify the EXTERNAL_URL to match desired URL for GitLab. After running the
# script, access GitLab through the provided URL and login using the displayed root password.
#
# Note:
# This script is intended for quick setups and should be reviewed for security and compliance
# with your organization's policies before use in a production environment.


sudo apt-get update
sudo apt-get install -y curl openssh-server ca-certificates tzdata perl
curl https://packages.gitlab.com/install/repositories/gitlab/gitlab-ee/script.deb.sh | sudo bash
sudo EXTERNAL_URL="https://gitlab.labarge.dev" apt-get install gitlab-ee
sudo cat /etc/gitlab/initial_root_password



