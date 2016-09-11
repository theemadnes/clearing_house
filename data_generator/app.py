# data generator script that generates trade messages that get published to an SQS queue
# before running, make sure sqs_queue_name points to an SQS queue that you have appropriate permissions to write to

import random
import boto3
from yahoo_finance import Share
import time
import json
#import decimal

sqs_queue_name = 'clearing_house'
ticker_symbols = ['amzn', 'msft', 'amd', 'intc', 'yhoo']
stock_operations = ['buy', 'sell']

sqs_client = boto3.resource('sqs')
sqs_queue = sqs_client.get_queue_by_name(QueueName=sqs_queue_name)

while True:

    transaction = {}
    ticker = random.choice(ticker_symbols)
    stock = Share(ticker)
    transaction['ticker'] = ticker
    transaction['price'] = float(stock.get_price())
    transaction['operation'] = random.choice(stock_operations)
    transaction['volume'] = int(random.randint(1, 1000) * 10)
    transaction['time_stamp'] = time.time() * 1000 # get epoch in ms
    sqs_queue.send_message(MessageBody=json.dumps(transaction))
    print(transaction)
    time.sleep(random.randint(1,3))
