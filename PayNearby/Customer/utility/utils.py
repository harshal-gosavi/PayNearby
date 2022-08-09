import logging
import re


def process_data(narration):
    """
        Process Narration String And Separated Require Fields
    """
    try:
        print("narration:", narration)
        narration = narration.split('/')
        txn, xxxx_number, rrn, account_number, bank, account_holder, transaction_type = \
            narration[0], narration[1], narration[2], narration[3], narration[4], narration[5], narration[6]
        return txn, xxxx_number, rrn, account_number, bank, account_holder, transaction_type
    except IndexError as e:
        logging.error("Process Data Index Error:{}".format(e))
        print(e)
        return '', '', '', '', '', '', ''

    except Exception as e:
        logging.error("Process Data:{}".format(e))
        print(e)
        return '', '', '', '', '', '', ''


def camel(value):
    """
        Convert value to camel case
    """
    list_words = value.replace(".", " ").replace("_", " ").split()
    converted = "".join(word[0].upper() + word[1:].lower() for word in list_words)
    return converted[0].lower() + converted[1:]
