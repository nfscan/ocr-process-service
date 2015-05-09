__author__ = 'paulo.rodenas'

from util.config import ConfigReader
from threading import Thread
from boto import sqs, s3
import time
import logging
import traceback


class BaseServiceIntegration(object):

    def __init__(self):
        self.config = ConfigReader()
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Loading config properties for AWS")
        self.default_region = self.config.get_property(
            self.config.SECTION_AWS_ACCOUNT,
            self.config.OPTION_DEFAULT_REGION
        )


class BaseSimpleQueueServiceIntegration(BaseServiceIntegration):

    def __init__(self):
        super(BaseSimpleQueueServiceIntegration, self).__init__()
        self.logger.debug("Connecting to AWS SQS")
        self.conn = sqs.connect_to_region(self.default_region)

    def send_message(self, queue_name, message_body):
        self.logger.info("Sending message to %s containing %s" % (queue_name, message_body))
        queue = self.conn.get_queue(queue_name)
        self.conn.send_message(queue, message_body)
        self.logger.debug("Message sent")


class SimpleQueueServiceIntegration(BaseSimpleQueueServiceIntegration):

    def __init__(self, queue_name_in=None, queue_name_out=None):
        super(SimpleQueueServiceIntegration, self).__init__()

        self.queue_name_in = queue_name_in
        self.queue_name_out = queue_name_out

    def handle_queue_in_message(self, queue_name_in,
                                handle_process_message,
                                handle_queue_out_message):
        queue_in = self.conn.get_queue(queue_name_in)
        while True:
            rs = queue_in.get_messages()
            for message in rs:
                self.logger.info('Received message from %s - %s' % (queue_in.name, message.get_body()))
                try:
                    ret_value = handle_process_message(message.get_body())
                    queue_in.delete_message(message)
                    handle_queue_out_message(ret_value)

                except Exception:
                    self.logger.error('An error happened when trying to process this queue')
                    traceback.print_exc()
            time.sleep(1)

    def handle_process_message(self, message_body):
        raise NotImplementedError("Please implement this method")

    def handle_queue_out_message(self, response_body):
        raise NotImplementedError("Please implement this method")

    def start_listening(self):
        self.logger.info('Starting listener on queue %s' % self.queue_name_in)

        thread_sqs = Thread(target=self.handle_queue_in_message,
                            args=(
                                self.queue_name_in,
                                self.handle_process_message,
                                self.handle_queue_out_message,
                            ))
        thread_sqs.daemon = True
        thread_sqs.start()
        return thread_sqs


class SimpleStorageServiceIntegration(BaseServiceIntegration):

    def __init__(self):
        super(SimpleStorageServiceIntegration, self).__init__()
        bucket_name = self.config.get_property(
            self.config.SECTION_AWS_S3, self.config.OPTION_BUCKET_NAME)

        self.logger.debug("Connecting to AWS S3")
        conn = s3.connect_to_region(self.default_region)
        self.logger.debug("Getting %s bucket" % bucket_name)
        self.bucket = conn.get_bucket(bucket_name)

    def list(self):
        return self.bucket.list()

    def download_file(self, key, dst_filename):
        self.logger.debug("Downloading %s from AWS S3" % key)
        key = self.bucket.get_key(key)
        key.get_contents_to_filename(dst_filename)


class TaxReceiptSimpleQueueServiceIntegration(SimpleQueueServiceIntegration):

    def __init__(self, handle_process_message_function, handle_queue_out_message_function):
        super(TaxReceiptSimpleQueueServiceIntegration, self).__init__()

        self.queue_name_in = self.config.get_property(
            self.config.SECTION_AWS_SQS, self.config.OPTION_QUEUE_NAME_IN)
        self.queue_name_out = self.config.get_property(
            self.config.SECTION_AWS_SQS, self.config.OPTION_QUEUE_NAME_OUT)

        if not handle_process_message_function is None:
            self.handle_process_message_function = handle_process_message_function
        else:
            raise ValueError('You must provide the '
                             'handle_process_message_function parameter')

        if not handle_queue_out_message_function is None:
            self.handle_queue_out_message_function = handle_queue_out_message_function
        else:
            raise ValueError('You must provide the '
                             'handle_queue_out_message_function parameter')

    def handle_process_message(self, message_body):
        return self.handle_process_message_function(self.queue_name_in, message_body)

    def handle_queue_out_message(self, response_body):
        return self.handle_queue_out_message_function(self.queue_name_out, response_body)