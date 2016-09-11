# data generator script that processes trade messages pulled from an SQS queue
# before running, make sure sqs_queue_name points to an SQS queue that you have appropriate permissions to write to and the dynamoDB table name is correct
# also configure the proper aws_region

import boto3
import time
import json
import decimal

aws_region = 'us-west-2'
dynamo_table_name = 'clearing_house'
sqs_queue_name = 'clearing_house'
sqs_client = boto3.resource('sqs', region_name=aws_region)
dynamo_client = boto3.resource('dynamodb', region_name=aws_region)
dynamo_table = dynamo_client.Table(dynamo_table_name)
sqs_queue = sqs_client.get_queue_by_name(QueueName=sqs_queue_name)

while True:

    try:

        for message in sqs_queue.receive_messages():
            # print(json.dumps(message))
            msg_body = json.loads(message.body)
            print('message receieved from queue: ' + json.dumps(msg_body))
            print('writing to dynamo table')
            dynamo_response = dynamo_table.put_item(
               Item={
                    'ticker': msg_body['ticker'],
                    'time_stamp': decimal.Decimal(str(msg_body['time_stamp'])), # casting first as str to preserve number
                    'price': decimal.Decimal(str(msg_body['price'])),
                    'operation': msg_body['operation'],
                    'volume': decimal.Decimal(str(msg_body['volume']))
                }
            )

            # clean up message from queue
            print("processing complete - deleting message from queue")
            message.delete()

    except:

        print("No messages or error connecting to queue")

    time.sleep(1)
