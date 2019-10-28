class ClassifierError(Exception):
    def __init__(self, reason=None):
        super(ClassifierError, self).__init__(reason)
        self.reason = reason
