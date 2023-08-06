import click
import shutil
from tabulate import tabulate
from pathlib import Path
from file_finder.utils import get_files_datails
from file_finder.utils import get_folders
from datetime import datetime
from file_finder.constants import SEARCH_MAPPING
from file_finder.constants import TABLE_HEADERS
from file_finder.exceptions import InvalidInputError
from file_finder.exceptions import ZeroFilesFoundError
from file_finder.exceptions import FileFinderError

def process_search(path, key, value, recursive):
    """
    Detém toda lógica necessária para realizar a pesquisa
    conforme os inputs do usuário
    :param path: Um objeto Path() que representa o diretório
    :param key: str que representa a chave de pesquisa.
    :param value: str que representa o nome que os arquivos podem ter.
    :param recursive: boolean que determina se a pesquisa deve percorrer
    os subdiretórios ou não.
    :return: Uma lista de objetos Path(), cada um representando um
     arquivo encontrado pela pesquisa
    """
    files = SEARCH_MAPPING[key](path, value)

    if recursive:
        subdirs = get_folders(path)
        for subdir in subdirs:
            files += process_search(subdir, key, value, recursive)

    return files

def process_results(files, key, value):
    """
    Processa os resultados da pesquisa, exibindo-os na tela em formato
    de tabela.
    :param files: Uma lista de objetos Path(), cada um representando um
     arquivo encontrado pela pesquisa
    :param key: str que representa a chave de pesquisa.
    :param value: str que representa o nome que os arquivos podem ter.
    :return: A string que representa os resultados tabulados.
    """
    if not files:
        raise ZeroFilesFoundError(f"Nenhum arquivo com {key} {value} foi encontrado.")

    table_data = get_files_datails(files)
    tabulated_data = tabulate(tabular_data=table_data, headers=TABLE_HEADERS, tablefmt="tsv")
    click.echo(tabulated_data)
    return  tabulated_data

def save_report(save, report, root):
    """
    Determina se o report deve ser ou nao salvo em um arquivo.
    Se sim, cria um arquivo no diretório 'root' com nome
    'finder_report_<timestamp>.txt' contendo os resultados em formato
    tabular.
    :param save: boolean que diz se um arquivo com o report deve ser
    criado ou nao
    :param report: string que representa os resultados tabulados.
    :param root: Path() que aponta para o diretorio da pesquisa.
    :return: None
    """
    if save and report:
        report_file_path = root / f"finder_report_{datetime.now().strftime('%d%m%Y%H%M%S%f')}.txt"
        with open(report_file_path.absolute(), mode="w") as report_file:
            report_file.write(report)

def copy_files(copy_to, files):
    """
    Copia arquivos encontrados na pesquisa para um diretorio
    especifico.

    :param copy_to: str que informa o nome do diretorio para onde
    os arquivos representados em 'files' devem ser copiados.
    :param files: uma lista de objetos Path() representando cada um
    dos arquivos encontrados na busca
    :return: None
    """
    if copy_to:
        copy_path = Path(copy_to)

        if not copy_path.is_dir():
            copy_path.mkdir(parents=True)

        for file in files:
            dst_file = copy_path / file.name

            if dst_file.is_file():
                dst_file = copy_path / f"{file.stem}{datetime.now().strftime('%d%m%Y%H%M%S%f')}{file.suffix}"

            shutil.copy(src=file.absolute(), dst=dst_file)

@click.command()
@click.argument("path", default="")
@click.option("-k", "--key", required=True, type=click.Choice(SEARCH_MAPPING.keys()), help="Define a chave de busca.")
@click.option("-v", "--value", required=True, help="Define o valor para a chave.")
@click.option("-r", "--recursive", is_flag=True, default=False, help="Se presente, realiza busca recursiva.")
@click.option("-s", "--save", is_flag=True, default=False, help="Se presente, salva um report da busca realiza no diretorio PATH.")
@click.option("-c", "--copy-to", help="Copia de todos os arquivos encontrados para diretorio informado.")
def finder(path, key, value, recursive, copy_to, save):
    """
    Um programa que realiza busca de arquivos atraves de uma chave (-k|--key) a partir do diretorio PATH.

    PATH define o diretorio onde a pesquisa inicia. Se nao informado, assume o diretorio atual.
    """
    root = Path(path)

    if not root.is_dir():
        raise InvalidInputError(f"O caminho '{path}' não representa um diretório existente.")

    click.echo(f"O diretório selecionado foi: {root.absolute()}")

    files = process_search(path=root, key=key, value=value, recursive=recursive)
    report = process_results(files=files, key=key, value=value)
    save_report(save=save, report=report, root=root)
    copy_files(copy_to=copy_to, files=files)


if __name__ == "__main__":
    try:
        finder()
    except FileFinderError as err:
        click.echo(click.style(f"❌ {err}", bg='black', fg='red', italic=True))
