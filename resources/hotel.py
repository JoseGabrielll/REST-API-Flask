from flask_restful import Resource, reqparse
from models.hotel import HotelModel

#lista de hoteis

hoteis = [
        {
            'hotel_id': '1231',
            'nome': 'Hotel Manaira',
            'estrelas': 4.3,
            'diaria': 420.00,
            'cidade': 'JP'
        },
        {
            'hotel_id': '2323',
            'nome': 'Hotel Globo',
            'estrelas': 4.0,
            'diaria': 220.00,
            'cidade': 'JP'
        },
        {
            'hotel_id': '4321',
            'nome': 'Hotel Turismo',
            'estrelas': 4.8,
            'diaria': 510.00,
            'cidade': 'Rio'
        }
]


class Hoteis(Resource): #primeiro recurso da api
    def get(self):
        return {'hoteis': hoteis} #retornando uma lista de elementos

class Hotel(Resource):

    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome')
    argumentos.add_argument('estrelas')
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')

    def find_hotel(hotel_id):
        for hotel in hoteis:
            if hotel['hotel_id'] == hotel_id:
                return hotel
        return None #se nao achar o hotel retorna none

    def get(self, hotel_id): #selecionar algum hotel de acordo com seu id
        hotel = Hotel.find_hotel(hotel_id)

        if hotel is not None:
            return hotel
        return{'message': 'Hotel não encontrado'}, 404 #codigo http not found

    def post(self, hotel_id): #cria um novo hotel. O id do hotel é passado pelo link

        dados = Hotel.argumentos.parse_args() #aqui estão todas as chaves e conteudos passados

        '''
        #Forma mais otimozada de passar os dados lá no put
        novo_hotel = { 
            'hotel_id': hotel_id,
            'nome': dados['nome'],
            'estrelas': dados['estrelas'],
            'diaria': dados['diaria'],
            'cidade': dados['cidade']
        }
        '''
        hotel_objeto = HotelModel(hotel_id, **dados)
        novo_hotel = hotel_objeto.json() #convertendo o objeto para dicionário

        hoteis.append(novo_hotel)
        return novo_hotel, 200 #codigo http de sucesso
    
    def put(self, hotel_id): #Se passar um id que existe ele altera os dados. Se o id n existir, cria um novo
        dados = Hotel.argumentos.parse_args()
        #novo_hotel = {'hotel_id': hotel_id, **dados} #Passando para o dicionário todos os argumentos de dados

        hotel_objeto = HotelModel(hotel_id, **dados)
        novo_hotel = hotel_objeto.json() #convertendo o objeto para dicionário

        hotel = Hotel.find_hotel(hotel_id) #Verifica se o hotel já existe     
        if hotel: #if hotel is not None
            hotel.update(novo_hotel)
            return novo_hotel, 200
        else:
            hoteis.append(novo_hotel)
            return novo_hotel, 201 #codigo para criado  

    def delete(self, hotel_id):
        global hoteis
        hoteis = [hotel for hotel in hoteis if hotel['hotel_id'] != hotel_id]
        return {'message': 'Hotel deletado'}