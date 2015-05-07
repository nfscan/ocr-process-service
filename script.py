
__author__ = 'paulo.rodenas'

import thread
import time

from service.ocr import *
from service.postprocessing import TaxReceiptFuzzyRegex
import boto
import boto.sqs

default_region = "us-west-1"


def start_listener_sqs(queue_name):
    print 'Starting listener on queue', queue_name
    thread.start_new_thread(handle_queue_message, (queue_name,))


def handle_queue_message(queue_name):
    conn = boto.sqs.connect_to_region(default_region)
    queue = conn.get_queue(queue_name)
    while True:
        rs = queue.get_messages()
        for message in rs:
            print 'Received message from', queue.name, message.get_body()
            queue.delete_message(message)
        time.sleep(1)


if __name__ == "__main__":
    ocr_tool = PyOCRIntegration('eng')
    results = ocr_tool.image_to_string('images/IMG_2943_SMALL.jpeg')
    for result in results:
        print result

    print 'Start - Fuzzy Matching'
    taxReceiptFuzzyRegex = TaxReceiptFuzzyRegex(results)
    print taxReceiptFuzzyRegex.identify_needed_fields()
    print 'End - Fuzzy Matching'