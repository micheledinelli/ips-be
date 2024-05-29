class ModelNotFound(Exception):
    """Raised when the model is not found"""
    def __init__(self, message="Model not found"):
        self.message = message
        super().__init__(self.message)

class DataNotFound(Exception):
    """Raised when the data is not found"""
    def __init__(self, message="Please provide data before"):
        self.message = message
        super().__init__(self.message)