#!/bin/bash
# Function to check if a port is in use
function is_port_in_use() {
    local port="$1"
    lsof -i :$port &> /dev/null
}

# Add a line break
echo ""

# Check if port 5000 is in use
if is_port_in_use 5000; then
    # Find all PIDs of the processes using port 5000 and kill them one by one
    pids=$(lsof -t -i :5000)
    if [ -n "$pids" ]; then
        echo -e "\e[33mPort 5000 is in use by the following PIDs: $pids. Killing the processes...\e[0m"
        for pid in $pids; do
            echo -e "\e[95mKilling process with PID $pid...\e[0m"
            if ps -p $pid > /dev/null; then
                kill "$pid"
                sleep 1 # Wait for one second before killing the next process
                if [ $? -eq 0 ]; then
                    echo -e "\e[32mProcess with PID $pid has been terminated.\e[0m"
                else
                    echo -e "\e[31mFailed to terminate process with PID $pid.\e[0m"
                fi
            else
                echo -e "\e[31mProcess with PID $pid is no longer running.\e[0m"
            fi
        done
    fi
fi

(
        # Check if lynx is installed
        if ! command -v lynx &>/dev/null; then
            echo "Error: Lynx is not installed. Please install Lynx and try again."
            exit 1
        fi
        
        sudo apt-get install -y lynx
        if [ $? -ne 0 ]; then
            echo "Error: Failed to install Lynx."
            exit 1
        fi
        
        source ./venv/bin/activate
        if [ $? -ne 0 ]; then
            echo "Error: Failed to activate virtual environment."
            exit 1
        fi
        
        echo -e "\e[1m\e[94mStarting Server\e[0m" # Light blue and bold
        nohup python app.py > /dev/null 2>&1 &
        if [ $? -ne 0 ]; then
            echo "Error: Failed to start the server."
            exit 1
        fi
        
        echo -e "\e[1m\e[94mStarted Secure Chat Server Successfully\e[0m" # Light blue and bold
        
        # Add a line break
        echo ""
        
        # Countdown timer
        for ((i=5; i>=1; i--)); do
            echo -e "\e[31mStarting test in $i seconds\e[0m"
            sleep 1
        done
        
        # Add a line break
        echo ""
        
        echo -e "\e[1m\e[94mTesting:\e[0m" # Light blue and bold
        
        # Dump the page and colorize it
        lynx -dump "https://crypt.labarge.dev" | sed 's/.*/\x1b[33m&\x1b[0m/' || {
            echo "Error: Failed to fetch the web page."
            exit 1
        }
        
        # Add a line break
        echo ""
        
        # Search for a specific pattern indicating success
        if lynx -dump "https://crypt.labarge.dev" | grep -q "Secure Chat Server"; then
            echo -e "\e[1m\e[94mThe Chat Server is up and running successfully, and forward public facing\e[0m" # Light blue and bold
	    echo ""
        else
            echo "Error: The Chat Server is not running as expected"
            exit 1
        fi
)

