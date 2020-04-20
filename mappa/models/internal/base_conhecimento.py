from typing import List

from base_model import BaseModel
from mappa.models.mappa.especialidade import EspecialidadeModel
from mappa.models.mappa.progressao import ProgressaoModel


class BaseConhecimentoModel(BaseModel):

    progressoes: List[ProgressaoModel]
    especialidades: List[EspecialidadeModel]
