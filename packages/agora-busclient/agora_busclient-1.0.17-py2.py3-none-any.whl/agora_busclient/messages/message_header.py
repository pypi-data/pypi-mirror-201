from datetime import datetime
from enum import Enum, auto
from agora_config import config
from agora_utils import AgoraTimeStamp


class MessageHeader:
    def __init__(self):
        self.SrcModule = config["Name"]
        self.MessageType = "NotSet"
        self.ConfigVersion = -1
        self.MessageID = self.__get_message_id()
        self.TimeStamp = AgoraTimeStamp()

    def __get_message_id(self):
        utcnow = datetime.utcnow()
        beginning_of_year = datetime(utcnow.year, 1, 1)
        time_difference = utcnow - beginning_of_year
        return int(time_difference.total_seconds()*10)