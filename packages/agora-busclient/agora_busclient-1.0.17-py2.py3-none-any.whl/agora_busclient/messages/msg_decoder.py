import json
from .iodatareport_message import IoDataReportMsg, IoDeviceData, IoPoint
from .io_tag_data_dict import IoTagDataDict
from .message_header import MessageHeader
from .request_msg import RequestMsg
from agora_logging import logger

class MessageDecoder():
    def decode(self, jsn, o):
        return self.__decode( json.loads(jsn), o)
    
    def __decode(self, d, o):
        if o == IoPoint:
            ret = IoPoint()
            try:
                if 'quality_code' in d: ret.quality_code = int(str(d['quality_code']))
            except Exception as e:
                logger.exception(e, f"Cannot decode IoPoint with 'quality_code' of '{d['quality_code']}'")

            try:
                if 'value' in d: ret.value = float(str(d['value']))
            except Exception as e:
                logger.exception(e, f"Cannot decode IoPoint with 'value' of '{d['value']}")

            if 'value_str' in d: ret.value_str = d['value_str']

            try:
                if 'timestamp' in d: ret.timestamp = float(str(d['timestamp']))
            except Exception as e:
                logger.exception(e, f"Cannot decode IoPoint with 'timestamp' of '{d['timestamp']}")

            return ret
        if o == IoDeviceData:
            ret = None
            try:
                if 'id' in d: id = int(d['id'])
                ret = IoDeviceData(id)
                if 'tags' in d: 
                    ret.tags = self.__decode(d['tags'], IoTagDataDict)
            except Exception as e:
                logger.exception(e, f"Cannot decode IoDeviceData with 'id' of '{d['id']}'")
            if ret is None:
                ret = IoDeviceData(-1)
            return ret
        if o == IoTagDataDict:
            ret = IoTagDataDict()
            for key, value in d.items():
                ret[key] = self.__decode(value, IoPoint)
            return ret
        if o == MessageHeader:
            ret = MessageHeader()
            if 'SrcModule' in d: ret.SrcModule = d['SrcModule']
            if 'MessageType' in d: ret.MessageType = d['MessageType']
            try:
                if 'ConfigVersion' in d: ret.ConfigVersion = int(str(d['ConfigVersion']))
            except:
                ret.ConfigVersion = -1
            try:
                if 'MessageID' in d: ret.MessageID = int(str(d['MessageID']))
            except:
                ret.MessageID = -1
            try:
                if 'TimeStamp' in d: ret.TimeStamp = float(str(d['TimeStamp']))
            except:
                ret.TimeStamp = -1
            return ret
        if o == IoDataReportMsg:
            ret = IoDataReportMsg()
            if 'header' in d: ret.header = self.__decode(d['header'], MessageHeader)
            if 'device' in d:
                for d in d['device']: 
                    ret.device.append( self.__decode(d, IoDeviceData) )
            return ret
        if o == RequestMsg:
            ret = RequestMsg()
            if 'header' in d: ret.header = self.__decode(d['header'], MessageHeader)
            if 'payload' in d: ret.payload = d['payload']
            if 'response' in d: ret.response = d['response']
            if 'device' in d: 
                for d in d['device']:
                    ret.device.append( self.__decode(d, IoDeviceData) )
            return ret
