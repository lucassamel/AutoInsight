from flask import redirect
from flask_openapi3 import OpenAPI, Info, Tag
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import *
from logger import logger
from schemas.error_schema import *
from schemas.obesity_schema import *
from flask_cors import CORS


# Instanciando o objeto OpenAPI
info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(
    __name__, info=info, static_folder="../front", static_url_path="/front"
)
CORS(app)

# Definindo tags para agrupamento das rotas
home_tag = Tag(
    name="Documentação",
    description="Seleção de documentação: Swagger, Redoc ou RapiDoc",
)
pessoa_tag = Tag(
    name="Pessoa",
    description="Adição, visualização, remoção e predição de pessoas com Obesidade",
)


# Rota home - redireciona para o frontend
@app.get("/", tags=[home_tag])
def home():
    """Redireciona para o index.html do frontend."""
    return redirect("/front/index.html")


# Rota para documentação OpenAPI
@app.get("/docs", tags=[home_tag])
def docs():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação."""
    return redirect("/openapi")


# Rota de listagem de pessoas
@app.get(
    "/pessoas",
    tags=[pessoa_tag],
    responses={"200": PessoaViewSchema, "404": ErrorSchema},
)
def get_pessoas():
    """Lista todas as pessoas cadastradas na base
    Args:
       none

    Returns:
        list: lista de pessoas cadastradas na base
    """
    logger.debug("Coletando dados sobre todas as pessoas")
    # Criando conexão com a base
    session = Session()
    # Buscando todas as pessoas
    pessoas = session.query(Pessoa).all()

    if not pessoas:
        # Se não houver pessoas cadastradas
        return {"pessoas": []}, 200
    else:
        logger.debug(f"%d pessoas econtradas" % len(pessoas))
        print(pessoas)
        return apresenta_pessoas(pessoas), 200


# Rota de adição de pessoa
@app.post(
    "/pessoa",
    tags=[pessoa_tag],
    responses={
        "200": PessoaViewSchema,
        "400": ErrorSchema,
        "409": ErrorSchema,
    },
)
def predict(form: PessoaSchema):
    """Adiciona uma nova pessoa à base de dados
    Retorna uma representação das pessoas e sua classificação de obesidade
    """
    # Instanciando classes
    preprocessador = PreProcessador()
    pipeline = Pipeline()

    # Recuperando os dados do formulário
    nome = form.nome
    gender = form.gender
    age = form.age
    height = form.height
    weight = form.weight
    family_history = form.family_history
    favc = form.favc
    fcvc = form.fcvc
    ncp = form.ncp
    caec = form.caec
    smoke = form.smoke
    ch2o = form.ch2o
    scc = form.scc
    faf = form.faf
    tue = form.tue
    calc = form.calc
    transportation = form.transportation

    # Preparando os dados para o modelo
    X_input = preprocessador.preparar_form(form)
    # Carregando modelo
    model_path = "./MachineLearning/pipelines/rf_obesity_pipeline.pkl"
    modelo = pipeline.carrega_pipeline(model_path)
    # Realizando a predição
    outcome = int(modelo.predict(X_input)[0])

    pessoa = Pessoa(
        nome=nome,
        gender=gender,
        age=age,
        height=height,
        weight=weight,
        family_history=family_history,
        favc=favc,
        fcvc=fcvc,
        ncp=ncp,
        caec=caec,
        smoke=smoke,
        ch2o=ch2o,
        scc=scc,
        faf=faf,
        tue=tue,
        calc=calc,
        transportation=transportation,
        outcome=outcome               
    )
    logger.debug(f"Adicionando uma pessoa: '{pessoa.nome}'")

    try:
        # Criando conexão com a base
        session = Session()

        # Checando se pessoa já existe na base
        if session.query(Pessoa).filter(Pessoa.nome == form.nome).first():
            error_msg = "Essa Pessoa já existente na base :/"
            logger.warning(
                f"Erro ao adicionar pessoa '{pessoa.nome}', {error_msg}"
            )
            logger.error(
                f"Erro ao adicionar pessoa '{pessoa.nome}', {error_msg}"
            )
            return {"message": error_msg}, 409

        # Adicionando pessoa
        session.add(pessoa)
        # Efetivando o comando de adição
        session.commit()
        # Concluindo a transação
        logger.debug(f"Adicionado pessoa de nome: '{pessoa.nome}'")
        return apresenta_pessoa(pessoa), 200

    # Caso ocorra algum erro na adição
    except Exception as e:
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(
            f"Erro ao adicionar pessoa '{pessoa.nome}', {error_msg}"
        )
        return {"message": error_msg}, 400


# Métodos baseados em nome
# Rota de busca de pessoa por nome
@app.get(
    "/pessoa",
    tags=[pessoa_tag],
    responses={"200": PessoaViewSchema, "404": ErrorSchema},
)
def get_pessoa(query: PessoaBuscaSchema):
    """Faz a busca por uma pessoa cadastrado na base a partir do nome

    Args:
        nome (str): nome da pessoa

    Returns:
        dict: representação da pessoa e classificação de obesidade
    """

    pessoa_nome = query.nome
    logger.debug(f"Coletando dados sobre produto #{pessoa_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    pessoa = (
        session.query(Pessoa).filter(Pessoa.nome == pessoa_nome).first()
    )

    if not pessoa:
        # se o pessoa não foi encontrado
        error_msg = f"Pessoa {pessoa_nome} não encontrado na base :/"
        logger.warning(
            f"Erro ao buscar produto '{pessoa_nome}', {error_msg}"
        )
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Pessoa econtrado: '{pessoa.nome}'")
        # retorna a representação do pessoa
        return apresenta_pessoa(pessoa), 200


# Rota de remoção de pessoa por nome
@app.delete(
    "/pessoa",
    tags=[pessoa_tag],
    responses={"200": PessoaViewSchema, "404": ErrorSchema},
)
def delete_paciente(query: PessoaBuscaSchema):
    """Remove um pessoa cadastrado na base a partir do nome

    Args:
        nome (str): nome da pessoa

    Returns:
        msg: Mensagem de sucesso ou erro
    """

    pessoa_nome = unquote(query.nome)
    logger.debug(f"Deletando dados sobre pessoa #{pessoa_nome}")

    # Criando conexão com a base
    session = Session()

    # Buscando pessoa
    pessoa = (
        session.query(Pessoa).filter(Pessoa.nome == pessoa_nome).first()
    )

    if not pessoa:
        error_msg = "Pessoa não encontrado na base :/"
        logger.warning(
            f"Erro ao deletar pessoa '{pessoa_nome}', {error_msg}"
        )
        return {"message": error_msg}, 404
    else:
        session.delete(pessoa)
        session.commit()
        logger.debug(f"Deletado pessoa #{pessoa_nome}")
        return {
            "message": f"Pessoa {pessoa_nome} removida com sucesso!"
        }, 200


if __name__ == "__main__":
    app.run(debug=True) 