from base_model import BaseModel


class SecaoModel(BaseModel):
    codigo: int
    nome: str
    codigoTipoSecao: int
    codigoGrupo: int
    codigoRegiao: str
