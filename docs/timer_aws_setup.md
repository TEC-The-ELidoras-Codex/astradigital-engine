# AWS DynamoDB Setup for Timer Persistence

This document provides instructions for setting up the required AWS DynamoDB table for Airth's timer persistence functionality.

## Prerequisites

- An AWS account with appropriate permissions
- AWS CLI installed and configured with your credentials
- Basic understanding of AWS DynamoDB

## Creating the DynamoDB Table

You can create the required DynamoDB table using the AWS Management Console or the AWS CLI.

### Using AWS Management Console

1. Sign in to the AWS Management Console and open the DynamoDB console at https://console.aws.amazon.com/dynamodb/
2. Choose "Create table"
3. Configure the table:
   - Table name: `TEC_PomodoroTimers`
   - Primary key: `user_id` (String)
4. Leave other settings as default or adjust as needed
5. Choose "Create"

### Using AWS CLI

Run the following command to create the DynamoDB table:

```bash
aws dynamodb create-table \
  --table-name TEC_PomodoroTimers \
  --attribute-definitions AttributeName=user_id,AttributeType=S \
  --key-schema AttributeName=user_id,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST
```

## Table Structure

The DynamoDB table has a simple structure:

- **Table Name**: `TEC_PomodoroTimers`
- **Primary Key**: `user_id` (String)
- **Attributes**:
  - `user_id`: String - Unique identifier for the user
  - `timer_state`: String - JSON string containing the serialized timer state

## Example Item

Here's an example of how the data is stored in the table:

```json
{
  "user_id": "default",
  "timer_state": "{\"work_minutes\": 25, \"short_break_minutes\": 5, \"long_break_minutes\": 15, \"long_break_interval\": 4, \"completed_pomodoros\": 2, \"current_phase\": \"work\", \"active\": true, \"end_time\": \"2025-05-09T15:30:45.123456\", \"last_updated\": \"2025-05-09T15:15:45.123456\"}"
}
```

## Configuration in Airth

To enable AWS integration, update your `config.yaml` file:

```yaml
aws:
  use_timer_storage: true
  region: us-east-1  # Your preferred AWS region
```

## AWS Permissions

Ensure your AWS user or role has the following permissions for the `TEC_PomodoroTimers` table:

- `dynamodb:PutItem`
- `dynamodb:GetItem`
- `dynamodb:UpdateItem`
- `dynamodb:DeleteItem`

You can attach the following IAM policy to your user or role:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:PutItem",
        "dynamodb:GetItem",
        "dynamodb:UpdateItem",
        "dynamodb:DeleteItem"
      ],
      "Resource": "arn:aws:dynamodb:*:*:table/TEC_PomodoroTimers"
    }
  ]
}
```

## Testing the Connection

You can test the AWS connection using the `airth_timer_demo.py` script with the `--aws` flag:

```bash
python scripts/airth_timer_demo.py --aws --interactive
```

This will initialize the timer with AWS persistence enabled, allowing you to test that timer states are properly saved to and loaded from DynamoDB.
