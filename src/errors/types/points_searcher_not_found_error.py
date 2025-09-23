class PointsSearcherNotFoundError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message
        self.name = 'PointsSearcherNotFoundError'
        self.status_code = 404
