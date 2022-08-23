from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

CLIENTES = [{'conta':'1000', 'nome':'Carlos', 'idade':30, 'profissao':'Médico', 'saldo':5000},
            {'conta':'1001', 'nome':'Luiz', 'idade':50, 'profissao':'Advogado', 'saldo':7500},
            {'conta':'1002', 'nome':'Maria', 'idade':31, 'profissao':'Juíza', 'saldo':10000},
            {'conta':'1003', 'nome':'Fabio', 'idade':26, 'profissao':'Programador', 'saldo':3000},
            {'conta':'1004', 'nome':'Ana', 'idade':35, 'profissao':'Professora', 'saldo':600}]

class Clientes(Resource):
    def get(self):
        return {"Clientes": CLIENTES}, 200

class Cliente(Resource):
    def get(self, conta):
        for cliente in CLIENTES:
            if cliente['conta'] == conta:
                return cliente
        return "Cliente não encontrado", 404

    def post(self, conta):
        # Interpretador de requisições
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument("nome", type=str, location="form")
        parser.add_argument("idade", type=int, location="form")
        parser.add_argument("profissao", type=str, location="form")
        parser.add_argument("saldo", type=float, location="form")

        dados = parser.parse_args()
        dados['conta'] = conta
        print(dados)
        CLIENTES.append(dados)
        print(CLIENTES)
        return {"Mensagem": "Cliente adicionado com sucesso."}

    def delete(self, conta):
        cliente_encontrado = None
        for cliente in CLIENTES:
            if cliente['conta'] == conta:
                cliente_encontrado = cliente
                break
        if not cliente_encontrado:
            return {"Mensagem": f"Cliente com conta {conta} não encontrado."}, 409

        CLIENTES.remove(cliente_encontrado)
        return {"Mensagem": "Cliente removido"}, 200 # 204 No content

    def put(self, conta):
        # Interpretador de requisição
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('nome', required=False, type=str, location="form")
        parser.add_argument('idade', required=False, type=int, location="form")
        parser.add_argument('profissao', required=False, type=str, location="form")
        parser.add_argument('saldo', required=False, type=float, location="form")

        dados = parser.parse_args()

        for cliente in CLIENTES:
            if cliente['conta'] == conta:
                cliente['nome'] = dados['nome'] or cliente["nome"]
                cliente['idade'] = dados['idade'] or cliente["idade"]
                cliente['profissao'] = dados['profissao'] or cliente["profissao"]
                cliente['saldo'] = dados['saldo'] or cliente["saldo"]
                return cliente, 201

        return {"Mensagem": f"Cliente com conta {conta} não foi encontrado."}, 404

api.add_resource(Clientes, "/clientes")
api.add_resource(Cliente, "/clientes/<string:conta>") # enpoint

if __name__ == '__main__':
    app.run(debug=True)
