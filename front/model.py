from dataclasses import dataclass

@dataclass
class ClienteModel:
    nome:str
    idade:int
    profissao:str
    saldo:float
    conta:int = None

    def to_dict(self):
        return {'nome': self.nome,
                'idade': self.idade,
                'profissao': self.profissao,
                'saldo': self.saldo}
