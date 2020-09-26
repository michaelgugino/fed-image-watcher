import json
import logging

STATUS_FILTER = ('FINISHED_INCOMPLETE', 'FINISHED')

logging.basicConfig(format='%(levelname)s %(asctime)s\t%(message)s', level=logging.DEBUG,
    datefmt='%H:%M:%S')

class ProcessMessage(object):
    """
    A fedora-messaging consumer that saves the message to a file.

    A single configuration key is used from fedora-messaging's
    "consumer_config" key, "path", which is where the consumer will save
    the messages::

        [consumer_config]
        path = "/tmp/fedora-messaging/messages.txt"
    """

    def __init__(self):
        print("ProcessMessage initializing\n")

    def __call__(self, message):
        """
        Invoked when a message is received by the consumer.

        Args:
            message (fedora_messaging.api.Message): The message from AMQP.
        """
        logging.debug("Message text: {}".format(message))
        try:
            logging.debug('Received message: {} {}'.format(message['topic'], message['body']['msg_id']))

            msg_info = message['body']['msg']
            if msg_info['status'] not in STATUS_FILTER:
                logging.debug('%s is not valid status' % msg_info['status'])
                return
        except:
            return
        return


if __name__ == "__main__":
    with open("../tests/cloud-31.compose.finished.json") as f:
        msg = json.load(f)
    tProcessMessage = ProcessMessage()
    tProcessMessage(msg)
