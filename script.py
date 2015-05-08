
__author__ = 'paulo.rodenas'

import time
from service.ocr import *
from service.postprocessing import TaxReceiptFuzzyRegex
from service.aws import SimpleQueueServiceIntegration



if __name__ == "__main__":
    # start = time.time()
    #
    # ocr_tool = PyOCRIntegration('eng')
    # results = ocr_tool.image_to_string('images/IMG_1821_50.JPG')
    # for result in results:
    #     print result
    #
    # print
    # print 'Start - Fuzzy Matching'
    # taxReceiptFuzzyRegex = TaxReceiptFuzzyRegex(results)
    # print taxReceiptFuzzyRegex.identify_needed_fields()
    # print 'End - Fuzzy Matching'
    #
    # end = time.time()
    # elapsed = end - start
    #
    # print 'Execution took', elapsed, 'seconds'
    aws_sqs = SimpleQueueServiceIntegration()
    thread = aws_sqs.start_listening()
    thread.join()