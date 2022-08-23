from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

CLIENTES = [{'nome':'Carlos', 'idade':30, 'profissao':'Médico', 'conta':'1000', 'saldo':5000},
            {'nome':'Luiz', 'idade':50, 'profissao':'Advogado', 'conta':'1001', 'saldo':7500},
            {'nome':'Maria', 'idade':31, 'profissao':'Juíza', 'conta':'1002', 'saldo':10000},
            {'nome':'Fabio', 'idade':26, 'profissao':'Programador', 'conta':'1003', 'saldo':3000},
            {'nome':'Ana', 'idade':35, 'profissao':'Professora', 'conta':'1004', 'saldo':600}]

# Classe para retornar todos os clientes
class Clientes(Resource):
    def get(self):
        return {"Clientes": CLIENTES}

class Cliente(Resource):
    def get(self, conta):
        for cliente in CLIENTES:
            if cliente["conta"] == conta:
                return {"Cliente": cliente}, 200
        return {"ERRO": "Cliente não encontrado"}, 404

    def post(self, conta):
        # Vamos verificar se a conta já existe
        for cliente in CLIENTES:
            if cliente["conta"] == conta:
                return {"Mensagem": f"Cliente com conta {conta} já existe"}, 409

        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('nome', location='form', required=True, type=str)
        parser.add_argument('idade', location='form', required=True, type=int)
        parser.add_argument('profissao', location='form', required=True, type=str)
        parser.add_argument('saldo', location='form', required=True, type=float)

        dados = parser.parse_args()
        dados['conta'] = conta
        CLIENTES.append(dados)

        return {"Mensagem": 'Cliente cadastrado com sucesso!'}, 201

    def delete(self, conta):
        for cliente in CLIENTES:
            if cliente['conta'] == conta:
                CLIENTES.remove(cliente)
                return {"Mensagem": f"Cliente com conta {conta}"
                                    f" foi excluída!"}, 200 # ou 204
        return {"Mensagem": f"Cliente com conta {conta} não foi encontrado"}, 409

    def put(self, conta):
        # Atualizar os dados dos clientes já cadastrados
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('nome', location='form', required=False, type=str)
        parser.add_argument('idade', location='form', required=False, type=int)
        parser.add_argument('profissao', location='form', required=False, type=str)
        parser.add_argument('saldo', location='form', required=False, type=float)

        dados = parser.parse_args()
        for cliente in CLIENTES:
            if cliente['conta'] == conta:
                cliente['nome'] = dados['nome'] or cliente['nome']
                cliente['idade'] = dados['idade'] or cliente['idade']
                cliente['profissao'] = dados['profissao'] or cliente['profissao']
                cliente['saldo'] = dados['saldo'] or cliente['saldo']
                return {"Mensagem": "Dados atualizados com sucesso!"}, 200

        return {"Mensagem": f"Cliente com conta {conta} não foi encontrado"}, 409


api.add_resource(Clientes, '/clientes')
api.add_resource(Cliente, '/clientes/<string:conta>')

if __name__ == '__main__':
    app.run(debug=True)