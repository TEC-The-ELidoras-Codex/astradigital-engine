# Timer Features in Airth

This document provides a quick overview of Airth's timer functionality, including examples of how to use the Pomodoro and countdown timers.

## Basic Usage

### Setting Timers

```python
from src.agents.airth_agent import AirthAgent

# Initialize the agent
airth = AirthAgent()

# Set a countdown timer
airth.set_timer(15, timer_type="countdown", timer_name="Meeting Timer")

# Set a Pomodoro timer
airth.set_timer(25, timer_type="pomodoro")
```

### Voice Commands

```python
# Process a voice command
result = airth.respond_to_timer_command("set a timer for 15 minutes")

# Start a Pomodoro
result = airth.respond_to_timer_command("start a pomodoro")

# Check timer status
result = airth.respond_to_timer_command("what's the status of my timer?")

# Pause, resume, and skip
result = airth.respond_to_timer_command("pause pomodoro")
result = airth.respond_to_timer_command("resume pomodoro")
result = airth.respond_to_timer_command("skip to next pomodoro phase")

# Cancel timers
result = airth.respond_to_timer_command("cancel timer")
```

## Running the Demo

```bash
# Interactive mode
python scripts/airth_timer_demo.py --interactive

# Run with a specific command
python scripts/airth_timer_demo.py --command "start a pomodoro"

# Run the automated demo sequence
python scripts/airth_timer_demo.py
```

## Further Reading

For more detailed information, see:
- [Timer Functionality Documentation](timer_functionality.md)
- [AWS Setup for Timer Persistence](timer_aws_setup.md)
