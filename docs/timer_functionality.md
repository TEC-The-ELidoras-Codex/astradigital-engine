# Airth Timer Functionality

This document explains how to use Airth's timer functionality, including the Pomodoro technique timer and simple countdown timers.

## Overview

Airth now supports two types of timers:

1. **Pomodoro Timer**: Implements the full Pomodoro technique with customizable work sessions, short breaks, and long breaks. Perfect for structured productivity.

2. **Countdown Timer**: Simple countdown functionality for when you just need a timer for a specific duration.

Both types of timers support:
- AWS DynamoDB integration for persistent timer storage across sessions
- Local file-based fallback storage
- Event callbacks for timer completion, start, pause, and other events

## Using Airth's Timers

You can interact with Airth's timers using natural language commands:

### Setting Timers

```
"Airth, set a timer for 15 minutes"
"Start a timer for 30 minutes called Meeting Timer"
"Set a pomodoro timer"
"Start a pomodoro"
```

### Checking Timer Status

```
"Airth, what's the status of my timer?"
"How much time is left on the timer?"
"What's the pomodoro status?"
```

### Controlling Timers

```
"Pause the pomodoro"
"Resume the pomodoro timer"
"Skip to the next pomodoro phase"
"Cancel the timer"
"Stop all timers"
```

## Pomodoro Technique

The Pomodoro Technique is a time management method developed by Francesco Cirillo that uses a timer to break work into intervals, traditionally 25 minutes in length, separated by short breaks. The method is based on the idea that frequent breaks can improve mental agility.

The standard Pomodoro technique follows this pattern:
1. **Work Session**: 25 minutes of focused work
2. **Short Break**: 5 minutes of rest
3. **Repeat**: After 4 work sessions, take a longer break
4. **Long Break**: 15-30 minutes of rest

Airth's implementation allows you to customize all of these parameters.

## AWS Integration

Airth's timers can seamlessly integrate with AWS to persist timer states across sessions and devices. This requires:

1. An AWS account with DynamoDB access
2. A DynamoDB table named `TEC_PomodoroTimers` with a primary key of `user_id`
3. Proper AWS credentials configuration (via environment variables or credentials file)

To enable AWS integration, update your `config.yaml` file:

```yaml
aws:
  use_timer_storage: true
  region: us-east-1  # Your preferred AWS region
```

## Demo Script

You can try out the timer functionality using the provided demo script:

```bash
python scripts/airth_timer_demo.py --interactive
```

This will start an interactive session where you can test various timer commands.

## Programmatic Usage

You can also use the timer functionality programmatically:

```python
from src.agents import AirthAgent

# Initialize Airth
airth = AirthAgent()

# Set a countdown timer
result = airth.set_timer(15, timer_type="countdown", timer_name="Meeting Timer")

# Set a Pomodoro timer
result = airth.set_timer(minutes=25, timer_type="pomodoro")

# Check timer status
status = airth.get_timer_status()

# Cancel a timer
airth.cancel_timer("pomodoro")
```

## Customizing Timer Settings

You can customize the Pomodoro timer settings in your `config.yaml` file:

```yaml
timer:
  pomodoro_work_minutes: 25
  pomodoro_short_break_minutes: 5
  pomodoro_long_break_minutes: 15
  pomodoro_long_break_interval: 4
```

## Advanced Usage: Custom Callbacks

You can register custom callback functions to be executed when timer events occur. This is useful for integrating with notification systems or other components.

```python
def on_timer_complete(timer):
    print(f"Timer completed: {timer.get_status()}")

# Initialize the agent
airth = AirthAgent()

# Initialize the timer if not already done
if airth.pomodoro_timer is None:
    airth._initialize_pomodoro_timer()

# Add the callback
airth.pomodoro_timer.add_callback("on_complete", on_timer_complete)
```

Available events include:
- `on_complete`: Triggered when the timer completes
- `on_start`: Triggered when the timer starts
- `on_pause`: Triggered when the timer is paused
- `on_resume`: Triggered when the timer resumes
- `on_cancel`: Triggered when the timer is cancelled
