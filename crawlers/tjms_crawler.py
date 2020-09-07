from abc import ABC

from crawlers.base_crawler import BaseCrawler


class TJMSCrawler(BaseCrawler, ABC):
    """
    Crawler for TJ-MS search.
    """
    def __init__(self, process_number: str):
        super(TJMSCrawler, self).__init__(process_number)
        self.base_url = 'https://esaj.tjms.jus.br/cpo{}'
        self.tj = 'TJ-MS'

    def get_first_instance_url(self) -> str:
        base = f'pg5/show.do?processo.numero={self.process_number}'
        return self.base_url.format(base)

    def get_second_instance_url(self) -> str:
        base = f'sg5/search.do?cbPesquisa=NUMPROC&tipoNuProcesso=UNIFICADO&dePesquisaNuUnificado={self.process_number}'
        return self.base_url.format(base)

    def get_base_context(self) -> list:
        header = self.context.select('.unj-entity-header__summary .container .row')
        more_details = self.context.select('.unj-entity-header__details .container .row div')

        try:
            return header[1].select('div') + more_details
        except (ValueError, Exception):
            return []

    def search_data(self, context_list: list, search_value: str) -> (str, list):
        for div in context_list:
            if div.span and search_value in div.span.text:
                context_list.remove(div)
                return div.div.text.strip(), context_list
        return None, context_list
