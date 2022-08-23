from flask_sqlalchemy import SQLAlchemy

bd = SQLAlchemy()

class ClienteModel(bd.Model):
    __tablename__ = "clientes" # Mapeamento da tabela
    conta = bd.Column(bd.Integer, primary_key=True, autoincrement=True) # Chave primaria
    nome = bd.Column(bd.String(100), nullable=False)
    idade = bd.Column(bd.Integer, nullable=False)
    profissao = bd.Column(bd.String(50), nullable=False)
    saldo = bd.Column(bd.Float(precision=2), nullable=False)

    @classmethod
    def encontre_cliente(cls, conta): # Encontrar cliente pela conta
        cliente = cls.query.get(conta)
        return None if not cliente else cliente

    # Atualizar os dados
    def update_cliente(self, **dados):
        self.nome = dados['nome'] or self.nome
        self.idade = dados['idade'] or self.idade
        self.profissao = dados['profissao'] or self.profissao
        self.saldo = dados['saldo'] or self.saldo

    # Método para deletar uma entidade
    def delete_cliente(self):
        bd.session.delete(self)
        bd.session.commit()

    # Método para salvar uma entidade
    def save_cliente(self):
        bd.session.add(self)
        bd.session.commit()

    def to_dict(self):
        return {'conta': self.conta,
                'nome': self.nome,
                'idade': self.idade,
                'profissao': self.profissao,
                'saldo': self.saldo}
