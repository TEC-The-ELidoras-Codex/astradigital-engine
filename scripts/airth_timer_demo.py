#!/usr/bin/env python3
"""
Demo script for Airth's Pomodoro timer functionality.
This script shows how to interact with Airth's timer features.
"""
import os
import sys
import time
import argparse
from datetime import datetime

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the Airth agent
from src.agents import AirthAgent

def format_response(response):
    """Format the agent's response for display."""
    if "airth_response" in response:
        return response["airth_response"]
    elif "message" in response:
        return response["message"]
    else:
        return str(response)

def main():
    """Run a demo of Airth's timer functionality."""
    parser = argparse.ArgumentParser(description='Demo Airth\'s timer functionality')
    parser.add_argument('--command', '-c', help='Timer command to execute')
    parser.add_argument('--interactive', '-i', action='store_true', 
                       help='Run in interactive mode')
    parser.add_argument('--aws', '-a', action='store_true',
                       help='Use AWS for timer persistence')
    
    args = parser.parse_args()
    
    # Initialize Airth agent
    config_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config')
    airth = AirthAgent(config_dir)
    
    # Override AWS setting if specified
    if args.aws:
        airth.use_aws_timers = True
        print("Using AWS for timer persistence")
    
    # If a command was provided, execute it and exit
    if args.command:
        response = airth.respond_to_timer_command(args.command)
        print(format_response(response))
        
        # If timer was started, wait for it to complete
        if response.get("success", False) and response.get("timer_type") in ["countdown", "pomodoro"]:
            try:
                while True:
                    # Check timer status every second
                    time.sleep(1)
                    status = airth.get_timer_status()
                    if not status.get("active_timers"):
                        print("\nTimer completed!")
                        break
                    
                    # Show a simple progress indicator
                    timer = status["active_timers"][0]
                    if "time_remaining" in timer:
                        sys.stdout.write(f"\rTimer: {timer['time_remaining']} remaining")
                        sys.stdout.flush()
            except KeyboardInterrupt:
                print("\nDemo interrupted. Cancelling timers...")
                airth.cancel_timer()
    
    # Interactive mode
    elif args.interactive:
        print("Airth Timer Demo - Interactive Mode")
        print("Type 'exit' or 'quit' to end the demo")
        print("Examples:")
        print("  - set a timer for 5 minutes")
        print("  - start a pomodoro")
        print("  - pause pomodoro")
        print("  - resume pomodoro")
        print("  - skip pomodoro")
        print("  - cancel timer")
        print("  - timer status")
        print()
        
        try:
            while True:
                command = input("Enter a command: ")
                if command.lower() in ["exit", "quit"]:
                    break
                    
                response = airth.respond_to_timer_command(command)
                print("\n" + format_response(response) + "\n")
        except KeyboardInterrupt:
            print("\nDemo ended. Cancelling timers...")
            airth.cancel_timer()
    
    # Default demo mode - show a sequence of commands
    else:
        print("Airth Timer Demo - Automated Sequence")
        print("Press Ctrl+C at any time to exit\n")
        
        try:
            # Start a pomodoro
            print("Command: start a pomodoro")
            response = airth.respond_to_timer_command("start a pomodoro")
            print(format_response(response) + "\n")
            time.sleep(3)
            
            # Check timer status
            print("Command: timer status")
            response = airth.respond_to_timer_command("timer status")
            print(format_response(response) + "\n")
            time.sleep(3)
            
            # Pause the timer
            print("Command: pause pomodoro")
            response = airth.respond_to_timer_command("pause pomodoro")
            print(format_response(response) + "\n")
            time.sleep(3)
            
            # Resume the timer
            print("Command: resume pomodoro")
            response = airth.respond_to_timer_command("resume pomodoro")
            print(format_response(response) + "\n")
            time.sleep(3)
            
            # Skip to next phase
            print("Command: skip to next phase")
            response = airth.respond_to_timer_command("skip pomodoro")
            print(format_response(response) + "\n")
            time.sleep(3)
            
            # Set a countdown timer
            print("Command: set a timer for 30 seconds called Demo Timer")
            response = airth.respond_to_timer_command("set a timer for 0.5 minutes called Demo Timer")
            print(format_response(response) + "\n")
            
            # Wait for the countdown to complete
            print("Waiting for the timer to complete...")
            start_time = time.time()
            while time.time() - start_time < 32:  # Wait up to 32 seconds
                status = airth.get_timer_status("countdown")
                if not any(t["timer_type"] == "countdown" for t in status.get("active_timers", [])):
                    print("Timer completed!")
                    break
                    
                time.sleep(1)
                sys.stdout.write(".")
                sys.stdout.flush()
            
            print("\n\nCancelling all timers")
            response = airth.respond_to_timer_command("cancel all timers")
            print(format_response(response))
            
        except KeyboardInterrupt:
            print("\nDemo interrupted. Cancelling timers...")
            airth.cancel_timer()
    
    print("\nDemo completed.")

if __name__ == "__main__":
    main()
