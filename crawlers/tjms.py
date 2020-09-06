import requests

from bs4 import BeautifulSoup


def get_base_data(context) -> dict:
    def search_data(div_list, search_value):
        for div in div_list:
            if div.span and search_value in div.span.text:
                div_list.remove(div)
                return div.div.text.strip(), div_list
        return None, div_list

    data = {}
    params = {'class': 'Classe', 'area': 'Área', 'subject': 'Assunto', 'distribution_date': 'Distribuição',
              'judge': 'Juiz', 'action_value': 'Valor da ação'}
    for key, value in params.items():
        data[key], context = search_data(context, value)
    return data


def get_moviments(context):
    moviments = []
    html_moviments = context.select('#tabelaTodasMovimentacoes tr')
    for mv in html_moviments:
        td = mv.select('td')
        date = td[0].text.strip()
        moviment = td[2].text.strip().replace('\n', '').replace('\t', '')
        moviments.append({'date': date, 'moviment': moviment})
    return moviments


def get_parts(context):
    parts = []
    html_moviments = context.select('#tableTodasPartes tr')
    for mv in html_moviments:
        td = mv.select('td')
        part_type = td[0].text.strip()
        name = td[1].text.strip().replace('\n', '').replace('\t', '')
        parts.append({'part_type': part_type, 'name': name})
    return parts


def get_instance_data(url: str):
    instance_data = {}
    response = requests.get(url)
    soup = BeautifulSoup(response.content, features="html.parser")
    header = soup.select('.unj-entity-header__summary .container .row')  # principais

    if not header:
        print("Nao há processos para esta instancia")
        return instance_data

    more_details = soup.select('.unj-entity-header__details .container .row div')
    base_context = header[1].select('div') + more_details

    instance_data.update(get_base_data(base_context))
    instance_data['parts'] = get_parts(soup)
    instance_data['moviments'] = get_moviments(soup)

    return instance_data


def get_process_info(process_number: str):
    base_url = 'https://esaj.tjms.jus.br/cpo{}'

    # Search First instance
    first_search = f'pg5/show.do?processo.numero={process_number}'
    first_url = base_url.format(first_search)
    first_instance = get_instance_data(first_url)

    # Search Second instance
    second_search = f'sg5/search.do?cbPesquisa=NUMPROC&tipoNuProcesso=UNIFICADO&dePesquisaNuUnificado={process_number}'
    second_url = base_url.format(second_search)
    second_instance = get_instance_data(second_url)

    return {
        'process_number': process_number,
        '1st_instance': first_instance,
        '2nd_instance': second_instance
    }
