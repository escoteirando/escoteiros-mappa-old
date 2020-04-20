import unittest
from datetime import datetime, tzinfo

from dateutil.tz import tzutc

from mappa.models.mappa.associado import AssociadoModel
from mappa.models.mappa.escotista import EscotistaModel
from mappa.models.mappa.login import LoginModel


class TestResponseModels(unittest.TestCase):

    def test_login_mappa(self):
        data = '''{
    "id": "904QVxCGR0mLG6uDqWt7EOZLZZyfbaBRatKnoMefohwfkpPjc5jeuyUNAWED5t7H",
    "ttl": 1209600,
    "created": "2019-10-26T02:19:09.146Z",
    "userId": 50442
}'''
        login = LoginModel(data)

        self.assertEqual(
            login.id, "904QVxCGR0mLG6uDqWt7EOZLZZyfbaBRatKnoMefohwfkpPjc5jeuyUNAWED5t7H")
        self.assertEqual(login.ttl, 1209600)
        self.assertEqual(login.created, datetime(
            2019, 10, 26, 2, 19, 9, 146000, tzutc()))
        self.assertEqual(login.userId, 50442)

    def test_associado_mappa(self):
        data = '''{
    "codigo":850829,
    "nome":"GUIONARDO FURLAN",
    "codigoFoto":null,
    "codigoEquipe":null,
    "username":1247937,
    "numeroDigito":3,
    "dataNascimento":"Sat Feb 05 1977 00:00:00 GMT+0000 (UTC)",
    "dataValidade":"2019-01-01T00:00:00.000Z",
    "nomeAbreviado":"",
    "sexo":"M",
    "codigoRamo":2,
    "codigoCategoria":5,
    "codigoSegundaCategoria":0,
    "codigoTerceiraCategoria":0,
    "linhaFormacao":"Escotista",
    "codigoRamoAdulto":2,
    "dataAcompanhamento":null
}'''
        associado = AssociadoModel(data)
        self.assertEqual(associado.codigo, 850829)
        self.assertEqual(associado.nome, 'GUIONARDO FURLAN')
        self.assertEqual(associado.codigoFoto, None)
        self.assertEqual(associado.dataAcompanhamento, None)

    def test_escotista_mappa(self):
        data = '''{
        "codigo": 50442,
        "codigoAssociado": 850829,
        "username": "Guionardo",
        "nomeCompleto": "GuionardoFurlan",
        "ativo": "S",
        "codigoGrupo": 32,
        "codigoRegiao": "SC",
        "codigoFoto": null
    }'''
        escotista = EscotistaModel(data)
        self.assertEqual(escotista.codigo, 50442)
        self.assertEqual(escotista.codigoAssociado, 850829)
        self.assertEqual(escotista.ativo, 'S')
