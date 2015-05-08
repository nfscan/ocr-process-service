__author__ = 'paulo.rodenas'

from itertools import ifilter, imap
import regex as re
from validation.cnpj import Cnpj
from validation.date import Date


class BaseFuzzyRegex(object):

    @staticmethod
    def approximate_match(word_re, lines, fuzziness='e<=1'):
        print 'Looking for', word_re
        best_partial_matches = []
        search = re.compile(
            ur'(' + word_re + '){' + fuzziness + '}',
            flags=re.BESTMATCH | re.IGNORECASE).search
        for m in ifilter(None, imap(search, lines)):
            print m.span(), m[0] # for debugginh purposes only
            best_partial_matches.append(m[0])
        return best_partial_matches

    @staticmethod
    def remove_non_numeric(text):
        non_decimal = re.compile(r'[^\d]+')
        return non_decimal.sub('', text)

    @staticmethod
    def remove_non_numeric_currency(text):
        regex = re.compile(r'[^\d\,\.]+')
        temp = regex.sub('', text)
        return temp.replace(',', ".")

    @staticmethod
    def remove_non_numeric_date(text):
        regex = re.compile(r'[^\d\/]+')
        return regex.sub('', text)


class TaxReceiptFuzzyRegex(object):

    def __init__(self, ocr_results):
        self.ocr_results = ocr_results

    def identify_needed_fields(self):
        default_fuzziness = 'e<=2'

        cnpj_found = None
        coo_found = None
        date_found = None
        total_found = None

        lines = "\n".join(self.ocr_results).rstrip().split('\n')
        # Try to get a good match for CNPJ
        cnpj_priority_1_matches = BaseFuzzyRegex.approximate_match(
            word_re='(CNPJ\:\s*){0,1}(\d{2}[\.\,]*\d{3}[\.\,]*\d{3}\/{0,1}\d{4}.{0,1}\d{2})',
            lines=lines,
            fuzziness=default_fuzziness
        )

        cnpj_priority_2_matches = BaseFuzzyRegex.approximate_match(
            word_re='(\d{2}[\.\,]*\d{3}[\.\,]*\d{3}\/{0,1}\d{4}.{0,1}\d{2})',
            lines=lines,
            fuzziness=default_fuzziness
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
                cnpj_found = BaseFuzzyRegex.remove_non_numeric(cnpjmerged_lists[0])

        # Try to get a good match for COO
        coo_priority_1_matches = BaseFuzzyRegex.approximate_match(
            word_re='COO\:\s*(\d{6})$',
            lines=lines,
            fuzziness=default_fuzziness
        )

        if not coo_priority_1_matches is None and len(coo_priority_1_matches) > 0:
            coo_found = BaseFuzzyRegex.remove_non_numeric(coo_priority_1_matches[0])

        # Try to get a good match for Data
        date_priority_1_matches = BaseFuzzyRegex.approximate_match(
            word_re='(\d{2}\/\d{2}\/\d{4})',
            lines=lines
        )

        if not date_priority_1_matches is None and len(date_priority_1_matches) > 0:
            valid_date_matches = []
            for possible_date in date_priority_1_matches:
                temp = Date.parse(possible_date)
                if not temp is None:
                    valid_date_matches.append(temp)

            if len(valid_date_matches) > 0:
                valid_date_matches.sort(reverse=True)
                date_found = Date.format(valid_date_matches[0])
            else:
                date_found = BaseFuzzyRegex.remove_non_numeric_date(
                    date_priority_1_matches[0]
                )

        # Try to get a good match for Total
        total_priority_1_matches = BaseFuzzyRegex.approximate_match(
            word_re='[TOTAL|R\$]\s*\d+[\,\.]\d{2}$',
            lines=lines
        )

        if not total_priority_1_matches is None and len(total_priority_1_matches) > 0:
            total_found = BaseFuzzyRegex.remove_non_numeric_currency(
                total_priority_1_matches[0])

        return {
            'cnpj': cnpj_found,
            'coo':coo_found,
            'date': date_found,
            'total': total_found
        }