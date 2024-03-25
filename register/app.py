from flask import Flask, request, jsonify
import logging

from exceptions.custom_exceptions import GetReportException, DBConnectoException, GetUserInformationException
from services.calculate_hours_worked import calcular_soma_diferenca_horarios, calcular_total_trabalhado
from services.db_connector import add_registro, buscar_registro_por_dia, buscar_registro_por_mes
from services.validate_user import get_username

logger = logging.getLogger()
app = Flask(__name__)

@app.route('/health_check',methods=["GET"])
def home():
    try:
        response = {'status':200}
        return jsonify(response)
    except Exception as e:
        logger.exception(e)
        return jsonify(error=str(e)), 500


@app.route("/register",methods=["POST"])
def create_register():
    try:  # pragma: no cover
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': 'Token de autorização ausente'}), 401
        token = auth_header.split(' ')[1]
        get_username(token)

        result = {}
        return jsonify(result)
    except GetUserInformationException:
        return jsonify({'error':'Impossivel localizar usuário'}), 404
    except DBConnectoException:
        return jsonify({'error':'Problemas com a conxão com o banco de dados'}), 500
    except Exception as e:
        logger.exception(e)
        return jsonify(error=str(e)), 500


@app.route("/register/<day>", methods=["GET"])
def get_day_register(day: int):
    try:  # pragma: no cover
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': 'Token de autorização ausente'}), 401
        token = auth_header.split(' ')[1]
        get_username(token)

        registros_dia = buscar_registro_por_dia(day)
        soma_diferencas = calcular_soma_diferenca_horarios(registros_dia)

        result = {"total trabalhado no dia": soma_diferencas}
        return jsonify(result)
    except GetReportException:
        return jsonify({'error': 'Impossivel gerar o relatório para o usuário'}), 500
    except GetUserInformationException:
        return jsonify({'error':'Impossivel localizar usuário'}), 404
    except DBConnectoException:
        return jsonify({'error': 'Problemas com a conxão com o banco de dados'}), 500
    except Exception as e:
        logger.exception(e)
        return jsonify(error=str(e)), 404


@app.route("/register/<month>", methods=["GET"])
def get_month_register(month: int):
    try:  # pragma: no cover
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': 'Token de autorização ausente'}), 401
        token = auth_header.split(' ')[1]
        get_username(token)

        registros_mes = buscar_registro_por_mes(month)
        result = calcular_total_trabalhado(registros_mes)
        return jsonify(result)
    except GetReportException:
        return jsonify({'error': 'Impossivel gerar o relatório para o usuário'}), 500
    except GetUserInformationException:
        return jsonify({'error':'Impossivel localizar usuário'}), 404
    except DBConnectoException:
        return jsonify({'error': 'Problemas com a conxão com o banco de dados'}), 500
    except Exception as e:
        logger.exception(e)
        return jsonify(error=str(e)), 500


if __name__ == '__main__':
    try: # pragma: no cover
        debug = True
        app.run(host='0.0.0.0', port=5001)
    except Exception as e:
        logger.exception(e)
        raise
