class UnknownModelType(Exception):
    def __init__(self, detail="Unknown Model Type!"):
        self.detail = detail
        super().__init__(detail)
