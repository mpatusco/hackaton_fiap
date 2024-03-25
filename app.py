from flask import Flask, request, jsonify
import logging

from exceptions.custom_exceptions import GetLocationException, DBConnectoException, GetMessageException
from services.db_connector import get_values, update_values
from services.message_interpreter import getmessage
from services.position_calculator import getlocation

logger = logging.getLogger()
app = Flask(__name__)

@app.route('/health_check',methods=["GET"])
def home():
    try:
        response = {'status':200}
        return jsonify(response)
    except Exception as e:
        logger.exception(e)
        return jsonify(error=str(e)), 404

@app.route("/topsecret",methods=["POST"])
def receptor():
    try:  # pragma: no cover
        received = request.get_json()
        update_values(received['satellites'])
        dict_distance, list_messages = get_values()
        distance = getlocation(dict_distance)
        message = getmessage(list_messages)
        result = {"position":{"X":float(distance[0]),"Y":float(distance[1])},"message": message}
        return jsonify(result)
    except GetLocationException:
        return jsonify({'error':'Impossivel calcular a distância'}), 404
    except GetMessageException:
        return jsonify({'error':'Impossivel intepretar a mensagem recebida'}), 404
    except DBConnectoException:
        return jsonify({'error':'Problemas com a conxão com o banco de dados'}), 404
    except Exception as e:
        logger.exception(e)
        return jsonify(error=str(e)), 404


@app.route("/topsecret_split/<satellite_name>",methods=["POST"])
def split_receptor(satellite_name):
    try:  # pragma: no cover
        received = request.get_json()
        received.update({'name':satellite_name})
        update_values(received)
        dict_distance, list_messages = get_values()
        distance = getlocation(dict_distance)
        message = getmessage(list_messages)
        result = {"position":{"X":float(distance[0]),"Y":float(distance[1])},"message": message}
        return jsonify(result)
    except GetLocationException:
        return jsonify({'error': 'Impossivel calcular a distância'}), 404
    except GetMessageException:
        return jsonify({'error': 'Impossivel intepretar a mensagem recebida'}), 404
    except DBConnectoException:
        return jsonify({'error': 'Problemas com a conxão com o banco de dados'}), 404
    except Exception as e:
        logger.exception(e)
        return jsonify(error=str(e)), 404

@app.route("/topsecret_split/", methods=["POST", "GET"])
def split_receptor_get():
    try:  # pragma: no cover
        if request.method == 'POST':
            received = request.get_json()
            update_values(received)
            dict_distance, list_messages = get_values()
            distance = getlocation(dict_distance)
            message = getmessage(list_messages)
        else:
            dict_distance, list_messages = get_values()
            distance = getlocation(dict_distance)
            message = getmessage(list_messages)
        result = {"position":{"X":float(distance[0]),"Y":float(distance[1])},"message": message}
        return jsonify(result)
    except GetLocationException:
        return jsonify({'error': 'Impossivel calcular a distância'}), 404
    except GetMessageException:
        return jsonify({'error': 'Impossivel intepretar a mensagem recebida'}), 404
    except DBConnectoException:
        return jsonify({'error': 'Problemas com a conxão com o banco de dados'}), 404
    except Exception as e:
        logger.exception(e)
        return jsonify(error=str(e)), 404


@app.route("/top_secret_clear",methods=["DELETE"])
def delete_information():
    try:  # pragma: no cover
        received = request.get_json()
        update_values(received)
        return 'Os satelites selecionados foram destruidos'
    except Exception as e:
        logger.exception(e)
        return jsonify(error=str(e)), 404

if __name__ == '__main__':
    try: # pragma: no cover
        debug = True
        app.run(host='0.0.0.0', port=5001)
    except Exception as e:
        logger.exception(e)
        raise
