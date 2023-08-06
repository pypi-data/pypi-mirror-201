from .io_tag_data_dict import IoTagDataDict

class IoDeviceData:
    """Creates an IoDeviceData object
    """
    def __init__(self,id:int):
        self.id: int = id
        self.tags: IoTagDataDict = IoTagDataDict()