from base_model import BaseModel


class EscotistaModel(BaseModel):
    codigo: int
    codigoAssociado: int
    username: str
    nomeCompleto: str
    ativo: str
    codigoGrupo: int
    codigoRegiao: str
    codigoFoto: int
