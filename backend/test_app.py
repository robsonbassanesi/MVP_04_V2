import pytest
from app import app, Model
from model.avaliador import Avaliador
from model.carregador import Carregador


@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    yield client


carregador = Carregador()
modelo = Model()
avaliador = Avaliador()


def test_predict_endpoint(client):
    # Dados de exemplo para o teste
    test_data = {
        'radius_mean': 15.0,
        'texture_mean': 20.0,
        'perimeter_mean': 95.0,
        'area_mean': 700.0,
        'smoothness_mean': 0.1,
        'compactness_mean': 0.2,
        'concavity_mean': 0.15,
        'concave_points_mean': 0.08,
        'symmetry_mean': 0.18,
        'fractal_dimension_mean': 0.065,
        'radius_se': 0.4,
        'texture_se': 1.2,
        'perimeter_se': 3.5,
        'area_se': 45.0,
        'smoothness_se': 0.01,
        'compactness_se': 0.03,
        'concavity_se': 0.02,
        'concave_points_se': 0.008,
        'symmetry_se': 0.017,
        'fractal_dimension_se': 0.0025,
        'radius_worst': 20.0,
        'texture_worst': 25.0,
        'perimeter_worst': 130.0,
        'area_worst': 1200.0,
        'smoothness_worst': 0.15,
        'compactness_worst': 0.3,
        'concavity_worst': 0.25,
        'concave_points_worst': 0.1,
        'symmetry_worst': 0.3,
        'fractal_dimension_worst': 0.08
    }

    # Envia uma requisição POST para o endpoint predict
    response = client.post('/predict', json=test_data)

    # Verifica se a resposta está correta e o status é 200 (OK)
    assert response.status_code == 200
    assert 'resultado' in response.json


url_dados = "database/cancer_golden.csv"
colunas = ['diagnosis', 'radius_mean', 'texture_mean', 'perimeter_mean', 'area_mean',
           'smoothness_mean', 'compactness_mean', 'concavity_mean', 'concave_points_mean',
           'symmetry_mean', 'fractal_dimension_mean', 'radius_se', 'texture_se',
           'perimeter_se', 'area_se', 'smoothness_se', 'compactness_se',
           'concavity_se', 'concave_points_se', 'symmetry_se', 'fractal_dimension_se',
           'radius_worst', 'texture_worst', 'perimeter_worst', 'area_worst',
           'smoothness_worst', 'compactness_worst', 'concavity_worst', 'concave_points_worst',
           'symmetry_worst', 'fractal_dimension_worst']

# Carga dos dados
dataset = carregador.carregar_dados(url_dados, colunas)

dataset['diagnosis'] = dataset['diagnosis'].map({'M': 1, 'B': 0})

# 2. Selecione os recursos (X) e os rótulos (Y)
X = dataset.iloc[:, 0:-1]
# Se a coluna 'label' estiver na última posição, você pode fazer
Y = dataset.iloc[:, 0]


def test_modelo_knn():
    # Importando modelo de KNN
    knn_path = 'modelo/modelo_finalizado.pkl'
    modelo_knn = Model.carrega_modelo(knn_path)

    # Obtendo as métricas do KNN
    acuracia_knn, recall_knn, precisao_knn, f1_knn = avaliador.avaliar(
        modelo_knn, X, Y)

    # Testando as métricas do KNN
    assert acuracia_knn >= 0.75
    assert recall_knn >= 0.5
    assert precisao_knn >= 0.5
    assert f1_knn >= 0.5


if __name__ == '__main__':
    pytest.main(['-v', 'test_app.py'])
