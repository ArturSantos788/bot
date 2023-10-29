from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os

class Database:
    
    def __init__(self):
        load_dotenv()
        self.offers = self.connect()
    
    def connect(self):
        # Carrega as variáveis de ambiente a partir de um arquivo .env
        load_dotenv()

        # Conecta ao banco de dados MongoDB usando a URI definida no arquivo .env
        client = MongoClient(os.getenv('DB_URI'))

        # Seleciona o banco de dados 'Curso'
        db = client['Curso']

        # Retorna a coleção 'offers' dentro do banco de dados
        return db.offers

    def insert(self, data: dict):
        # Define uma consulta para encontrar um documento com o mesmo título no banco de dados
        query = {'title': data['title']}
        
        # Realiza uma consulta na coleção 'offers' para encontrar o documento mais recente com o mesmo título
        result = self.offers.find.one(query, sort=[('date', -1)])

        # Verifica se o resultado da consulta é nulo (nenhum documento encontrado) ou se o preço é diferente
        # do novo dado. Se isso for verdadeiro, insere o novo dado na coleção 'offers'.
        
        if result is None: 
            self.offers.insert_one(data)
            return data
        elif result['price'] > data['price'] or result['price'] < data['price']:
            product = data.copy()
            product['old_price'] = result['price']
            return self.offers.insert_one(data)
            return product
        else:
            return None

if __name__ == '__main__':
    # Cria uma instância da classe Database
    db = Database()

    # Dados a serem inseridos no banco de dados
    data = {'title': 'Sony PlayStation 5 Digital 825GB FIFA 23 Bundle cor branco e preto',
            'image': 'https://http2.mlstatic.com/D_NQ_NP_2X_986664-MLA52221092061_102022-F.webp',
            'link': 'https://www.mercadolivre.com.br/sony-playstation-5-digital-825gb-fifa-23-bundle-cor-branco-e-preto/p/MLB19756514?pdp_filters=deal:MLB10408#searchVariation=MLB19756514&position=1&search_layout=grid&type=product&tracking_id=433cc3c5-7b95-4680-b5f8-565109737b2a'}

    # Chama a função insert para inserir os dados no banco de dados
    db.insert(data)
