import queue

from .messages import MessageDecoder, IoDataReportMsg, RequestMsg
from agora_logging import LogLevel, logger


class MessageQueue:
    def __init__(self):
        """
        Initializes the queues for each message type
        """
        self.data_in_q = queue.Queue()
        self.request_in_q = queue.Queue()
        self.application_messages_q = queue.Queue()
        self.decoder = MessageDecoder()

    def get_topic_name(self,topic):
        """
        Extracts the topic name from the message 
        """
        topic_name=""
        topic_parts=topic.split("/")
        if len(topic_parts) > 0:
            topic_name=topic_parts[-1]
        else:
            return None
        return topic_name.lower()

    def process_message(self,msg):
        """
        Store message to corresponding queue

        Args:
            msg (bytes): message received from the MQTT net server
        """
        topic=msg.topic
        payload=msg.payload
        self.store_to_queue(topic,payload)

    def store_to_queue(self,topic,payload):
        """Stores message to the queues based on the topic
        """
        topic_name=self.get_topic_name(topic)
        if topic_name is None:
            logger.trace("topic name is None")
            return 0
        if topic_name == "datain":
            try:
                msg = self.decoder.decode(payload.decode("utf-8"), IoDataReportMsg)
                if msg is None:
                    logger.error(f"DataIn Message: Failed to parse '{payload}'")
                self.data_in_q.put(msg)
            except Exception as e:
                logger.write(LogLevel.ERROR,str(e))
                logger.write(LogLevel.ERROR,"Unable to read the json from DataIn message")
        elif topic_name == "requestin":
            try:
                msg = self.decoder.decode(payload.decode("utf-8"), RequestMsg)
                if msg is None:
                    logger.error(f"Request Message: Failed to parse '{payload}'")
                self.request_in_q.put(msg)
            except Exception as e:
                logger.exception(e, "Unable to read json from RequestIn message.")
        else:
            self.application_messages_q.put(payload)

    def __array_from_queue(self, q: queue.Queue):
        items = []
        try:
            while not q.empty():
                item = q.get_nowait()
                items.append(item)
        except queue.Empty:
            logger.trace("Queue is empty")
        return items


    def get_data_messages(self):
        return self.__array_from_queue(self.data_in_q)

    def get_application_messages(self):
        return self.__array_from_queue(self.application_messages_q)
    
    def get_request_messages(self):
        return self.__array_from_queue(self.request_in_q)
    
    def has_data_messages(self):
        return not self.data_in_q.empty()
    
    def has_request_messages(self):
        return not self.request_in_q.empty()
    