
from typing import List
from agora_config import config

from .io_device_data import IoDeviceData
from .io_point import IoPoint
from .message_header import MessageHeader


class IoDataReportMsg:
    default_device_id = 999
    def __init__(self):
        """Represents an IoDataReport message
        """
        self.version = 1
        self.header = MessageHeader()
        self.header.Compressed = False
        self.header.MessageType = "IODataReport"
        self.header.ConfigVersion = self.version
        self.device: List[IoDeviceData]=[]
    
    def get_device_data(self,device_id:int) -> IoDeviceData:
        """Get device data for a specific device

        Args:
            device_id (int): device id 

        Returns:
            IoDeviceData: Device data for the given device
        """
        return next((iod_item for iod_item in self.device if iod_item.id == device_id), None)

    def add_device_data(self,device_id:int, tagname:str, io_point:IoPoint):
        if tagname:
            io_d_data=self.get_device_data(device_id)
            if io_d_data is None:
                device = IoDeviceData(device_id)
                self.device.append(device)
                io_d_data = device
            io_d_data.tags[tagname] = io_point

    def add_data(self, tagname: str, io_point:IoPoint):
        if tagname:
            io_d_data=self.get_device_data(IoDataReportMsg.default_device_id)
            if io_d_data is None:
                device = IoDeviceData(IoDataReportMsg.default_device_id)
                self.device.append(device)
                io_d_data = device
            io_d_data.tags[tagname] = io_point

    def get(self,device_id:int,tagname:str) -> IoPoint:
        if tagname:
            io_d_data=self.get_device_data(device_id)
            return None if io_d_data is None else io_d_data.get_io_point(tagname)
        return None