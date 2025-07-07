from model import *
from sklearn.preprocessing import LabelEncoder

# To run: pytest -v test_modelos.py

# Instanciação das Classes
carregador = Carregador()
modelo = Model()
avaliador = Avaliador()
pipeline = Pipeline()

# Parâmetros    
url_dados = "./MachineLearning/data/test_dataset_obesity.csv"
colunas = ['Gender', 'Age', 'Height', 'Weight', 'family_history_with_overweight', 'FAVC',	
           'FCVC', 'NCP', 'CAEC', 'SMOKE', 'CH2O', 'SCC', 'FAF', 'TUE',	'CALC',	'MTRANS', 'NObeyesdad']

# Carga dos dados
dataset = carregador.carregar_dados(url_dados, colunas)

caec_map = {'no': 0, 'Sometimes': 1, 'Frequently': 2, 'Always': 3}
calc_map = {'no': 0, 'Sometimes': 1, 'Frequently': 2, 'Always': 3}
mtrans_map = {'Public_Transportation': 0, 'Walking': 1, 'Motorbike': 2, 'Bike': 3, 'Automobile': 4}
obeyesdad_map = {'Normal_Weight': 0, 'Insufficient_Weight': 1, 'Obesity_Type_I': 2, 'Obesity_Type_II': 3,
                 'Obesity_Type_III': 4, 'Overweight_Level_I': 5, 'Overweight_Level_II': 6}

dataset['CAEC'] = dataset['CAEC'].map(caec_map)
dataset['CALC'] = dataset['CALC'].map(calc_map)
dataset['MTRANS'] = dataset['MTRANS'].map(mtrans_map)
dataset['NObeyesdad'] = dataset['NObeyesdad'].map(obeyesdad_map)

label_cols = ['Gender', 'family_history_with_overweight',  'FAVC', 'SMOKE', 
               'SCC','NObeyesdad' ]
for col in label_cols:
    dataset[col] = LabelEncoder().fit_transform(dataset[col])

array = dataset.values
X = array[:,0:-1]
y = array[:,-1]
    
# Método para testar o modelo de Regressão Logística a partir do arquivo correspondente
# O nome do método a ser testado necessita começar com "test_"
def test_modelo_gb():  
    # Importando o modelo de regressão logística
    gb_path = './MachineLearning/pipelines/gb_obesity_pipeline.pkl'
    modelo_gb = modelo.carrega_modelo(gb_path)

    # Obtendo as métricas da Regressão Logística
    acuracia_gb = avaliador.avaliar(modelo_gb, X, y)
    
    # Testando as métricas da Regressão Logística 
    # Modifique as métricas de acordo com seus requisitos
    assert acuracia_gb >= 0.78 
    # assert recall_lr >= 0.5 
    # assert precisao_lr >= 0.5 
    # assert f1_lr >= 0.5 

# Método para testar modelo KNN a partir do arquivo correspondente
def test_modelo_knn():
    # Importando modelo de KNN
    knn_path = './MachineLearning/models/rf_obesity_classifier.pkl'
    modelo_knn = modelo.carrega_modelo(knn_path)

    # Obtendo as métricas do KNN
    acuracia_knn = avaliador.avaliar(modelo_knn, X, y)
    
    # Testando as métricas do KNN
    # Modifique as métricas de acordo com seus requisitos
    assert acuracia_knn >= 0.78
    # assert recall_knn >= 0.5 
    # assert precisao_knn >= 0.5 
    # assert f1_knn >= 0.5 

# Método para testar pipeline Random Forest a partir do arquivo correspondente
def test_modelo_rf():
    # Importando pipeline de Random Forest
    rf_path = './MachineLearning/models/rf_obesity_classifier.pkl'
    modelo_rf = pipeline.carrega_pipeline(rf_path)

    # Obtendo as métricas do Random Forest
    acuracia_rf = avaliador.avaliar(modelo_rf, X, y)
    
    # Testando as métricas do Random Forest
    # Modifique as métricas de acordo com seus requisitos
    assert acuracia_rf >= 0.78
    # assert recall_rf >= 0.5 
    # assert precisao_rf >= 0.5 
    # assert f1_rf >= 0.5
    