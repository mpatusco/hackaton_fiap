from sympy import solve_poly_system
import sympy
import operator
import logging

from exceptions.custom_exceptions import GetLocationException

logger = logging.getLogger()

# Xa^2 - 2*Xa*Xb + Xb^2 + Ya^2 - 2*Ya*Yb + Yb^2 - D^2
def getlocation(distance, equations = [], x = sympy.Dummy('x'), y = sympy.Dummy('y'),position_kenobi=None,
                position_skywalker=None, position_sato=None):
    try:
        #Define as equações que serão utilizadas
        if position_sato is None and distance.get('sato'):
            logger.debug("adicionando informações do satelite Sato")
            position_sato = [500, 100]
            eq_sato = x ** 2 - 2 * x * (position_sato[0]) + (position_sato[0]) ** 2 + y ** 2 - 2 * y * (
            position_sato[1]) + (position_sato[1]) ** 2 - (distance['sato']) ** 2
            equations.append(eq_sato)

        if position_skywalker is None and distance.get('skywalker'):
            logger.debug("adicionando informações do satelite skywalker")
            position_skywalker = [100, -100]
            eq_skywalker = x ** 2 - 2 * x * (position_skywalker[0]) + (position_skywalker[0]) ** 2 + y ** 2 - 2 * y * (
            position_skywalker[1]) + (position_skywalker[1]) ** 2 - (distance['skywalker']) ** 2
            equations.append(eq_skywalker)

        if position_kenobi is None and distance.get('kenobi'):
            logger.debug("adicionando informações do satelite kenobi")
            position_kenobi = [-500, -200]
            eq_kenobi = x ** 2 - 2 * x * (position_kenobi[0]) + (position_kenobi[0]) ** 2 + y ** 2 - 2 * y * (
            position_kenobi[1]) + (position_kenobi[1]) ** 2 - (distance['kenobi']) ** 2
            equations.append(eq_kenobi)

        #Calcula a possivel localização com margem de erro +/-1
        if len(distance)==3:
            logger.debug("calculando a posição")
            solutions = solve_poly_system([equations[0], equations[1]], x, y) + solve_poly_system([equations[0], equations[2]], x, y) + solve_poly_system([equations[1], equations[2]], x,y)
            print(solutions)
            return(solutions_treatment(solutions))
        elif len(distance)==2:
            logger.debug("calculando a possivel posição")
            solutions = solve_poly_system([equations[0], equations[1]], x, y)
            return f"Com apenas dois pontos conhecidos, existe a possibilidade dessas duas localizações: {solutions}"
        else:
            raise
    except Exception as e:
        logger.exception(e)
        raise GetLocationException(Exception)


def solutions_treatment(solutions, position = []):
    #Se tivermos uma solução real para a localização, as três equações geram 6 resultados, ordenado da seguinte maneira:
    #(solução1 da equação 1, solução2 da equação1, solução1 da equação 2, solução2 da equação2, solução1 da equação 3, solução2 da equação3)
    #Como o ponto existe, ou a solução1 ou a solução 2 da equação 1 tem que ser igual a uma solução de cada equação, ou seja,
    #terão mais dois resultados iguais. Com isso, quando encontramos esses valores iguais dizemos que encontramos o valor.
    #Um ponto de atenção é que o resultado não é exatamente igual, como estamos trabalhando com solve_poly_system,
    #podemos ter uma pequena variância de +/- 0.02, para  evitar problema ou erros por conta disso, colocamos um intervalo de
    #diferença aceitavel de +/-1. Outro ponto de atenção é não aceitar valores colplexos.
    for i in range(0, 5):
        for j in solutions[i]:
            if type(j) != sympy.core.numbers.Float:
                pass
            else:
                if tuple(map(operator.sub, solutions[0], solutions[i])) < (1, 1):
                    position.append(solutions[0])
                    if len(position) == 3:
                        break
                elif tuple(map(operator.sub, solutions[1], solutions[i])) < (1, 1):
                    position.append(solutions[1])
                    if len(position) == 3:
                        break
    return(position[0])


