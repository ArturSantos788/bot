import requests                 
from bs4 import BeautifulSoup   
import re

class Crawler:
# Solicitará o http para obter o conteúdo da página.
    def request_data(self, url: str):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
# Aqui será extraido o conteúdo da página.        
    def extract_from_website(self):
        raw_website = self.request_data('https://www.kabum.com.br/gamer?page_number=1&page_size=20&facet_filters=&sort=-number_ratings')

        products = raw_website.find_all('div', {'class': 'productCard'})

        all_data = []
# Aqui vão ser extraídos o nome, o preço, a imagem e o link do produto.
        for product in products:
            title = product.find('span', {'class': 'nameCard'})
            raw_price = product.find('span', {'class': 'priceCard'}).text

            price = str(raw_price.replace('R$ ', ''))
            format_price = float(price.replace('.', '').replace(',', '.'))
            
            link = product.find('a', {'class': 'productLink'})
# Aqui todas as imformações são postas em uma lista, depois, essa lista é impressa, mostrando todas as informações extraídas.
            data = {
                'image': image.attrs['src'],
                'title': title.text,
                'price': format_price,
                'link': 'https://www.kabum.com.br/' + link.attrs['href']
            }
            all_data.append(data)
        
        print(all_data)

if __name__ == '__main__':
    crawler = Crawler()
    crawler.extract_from_website()
