__author__ = 'paulo.rodenas'

import boto
import boto.sqs

conn = boto.sqs.connect_to_region('us-west-1')

queue = conn.get_queue('INSTAGRAACC-OCR-PROCESS-IN')

print conn.send_message(queue, 'Teste')
