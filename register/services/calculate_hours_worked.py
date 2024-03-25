from datetime import datetime, timedelta
from collections import defaultdict

def calcular_soma_diferenca_horarios(resultados_busca):
    horarios = [item['horario_registro'] for item in resultados_busca]
    soma_diferencas = timedelta()
    horarios.sort()  # Ordena os horários em ordem crescente
    
    for i in range(0, len(horarios), 2):
        if i + 1 < len(horarios):
            diferenca = datetime.strptime(horarios[i + 1], '%H:%M') - datetime.strptime(horarios[i], '%H:%M')
            soma_diferencas += diferenca
    
    # Se a quantidade de horários for ímpar, calcula a diferença entre o último horário e o horário atual
    if len(horarios) % 2 == 1:
        ultimo_horario = datetime.strptime(horarios[-1], '%H:%M')
        horario_atual = datetime.now().replace(second=0, microsecond=0)
        diferenca_ultimo = horario_atual - ultimo_horario
        soma_diferencas += diferenca_ultimo
    
    return soma_diferencas


def calcular_total_trabalhado(resultados_busca):
    total_por_dia = defaultdict(timedelta)
    total_trabalhado = timedelta()

    for item in resultados_busca:
        dia_registro = item['dia_registro']
        horario_registro = item['horario_registro']
        total_por_dia[dia_registro] += timedelta(hours=int(horario_registro.split(':')[0]), minutes=int(horario_registro.split(':')[1]))
    
    for total_dia in total_por_dia.values():
        total_trabalhado += total_dia

    return {'total_por_dia': dict(total_por_dia), 'total_trabalhado': total_trabalhado}
