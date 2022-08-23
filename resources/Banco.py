from flask_restful import Resource, reqparse
from model.Cliente import ClienteModel # importar a lista de Clientes

# Classe para retornar todos os clientes
class ClientesResource(Resource):
    def get(self): # GET ALL
        getall_parser = reqparse.RequestParser()
        getall_parser.add_argument("page", type=int, location="args")
        getall_parser.add_argument("limit", type=int, location="args")

        pagination_data = getall_parser.parse_args()
        page = pagination_data["page"] or 1
        limit = pagination_data["limit"] or 10
        pagination = ClienteModel.query.paginate(page, limit, error_out=False)

        data = {"clientes": [c.to_dict() for c in pagination.items],
                "pages": pagination.pages,
                "total": pagination.total,
                "page": page,
                "limit": limit}

        if pagination.has_next: # Configurar próxima página
            data["next"] = f"/clientes?page={pagination.next_num}&limit={limit}"

        if pagination.has_prev: # Configurar página anterior
            data["prev"] = f"/clientes?page={pagination.prev_num}&limit={limit}"

        return data, 200

    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('nome', location='form', required=True, type=str)
        parser.add_argument('idade', location='form', required=True, type=int)
        parser.add_argument('profissao', location='form', required=True, type=str)
        parser.add_argument('saldo', location='form', required=True, type=float)

        dados = parser.parse_args()
        novo_cliente = ClienteModel(**dados)
        novo_cliente.save_cliente()
        return novo_cliente.to_dict(), 201


class ClienteResource(Resource):
    def get(self, conta):
        cliente = ClienteModel.encontre_cliente(conta)
        if cliente: # None (False) ou cliente (True)
            return cliente.to_dict(), 200
        return {"ERRO": "Cliente não encontrado"}, 404

    def delete(self, conta):
        cliente = ClienteModel.encontre_cliente(conta)
        if cliente:
            cliente.delete_cliente()
            return {"Mensagem": f"Cliente com conta {conta} foi excluída!"}, 200 # ou 204
        return {"Mensagem": f"Cliente com conta {conta} não foi encontrado"}, 409

    def put(self, conta):
        # Atualizar os dados dos clientes já cadastrados
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('nome', location='form', required=False, type=str)
        parser.add_argument('idade', location='form', required=False, type=int)
        parser.add_argument('profissao', location='form', required=False, type=str)
        parser.add_argument('saldo', location='form', required=False, type=float)

        dados = parser.parse_args()
        cliente = ClienteModel.encontre_cliente(conta)
        if cliente:
            cliente.update_cliente(**dados)
            cliente.save_cliente()
            return {"Mensagem": "Dados atualizados com sucesso!"}, 200

        return {"Mensagem": f"Cliente com conta {conta} não foi encontrado"}, 409
