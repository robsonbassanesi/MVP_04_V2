import { useState } from 'react';
import axios from 'axios';
import { HandleForm } from './Elements';

//função para exibir, cadastrar e excluir os exames além de exibi-los
export function ExamTable() {
  const [diagnosis, setDiagnosis] = useState(null);
  const [form, setForm] = useState({});

  const dataForm = e => {
    const { name, value } = e.target;
    setForm({ ...form, [name]: value });
  };

  //função para cadastrar um novo exames e enviar para o backend
  async function createExam(e) {
    e.preventDefault();
    try {
      const formData = {
        // name: form.name,
        radius_mean: form.radius_mean,
        texture_mean: form.texture_mean,
        perimeter_mean: form.perimeter_mean,
        area_mean: form.area_mean,
        smoothness_mean: form.smoothness_mean,
        compactness_mean: form.compactness_mean,
        concavity_mean: form.concavity_mean,
        concave_points_mean: form.concave_points_mean,
        symmetry_mean: form.symmetry_mean,
        fractal_dimension_mean: form.fractal_dimension_mean,
        radius_se: form.radius_se,
        texture_se: form.texture_se,
        perimeter_se: form.perimeter_se,
        area_se: form.area_se,
        smoothness_se: form.smoothness_se,
        compactness_se: form.compactness_se,
        concavity_se: form.concavity_se,
        concave_points_se: form.concave_points_se,
        symmetry_se: form.symmetry_se,
        fractal_dimension_se: form.fractal_dimension_se,
        radius_worst: form.radius_worst,
        texture_worst: form.texture_worst,
        perimeter_worst: form.perimeter_worst,
        area_worst: form.area_worst,
        smoothness_worst: form.smoothness_worst,
        compactness_worst: form.compactness_worst,
        concavity_worst: form.concavity_worst,
        concave_points_worst: form.concave_points_worst,
        symmetry_worst: form.symmetry_worst,
        fractal_dimension_worst: form.fractal_dimension_worst
      };
      const response = await axios.post(
        'http://127.0.0.1:5000/predict',
        formData
      );

      // Atualiza o estado com o resultado da predição
      setDiagnosis(response.data.resultado);
    } catch (error) {
      console.error('Erro ao enviar o formulário:', error);
    }
  }

  return (
    <div className="p-8 bg-gray-100">
      <div className="flex items-center justify-around">
        <h1 className="text-3xl font-bold">Predição exames de mama</h1>
      </div>
      <div className="mt-4 bg-white rounded-lg shadow-md">
        <form onSubmit={createExam} className="p-4">
          <HandleForm form={form} handleDataForm={dataForm} />
          <div className="text-right items-center">
            <button
              type="submit"
              className="items-end px-4 py-2 text-white bg-blue-500 rounded-full"
            >
              Realizar predição
            </button>
          </div>
        </form>
        <div className="text-2xl font-bold flex p-2 border-x-0 border-dashed border-4 justify-around items-center m-4">
          <h1>Resultado da Predição</h1>
          <span>
            {diagnosis === 1
              ? 'Maligno'
              : diagnosis === 0
              ? 'Benigno'
              : 'Resultado Inválido'}
          </span>
        </div>
      </div>
    </div>
  );
}
