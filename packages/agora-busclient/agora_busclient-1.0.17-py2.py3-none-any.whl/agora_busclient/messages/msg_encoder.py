import json
from .iodatareport_message import IoDataReportMsg, IoDeviceData, IoPoint
from .io_tag_data_dict import IoTagDataDict
from .message_header import MessageHeader
from .request_msg import RequestMsg

class MessageEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, IoPoint):
            d = dict()
            if o.value != None:
                d['value'] = o.value
            if o.value_str != None:
                d['value_str'] = o.value_str
            if o.quality_code != None:
                d['quality_code'] = o.quality_code
            if o.timestamp != None:
                d['timestamp'] = int(o.timestamp)
            return d
        elif isinstance(o, IoTagDataDict):
            d = dict()
            for key,val in o.items():
                d[key] = self.default(val)
            return d
        elif isinstance(o, IoDeviceData):
            d = dict()
            d['id'] = str(o.id)
            d['tags'] = self.default(o.tags)
            return d
        elif isinstance(o, MessageHeader):
            d = dict()
            d['SrcModule'] = o.SrcModule
            d['MessageType'] = o.MessageType
            d['ConfigVersion'] = o.ConfigVersion
            d['MessageID'] = o.MessageID
            d['TimeStamp'] = int(o.TimeStamp)
            return d
        elif isinstance(o, IoDataReportMsg):
            d = dict()
            d['header'] = self.default(o.header)
            lst = list()
            for device in o.device:
                lst.append( self.default(device))
            d['device'] = lst
            return d
        elif isinstance(o, RequestMsg):
            d = dict()
            d['header'] = self.default(o.header)
            d['payload'] = o.payload
            lst = list()
            for device in o.device:
                lst.append( self.default(device))
            d['device'] = lst
            d['response'] = o.response
            return d
        return super().default(o)