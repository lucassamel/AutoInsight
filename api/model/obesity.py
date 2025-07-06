from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base

# colunas = Pregnancies,Glucose,BloodPressure,SkinThickness,test,BMI,DiabetesPedigreeFunction,Age,Outcome

class Pessoa(Base):
    __tablename__ = 'pessoas'
    
    id = Column(Integer, primary_key=True)
    nome = Column("Name", String(100))
    gender= Column("Gender", String(50))
    age = Column("Age", Integer)
    height = Column("Height", Float)
    weight = Column("Weight", Integer)
    family_history = Column("FamilyHistory", Integer)
    favc = Column("FAVC", Integer)
    fcvc = Column("FCVC", Integer)
    ncp = Column("NCP", Integer)
    caec = Column("CAEC", Integer)
    smoke = Column("Smoke", Integer)
    ch2o = Column("CH2O", Integer)
    scc = Column("SCC", Integer)
    faf = Column("FAF", Integer)
    tue = Column("TUE", Integer)
    calc = Column("CALC", Integer)    
    transportation = Column("PublicTransportation", Integer)    
    outcome = Column("Diagnostic", Integer, nullable=True)
    data_insercao = Column(DateTime, default=datetime.now())
    
    def __init__(self, nome:str, gender:int, height:float, weight:int, family_history:int,
                 age:int, favc:int, fcvc:int, ncp:int, 
                 caec:int, smoke:int, ch2o:int, 
                 scc:int, faf:int, tue:int,
                 calc:int, transportation:int, outcome:int, 
                 data_insercao:Union[DateTime, None] = None):
        """
        Cria uma Pessoa com os atributos necessários 
        para o diagnóstico de obesidade.

        Arguments:
            nome: nome da pessoa
            gender: genero 
            height: altura
            weight: peso
            family_history: historico familiar de obesidade
            favc: consumo de alimentos caloricos com frequência
            fcvc: frequência de consumo de vegetais
            ncp: numero de porcoes de frutas e vegetais consumidos diariamente
            caec: consumo de alimentos entre refeições
            smoke: fumante
            ch2o: copos de água consumidos diariamente
            scc: monitora as calorias consumidas
            faf: frequencia de atividade fisica
            tue: tempo de uso de tela
            calc: frequencia de consumo de alcool             
            transportation: idade            
            outcome: diagnóstico
            data_insercao: data de quando o paciente foi inserido à base
        """
        self.nome = nome
        self.gender = gender
        self.age = age
        self.height = height
        self.weight = weight
        self.family_history = family_history
        self.favc = favc
        self.fcvc = fcvc
        self.ncp = ncp
        self.caec = caec
        self.smoke = smoke
        self.ch2o = ch2o
        self.scc = scc
        self.faf = faf
        self.tue = tue
        self.calc = calc
        self.transportation = transportation
        self.outcome = outcome

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao