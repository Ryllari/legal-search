from abc import abstractmethod, ABC

import requests

from bs4 import BeautifulSoup


class BaseCrawler(ABC):
    def __init__(self, process_number: str):
        self.base_url = ''
        self.context = None
        self.process_number = process_number

    @abstractmethod
    def get_first_instance_url(self) -> str:
        pass

    @abstractmethod
    def get_second_instance_url(self) -> str:
        pass

    @abstractmethod
    def get_base_context(self) -> list:
        pass

    @abstractmethod
    def search_data(self, context_list: list, search_value: str) -> (str, list):
        pass

    def get_base_data(self, base_context: list) -> dict:
        data = {}
        params = {'class': 'Classe', 'area': 'Área', 'subject': 'Assunto', 'distribution_date': 'Distribuição',
                  'judge': 'Juiz', 'action_value': 'Valor da ação'}
        for key, value in params.items():
            data[key], base_context = self.search_data(base_context, value)
        return data

    def get_moviments(self) -> list:
        moviments = []
        html_moviments = self.context.select('#tabelaTodasMovimentacoes tr')
        for mv in html_moviments:
            td = mv.select('td')
            date = td[0].text.strip()
            moviment = td[2].text.strip().replace('\n', '').replace('\t', '')
            moviments.append({'date': date, 'moviment': moviment})
        return moviments

    def get_parts(self) -> list:
        parts = []
        html_moviments = self.context.select('#tableTodasPartes tr')
        for mv in html_moviments:
            td = mv.select('td')
            part_type = td[0].text.strip().replace(':', '')
            name = td[1].text.strip().replace('\n', '').replace('\t', '')
            parts.append({'part_type': part_type, 'name': name})
        return parts

    def get_instance_data(self, url: str):
        instance_data = {}
        response = requests.get(url)
        self.context = BeautifulSoup(response.content, features="html.parser")
        base_context = self.get_base_context()

        if not base_context:
            print("Nao há processos para esta instancia")
            return instance_data

        instance_data.update(self.get_base_data(base_context))
        instance_data['parts'] = self.get_parts()
        instance_data['moviments'] = self.get_moviments()

        return instance_data

    def get_process_info(self):
        first_url = self.get_first_instance_url()
        second_url = self.get_second_instance_url()

        return {
            'process_number': self.process_number,
            'first_instance_data': self.get_instance_data(first_url),
            'second_instance_data': self.get_instance_data(second_url)
        }
