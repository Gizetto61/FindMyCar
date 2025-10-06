# app/core/recommendation.py

def calculate_recommendations(carros, pesos):
    """
    Calcula o score de recomendação usando as 6 novas características.
    """
    resultados = []

    for carro in carros:
        score = 0
        
        # O dicionário 'pesos' vem do frontend (ex: 'conforto', 'consumo', etc.)
        for chave, preferencia in pesos.items():
            # Mapeia a chave do frontend para a chave do banco de dados (ex: 'conforto' -> 'nota_conforto')
            chave_banco = f"nota_{chave}"
            
            valor_carro = carro.get(chave_banco)
            
            if valor_carro is None:
                continue
            
            # A fórmula de cálculo continua a mesma
            proximidade = 1 - abs(preferencia - int(valor_carro)) / 4
            score += proximidade

        resultados.append({'carro': carro, 'score': score})

    top_5_com_score = sorted(resultados, key=lambda x: x['score'], reverse=True)[:5]
    top_5_carros = [r['carro'] for r in top_5_com_score]
    
    return top_5_carros