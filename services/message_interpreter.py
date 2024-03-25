import logging

from exceptions.custom_exceptions import GetMessageException

logger = logging.getLogger()

def concatenate_lists(lists):
    try:
        logger.debug("concatenando")
        list_itens_count = len(lists[0])

        for l in lists[1:]:
            assert len(l) == list_itens_count

        n = len(lists)
        final_length = list_itens_count * n

        return [lists[i % n][int(i / n)] for i in range(final_length)]
    except Exception as e:
        logger.exception(e)
        raise

def message_generate(concatenation = [], unique_list = []):
    try:
        logger.debug("gernado mensagem")
        for word in range(len(concatenation)):
            if concatenation[word] != "" and len(unique_list)==(word//3):
                unique_list.append(concatenation[word])
        return (" ".join(unique_list))
    except Exception as e:
        logger.exception(e)
        raise

def getmessage(message):
    try:
        logger.debug("Interpretando as mensagens")
        concatenation = concatenate_lists(message)
        message_list = message_generate(concatenation)
        return message_list
    except Exception as e:
        logger.exception(e)
        raise GetMessageException(Exception)