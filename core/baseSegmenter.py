import abc

class BaseSegmenter(abc.ABC):
    def __init__(self, target):
        self.target = target

    @abc.abstractmethod
    def segment(self, image):
        pass
