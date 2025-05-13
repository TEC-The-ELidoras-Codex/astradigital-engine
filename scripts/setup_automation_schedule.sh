#!/bin/bash
# Setup Airth News Automation Scheduling for Unix-based systems
# This script helps set up cron jobs for the Airth News Automation system

# Default values
TASK_NAME="Airth News Automation"
TIME_HOUR=8
TIME_MINUTE=0
MAX_AGE=1
MAX_TOPICS=3
STATUS="draft"
PUBLISH=false
NOTIFY=true

# Display help
show_help() {
    echo "Usage: $0 [options]"
    echo "Options:"
    echo "  -h, --help          Show this help message"
    echo "  -t, --time HH:MM    Set the time for the daily run (default: 08:00)"
    echo "  -a, --max-age N     Set maximum age in days for news articles (default: 1)"
    echo "  -n, --max-topics N  Set maximum number of topics to process (default: 3)"
    echo "  -s, --status STATUS Set WordPress publishing status (default: draft)"
    echo "  -p, --publish       Enable publishing to WordPress (default: disabled)"
    echo "  --no-notify         Disable email notifications (default: enabled)"
    exit 0
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        -h|--help)
            show_help
            ;;
        -t|--time)
            IFS=':' read -ra TIME_PARTS <<< "$2"
            TIME_HOUR=${TIME_PARTS[0]}
            TIME_MINUTE=${TIME_PARTS[1]}
            shift 2
            ;;
        -a|--max-age)
            MAX_AGE="$2"
            shift 2
            ;;
        -n|--max-topics)
            MAX_TOPICS="$2"
            shift 2
            ;;
        -s|--status)
            STATUS="$2"
            shift 2
            ;;
        -p|--publish)
            PUBLISH=true
            shift
            ;;
        --no-notify)
            NOTIFY=false
            shift
            ;;
        *)
            echo "Unknown option: $1"
            show_help
            ;;
    esac
done

# Get the script directory and project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_DIR="$( cd "$SCRIPT_DIR/.." &> /dev/null && pwd )"
AUTOMATION_SCRIPT="$PROJECT_DIR/scripts/airth_news_automation.py"

# Build parameters
PUBLISH_PARAM=""
if [ "$PUBLISH" = false ]; then
    PUBLISH_PARAM="--no-publish"
fi

NOTIFY_PARAM=""
if [ "$NOTIFY" = true ]; then
    NOTIFY_PARAM="--notify"
fi

# Create the cron job command
COMMAND="cd $PROJECT_DIR && python $AUTOMATION_SCRIPT --max-age $MAX_AGE --max-topics $MAX_TOPICS --status $STATUS $PUBLISH_PARAM $NOTIFY_PARAM >> $PROJECT_DIR/logs/cron_automation.log 2>&1"

# Display the setup
echo "Setting up cron job for Airth News Automation:"
echo "Time: $TIME_MINUTE $TIME_HOUR * * * (daily at $TIME_HOUR:$TIME_MINUTE)"
echo "Command: $COMMAND"

# Prepare the cron entry
CRON_ENTRY="$TIME_MINUTE $TIME_HOUR * * * $COMMAND"

# Add to crontab
(crontab -l 2>/dev/null | grep -v "Airth News Automation"; echo "# Airth News Automation"; echo "$CRON_ENTRY") | crontab -

# Check if successful
if [ $? -eq 0 ]; then
    echo "Cron job created successfully. It will run daily at $TIME_HOUR:$TIME_MINUTE."
    
    # Create a log file for verification
    LOG_FILE="$PROJECT_DIR/logs/schedule_setup.log"
    mkdir -p "$(dirname "$LOG_FILE")"
    
    echo "Airth News Automation Schedule" > "$LOG_FILE"
    echo "-----------------------------" >> "$LOG_FILE"
    echo "Scheduled on: $(date)" >> "$LOG_FILE"
    echo "Runs at: $TIME_HOUR:$TIME_MINUTE daily" >> "$LOG_FILE"
    echo "Command: $COMMAND" >> "$LOG_FILE"
    echo "" >> "$LOG_FILE"
    
    echo "Schedule information saved to logs/schedule_setup.log"
else
    echo "Failed to create cron job. Please check your permissions."
fi

# Show current crontab
echo -e "\nCurrent crontab:"
crontab -l
