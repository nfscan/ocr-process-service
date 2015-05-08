#!/usr/bin/python
# -*- coding: utf-8 -*-


__author__ = 'paulo.rodenas'

import os
import time
from tempfile import NamedTemporaryFile
from service.ocr import *
from service.postprocessing import TaxReceiptFuzzyRegex
from service.aws import TaxReceiptSimpleQueueServiceIntegration, \
    SimpleStorageServiceIntegration
import json


def handle_process_message_function(queue_name_in, message_body):
    '''

    >>> {
    ...     "transaction_id": 1,
    ...     "object": "IMG_2943_SMALL.jpeg"
    ... }

    :param message_body:
    :return:
    '''
    start = time.time()

    # Receive message from SQS
    json_message = json.loads(message_body)

    # Create a temp file
    file_suffix = os.path.splitext(json_message.get('object'))[1]
    image_file = NamedTemporaryFile(suffix=file_suffix, delete=True)

    s3 = SimpleStorageServiceIntegration()
    s3.download_file(json_message.get('object'), image_file.name)

    ocr_tool = PyOCRIntegration('eng')
    results = ocr_tool.image_to_string(image_file.name)

    # Close file which causes this temp file to be deleted
    image_file.close()

    # Debug messages only.
    for result in results:
        print result

    print '\nStart - Fuzzy Matching'
    tax_receipt_fuzzy_regex = TaxReceiptFuzzyRegex(results)
    print tax_receipt_fuzzy_regex.identify_needed_fields()
    print 'End - Fuzzy Matching'

    end = time.time()
    elapsed = end - start

    print 'Execution took', elapsed, 'seconds'


def handle_queue_out_message_function(queue_name_out, response_body):
    json_response = json.dumps(response_body)

    pass

if __name__ == "__main__":

    aws_sqs = TaxReceiptSimpleQueueServiceIntegration(
        handle_process_message_function,
        handle_queue_out_message_function
    )
    thread = aws_sqs.start_listening()
    thread.join()