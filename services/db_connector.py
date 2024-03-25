import os
import boto3
from boto3.dynamodb.conditions import Key
from decimal import Decimal

from exceptions.custom_exceptions import DBConnectoException


def get_values(dict_distance = {}, list_messages = []):
    #obtem os valores armazenados no banco de dados
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('Challenge_Meli')
        resp = table.scan()
        for item in resp['Items']:
            if item['distance'] != 0 and item['message']!=[]:
                dict_distance[item['satellites']] = float(item['distance'])
                list_messages.append(item['message'])

        return dict_distance, list_messages
    except Exception as e:
        raise DBConnectoException(Exception)

def update_values(satellites):
    #atualiza as informações referentes ao sátelites que já estão no banco de dados
    try:
        for values in satellites:
            decimal = Decimal((str(values['distance'])))
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Challenge_Meli')
            table.update_item(
                Key={
                        'satellites': values['name'],
                    },
                UpdateExpression="set distance = :d, message=:m",
                ExpressionAttributeValues={
                        ':d': decimal,
                        ':m': values['message']
                    },
                ReturnValues="UPDATED_NEW"
                )
    except Exception as e:
        raise DBConnectoException(Exception)
