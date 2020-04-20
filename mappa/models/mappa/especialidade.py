from typing import List

from base_model import BaseModel
from mappa.models.mappa.item_especialidade import ItemEspecialidadeModel


class EspecialidadeModel(BaseModel):

    codigo: int
    descricao: str
    ramoConhecimento: str
    prerequisito: str
    itens: List[ItemEspecialidadeModel]
