from datetime import date, datetime

from base_model import BaseModel


class MarcacaoModel(BaseModel):

    codigoAtividade: int
    codigoAssociado: int
    dataAtividade: date
    dataStatusJovem: datetime
    dataStatusEscotista: datetime
    statusJovem: str
    statusEscotista: str
    dataHoraAtualizacao: datetime
    codigoUltimoEscotista: int
    segmento: str
