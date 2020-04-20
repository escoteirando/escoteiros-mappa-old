import os
import unittest

from dotenv import load_dotenv

from mappa.service.mappa_export_service import MAPPAExportService
from mappa.service.mappa_service import MAPPAService


class TestExportXLSX(unittest.TestCase):

    def setUp(self):
        load_dotenv('.testing_env', verbose=True)
        self.cache_file = os.getenv('CACHE')
        self.username = os.getenv('MAPPA_USER')
        self.password = os.getenv('MAPPA_PASS')
        self.svc = MAPPAService(self.cache_file)
        self.svc.login(self.username, self.password)
        self.esvc = MAPPAExportService(self.svc)

    def test_exporta_progressoes(self):
        wb = self.esvc.export_all('A')
        wb.save('test.xlsx')

