# app/core/recommendation.py

def calculate_recommendations(carros, pesos):
    """
    Calcula o score de recomendação para uma lista de carros com base nos pesos do usuário.

    :param carros: Uma lista de dicionários, onde cada dicionário é um carro.
    :param pesos: Um dicionário com as preferências do usuário (conforto, consumo, etc.).
    :return: Uma lista dos 5 melhores carros (dicionários), ordenados por score.
    """
    resultados = []

    for carro in carros:
        score = 0
        for chave, preferencia in pesos.items():
            # No seu código original, a chave no dicionário do carro está capitalizada
            # Ex: 'Conforto', 'Consumo'.
            valor_carro = carro.get(chave.capitalize())
            
            if valor_carro is None:
                continue
            
            # A fórmula de cálculo da proximidade
            proximidade = 1 - abs(preferencia - int(valor_carro)) / 4
            score += proximidade

        resultados.append({'carro': carro, 'score': score})

    # Ordena os resultados pelo score em ordem decrescente e pega os 5 primeiros
    top_5_com_score = sorted(resultados, key=lambda x: x['score'], reverse=True)[:5]

    # Retorna apenas os dicionários dos carros, sem o score
    top_5_carros = [r['carro'] for r in top_5_com_score]
    
    return top_5_carros