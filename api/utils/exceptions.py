from fastapi import HTTPException, status


class ExceptionInternalErro(HTTPException):
    def __init__(self, detail: str = "Erro interno"):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)

class ExceptionNotFound(HTTPException):
    def __init__(self, detail: str = "Não encontrado"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)