import boto3
import json


ses_client = boto3.client('ses')


def enviar_email(report_result, email_destino):
    # Construa o corpo do e-mail usando o resultado do relatório
    # Suponha que report_result é um dicionário contendo os detalhes do relatório
    email_body = f"Relatório de registro do mês:\n\n{json.dumps(report_result, indent=4)}"

    # Envie o e-mail usando o Amazon SES
    response = ses_client.send_email(
        Source='seu-email@dominio.com',  # Seu endereço de e-mail SES verificado
        Destination={'ToAddresses': [email_destino]},
        Message={
            'Subject': {'Data': 'Relatório de Registro Mensal'},
            'Body': {'Text': {'Data': email_body}}
        }
    )