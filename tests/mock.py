def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, status_code, content):
            self.status_code = status_code
            self.content = content

    filename = '0.html'  # Default file return process without data TJ-AL

    # TJ-MS urls
    if args[0] == 'https://esaj.tjms.jus.br/cpopg5/show.do?processo.numero=0821901-51.2018.8.12.0001':
        filename = 'tjms1.html'

    elif args[0] == 'https://esaj.tjms.jus.br/cposg5/search.do?cbPesquisa=NUMPROC&tipoNuProcesso=UNIFICADO&' \
                    'dePesquisaNuUnificado=0821901-51.2018.8.12.0001':
        filename = 'tjms2.html'

    # TJ-AL urls
    elif args[0] == 'https://www2.tjal.jus.br/cpopg/search.do?cbPesquisa=NUMPROC&tipoNuProcesso=UNIFICADO&' \
                    'dadosConsulta.valorConsultaNuUnificado=0710802-55.2018.8.02.0001':
        filename = 'tjal1.html'
    elif args[0] == 'https://www2.tjal.jus.br/cposg5/search.do?cbPesquisa=NUMPROC&tipoNuProcesso=UNIFICADO&' \
                    'dePesquisaNuUnificado=0710802-55.2018.8.02.0001':
        filename = 'tjal2.html'

    with open(f'tests/mock_files/{filename}', 'r') as f:
        content_file = f.read()
        return MockResponse(200, content_file)
