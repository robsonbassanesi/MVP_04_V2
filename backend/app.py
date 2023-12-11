from flask import Flask, request, jsonify
import numpy as np
import pickle
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


class Model:
    @staticmethod
    def carrega_modelo(path):
        """Dependendo se o final for .pkl ou .joblib, carregamos de uma forma ou de outra
        """
        model = pickle.load(open(path, 'rb'))
        print(model)
        return model

    @staticmethod
    def preditor(model, form):
        """Realiza a predição de um paciente com base no modelo treinado
        """
        # Faremos o reshape para que o modelo entenda que estamos passando
        diagnosis = model.predict(np.array(form).reshape(1, -1))
        print(f'Este é o diagnóstico: {diagnosis[0]}')
        return int(diagnosis[0])

    @staticmethod
    def get_feature_names():
        return [
            'radius_mean', 'texture_mean', 'perimeter_mean', 'area_mean',
            'smoothness_mean', 'compactness_mean', 'concavity_mean', 'concave_points_mean',
            'symmetry_mean', 'fractal_dimension_mean', 'radius_se', 'texture_se',
            'perimeter_se', 'area_se', 'smoothness_se', 'compactness_se',
            'concavity_se', 'concave_points_se', 'symmetry_se', 'fractal_dimension_se',
            'radius_worst', 'texture_worst', 'perimeter_worst', 'area_worst',
            'smoothness_worst', 'compactness_worst', 'concavity_worst', 'concave_points_worst',
            'symmetry_worst', 'fractal_dimension_worst'
        ]


@app.route('/predict', methods=['POST'])
def predict():
    """Realiza a predição com base nos dados do formulário e retorna o resultado.

    Returns:
        dict: representação do resultado da predição
    """
    try:
        # Obtenha os dados do formulário do pedido
        form_data = request.json

        # Crie uma instância do modelo e carregue o modelo treinado
        path = 'modelo/modelo_finalizado.pkl'
        modelo = Model.carrega_modelo(path)

        # Crie um array numpy a partir dos dados do formulário
        X_input = [float(form_data.get(field, 0.0))
                   for field in Model.get_feature_names()]

        # Fazer a predição
        resultado = Model.preditor(modelo, X_input)
        print(f'Este é o diagnóstico: {resultado}')

        # Retorna o resultado da predição
        return jsonify({"resultado": resultado}), 200

    except Exception as e:
        error_msg = "Erro ao processar o formulário :/"
        return {"message": error_msg}, 400


if __name__ == '__main__':
    app.run(debug=True)
