from pydantic import BaseModel
from typing import Optional, List
from model.obesity import Pessoa
import json
import numpy as np

class PessoaSchema(BaseModel):
    """ Define como um novo paciente a ser inserido deve ser representado
    """
    name: str = "Maria"
    preg: int = 6
    plas: int = 148
    pres: int = 72
    skin: int = 35
    test: int = 2
    mass: float = 33.6
    pedi: float = 0.627
    age: int = 50
    
class PessoaViewSchema(BaseModel):
    """Define como uma Pessoa será retornado
    """
    id: int = 1
    name: str = "Maria"
    preg: int = 6
    plas: int = 148
    pres: int = 72
    skin: int = 35
    test: int = 0
    mass: float = 33.6
    pedi: float = 0.627
    age: int = 50
    outcome: int = None
    
class PessoaBuscaSchema(BaseModel):
    """Define como deve ser a estrutura que representa a busca.
    Ela será feita com base no nome do paciente.
    """
    name: str = "Maria"

class ListaPessoasSchema(BaseModel):
    """Define como uma lista de pacientes será representada
    """
    pessoas: List[PessoaSchema]

    
class PessoaDelSchema(BaseModel):
    """Define como um paciente para deleção será representado
    """
    name: str = "Maria"
    
# Apresenta apenas os dados de um paciente    
def apresenta_pessoa(pessoa: Pessoa):
    """ Retorna uma representação do paciente seguindo o schema definido em
        PacienteViewSchema.
    """
    return {
        "id": paciente.id,
        "name": paciente.name,
        "preg": paciente.preg,
        "plas": paciente.plas,
        "pres": paciente.pres,
        "skin": paciente.skin,
        "test": paciente.test,
        "mass": paciente.mass,
        "pedi": paciente.pedi,
        "age": paciente.age,
        "outcome": paciente.outcome
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
            "name": pessoa.name,
            "preg": pessoa.preg,
            "plas": pessoa.plas,
            "pres": pessoa.pres,    
            "skin": pessoa.skin,
            "test": pessoa.test,
            "mass": pessoa.mass,
            "pedi": pessoa.pedi,
            "age": pessoa.age,
            "outcome": pessoa.outcome
        })

    return {"pessoas": result}