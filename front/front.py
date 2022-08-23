from flask import Flask, render_template, request, redirect, url_for
import api
from model import ClienteModel

front = Flask(__name__)

@front.route('/')
def home():
    return render_template("cliente/index.html")

@front.route('/clientes')
def clientes():
    page = request.args.get("page")
    limit = request.args.get("limit")
    response = api.get_all(page=page, limit=limit)
    clientes = response["clientes"]
    page = response.get("page", 0)
    pages = response["pages"]
    next = response.get("next")
    prev = response.get("prev")
    return render_template('cliente/clientes.html', clientes=clientes,
                           page=page, next=next, prev=prev, pages=pages)

@front.route('/clientes/cadastrar', methods=['GET', 'POST'])
def cadastrar_cliente():
    if request.method == "GET":
        return render_template("cliente/cadastrar.html")

    cliente = ClienteModel(nome=request.form.get("nome"),
                           idade=int(request.form.get("idade")),
                           profissao=request.form.get("profissao"),
                           saldo=float(request.form.get("saldo")))
    api.post(cliente)
    return redirect(url_for("clientes"))

@front.route("/clientes/editar/<int:conta>", methods=["GET", "POST"])
def editar_cliente(conta):
    if request.method == "GET":
        cliente = api.get(conta)
        return render_template("cliente/editar.html", cliente=cliente)

    cliente = ClienteModel(
                            nome=request.form.get("nome"),
                            idade=int(request.form.get("idade")),
                            profissao=request.form.get("profissao"),
                            saldo=float(request.form.get("saldo")),
                            conta=conta)

    api.put(cliente)
    return redirect(url_for("clientes"))

@front.route("/clientes/excluir/<int:conta>", methods=["GET", "POST"])
def excluir_cliente(conta):
    must_delete = "delete" in request.form
    if not must_delete:
        cliente = api.get(conta)
        return render_template("cliente/excluir.html", cliente=cliente, delete=True)

    api.delete(conta)
    return redirect(url_for("clientes"))

if __name__ == '__main__':
    front.run(debug=True, port=8090)