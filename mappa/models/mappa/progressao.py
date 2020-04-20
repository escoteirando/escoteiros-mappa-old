from base_model import BaseModel


class ProgressaoModel(BaseModel):

    codigo: int
    descricao: str
    codigoUeb: str
    ordenacao: int
    codigoCaminho: int
    codigoDesenvolvimento: int
    numeroGrupo: int
    codigoRegiao: str
    codigoCompetencia: int
    segmento: str

    @property
    def ramo(self):
        """ Retorna o tipo do ramo da progressão

        A = Alcatéia, E = Escoteiro, S = Sênior, P = Pioneiro"""
        if self.codigoCaminho in [1, 2, 3]:
            return 'A'
        elif self.codigoCaminho in [4, 5, 6]:
            return 'E'
        elif self.codigoCaminho in [11, 12]:
            return 'S'
        elif self.codigoCaminho in [15, 16]:
            return 'P'

        return '_'
