This script performs the following steps:

1. Updates the package lists for upgrades and new package installations.
2. Installs `python-is-python3` package which sets python command to run Python 3.
3. Installs `git` for version control.
4. Clones the SecureChatServer repository from GitHub.
5. Installs `python3-venv` for creating virtual environments.
6. Navigates into the cloned repository, creates a virtual environment and activates it.
7. Installs the Python dependencies listed in the `dependencies.txt` file.
8. Installs `nginx` for serving the application.
9. Creates a new nginx site configuration for the domain `crypt.labarge.dev`.
10. Enables the nginx site by creating a symbolic link to the sites-enabled directory.
11. Tests the nginx configuration to make sure there are no syntax errors.
12. Restarts nginx to apply the new configuration.
13. Installs Certbot for managing SSL certificates.
14. Obtains an SSL certificate for the domain `crypt.labarge.dev` using Certbot.
15. Runs the Python application using the command `python app.py`.
16. End state: https://crypt.labarge.dev shows our group's chat server live.
