import pytest
import json
from app import app
from model import Session, Pessoa

# To run: pytest -v test_api.py

@pytest.fixture
def client():
    """Configura o cliente de teste para a aplicação Flask"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def sample_pessoa_data():
    """Dados de exemplo para teste de pessoa"""
    return {        
        "nome": "Maria",
        "gender": 0,
        "age": 30,
        "height": 1.70,
        "weight": 70,
        "family_history": 0,
        "favc": 1,
        "fcvc": 1,
        "ncp": 1,
        "caec": 2,
        "smoke": 1,
        "ch2o": 3,
        "scc": 2,
        "faf": 1,
        "tue": 1,
        "calc": 1,
        "transportation": 3          
    }

def test_home_redirect(client):
    """Testa se a rota home redireciona para o frontend"""
    response = client.get('/')
    assert response.status_code == 302
    assert '/front/index.html' in response.location

def test_docs_redirect(client):
    """Testa se a rota docs redireciona para openapi"""
    response = client.get('/docs')
    assert response.status_code == 302
    assert '/openapi' in response.location

def test_get_pessoas_empty(client):
    """Testa a listagem de pessoas quando não há nenhuma"""
    response = client.get('/pessoas')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'pessoas' in data
    assert isinstance(data['pessoas'], list)

def test_add_pessoa_prediction(client, sample_pessoa_data):
    """Testa a adição de uma pessoa com predição"""
    # Primeiro, vamos limpar qualquer pessoa existente com o mesmo nome
    session = Session()
    existing_pessoa = session.query(Pessoa).filter(Pessoa.nome == sample_pessoa_data['nome']).first()
    if existing_pessoa:
        session.delete(existing_pessoa)
        session.commit()
    session.close()
    
    # Agora testamos a adição
    response = client.post('/pessoa', 
                          data=json.dumps(sample_pessoa_data),
                          content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    
    
    
    # Verifica se o pessoa foi criado com todas as informações
    assert data['nome'] == sample_pessoa_data['nome']
    assert data['gender'] == sample_pessoa_data['gender']
    assert data['age'] == sample_pessoa_data['age']
    assert data['height'] == sample_pessoa_data['height']
    assert data['weight'] == sample_pessoa_data['weight']
    assert data['family_history'] == sample_pessoa_data['family_history']
    assert data['favc'] == sample_pessoa_data['favc']
    assert data['fcvc'] == sample_pessoa_data['fcvc']
    assert data['ncp'] == sample_pessoa_data['ncp']
    assert data['caec'] == sample_pessoa_data['caec']
    assert data['smoke'] == sample_pessoa_data['smoke']
    assert data['ch2o'] == sample_pessoa_data['ch2o']
    assert data['scc'] == sample_pessoa_data['scc']
    assert data['faf'] == sample_pessoa_data['faf']
    assert data['tue'] == sample_pessoa_data['tue']
    assert data['calc'] == sample_pessoa_data['calc']
    assert data['transportation'] == sample_pessoa_data['transportation']    
    
    # Verifica se a predição foi feita (outcome deve estar presente)
    assert 'outcome' in data
    assert data['outcome'] in [0, 1, 2, 3, 4, 5, 6]  # Deve ser entre 0 e 6, representando as classes de obesidade

def test_add_duplicate_pessoa(client, sample_pessoa_data):
    """Testa a adição de uma pessoa duplicada"""
    # Primeiro adiciona uma pessoa
    client.post('/pessoa', 
                data=json.dumps(sample_pessoa_data),
                content_type='application/json')
    
    # Tenta adicionar novamente
    response = client.post('/pessoa', 
                          data=json.dumps(sample_pessoa_data),
                          content_type='application/json')
    
    assert response.status_code == 409
    data = json.loads(response.data)
    assert 'message' in data
    assert 'já existente' in data['message']

def test_get_pessoa_by_nome(client, sample_pessoa_data):
    """Testa a busca de uma pessoa por nome"""
    # Primeiro adiciona uma pessoa
    client.post('/pessoa', 
                data=json.dumps(sample_pessoa_data),
                content_type='application/json')
    
    # Busca o pessoa por nome
    response = client.get(f'/pessoa?nome={sample_pessoa_data["nome"]}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['nome'] == sample_pessoa_data['nome']

def test_get_nonexistent_pessoa(client):
    """Testa a busca de um pessoa que não existe"""
    response = client.get('/pessoa?nome=PessoaInexistente')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'mesage' in data 

def test_delete_pessoa(client, sample_pessoa_data):
    """Testa a remoção de um pessoa"""
    # Primeiro adiciona uma pessoa
    client.post('/pessoa', 
                data=json.dumps(sample_pessoa_data),
                content_type='application/json')
    
    # Remove uma pessoa
    response = client.delete(f'/pessoa?nome={sample_pessoa_data["nome"]}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'message' in data
    assert 'removida com sucesso' in data['message']

def test_delete_pessoa_inexistente(client):
    """Testa a remoção de um pessoa que não existe"""
    response = client.delete('/pessoa?nome=PessoaInexistente')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'message' in data

def test_prediction_edge_cases(client):
    """Testa casos extremos para predição"""
    # Teste com valores mínimos
    min_data = {
        "nome": "José",
        "gender": 0,
        "age": 65,
        "height": 1.90,
        "weight": 150,
        "family_history": 1,
        "favc": 1,
        "fcvc": 1,
        "ncp": 1,
        "caec": 2,
        "smoke": 1,
        "ch2o": 3,
        "scc": 2,
        "faf": 1,
        "tue": 1,
        "calc": 1,
        "transportation": 4
    }
    
    response = client.post('/pessoa', 
                          data=json.dumps(min_data),
                          content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'outcome' in data
    
    # Teste com valores máximos típicos
    max_data = {
        "nome": "Ana",
        "gender": 1,
        "age": 1,
        "height": 1,
        "weight": 1,
        "family_history": 0,
        "favc": 0,
        "fcvc": 0,
        "ncp": 0,
        "caec": 0,
        "smoke": 0,
        "ch2o": 0,
        "scc": 0,
        "faf": 0,
        "tue": 0,
        "calc": 0,
        "transportation": 0
    }
    
    response = client.post('/pessoa', 
                          data=json.dumps(max_data),
                          content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'outcome' in data

def cleanup_test_pessoas():
    """Limpa pessoas de teste do banco"""
    session = Session()
    test_patients = session.query(Pessoa).filter(
        Pessoa.nome.in_(['Ana', 'José', 'Maria'])
    ).all()
    
    for patient in test_patients:
        session.delete(patient)
    session.commit()
    session.close()

# Executa limpeza após os testes
def test_cleanup():
    """Limpa dados de teste"""
    cleanup_test_pessoas()