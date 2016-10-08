# clearing_house
Demo of sending messages to an SQS and processing those messages downstream. Simulates stock trades as messages. Includes some basic IAM policies that are overly permissive for production but works OK for testing.

Uses CloudWatch Logs as an aggregation point for logs per https://aws.amazon.com/blogs/compute/centralized-container-logs-with-amazon-ecs-and-amazon-cloudwatch-logs/

Assumes log group called 'clearingHouse'.
