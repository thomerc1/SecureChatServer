#!/bin/bash
(
        source ./venv/bin/activate
        echo "Starting Server"
        nohup python app.py &
        echo "Started Secure Chat Server Successfully"
        echo "Testing: "
        output=$(curl -s "https://crypt.labarge.dev")
        echo "First 3 lines of curl output:"
        echo "$output" | head -n 3
        if [[ $output == *"<h1>Secure Chat Server</h1>"* ]]; then
            echo "The Chat Server is up and running successfully, and forward public facing"
        else
            echo "The Chat Server is not running as expected"
        fi
)
