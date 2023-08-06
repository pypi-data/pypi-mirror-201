import json

class IoPoint:
    def __init__(self, 
                 value: float = None,
                 value_str: str = None,
                 quality_code: int = None,
                 timestamp: float = None):
        """
        Args:
            value (int, optional): Value of the IoPoint.
            quality_code (int, optional): 0 if good quality,1 if bad quality.
            timestamp (_type_, optional): AgoraTimeStamp
            value_str (str, optional): Supports sending non numeric value. Defaults to "".
        """
        self.value = value
        self.quality_code = quality_code
        self.timestamp = timestamp
        self.value_str = value_str
