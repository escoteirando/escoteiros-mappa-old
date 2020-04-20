import os
import unittest

from dotenv import load_dotenv

from mappa.service.mappa_service import MAPPAService
from mappa.models.mappa.login import LoginModel
from mappa.service.mappa_export_service import MAPPAExportService
from unittest.mock import Mock,patch
from tests.mocks.request import MockHTTP

class TestMAPPAService(unittest.TestCase):

    def setUp(self):
        load_dotenv('.testing_env', verbose=True)
        self.cache_file = os.getenv('CACHE')
        self.username = os.getenv('MAPPA_USER')
        self.password = os.getenv('MAPPA_PASS')
        self.svc = MAPPAService(self.cache_file)
        self.svc._http = MockHTTP(self.svc.cache)

    def tearDown(self):
        self.svc._cache.delete_value('TEST', 'LOGIN')

    def test_cache(self):
        data = '''{
    "id": "904QVxCGR0mLG6uDqWt7EOZLZZyfbaBRatKnoMefohwfkpPjc5jeuyUNAWED5t7H",
    "ttl": 1209600,
    "created": "2019-10-26T02:19:09.146Z",
    "userId": 50442
}'''
        lm = LoginModel(data)
        self.assertTrue(self.svc._cache.set_value(
            'TEST', 'LOGIN', lm.to_json()))

        cached = self.svc._cache.get_value('TEST', 'LOGIN')
        self.assertIsNotNone(cached)

        lm2 = LoginModel(cached)
        self.assertDictEqual(lm.to_dict(), lm2.to_dict())
    
    def testLogin(self):
        self.assertTrue(self.svc.login(self.username, self.password))

        userinfo = self.svc.get_user_info(self.svc._user_id)
        self.assertIsNotNone(userinfo)

        sessoes = self.svc.get_secoes(self.svc._user_id)
        self.assertEqual(len(sessoes), 1)

        equipe = self.svc.get_equipe(self.svc._user_id, sessoes[0].codigo)
        self.assertIsNotNone(equipe)

        marcacoes = self.svc.get_marcacoes(sessoes[0].codigo)
        self.assertIsNotNone(marcacoes)

    def test_base_conhecimento(self):
        self.assertTrue(self.svc.login(self.username, self.password))
        bc = self.svc.get_base_conhecimento()
        self.assertIsNotNone(bc)

    def test_export(self):
        self.assertTrue(self.svc.login(self.username, self.password))
        exp_svc = MAPPAExportService(self.svc)

        progressoes_lobo = exp_svc.get_progressoes_ramo('A')

        self.assertGreater(len(progressoes_lobo), 0)
