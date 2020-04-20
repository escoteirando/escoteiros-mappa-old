import datetime
import json
import time
from typing import List

from base_model import ListBaseModel
from cache_gs import CacheGS
from cache_gs.utils.logging import get_logger

from mappa.models.internal.base_conhecimento import BaseConhecimentoModel
from mappa.models.internal.user_info import UserInfoModel
from mappa.models.mappa.associado import AssociadoModel
from mappa.models.mappa.escotista import EscotistaModel
from mappa.models.mappa.especialidade import EspecialidadeModel
from mappa.models.mappa.grupo import GrupoModel
from mappa.models.mappa.login import LoginModel
from mappa.models.mappa.marcacao import MarcacaoModel
from mappa.models.mappa.marcacoes import MarcacoesModel
from mappa.models.mappa.progressao import ProgressaoModel
from mappa.models.mappa.secao import SecaoModel
from mappa.models.mappa.subsecao import SubSecaoModel
from mappa.tools.request import HTTP, HTTPResponse


class MAPPAService:

    def __init__(self, cache_string_connection: str = '.cache'):

        self._cache = CacheGS(cache_string_connection)
        self._logger = get_logger()
        self._http = HTTP(self._cache)
        self._user_id = None

    def login(self, username, password) -> bool:
        """ Gets authorization for username, using cache if available """

        self._http.set_authorization(None, 0)
        self._user_id = None

        try:
            cache_login = LoginModel(self._cache.get_value(
                'mappa', 'login_'+username, None))
        except:
            cache_login = LoginModel()

        if cache_login.id and \
                cache_login.ttl > 0 and \
                cache_login.userId:
            self._http.set_authorization(
                cache_login.id, cache_login.created.timestamp()+cache_login.ttl)
            self._user_id = cache_login.userId
            self._logger.info('login from cache (%s) valid until (%s)',
                              username, datetime.datetime.fromtimestamp(cache_login.ttl))
            return True

        # Sem informação de login ou autorização expirada - Efetua o request a API mappa

        response = self._http.post(
            url='/api/escotistas/login',
            params={"type": "LOGIN_REQUEST",
                    "username": username,
                    "password": password})

        if not response.is_ok:
            self._logger.warning('login user (%s) failed', username)
            return False

        login_user = LoginModel(response.content)
        if not login_user.ttl:
            self._logger.warning('login user (%s) failed: TTL unidentified')
            return False

        valid_until = login_user.created + \
            datetime.timedelta(seconds=login_user.ttl)

        self.cache.set_value(
            section='mappa',
            key='login_'+username,
            value=login_user.to_json(),
            ttl=login_user.ttl
        )
        
        self._http.set_authorization(login_user.id, time.time()+login_user.ttl)
        self._user_id = login_user.userId
        self._logger.info(
            'login from mappa (%s) valid until (%s)',
            username, valid_until)
        return True

    def get_user_info(self, user_id) -> UserInfoModel:
        escotista = self.get_escotista(user_id)
        if not escotista:
            return None

        associado = self.get_associado(escotista.codigoAssociado)
        if not associado:
            return None

        grupo = self.get_grupo(escotista.codigoGrupo, escotista.codigoRegiao)
        if not grupo:
            return None

        user_info = {
            "id": escotista.codigo,
            "user_name": escotista.username,
            "cod_associado": escotista.codigoAssociado,
            "dig_associado": associado.numeroDigito,
            "nome_completo": escotista.nomeCompleto,
            "nome_abreviado": associado.nomeAbreviado,
            "data_nascimento": associado.dataNascimento,
            "sexo": associado.sexo,
            "ativo": escotista.ativo == 'S',
            "data_validade": associado.dataValidade,
            "cod_grupo": escotista.codigoGrupo,
            "cod_regiao": escotista.codigoRegiao,
            "nom_grupo": grupo.nome,
            "cod_modalidade": grupo.codigoModalidade,
        }

        return UserInfoModel(user_info)

    def get_escotista(self, user_id) -> EscotistaModel:
        """ Retorna o escotista do usuário

        :param userId: userId obtido a partir do Login
        """

        response = self._http.get(f'/api/escotistas/{user_id}', 'Escotista')

        if response.is_ok:
            escotista = EscotistaModel(response.content)
        else:
            escotista = None

        return escotista

    def get_associado(self, cod_associado) -> AssociadoModel:
        """ Retorna o associado do usuário

        :param userId: userId obtido a partir do login
        """
        response = self._http.get(
            f"/api/associados/{cod_associado}", 'Associado')

        if response.is_ok:
            associado = AssociadoModel(response.content)
        else:
            associado = None

        return associado

    def get_grupo(self, cod_grupo, cod_regiao) -> GrupoModel:
        """ Retorna o grupo escoteiro """
        filter = {"filter": {
            "where": {
                "codigo": cod_grupo,
                "codigoRegiao": cod_regiao
            }
        }}
        response = self._http.get(f'/api/grupos',
                                  params=filter,
                                  description='Grupo')
        grupo = None
        if response.is_ok:
            list_grupo = ListBaseModel(GrupoModel, response.content)
            if len(list_grupo) > 0:
                grupo = list_grupo[0]

        return grupo

    def get_secoes(self, user_id) -> List[SecaoModel]:
        """ Retorna as seções do associado """
        response = self._http.get(f'/api/escotistas/{user_id}/secoes')

        secoes = []
        if response.is_ok:
            list_secao = ListBaseModel(SecaoModel, response.content)
            secoes = list_secao.to_list()

        else:
            secoes = []

        return secoes

    def get_equipe(self, user_id, cod_secao) -> List[SubSecaoModel]:
        """ Retorna as subsecoes, com seus integrantes """
        filter = {"filter": {"include": "associados"}}
        response = self._http.get('/api/escotistas/{0}/secoes/{1}/equipes'.
                                  format(user_id, cod_secao), params=filter)
        equipe = []
        if response.is_ok:
            le = ListBaseModel(SubSecaoModel, response.content)
            equipe = le.to_list()

        return equipe

    def get_base_conhecimento(self) -> BaseConhecimentoModel:
        progressoes = self.get_progressoes()
        if not progressoes:
            return None
        especialidades = self.get_especialidades()
        if not especialidades:
            return None

        bc = {
            "progressoes": progressoes,
            "especialidades": especialidades
        }

        kb = BaseConhecimentoModel(bc)
        return kb

    def get_progressoes(self) -> List[ProgressaoModel]:
        """ Retorna todas as progressões disponíveis """
        filter = {"filter":
                  {"where":        {
                      "numeroGrupo": None,
                      "codigoRegiao": None,
                      "codigoCaminho": {"inq": [1, 2, 3, 4, 5, 6, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]}
                  }}}
        response = self._http.get(
            '/api/progressao-atividades', params=filter)
        progressoes = []
        if response.is_ok:
            lp = ListBaseModel(ProgressaoModel, response.content)
            progressoes = lp.to_list()

        return progressoes

    def get_especialidades(self) -> List[EspecialidadeModel]:
        """ Retorna todas as especialidades disponíveis """
        filter = {
            "filter[include]": "itens"
        }
        response = self._http.get(
            '/api/especialidades', params=filter, description='Especialidades')
        especialidades = []
        if response.is_ok:
            le = ListBaseModel(EspecialidadeModel, response.content)
            especialidades = le.to_list()

        return especialidades

    def get_marcacoes(self, cod_secao) -> List[MarcacaoModel]:
        """ Retorna todas as marcações dos associados da seção """
        url = '/api/marcacoes/v2/updates?dataHoraUltimaAtualizacao={0}&codigoSecao={1}'.format(
            "1970-01-01T00:00:00.000Z",
            cod_secao
        )

        response = self._http.get(
            url, description="Marcações", max_age=86400)
        marcacoes = []

        if response.is_ok:
            lm = MarcacoesModel(response.content)
            marcacoes = lm.values

        return marcacoes

    @property
    def cache(self) -> CacheGS:
        return self._cache
