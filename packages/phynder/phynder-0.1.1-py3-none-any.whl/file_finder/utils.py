from datetime import datetime
from file_finder.exceptions import InvalidInputError
import platform

def get_folders(path):
    """
    Obtém todos os subdiretorios no diretório pesquisado.
    :param path: Um objeto Path() que representa o diretório
    :return: uma lista de objetos Path() em que cada elemento
    será um diretorio que existe em `path`
    """
    return [item for item in path.iterdir() if item.is_dir()]

def get_files(path):
    """
    Obtém todos os arquivos no diretório pesquisado.
    :param path: Um objeto Path() que representa o diretório
    :return: uma lista de objetos Path() em que cada elemento
    será um arquivo que existe em `path`
    """
    return [item for item in path.iterdir() if item.is_file()]

def find_by_name(path, value):
    """
    Obtém todos os arquivos no diretório pesquisado que tenham um nome
    igual a `value` (independente da extensão).
    :param path: Um objeto Path() que representa o diretório
    :param value: str que representa o nome que os arquivos podem ter.
    :return: uma lista de objetos Path() em que cada elemento será um
    arquivo em `path` com um nome igual a `value`.
    """
    return [file for file in get_files(path) if file.stem == value]

def find_by_ext(path, value):
    """
    Obtém todos os arquivos no diretório pesquisado que tenham a extensão
    igual a `value` (independente do nome).
    :param path: Um objeto Path() que representa o diretório
    :param value: str que representa a ext. que os arquivos podem ter.
    :return: uma lista de objetos Path() em que cada elemento será um
    arquivo em `path` com uma extensão igual a `value`.
    """
    return [file for file in get_files(path) if file.suffix == value]

def find_by_mod(path, value):
    """
    Obtém todos os arquivos no diretório pesquisado que tenham uma data de
    modificação maior ou igual ao parametro informado.
    :param path: Um objeto Path() que representa o diretório
    :param value: str que representa a menor data de modificação que os
    arquivos podem ter.
    :return: uma lista de objetos Path() em que cada elemento será um
    arquivo em `path` com a data de modificação maior ou igual a `value`.
    """
    # input: dd/mm/aaaa
    try:
        datetime_obj = datetime.strptime(value, "%d/%m/%Y")
    except ValueError:
        raise InvalidInputError(f"'{value}' não é uma data válida no formato dd/mm/aaaa.")

    return [file for file in get_files(path) if datetime.fromtimestamp(file.stat().st_mtime) >= datetime_obj]

def timestamp_to_string(system_timestamp):
    """
    A partir de um timestamp de sistema, gera uma string humanamente
    legivel com a mesma informação de data e hora.
    :param system_timestamp: um float que representa um timestamp do sistema
    :return: uma string que representa o timestamp em 'dd/mm/aaaa - hh:mm:ss.uuuuu'
    """
    datetime_obj = datetime.fromtimestamp(system_timestamp)
    return datetime_obj.strftime('%d/%m/%Y - %H:%M:%S:%f')

def get_files_datails(files):
    """
    Obtem a uma lista de listas contendo os detalhes importantes
    para cada arquivo representado em `files`
    :param files: uma lista de objetos Path() apontando para arquivos
    no sistema de arquivos.
    :return: uma lista de listas, em que cada elemento das listas internas
    contém: Nome, Criacao, Modificacao e Caminho para cada um dos arquivos
    em `files`
    """
    files_details = []

    for file in files:
        stat = file.stat()
        details = [
            file.name,
            timestamp_to_string(get_created_timestamp(stat)),
            timestamp_to_string(stat.st_mtime),
            file.absolute()
        ]

        files_details.append(details)

    return files_details


def get_created_timestamp(stat):
    if platform.system() == "Darwin":
        return stat.st_birthtime

    return stat.st_ctime
