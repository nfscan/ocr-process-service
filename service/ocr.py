__author__ = 'paulo.rodenas'

import logging
from PIL import Image
import pyocr
import pyocr.builders


class PyOCRIntegration(object):

    def __init__(self, lang):
        self.logger = logging.getLogger(__name__)
        self.tools = pyocr.get_available_tools()
        self.lang = lang

    def image_to_string(self, filename):
        if len(self.tools) == 0:
            raise PyOCRIntegrationNoOCRFound('No OCR tool has been found on '
                                             'this system. Make sure it\'s on'
                                             'PATH variable of your system')
        result = []
        for tool in self.tools:
            logging.debug("Running %s tool" % tool.get_name())
            if tool.get_name() == "Tesseract":
                txt = tool.image_to_string(
                    Image.open(filename),
                    lang=self.lang
                )
                result.append(txt)
                logging.debug("Result %s" % txt)
            else:
                # Default Cuneiform parameters
                txt = tool.image_to_string(
                    Image.open(filename),
                    lang=self.lang
                )
                result.append(txt)
                logging.debug("Result %s" % txt)

                # Fax Cuneiform ocr
                txt = tool.image_to_string(
                    Image.open(filename),
                    lang=self.lang,
                    builder=pyocr.builders.TextBuilder(
                        cuneiform_fax=True
                    )
                )
                result.append(txt)
                logging.debug("Result %s" % txt)
        return result

    @staticmethod
    def check_required_software():
        logger = logging.getLogger(__name__)
        tools = pyocr.get_available_tools()
        if len(tools) == 0:
            raise PyOCRIntegrationNoOCRFound('No OCR tool has been found on '
                                             'this system. Make sure it\'s on')
        elif len(tools) == 1:
            logger.info("I've found only one ocr tool [%s]. This is not exactly an error but you should get better " \
                  "results if you have both Tesseract and Cuneiform installed" % tools[0].get_name())
        else:
            logger.info("I've found all required software. We're good to go =)")

class PyOCRIntegrationNoOCRFound(Exception):

    def __init__(self, message):
        super(Exception, self).__init__(message)