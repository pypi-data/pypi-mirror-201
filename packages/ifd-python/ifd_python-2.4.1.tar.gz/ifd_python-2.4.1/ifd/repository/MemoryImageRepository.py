from .Interfaces import IImageRepository
class MemoryImageRepository(IImageRepository):
    def __init__(self):
        pass
    def sendMessageToChannel(self, message: str):
        pass