#!/usr/bin/python
# -*- coding: utf-8 -*-


__author__ = 'paulo.rodenas'

import logging
import os, sys, time
from tempfile import NamedTemporaryFile
from service.ocr import *
from service.postprocessing import TaxReceiptFuzzyRegex
from service.aws import TaxReceiptSimpleQueueServiceIntegration, \
    SimpleStorageServiceIntegration, BaseSimpleQueueServiceIntegration
import json


def handle_process_message_function(queue_name_in, message_body):
    """
    {"transaction_id": 1,"object": "IMG_2943_SMALL.jpeg"}
    """

    logger = logging.getLogger(__name__)

    start = time.time()

    # Receive message from SQS
    json_message = json.loads(message_body)

    # Create a temp file
    file_suffix = os.path.splitext(json_message.get('object'))[1]
    image_file = NamedTemporaryFile(suffix=file_suffix, delete=True)

    # Retrieve file from Amazon S3
    s3 = SimpleStorageServiceIntegration()
    s3.download_file(json_message.get('object'), image_file.name)

    # Perform OCR on it
    ocr_tool = PyOCRIntegration('eng')
    results = ocr_tool.image_to_string(image_file.name)

    # Close file which causes this temp file to be deleted
    image_file.close()

    # Start looking for meaningful values
    logger.debug('Start - Fuzzy Matching')
    tax_receipt_fuzzy_regex = TaxReceiptFuzzyRegex(results)
    ret_value = tax_receipt_fuzzy_regex.identify_needed_fields()
    logger.debug(ret_value)
    logger.debug('End - Fuzzy Matching')

    # Calculate the time it took to perform all those steps
    end = time.time()
    elapsed = end - start
    logger.debug('Execution took %f seconds' % elapsed)

    ret_value.update({'transaction_id': json_message.get('transaction_id'), 'elapsedTime': elapsed})
    return ret_value


def handle_queue_out_message_function(queue_name_out, response_body):
    json_response = json.dumps(response_body)

    sqs_service = BaseSimpleQueueServiceIntegration()
    sqs_service.send_message(queue_name_out, json_response)

if __name__ == "__main__":
    logging.config.fileConfig('/etc/ocr-processing-service/logging.ini')
    PyOCRIntegration.check_required_software()

    aws_sqs = TaxReceiptSimpleQueueServiceIntegration(
        handle_process_message_function,
        handle_queue_out_message_function
    )

    try:
        thread = aws_sqs.start_listening()
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        sys.exit()
