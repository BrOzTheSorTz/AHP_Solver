from flask import Flask, request, render_template, redirect, url_for
import numpy as np
import pandas as pd
from models import AHPAutovalores

app = Flask(__name__)


# Función para procesar los archivos y calcular AHP
def calcular_ahp(alternatives_path, criterios_path):
    ahp_method = AHPAutovalores(criterios_path, alternatives_path)
    ranking, info_consistencia = ahp_method.obtain_ranking()

    return ranking, info_consistencia


# Ruta principal para cargar archivos y procesar datos
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Obtener archivos cargados
        alt_file = request.files.get('alternatives')
        crit_file = request.files.get('criterios')

        # Guardar temporalmente los archivos
        alt_path = './tmp/alternatives.csv'
        crit_path = './tmp/criterios.csv'
        alt_file.save(alt_path)
        crit_file.save(crit_path)

        # Calcular AHP
        ranking, info_consistencia = calcular_ahp(alt_path, crit_path)
        name_ranking = []
        i = 1
        for n in ranking:
            name_alternative = "A" + str(i)
            i = i + 1
            name_ranking.append([name_alternative, n])
        name_ranking_order = sort_alternatives(name_ranking)
        # Redirigir a la página de resultados con los datos calculados
        return render_template('result.html', ranking=name_ranking_order, info=info_consistencia)

    return render_template('index.html')


def sort_alternatives(name_ranking):
    """
    :param name_ranking: List of lists, e.g., [[A1,0.34],[A2,0.02],...]
    :return: name_ranking sorted in descending order by ranking values
    """

    n = len(name_ranking)
    for i in range(n):
        for j in range(0, n - i - 1):
            if name_ranking[j][1] < name_ranking[j + 1][1]:  # Orden descendente
                # Intercambia elementos
                name_ranking[j], name_ranking[j + 1] = name_ranking[j + 1], name_ranking[j]

    return name_ranking

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
