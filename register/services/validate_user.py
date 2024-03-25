import boto3
import json
from jose import jwt


# Função para decodificar o token JWT
def get_username(token):
    try:
        region_name = 'us_east-2'  # Substitua pelo nome da sua região AWS
        userpool_id = 'us-east-2_DnmccQ3fj'  # Substitua pelo ID do seu pool de usuários Cognito

        # Use o serviço CognitoIdentityProvider para buscar a chave de assinatura do JWT
        client = boto3.client('cognito-idp', region_name=region_name)
        keys = client.get_signing_certificate(certificate_id=userpool_id)
        key = keys['Certificate']

        # Decodifique o token JWT usando a chave
        decoded_token = jwt.decode(token, key, algorithms=['RS256'], audience=userpool_id)

        return decoded_token['username']
    except Exception as e:
        # Em caso de erro ao decodificar o token ou obter informações do usuário, retorne uma resposta de erro
        raise Exception("Usuário não identificado pelo cognito")
