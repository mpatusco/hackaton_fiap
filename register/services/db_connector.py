import os
import boto3
from boto3.dynamodb.conditions import Key
from decimal import Decimal

from exceptions.custom_exceptions import DBConnectoException


def add_registro(registro_obj):
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('registro')
        table.put_item(
            Item={
                'mes_registro': registro_obj.mes_registro,
                'dia_registro': registro_obj.dia_registro,
                'horario_registro': registro_obj.horario_registro,
                'tipo_registro': registro_obj.tipo_registro,
                'empregado_id': registro_obj.empregado_id
            }
        )
    except Exception as e:
        raise DBConnectoException(Exception)

def buscar_registro_por_dia(dia_registro):
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('registro')
        response = table.query(
            KeyConditionExpression=Key('dia_registro').eq(dia_registro),
            ProjectionExpression="horario_registro, tipo_registro",
            ScanIndexForward=False  # Isso garante que as consultas serão retornadas em ordem decrescente
        )
        return response['Items']
    except Exception as e:
        raise DBConnectoException(Exception)

def buscar_registro_por_mes(mes_registro):
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('registro')
        response = table.query(
            IndexName='mes_registro-index',  # Supondo que você tenha um índice global secundário com o nome 'mes_registro-index'
            KeyConditionExpression=Key('mes_registro').eq(mes_registro),
            ScanIndexForward=False  # Isso garante que as consultas serão retornadas em ordem decrescente
        )
        return response['Items']
    except Exception as e:
        raise DBConnectoException(Exception)