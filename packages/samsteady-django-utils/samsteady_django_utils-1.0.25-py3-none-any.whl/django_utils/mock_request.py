class MockRequest:
    def __init__(self, user, data={}):
        self.user = user
        self.data = data