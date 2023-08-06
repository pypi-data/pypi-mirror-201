class FileFinderError(Exception):
    """Classe mãe para tratar todas as exceções do programa"""
    pass


class InvalidInputError(FileFinderError):
    """Classe especiífica para erros que aconteçam devido a inputs inválidos do usuário"""
    pass


class ZeroFilesFoundError(FileFinderError):
    """Classe especiífica para quando nenhum arquivo é encontrado na busca"""
    pass
