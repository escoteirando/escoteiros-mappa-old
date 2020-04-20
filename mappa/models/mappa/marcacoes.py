from datetime import datetime
from typing import List

from base_model import BaseModel
from mappa.models.mappa.marcacao import MarcacaoModel


class MarcacoesModel(BaseModel):

    dataHora: datetime
    values: List[MarcacaoModel]
