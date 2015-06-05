__author__ = 'paulo.rodenas'

import ConfigParser


class ConfigReader(object):

    SECTION_AWS_ACCOUNT = 'aws_account'
    SECTION_AWS_SQS = 'aws_sqs'
    SECTION_AWS_S3 = 'aws_s3'

    OPTION_DEFAULT_REGION = 'default_region'
    OPTION_QUEUE_NAME_IN = 'queue_name_in'
    OPTION_QUEUE_NAME_OUT = 'queue_name_out'
    OPTION_BUCKET_NAME = 'bucket_name'

    def __init__(self, config_file='/etc/ocr-process-service/ocr-process-service.cfg'):
        config = ConfigParser.RawConfigParser(allow_no_value=True)
        config.read(config_file)
        self.config = config

    def get_property(self, section, option):
        return self.config.get(section, option)