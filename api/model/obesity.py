from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base

# colunas = Pregnancies,Glucose,BloodPressure,SkinThickness,test,BMI,DiabetesPedigreeFunction,Age,Outcome

class Pessoa(Base):
    __tablename__ = 'pessoas'
    
    id = Column(Integer, primary_key=True)
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
    bike = Column("Bike", Integer)
    motorbike = Column("Motorbike", Integer)
    public_transportation = Column("PublicTransportation", Integer)
    walking = Column("Walking", Integer)
    outcome = Column("Diagnostic", Integer, nullable=True)
    data_insercao = Column(DateTime, default=datetime.now())
    
    def __init__(self, gender:int, height:float, weight:int, family_history:int,
                 age:int, favc:int, fcvc:int, ncp:int, 
                 caec:int, smoke:int, sh2o:int, 
                 scc:int, faf:int, tue:int,
                 calc:int, bike:int, motorbike:int,
                 automobile:int, public_transportation:int, walking:int,
                 outcome:int, 
                 data_insercao:Union[DateTime, None] = None):
        """
        Cria uma Pessoa com os atributos necessários 
        para o diagnóstico de obesidade.

        Arguments:
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
            bike: Bicicleta como transporte pricipal
            motorbike: idade
            public_transportation: idade
            walking: idade
            outcome: diagnóstico
            data_insercao: data de quando o paciente foi inserido à base
        """
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
        self.sh2o = sh2o
        self.scc = scc
        self.faf = faf
        self.tue = tue
        self.calc = calc
        self.bike = bike
        self.motorbike = motorbike
        self.automobile = automobile
        self.public_transportation = public_transportation
        self.walking = walking
        self.outcome = outcome

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao