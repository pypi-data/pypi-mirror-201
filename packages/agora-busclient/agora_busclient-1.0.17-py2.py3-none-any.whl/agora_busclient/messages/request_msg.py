from typing import List

from .message_header import MessageHeader
from .io_device_data import IoDeviceData


class RequestMsg:
    def __init__(self, requestName: str = "", version: int = -1):
        """
        Represents a Request message
        """
        self.version = version
        self.header = MessageHeader()
        self.header.Compressed = False
        self.header.MessageType = requestName
        self.header.ConfigVersion = self.version
        self.payload = dict()
        self.response = dict()
        self.device: List[IoDeviceData]=[]
