import requests
from bs4 import BeautifulSoup
import json
import time
import schedule
from datetime import datetime
from database import Database
from dotenv import load_dotenv
from bot import BOT

class Crawler:
    
    def __init__(self):
        load_dotenv()
        self.db = Database()
        self.bot =  BOT()

    def request_data(self, url: str, retry: bool = False):
        try:    
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup
        except Exception as e:
            if not retry:
                time.sleep(3)
                return self.request_data(url, True)
            else:
                raise e
    
    @staticmethod
    def format_price(price: str) -> float:
        return float(price.replace('R$', '')).replace('.', '').replace(('.', ''))
    
    def extract_from_website(self, page: int = 1, retry: bool = False) -> None:
        # Realiza uma solicitação HTTP para uma página da web e obtém seu conteúdo
        raw_website = self.request_data(
            f'https://lista.mercadolivre.com.br/_Deal_selecao-console-gamer#deal_print_id=d4cae6a0-6baf-11ee-a944-29c31240e153&c_id=banner-small&c_element_order=2&c_campaign=BANNER_SMALL_CONSOLES&c_uid=d4cae6a0-6baf-11ee-a944-29c31240e153{page}'
        )
        products = raw_website.find_all('div', {'class': 'ui-search-results ui-search-results--without-disclaimer'})
        
        if products is None:
            if not retry:
                time.sleep(3)
                self.extract_from_website(retry=True)
        else:
            # Itera sobre os produtos encontrados na página
            for product in products:
                title = product.find('span', {'class': 'ui-search-item__title'}).text
                
                link = 'https://www.mercadolivre.com.br/' + str(product.find('a', {'class': 'ui-pdp--sticky-wrapper ui-pdp--sticky-wrapper-center'})['href'])
                second_request = self.request_data(link)

                price = second_request.find("h4", {'class': 'ui-search-item__group__element ui-search-link'}).text
                price = self.format_price(price)

                image = second_request.find_all("script")[1].text.replace('\\\\"', '')
                image = json.loads(image)['image']

                data = {
                    'image': image,
                    'title': title,
                    'price': price,
                    'link': link,
                    'date': datetime.now
                }
                
                response = self.db.insert(data)
                if response is not None:
                    if 'old_price' in response:
                        response["old_price"] = 0
                    self.bot.post(response)


    def execute(self, num_pages: int = 3):
        # Itera sobre um número especificado de páginas e extrai informações dos produtos em cada página
        for page in range(1, num_pages):
            self.extract_from_website(page)

if __name__ == '__main__':
    crawler = Crawler()
    
    # Inicializa o web crawler para extrair informações da página
    crawler.execute(1)

    def job():
        # Define uma função que será agendada para execução periódica
        print('\n Execute job. Time: {}'.format(str(datetime.now())))
        crawler.execute()
    
    # Agenda a execução da função "job" a cada 2 minutos
    schedule.every(2).minutes.do(job)

    while True:
        # Mantém o programa em execução para permitir a execução agendada
        schedule.run_pending()
