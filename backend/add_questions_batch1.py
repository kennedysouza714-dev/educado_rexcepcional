#!/usr/bin/env python3
"""
Script to add first batch of extracted questions to the database
"""

import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

# Extracted questions from Module 1 (questions 51-70)
NEW_QUESTIONS = [
    {"modulo": "1", "numero": "51", "questao": "A placa PARE exige que o motorista:", "alternativas": {"A": "Diminua a marcha e buzine antes de cruzar.", "B": "Faça parada total e só siga após garantir segurança.", "C": "Avance se tiver prioridade.", "D": "Pare apenas se houver pedestres."}, "resposta": "B", "comentario": "Parar completamente é uma obrigação legal, mesmo se o cruzamento parecer livre."},
    {"modulo": "1", "numero": "52", "questao": "A placa Sentido Proibido serve para:", "alternativas": {"A": "Indicar que a entrada de veículos naquela via ou faixa é proibida, pois o tráfego flui no sentido contrário.", "B": "Avisar sobre obras na pista.", "C": "Indicar estacionamento regulamentado.", "D": "Mostrar a existência de pedágio."}, "resposta": "A", "comentario": "É usada para manter a ordem de fluxo e evitar entrada em vias de sentido único no sentido contrário."},
    {"modulo": "1", "numero": "53", "questao": "A placa de sentido obrigatório à esquerda obriga o condutor a:", "alternativas": {"A": "Virar à esquerda no local indicado.", "B": "Seguir em frente.", "C": "Virar à direita.", "D": "Fazer retorno."}, "resposta": "A", "comentario": "A seta curvada indica que o motorista deve obrigatoriamente virar à esquerda."},
    {"modulo": "1", "numero": "54", "questao": "A placa de proibido virar à esquerda proíbe o motorista de:", "alternativas": {"A": "Fazer conversão à esquerda, inclusive retorno.", "B": "Fazer conversão à direita.", "C": "Parar o veículo.", "D": "Entrar em via preferencial."}, "resposta": "A", "comentario": "A seta cortada para a esquerda representa a proibição de virar ou retornar nessa direção."},
    {"modulo": "1", "numero": "55", "questao": "A principal diferença entre a placa Dê a Preferência e a placa PARE é que:", "alternativas": {"A": "Na placa dê a preferência o condutor só para se houver necessidade, na placa pare a parada é obrigatória.", "B": "Ambas obrigam parada total.", "C": "A Dê a Preferência é usada em rodovias e a PARE apenas em cidades.", "D": "A Dê a Preferência indica via sem cruzamento."}, "resposta": "A", "comentario": "Dê a Preferência indica atenção e redução de velocidade, com parada apenas se necessário, já PARE exige parada total."},
    {"modulo": "1", "numero": "56", "questao": "A principal função da placa de pista dividida é:", "alternativas": {"A": "Alertar o motorista sobre o início de uma pista dividida, aumentando a segurança do tráfego.", "B": "Informar que há pedágio adiante.", "C": "Indicar pista escorregadia.", "D": "Anunciar a presença de curvas perigosas."}, "resposta": "A", "comentario": "A placa orienta o condutor sobre mudança física na via, melhorando a organização do tráfego."},
    {"modulo": "1", "numero": "57", "questao": "Ana dirige em pista simples e encontra a placa de proibido ultrapassar. Essa proibição deve ser seguida enquanto:", "alternativas": {"A": "Houver essa sinalização na via.", "B": "O condutor achar que é seguro.", "C": "Houver espaço suficiente.", "D": "O veículo da frente mantiver a velocidade."}, "resposta": "A", "comentario": "A sinalização de fim de proibição deve indicar claramente o término da restrição."},
    {"modulo": "1", "numero": "58", "questao": "André dirige em uma avenida e vê a placa de proibido mudar de faixa. O que deve fazer?", "alternativas": {"A": "Permanecer na faixa em que está até o final da restrição.", "B": "Mudar de faixa com cuidado, se não houver veículos.", "C": "Encostar à direita para seguir devagar.", "D": "Ultrapassar pela direita."}, "resposta": "A", "comentario": "A placa R-8a proíbe qualquer deslocamento lateral da esquerda para a direita enquanto durar o trecho sinalizado."},
    {"modulo": "1", "numero": "59", "questao": "Ao aproximar-se de uma interseção sinalizada com Dê a Preferência, o condutor deve:", "alternativas": {"A": "Reduzir a velocidade, observar o tráfego na via principal e só avançar se for seguro.", "B": "Parar sobre a faixa de pedestres.", "C": "Seguir direto, pois tem prioridade.", "D": "Buzinar para indicar sua intenção de cruzar."}, "resposta": "A", "comentario": "Essa placa exige comportamento prudente e observação antes de atravessar, sem necessidade de parada total."},
    {"modulo": "1", "numero": "60", "questao": "Ao dirigir em área rural e ver a placa de máquinas agrícolas, o que o condutor deve prever?", "alternativas": {"A": "Possível entrada ou saída lenta de tratores.", "B": "Alta velocidade no trecho.", "C": "Presença de pedestres.", "D": "Obras em pista."}, "resposta": "A", "comentario": "A sinalização previne acidentes causados por diferença de velocidade entre veículos."},
    {"modulo": "1", "numero": "61", "questao": "Ao encontrar a placa PARE em um cruzamento, o condutor deve:", "alternativas": {"A": "Parar completamente o veículo antes da linha de retenção e só seguir quando a via estiver livre.", "B": "Reduzir a velocidade e atravessar devagar se não houver veículos.", "C": "Parar apenas se houver outro veículo aproximando-se.", "D": "Aumentar a velocidade para não atrapalhar o fluxo."}, "resposta": "A", "comentario": "A parada total é obrigatória mesmo sem trânsito no local. Essa placa indica um ponto de risco elevado."},
    {"modulo": "1", "numero": "62", "questao": "Ao encontrar a placa de sentido obrigatório à esquerda, o motorista deve:", "alternativas": {"A": "Sinalizar e virar à esquerda com segurança.", "B": "Seguir reto, sem reduzir a velocidade.", "C": "Virar à direita imediatamente.", "D": "Parar no acostamento."}, "resposta": "A", "comentario": "A manobra deve ser feita com antecedência, respeitando pedestres e ciclistas."},
    {"modulo": "1", "numero": "63", "questao": "Ao ver a placa de velocidade máxima 60 km/h, o condutor deve entender que:", "alternativas": {"A": "Essa é a velocidade máxima permitida para aquele trecho da via.", "B": "É a velocidade obrigatória.", "C": "É apenas uma recomendação.", "D": "É a velocidade mínima."}, "resposta": "A", "comentario": "A placa R-19 fixa o limite máximo permitido, não a velocidade obrigatória."},
    {"modulo": "1", "numero": "64", "questao": "Ao ver a placa Dê a Preferência, o motorista deve:", "alternativas": {"A": "Reduzir a velocidade e deixar passar os veículos que vêm pela via principal.", "B": "Parar completamente o veículo, mesmo sem outros carros.", "C": "Avançar primeiro, pois tem prioridade.", "D": "Buzinar para sinalizar que vai passar."}, "resposta": "A", "comentario": "A placa R-2 orienta o condutor a ceder a passagem, parando apenas se for necessário para evitar colisão."},
    {"modulo": "1", "numero": "65", "questao": "Ao ver a placa Proibido Virar à Esquerda, o motorista deve:", "alternativas": {"A": "Seguir em frente ou virar à direita, respeitando a proibição.", "B": "Fazer a conversão à esquerda com cuidado.", "C": "Parar o veículo no cruzamento.", "D": "Reduzir a velocidade e virar rapidamente."}, "resposta": "A", "comentario": "Essa placa impede qualquer conversão à esquerda naquele ponto, devendo o condutor escolher outro trajeto permitido."},
    {"modulo": "1", "numero": "66", "questao": "Ao ver a placa com uma buzina cortada por uma faixa vermelha, o condutor deve entender que:", "alternativas": {"A": "É proibido usar buzina ou qualquer sinal sonoro no local.", "B": "Deve buzinar para avisar pedestres.", "C": "Só pode buzinar durante o dia.", "D": "O uso da buzina é obrigatório."}, "resposta": "A", "comentario": "A placa R-20 indica proibição de sons que possam causar incômodo ou perturbação."},
    {"modulo": "1", "numero": "67", "questao": "Ao ver a placa de passagem obrigatória, o condutor deve entender que:", "alternativas": {"A": "A passagem é obrigatória pelo lado direito do obstáculo.", "B": "Ele deve virar à esquerda.", "C": "É permitido passar por qualquer lado.", "D": "Deve parar o veículo."}, "resposta": "A", "comentario": "A placa R-24b obriga o condutor a contornar o obstáculo pelo lado indicado."},
    {"modulo": "1", "numero": "68", "questao": "Ao ver a placa de trânsito de pedestres, o motorista deve:", "alternativas": {"A": "Reduzir a velocidade e ficar atento à travessia de pessoas.", "B": "Aumentar a velocidade.", "C": "Buzinar para os pedestres saírem.", "D": "Seguir sem se preocupar."}, "resposta": "A", "comentario": "O respeito ao pedestre é um dos pilares da segurança viária."},
    {"modulo": "1", "numero": "69", "questao": "Camila trafega atrás de um caminhão em um trecho com placa de proibido ultrapassar. O que ela deve fazer?", "alternativas": {"A": "Permanecer em sua faixa, mantendo distância segura.", "B": "Ultrapassar pela faixa da esquerda rapidamente.", "C": "Deslocar-se pelo acostamento.", "D": "Fazer sinal de luz pedindo passagem."}, "resposta": "A", "comentario": "A segurança exige paciência, ultrapassar em trecho proibido pode causar colisões frontais."},
    {"modulo": "1", "numero": "70", "questao": "Carla vê a placa de proibido mudar de faixa em uma ponte. Por que ela foi instalada ali?", "alternativas": {"A": "Para evitar que os veículos mudem de faixa em local estreito e causem colisões.", "B": "Porque há radar de velocidade.", "C": "Porque é área de pedágio.", "D": "Porque é trecho de ultrapassagem."}, "resposta": "A", "comentario": "Em pontes e viadutos, mudar de faixa representa risco de choque lateral e deve ser evitado."},
    {"modulo": "1", "numero": "71", "questao": "Cláudia conduz um caminhão com carga de fardos empilhados e vê a placa de altura máxima antes de um viaduto. O que deve fazer?", "alternativas": {"A": "Verificar se a carga ultrapassa o limite e não passar se estiver acima.", "B": "Acelerar para passar rápido.", "C": "Passar pela calçada lateral.", "D": "Pedir ajuda a outro motorista."}, "resposta": "A", "comentario": "O condutor é responsável por garantir que o veículo e a carga estejam dentro dos limites de altura."},
    {"modulo": "1", "numero": "72", "questao": "Cláudia dirige um automóvel e vê a placa de proibido trânsito de caminhões. Ela pode seguir?", "alternativas": {"A": "Sim, pois a restrição é apenas para caminhões.", "B": "Não, a via é totalmente bloqueada.", "C": "Somente se for moradora.", "D": "Apenas se for horário noturno."}, "resposta": "A", "comentario": "A placa R-9 restringe apenas o trânsito de caminhões, veículos de passeio, ônibus e motos podem transitar."},
    {"modulo": "1", "numero": "73", "questao": "Como o condutor deve agir ao entrar em uma rotatória sinalizada?", "alternativas": {"A": "Deve ceder passagem aos veículos que já circulam dentro dela.", "B": "Deve entrar sem olhar.", "C": "Deve parar no meio da pista.", "D": "Deve buzinar antes de entrar."}, "resposta": "A", "comentario": "Nas rotatórias, a preferência é de quem já está circulando nelas. CTB art. 29, III, c."},
    {"modulo": "1", "numero": "74", "questao": "Em quais locais a placa de proibido trânsito de veículos de grande porte é mais utilizada?", "alternativas": {"A": "Em vias estreitas, áreas residenciais ou centros históricos.", "B": "Em rodovias de pista dupla.", "C": "Em estações rodoviárias.", "D": "Em faixas de ônibus."}, "resposta": "A", "comentario": "Essas áreas não comportam veículos grandes com segurança."},
    {"modulo": "1", "numero": "75", "questao": "Em que locais a placa de passagem obrigatória costuma ser instalada?", "alternativas": {"A": "Antes de canteiros centrais, ilhas, obras e divisores de pista.", "B": "Em estacionamentos subterrâneos.", "C": "Em faixas de pedestre.", "D": "Em zonas escolares."}, "resposta": "A", "comentario": "Essa placa orienta o motorista a contornar obstáculos fixos ou temporários com segurança."},
    {"modulo": "1", "numero": "76", "questao": "Em que locais costuma ser instalada a placa de mão dupla?", "alternativas": {"A": "No final de vias de mão única, indicando o início do duplo sentido.", "B": "Em pontes de pista dupla.", "C": "Em estacionamentos privados.", "D": "Em pedágios automáticos."}, "resposta": "A", "comentario": "É usada na transição entre vias de mão única e mão dupla."},
    {"modulo": "1", "numero": "77", "questao": "Essa placa de circulação exclusiva de pedestres é mais comum em quais locais?", "alternativas": {"A": "Calçadões, parques e ciclovias compartilhadas.", "B": "Rodovias de pista dupla.", "C": "Pontes exclusivas para caminhões.", "D": "Estacionamentos subterrâneos."}, "resposta": "A", "comentario": "É usada em locais urbanos voltados à mobilidade ativa."},
    {"modulo": "1", "numero": "78", "questao": "Fernanda está em uma via de pista dupla e vê a placa de proibido retorno. Qual é o significado dessa placa?", "alternativas": {"A": "É proibido fazer retorno à esquerda no local indicado.", "B": "É permitido virar à esquerda para estacionar.", "C": "É obrigatório virar à direita.", "D": "Indica fim de proibição."}, "resposta": "A", "comentario": "Essa placa proíbe a manobra de retorno à esquerda, que pode causar risco a veículos vindos no sentido oposto."},
    {"modulo": "1", "numero": "79", "questao": "João para o carro por alguns segundos em frente à placa de proibido parar para deixar um passageiro. Ele está correto?", "alternativas": {"A": "Não, pois a placa proíbe qualquer parada, mesmo rápida.", "B": "Sim, se o passageiro descer rápido.", "C": "Sim, se mantiver o pisca-alerta ligado.", "D": "Sim, se o motor permanecer ligado."}, "resposta": "A", "comentario": "Essa placa proíbe imobilizar o veículo por qualquer motivo, mesmo por tempo curto."},
    {"modulo": "1", "numero": "80", "questao": "Júlio para seu carro na frente de um portão onde há a placa de proibido estacionar. Qual é a infração cometida?", "alternativas": {"A": "Estacionar em local proibido pela sinalização.", "B": "Parar o veículo para embarque rápido.", "C": "Transitar em faixa exclusiva.", "D": "Nenhuma infração."}, "resposta": "A", "comentario": "A placa R-6a proíbe estacionar, inclusive em frente a garagens e acessos a propriedades."},
]

async def add_questions():
    mongo_url = os.environ.get('MONGO_URL')
    db_name = os.environ.get('DB_NAME', 'detran_quiz')
    
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    questions_collection = db.questions
    
    # Get existing question numbers to avoid duplicates
    existing = await questions_collection.find({"modulo": "1"}, {"numero": 1}).to_list(length=1000)
    existing_nums = {q.get("numero") for q in existing}
    
    questions_to_insert = []
    for q in NEW_QUESTIONS:
        if q["numero"] not in existing_nums:
            question_doc = {
                "_id": str(uuid.uuid4()),
                "modulo": q["modulo"],
                "numero": q["numero"],
                "questao": q["questao"],
                "alternativas": q["alternativas"],
                "resposta": q["resposta"],
                "comentario": q["comentario"],
                "has_image": False,
                "image_placeholder": None
            }
            questions_to_insert.append(question_doc)
    
    if questions_to_insert:
        await questions_collection.insert_many(questions_to_insert)
        print(f"Inseridas {len(questions_to_insert)} novas questões!")
    else:
        print("Nenhuma questão nova para inserir.")
    
    # Print summary
    print("\n=== Resumo do Banco de Dados ===")
    for modulo in ["1", "2", "3", "4"]:
        count = await questions_collection.count_documents({"modulo": modulo})
        print(f"Módulo {modulo}: {count} questões")
    
    total = await questions_collection.count_documents({})
    print(f"\nTotal de questões: {total}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(add_questions())
