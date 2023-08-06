from file_finder.utils import find_by_ext
from file_finder.utils import find_by_name
from file_finder.utils import find_by_mod


SEARCH_MAPPING = {
    "name": find_by_name,
    "ext": find_by_ext,
    "mod": find_by_mod,
}


TABLE_HEADERS = ["Nome", "Criação", "Modificação", "Localização"]