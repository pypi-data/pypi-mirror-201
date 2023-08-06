from .entities import Image, LogResult
import json

def getDictFromBytes(data: bytes):
    data = data.decode("utf-8")
    return json.loads(data)
def getImageFromJson(json_image: str) -> Image:
    image: Image = Image()
    image.deserialize(json_image)
    return image
def getJsonFromImage(image: Image) -> str:
    return image.serialize()
def getLogResultFromJson(json_log: str) -> LogResult:
    log: LogResult = LogResult()
    log.deserialize(json_log)
    return log
def getJsonFromLogResult(log: LogResult) -> str:
    return log.serialize()
    
