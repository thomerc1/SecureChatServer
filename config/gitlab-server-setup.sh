#!/bin/bash

sudo apt-get update
sudo apt-get install -y curl openssh-server ca-certificates tzdata perl
curl https://packages.gitlab.com/install/repositories/gitlab/gitlab-ee/script.deb.sh | sudo bash
sudo EXTERNAL_URL="https://gitlab.labarge.dev" apt-get install gitlab-ee
sudo cat /etc/gitlab/initial_root_password



