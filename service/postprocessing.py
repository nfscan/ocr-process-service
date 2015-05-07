__author__ = 'paulo.rodenas'

from itertools import ifilter, imap
import regex as re
from validation.cnpj import Cnpj

class BaseFuzzyRegex(object):

    @staticmethod
    def approximate_match(word_re, lines, fuzziness='e<=1'):
        print 'Looking for', word_re
        best_partial_matches = []
        search = re.compile(ur'(' + word_re + '){' + fuzziness + '}', flags=re.BESTMATCH).search
        for m in ifilter(None, imap(search, lines)):
            print m.span(), m[0] # for debugginh purposes only
            best_partial_matches.append(m[0])
        return best_partial_matches

    @staticmethod
    def remove_non_numeric(str):
        non_decimal = re.compile(r'[^\d]+')
        return non_decimal.sub('', str)


class TaxReceiptFuzzyRegex(object):

    def __init__(self, ocr_results):
        self.ocr_results = ocr_results

    def identify_needed_fields(self):

        cnpj_found = None
        coo_found = None
        date_found = None
        total_found = None

        for result in self.ocr_results:
            lines = result.rstrip().split('\n')
            # Try to get a good match for CNPJ
            cnpj_priority_1_matches = BaseFuzzyRegex.approximate_match(
                word_re='(CNPJ\:\s*){0,1}(\d{2}[\.\,]*\d{3}[\.\,]*\d{3}\/{0,1}\d{4}.{0,1}\d{2})',
                lines=lines,
                fuzziness='e<=2'
            )

            cnpj_priority_2_matches = BaseFuzzyRegex.approximate_match(
                word_re='(\d{2}[\.\,]*\d{3}[\.\,]*\d{3}\/{0,1}\d{4}.{0,1}\d{2})',
                lines=lines,
                fuzziness='e<=2'
            )

            cnpjmerged_lists = cnpj_priority_1_matches + cnpj_priority_2_matches
            if not cnpjmerged_lists is None and len(cnpjmerged_lists) > 0:
                for possible_cnpj in cnpjmerged_lists:
                    possible_cnpj = BaseFuzzyRegex.remove_non_numeric(possible_cnpj)
                    if Cnpj.validate(possible_cnpj):
                        cnpj_found = possible_cnpj
                        break
                # In case we haven't found a match yet we'll use the best match
                # for the priority group 1
                if cnpj_found is None:
                    cnpj_found = cnpjmerged_lists[0]

            # Try to get a good match for COO
            coo_priority_1_matches = BaseFuzzyRegex.approximate_match(
                word_re='COO\:(\d{6})$',
                lines=lines,
                fuzziness='e<=2'
            )

            if not coo_priority_1_matches is None and len(coo_priority_1_matches) > 0:
                coo_found = BaseFuzzyRegex.remove_non_numeric(coo_priority_1_matches[0])

            # Try to get a good match for Data
            data_priority_1_matches = BaseFuzzyRegex.approximate_match(
                word_re='(\d{2}\/\d{2}\/\d{4})',
                lines=lines,
                fuzziness='e<=1'
            )

            if not data_priority_1_matches is None and len(data_priority_1_matches) > 0:
                date_found = data_priority_1_matches[0]

        return cnpj_found, coo_found, date_found, total_found