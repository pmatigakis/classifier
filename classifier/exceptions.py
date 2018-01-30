class ClassifierError(Exception):
    def __init__(self, reason=None):
        super(ClassifierError, self).__init__(reason)
        self.reason = reason


class ClassifierMethodVerificationError(ClassifierError):
    def __init__(self, method=None):
        if method:
            reason = "the classifier doesn't have the '{}' " \
                     "method".format(method)
        else:
            reason = "invalid classifier"

        super(ClassifierMethodVerificationError, self).__init__(reason)
        self.method = method
