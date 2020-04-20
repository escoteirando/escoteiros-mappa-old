from base_model.base_model import BaseModel
from datetime import datetime


class AssociadoModel(BaseModel):
    codigo: int
    nome: str
    codigoFoto: int
    codigoEquipe: int
    username: int
    numeroDigito: int
    dataNascimento: datetime
    dataValidade: datetime
    nomeAbreviado: str
    sexo: str
    codigoRamo: int
    codigoCategoria: int
    codigoSegundaCategoria: int
    codigoTerceiraCategoria: int
    linhaFormacao: str
    codigoRamoAdulto: int
    dataAcompanhamento: datetime
