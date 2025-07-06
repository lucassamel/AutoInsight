from pydantic import BaseModel
from typing import Optional, List
from model.obesity import Pessoa
import json
import numpy as np

class PessoaSchema(BaseModel):
    """ Define como uma nova pessoa a ser inserida deve ser representada
    """
    nome: str = "Maria"
    gender: int = 0
    age: int = 30
    height: float = 1.70
    weight: int = 70
    family_history: int = 0
    favc: float = 33.6
    fcvc: float = 0.627
    ncp: int = 50
    caec: int = 50
    smoke: int = 50
    ch2o: int = 50
    scc: int = 50
    faf: int = 50
    tue: int = 50
    calc: int = 50
    transportation: int = 50
    
class PessoaViewSchema(BaseModel):
    """Define como uma Pessoa será retornado
    """
    id: int = 1
    nome: str = "Maria"
    gender: int = 0
    age: int = 30
    height: float = 1.70
    weight: int = 70
    family_history: int = 0
    favc: float = 33.6
    fcvc: float = 0.627
    ncp: int = 50
    caec: int = 50
    smoke: int = 50
    ch2o: int = 50
    scc: int = 50
    faf: int = 50
    tue: int = 50
    calc: int = 50
    transportation: int = 50
    outcome: int = None           
        
class PessoaBuscaSchema(BaseModel):
    """Define como deve ser a estrutura que representa a busca.
    Ela será feita com base no nome da pessoa
    """
    name: str = "Maria"

class ListaPessoasSchema(BaseModel):
    """Define como uma lista de pessoas será representada
    """
    pessoas: List[PessoaSchema]

    
class PessoaDelSchema(BaseModel):
    """Define como uma pessoa para deleção será representado
    """
    name: str = "Maria"
    
# Apresenta apenas os dados de um paciente    
def apresenta_pessoa(pessoa: Pessoa):
    """ Retorna uma representação de uma pessoa seguindo o schema definido em
        PessoaViewSchema.
    """
    return {
        "id": pessoa.id,
        "nome": pessoa.nome,
        "gender": pessoa.gender,
        "age": pessoa.age,
        "height": pessoa.height,
        "weight": pessoa.weight,
        "family_history": pessoa.family_history,
        "favc": pessoa.favc,
        "fcvc": pessoa.fcvc,
        "ncp": pessoa.ncp,
        "caec": pessoa.caec,
        "smoke": pessoa.smoke,
        "ch2o": pessoa.ch2o,
        "scc": pessoa.scc,
        "faf": pessoa.faf,
        "tue": pessoa.tue,
        "calc": pessoa.calc,
        "transportation": pessoa.transportation,
        "outcome": pessoa.outcome        
    }
    
# Apresenta uma lista de pessoas
def apresenta_pessoas(pessoas: List[Pessoa]):
    """ Retorna uma representação do paciente seguindo o schema definido em
        PessoasViewSchema.
    """
    result = []
    for pessoa in pessoas:
        result.append({
            "id": pessoa.id,
        "nome": pessoa.nome,
        "gender": pessoa.gender,
        "age": pessoa.age,
        "height": pessoa.height,
        "weight": pessoa.weight,
        "family_history": pessoa.family_history,
        "favc": pessoa.favc,
        "fcvc": pessoa.fcvc,
        "ncp": pessoa.ncp,
        "caec": pessoa.caec,
        "smoke": pessoa.smoke,
        "ch2o": pessoa.ch2o,
        "scc": pessoa.scc,
        "faf": pessoa.faf,
        "tue": pessoa.tue,
        "calc": pessoa.calc,
        "transportation": pessoa.transportation,
        "outcome": pessoa.outcome
        })

    return {"pessoas": result}