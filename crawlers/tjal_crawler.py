from abc import ABC

from crawlers.base_crawler import BaseCrawler


class TJALCrawler(BaseCrawler, ABC):
    """
    Crawler for TJ-AL search.
    """
    def __init__(self, process_number: str):
        super(TJALCrawler, self).__init__(process_number)
        self.base_url = 'https://www2.tjal.jus.br/cpo{}/search.do?cbPesquisa=NUMPROC&tipoNuProcesso=UNIFICADO&{}'
        self.tj = 'TJ-AL'

    def get_first_instance_url(self) -> str:
        first_level, process_search = 'pg', f'dadosConsulta.valorConsultaNuUnificado={self.process_number}'
        return self.base_url.format(first_level, process_search)

    def get_second_instance_url(self) -> str:
        second_level, process_search = 'sg5', f'dePesquisaNuUnificado={self.process_number}'
        return self.base_url.format(second_level, process_search)

    def get_base_context(self) -> list:
        return self.context.select('.secaoFormBody:not(#secaoFormConsulta) tr')

    def search_data(self, context_list: list, search_value: str) -> (str, list):
        for tr in context_list:
            td = tr.find('td')
            if search_value in td.text.strip():
                context_list.remove(tr)
                try:
                    return td.find_next_sibling('td').text.strip(), context_list
                except AttributeError:
                    return td.contents[-1].strip(), context_list
        return None, context_list
