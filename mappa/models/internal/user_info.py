from datetime import date

from base_model import BaseModel


class UserInfoModel(BaseModel):    
    id: int              # e.codigo
    user_name: str       # e.username
    cod_associado: int   # e.codigoAssociado
    dig_associado: int   # e.numeroDigito
    nome_completo: str   # e.nomeCompleto
    nome_abreviado: str  # a.nomeAbreviado
    data_nascimento: date   # a.dataNascimento
    sexo: str            # a.sexo
    ativo: bool          # e.ativo (testar contra 'S')
    data_validade: date  # a.dataValidade
    
    cod_grupo: int       # e.codigoGrupo
    cod_regiao: str      # e.codigoRegiao
    nom_grupo: str       # g.nome
    cod_modalidade: int  # g.codigoModalidade

    cod_secao: int       # s.codigo
    nom_secao: str       # s.nome
    tip_secao: int       # s.codigoTipoSecao


# Associado
# {
#     "codigo": 850829,
#     "nome": "GUIONARDO FURLAN",
#     "codigoFoto": null,
#     "codigoEquipe": null,
#     "username": 1247937,
#     "numeroDigito": 3,
#     "dataNascimento": "Sat Feb 05 1977 00:00:00 GMT+0000 (UTC)",
#     "dataValidade": "2019-01-01T00:00:00.000Z",
#     "nomeAbreviado": "",
#     "sexo": "M",
#     "codigoRamo": 2,
#     "codigoCategoria": 5,
#     "codigoSegundaCategoria": 0,
#     "codigoTerceiraCategoria": 0,
#     "linhaFormacao": "Escotista",
#     "codigoRamoAdulto": 2,
#     "dataAcompanhamento": null
# }

# Escotista
# {
#     "codigo": 50442,
#     "codigoAssociado": 850829,
#     "username": "Guionardo",
#     "nomeCompleto": "GuionardoFurlan",
#     "ativo": "S",
#     "codigoGrupo": 32,
#     "codigoRegiao": "SC",
#     "codigoFoto": null
# }

# Grupo
# {
#     "codigo":32,
#     "codigoRegiao":"SC",
#     "nome":"LEÕES DE BLUMENAU",
#     "codigoModalidade":1
# }

# Seção
# {
#     "codigo": 1424,
#     "nome": "ALCATÉIA 1",
#     "codigoTipoSecao": 1,
#     "codigoGrupo": 32,
#     "codigoRegiao": "SC"
# }
