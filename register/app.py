from flask import Flask, request, jsonify
import logging
from datetime import datetime

from exceptions.custom_exceptions import GetReportException, DBConnectoException, GetUserInformationException
from services.send_email import enviar_email
from services.calculate_hours_worked import calcular_soma_diferenca_horarios, calcular_total_trabalhado
from services.db_connector import add_registro, buscar_registro_por_dia, buscar_registro_por_mes
from services.validate_user import get_user_email, get_username

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
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': 'Token de autorização ausente'}), 401
        token = auth_header.split(' ')[1]
        empregado_id = get_username(token)

        # Obter a data e hora atuais
        now = datetime.now()
        mes_registro = str(now.month)
        dia_registro = str(now.day)
        horario_registro = now.strftime("%H:%M")  # Formato HH:MM

        # Criar o objeto registro_obj
        registro_obj = {
            'mes_registro': mes_registro,
            'dia_registro': dia_registro,
            'horario_registro': horario_registro,
            'tipo_registro': 'batida',
            'empregado_id': empregado_id
        }

        # Adicionar o registro ao banco de dados
        add_registro(registro_obj)

        result = {"Registro realizado": horario_registro}
        return jsonify(result)
    except GetUserInformationException:
        return jsonify({'error':'Impossivel localizar usuário'}), 404
    except DBConnectoException:
        return jsonify({'error':'Problemas com a conxão com o banco de dados'}), 500
    except Exception as e:
        logger.exception(e)
        return jsonify(error=str(e)), 500


@app.route("/register/<day>", methods=["GET"])
def get_day_register(day: str):
    try:  # pragma: no cover
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': 'Token de autorização ausente'}), 401
        token = auth_header.split(' ')[1]

        registros_dia = buscar_registro_por_dia(day)
        soma_diferencas = calcular_soma_diferenca_horarios(registros_dia, get_username(token))

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
def get_month_register(month: str):
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': 'Token de autorização ausente'}), 401
        token = auth_header.split(' ')[1]

        registros_mes = buscar_registro_por_mes(month, get_username(token))
        result = calcular_total_trabalhado(registros_mes)

        # Enviar e-mail
        email_destino = get_user_email(token)  # Supondo que você tenha uma função para obter o e-mail do usuário
        enviar_email(result, email_destino)

        return jsonify({'message': 'Relatório enviado por e-mail com sucesso!'})
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
