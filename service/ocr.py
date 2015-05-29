__author__ = 'paulo.rodenas'

import logging
import os
from PIL import Image
import pyocr
import pyocr.builders
from pyocr.cuneiform import CuneiformError
from wand.image import Image as WandImage
from opencv import OpenCVIntegration
from threading import Thread


class PyOCRIntegration(object):

    def __init__(self, lang):
        self.logger = logging.getLogger(__name__)
        self.lang = lang

    def image_to_string(self, filename):
        tools = pyocr.get_available_tools()
        if len(tools) == 0:
            raise PyOCRIntegrationNoOCRFound('No OCR tool has been found on '
                                             'this system. Make sure it\'s on'
                                             'PATH variable of your system')

        filename_split, fileextension_split = os.path.splitext(filename)

        grayscale_filename = filename_split + '_gray' + fileextension_split
        with WandImage(filename=filename) as img:
            img.type = 'grayscale'
            img.save(filename=grayscale_filename)

        adaptive_thresh_filename = filename_split + '_adt' + fileextension_split
        OpenCVIntegration.adaptive_threshold(filename, adaptive_thresh_filename)

        processes = []
        for tool in tools:
            if tool.get_name() == "Tesseract":

                thread_t = self._OCRProcessingThread(tool, self.lang, filename)
                thread_t.start()
                processes.append(thread_t)

            else:
                thread_c_raw = self._OCRProcessingThread(tool, self.lang,
                                                         filename)
                thread_c_raw.start()
                processes.append(thread_c_raw)

                thread_c_gs = self._OCRProcessingThread(tool, self.lang,
                                                        grayscale_filename)
                thread_c_gs.start()
                processes.append(thread_c_gs)

                thread_c_prd = self._OCRProcessingThread(tool, self.lang,
                                                         adaptive_thresh_filename)
                thread_c_prd.start()
                processes.append(thread_c_prd)

        # Wait this all threads finish processing
        result = []
        threads_running = True
        while threads_running:
            found_thread_alive = False
            for p in processes:
                if p.is_alive():
                    found_thread_alive = True

            if not found_thread_alive:
                threads_running = False
                for p in processes:
                    result.append(p.return_value)

        return result

    class _OCRProcessingThread(Thread):

        def __init__(self, tool, lang, filename):
            Thread.__init__(self)
            self.return_value = ''
            self.tool = tool
            self.lang = lang
            self.filename = filename

        def run(self):
            logging.debug("Running %s tool" % self.tool.get_name())
            try:
                txt = self.tool.image_to_string(
                    Image.open(self.filename),
                    lang=self.lang
                )
                self.return_value = txt
                logging.debug("Result %s" % txt)
            except CuneiformError:
                    logging.error('I got an error when trying to process this '
                                  'image with %s' % self.tool.get_name())

    @staticmethod
    def check_required_software():
        logger = logging.getLogger(__name__)
        tools = pyocr.get_available_tools()
        if len(tools) == 0:
            raise PyOCRIntegrationNoOCRFound('No OCR tool has been found on '
                                             'this system. Make sure it\'s on')
        elif len(tools) == 1:
            logger.info("I've found only one ocr tool [%s]. This is not exactly "
                        "an error but you should get better results if you have "
                        "both Tesseract and Cuneiform installed"
                        % tools[0].get_name())
        else:
            logger.info("I've found all required software. We're good to go =)")


class PyOCRIntegrationNoOCRFound(Exception):

    def __init__(self, message):
        super(Exception, self).__init__(message)