import pickle

class Model:
    
    def __init__(self):
        """Inicializa o modelo"""
        self.model = None
    
    def carrega_modelo(self, path):        
        
        if path.endswith('.pkl'):
            with open(path, 'rb') as file:
                self.model = pickle.load(file)
        else:
            raise Exception('Formato de arquivo não suportado')
        return self.model
    
    def preditor(self, X_input):
        """Realiza a classificação da pessoa com base no modelo treinado
        """
        if self.model is None:
            raise Exception('Modelo não foi carregado. Use carrega_modelo() primeiro.')
        diagnosis = self.model.predict(X_input)
        return diagnosis