#!/bin/bash

# Ensure the script is run as root
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi

# Initialize an empty JSON object
echo "{"

# Flag to handle comma placement in JSON
first=true

# Read the output of networksetup and process each Hardware Port block
networksetup -listallhardwareports | while IFS= read -r line; do
    if [[ "$line" == "Hardware Port:"* ]]; then
        # Extract Hardware Port name (optional, not used in JSON)
        hardware_port=$(echo "$line" | awk -F": " '{print $2}')
    elif [[ "$line" == "Device:"* ]]; then
        # Extract Device identifier (e.g., en0, en1)
        device=$(echo "$line" | awk -F": " '{print $2}')
        
        # Retrieve the media status for the device
        link_speed=$(networksetup -getMedia "$device" 2>/dev/null | awk -F": " '{print $2}')
        
        # If link_speed is empty, set it to "Unknown"
        if [ -z "$link_speed" ]; then
            link_speed="Unknown"
        fi
        
        # Escape special characters in device and link_speed
        device_escaped=$(printf '%s' "$device" | sed 's/\\/\\\\/g; s/"/\\"/g')
        link_speed_escaped=$(printf '%s' "$link_speed" | sed ':a; N; $!ba; s/\\/\\\\/g; s/"/\\"/g; s/\n/ /g')  # Replace \n with a space

        # Handle comma placement
        if [ "$first" = true ]; then
            first=false
        else
            echo ","
        fi
        
        # Output the JSON key-value pair
        echo "  \"$device_escaped\": \"$link_speed_escaped\""
    fi
done

# Close the JSON object
echo
echo "}"
