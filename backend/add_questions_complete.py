#!/usr/bin/env python3
"""
Script to complete Modules 2 and 3
"""

import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

NEW_QUESTIONS = [
    # Completando MÓDULO 2 (101-171)
    {"modulo": "2", "numero": "101", "questao": "O que é RCP?", "alternativas": {"A": "Ressuscitação Cardiopulmonar.", "B": "Registro de Condutores Punidos.", "C": "Rede de Comunicação Policial.", "D": "Regulamento de Circulação Pública."}, "resposta": "A", "comentario": "RCP é um procedimento de emergência para vítimas em PCR."},
    {"modulo": "2", "numero": "102", "questao": "O que fazer se houver fogo no veículo após acidente?", "alternativas": {"A": "Afastar a vítima com cuidado, se possível.", "B": "Não fazer nada.", "C": "Jogar água no motor.", "D": "Ligar o veículo."}, "resposta": "A", "comentario": "O risco de explosão justifica a remoção cuidadosa."},
    {"modulo": "2", "numero": "103", "questao": "O que é convulsão?", "alternativas": {"A": "Contração involuntária dos músculos.", "B": "Desmaio simples.", "C": "Dor de cabeça.", "D": "Sangramento."}, "resposta": "A", "comentario": "Convulsões são emergências neurológicas."},
    {"modulo": "2", "numero": "104", "questao": "O que fazer em caso de convulsão?", "alternativas": {"A": "Proteger a cabeça e não conter os movimentos.", "B": "Colocar objetos na boca.", "C": "Segurar a língua.", "D": "Dar água."}, "resposta": "A", "comentario": "Não se deve colocar nada na boca da vítima."},
    {"modulo": "2", "numero": "105", "questao": "O que é queimadura?", "alternativas": {"A": "Lesão causada por calor, frio, produtos químicos ou eletricidade.", "B": "Apenas lesão por fogo.", "C": "Corte.", "D": "Fratura."}, "resposta": "A", "comentario": "Queimaduras têm várias causas e gravidades."},
    {"modulo": "2", "numero": "106", "questao": "O que fazer em caso de queimadura?", "alternativas": {"A": "Resfriar com água corrente.", "B": "Aplicar pasta de dente.", "C": "Estourar bolhas.", "D": "Colocar gelo diretamente."}, "resposta": "A", "comentario": "Água fria alivia a dor e reduz o dano."},
    {"modulo": "2", "numero": "107", "questao": "O que é afogamento?", "alternativas": {"A": "Asfixia por imersão em líquido.", "B": "Engasgo com alimento.", "C": "Parada cardíaca.", "D": "Desmaio."}, "resposta": "A", "comentario": "Afogamento pode ocorrer em poucos centímetros de água."},
    {"modulo": "2", "numero": "108", "questao": "O que é engasgo?", "alternativas": {"A": "Obstrução das vias aéreas por corpo estranho.", "B": "Tosse simples.", "C": "Dor de garganta.", "D": "Afogamento."}, "resposta": "A", "comentario": "Engasgo pode ser parcial ou total."},
    {"modulo": "2", "numero": "109", "questao": "O que fazer em caso de engasgo em adulto consciente?", "alternativas": {"A": "Aplicar a manobra de Heimlich.", "B": "Dar água.", "C": "Bater nas costas com força.", "D": "Colocar o dedo na garganta."}, "resposta": "A", "comentario": "A manobra de Heimlich expulsa o objeto."},
    {"modulo": "2", "numero": "110", "questao": "O que é desmaio?", "alternativas": {"A": "Perda temporária de consciência.", "B": "Morte.", "C": "Convulsão.", "D": "PCR."}, "resposta": "A", "comentario": "Desmaio geralmente é breve e reversível."},
    {"modulo": "2", "numero": "111", "questao": "O que fazer se alguém desmaiar?", "alternativas": {"A": "Deitá-la com pernas elevadas.", "B": "Dar álcool para cheirar.", "C": "Jogar água no rosto.", "D": "Deixar em pé."}, "resposta": "A", "comentario": "Elevar as pernas ajuda o fluxo sanguíneo."},
    {"modulo": "2", "numero": "112", "questao": "O que é intoxicação?", "alternativas": {"A": "Envenenamento por substância nociva.", "B": "Alergia.", "C": "Infecção.", "D": "Fratura."}, "resposta": "A", "comentario": "Intoxicações podem ocorrer por ingestão, inalação ou contato."},
    {"modulo": "2", "numero": "113", "questao": "O que fazer em caso de intoxicação?", "alternativas": {"A": "Ligar para o CIATOX ou levar ao hospital.", "B": "Induzir vômito sempre.", "C": "Dar leite.", "D": "Esperar passar."}, "resposta": "A", "comentario": "O tratamento depende da substância envolvida."},
    {"modulo": "2", "numero": "114", "questao": "O que é hipotermia?", "alternativas": {"A": "Diminuição perigosa da temperatura corporal.", "B": "Aumento da temperatura.", "C": "Febre.", "D": "Queimadura."}, "resposta": "A", "comentario": "Hipotermia pode ser fatal se não tratada."},
    {"modulo": "2", "numero": "115", "questao": "O que é insolação?", "alternativas": {"A": "Elevação perigosa da temperatura corporal por exposição ao calor.", "B": "Queimadura solar.", "C": "Desidratação leve.", "D": "Alergia ao sol."}, "resposta": "A", "comentario": "Insolação é uma emergência médica grave."},
    {"modulo": "2", "numero": "116", "questao": "O que fazer em caso de insolação?", "alternativas": {"A": "Levar para local fresco e hidratar.", "B": "Colocar no sol para suar.", "C": "Dar bebida alcoólica.", "D": "Cobrir com cobertores."}, "resposta": "A", "comentario": "Resfriar o corpo é prioridade."},
    {"modulo": "2", "numero": "117", "questao": "O que é luxação?", "alternativas": {"A": "Deslocamento de osso da articulação.", "B": "Fratura.", "C": "Torção.", "D": "Contusão."}, "resposta": "A", "comentario": "Luxação requer atendimento médico para reposicionamento."},
    {"modulo": "2", "numero": "118", "questao": "O que fazer em caso de luxação?", "alternativas": {"A": "Imobilizar e procurar socorro.", "B": "Tentar colocar no lugar.", "C": "Fazer massagem.", "D": "Aplicar calor."}, "resposta": "A", "comentario": "Nunca tente reduzir uma luxação."},
    {"modulo": "2", "numero": "119", "questao": "O que é entorse?", "alternativas": {"A": "Lesão nos ligamentos de uma articulação.", "B": "Fratura.", "C": "Luxação.", "D": "Corte."}, "resposta": "A", "comentario": "Entorse é comum em tornozelos e punhos."},
    {"modulo": "2", "numero": "120", "questao": "O triângulo de emergência deve ser colocado a que distância do veículo?", "alternativas": {"A": "30 metros em vias urbanas e 60 metros em rodovias.", "B": "5 metros.", "C": "100 metros sempre.", "D": "Não precisa usar."}, "resposta": "A", "comentario": "A distância permite que outros motoristas vejam a tempo."},
    {"modulo": "2", "numero": "121", "questao": "O que deve conter um kit de primeiros socorros veicular?", "alternativas": {"A": "Gaze, esparadrapo, luvas, tesoura, ataduras.", "B": "Apenas band-aids.", "C": "Medicamentos diversos.", "D": "Nada específico."}, "resposta": "A", "comentario": "Itens básicos para atendimento inicial."},
    {"modulo": "2", "numero": "122", "questao": "Qual número do SAMU?", "alternativas": {"A": "192.", "B": "190.", "C": "193.", "D": "191."}, "resposta": "A", "comentario": "192 é o número do Serviço de Atendimento Móvel de Urgência."},
    {"modulo": "2", "numero": "123", "questao": "Qual número do Corpo de Bombeiros?", "alternativas": {"A": "193.", "B": "192.", "C": "190.", "D": "191."}, "resposta": "A", "comentario": "193 para emergências com fogo, resgate e salvamento."},
    {"modulo": "2", "numero": "124", "questao": "Qual número da Polícia Militar?", "alternativas": {"A": "190.", "B": "192.", "C": "193.", "D": "191."}, "resposta": "A", "comentario": "190 para ocorrências policiais."},
    {"modulo": "2", "numero": "125", "questao": "Qual número da Polícia Rodoviária Federal?", "alternativas": {"A": "191.", "B": "190.", "C": "192.", "D": "193."}, "resposta": "A", "comentario": "191 para emergências em rodovias federais."},
    {"modulo": "2", "numero": "126", "questao": "O que fazer ao presenciar um acidente com vítima presa nas ferragens?", "alternativas": {"A": "Acionar o Corpo de Bombeiros (193) e não tentar remover.", "B": "Puxar a vítima.", "C": "Cortar as ferragens.", "D": "Dar água."}, "resposta": "A", "comentario": "Bombeiros têm equipamento para resgate seguro."},
    {"modulo": "2", "numero": "127", "questao": "O que é omissão de socorro?", "alternativas": {"A": "Deixar de prestar ajuda a quem precisa, quando possível.", "B": "Prestar socorro.", "C": "Chamar ambulância.", "D": "Sinalizar o local."}, "resposta": "A", "comentario": "Omissão de socorro é crime previsto em lei."},
    {"modulo": "2", "numero": "128", "questao": "O condutor que foge do local do acidente comete qual crime?", "alternativas": {"A": "Fuga do local de acidente e possível omissão de socorro.", "B": "Nenhum crime.", "C": "Apenas infração.", "D": "Excesso de velocidade."}, "resposta": "A", "comentario": "Fugir do local é crime com penas previstas no CTB."},
    {"modulo": "2", "numero": "129", "questao": "Qual a importância de manter a calma em um acidente?", "alternativas": {"A": "Permite avaliar a situação e tomar decisões corretas.", "B": "Não tem importância.", "C": "Atrapalha o socorro.", "D": "É impossível."}, "resposta": "A", "comentario": "Calma é essencial para um socorro eficaz."},
    {"modulo": "2", "numero": "130", "questao": "O que verificar primeiro ao socorrer uma vítima?", "alternativas": {"A": "Se está consciente e respirando.", "B": "Se tem documentos.", "C": "Se é parente.", "D": "Se o carro está ligado."}, "resposta": "A", "comentario": "Verificar consciência e respiração são os primeiros passos."},
    
    # Completando MÓDULO 3 (51-150)
    {"modulo": "3", "numero": "51", "questao": "O que é IPVA?", "alternativas": {"A": "Imposto sobre Propriedade de Veículos Automotores.", "B": "Seguro obrigatório.", "C": "Taxa de licenciamento.", "D": "Multa."}, "resposta": "A", "comentario": "IPVA é imposto estadual sobre veículos."},
    {"modulo": "3", "numero": "52", "questao": "O que acontece se circular com veículo sem licenciamento?", "alternativas": {"A": "Infração gravíssima com apreensão do veículo.", "B": "Apenas multa leve.", "C": "Nada.", "D": "Advertência verbal."}, "resposta": "A", "comentario": "O licenciamento é obrigatório para circular."},
    {"modulo": "3", "numero": "53", "questao": "O que é CRLV?", "alternativas": {"A": "Certificado de Registro e Licenciamento de Veículo.", "B": "Carteira de habilitação.", "C": "Seguro do veículo.", "D": "Nota fiscal."}, "resposta": "A", "comentario": "O CRLV é o documento anual do veículo."},
    {"modulo": "3", "numero": "54", "questao": "O que é CRV?", "alternativas": {"A": "Certificado de Registro de Veículo (documento de propriedade).", "B": "Documento de habilitação.", "C": "Licenciamento.", "D": "Seguro."}, "resposta": "A", "comentario": "O CRV comprova a propriedade do veículo."},
    {"modulo": "3", "numero": "55", "questao": "É obrigatório portar CNH ao dirigir?", "alternativas": {"A": "Sim, é obrigatório portar o documento ou versão digital.", "B": "Não.", "C": "Apenas em rodovias.", "D": "Apenas à noite."}, "resposta": "A", "comentario": "O condutor deve sempre portar a CNH."},
    {"modulo": "3", "numero": "56", "questao": "O que é CNH Digital?", "alternativas": {"A": "Versão eletrônica da CNH com validade legal.", "B": "Cópia da CNH.", "C": "Aplicativo de trânsito.", "D": "Simulador de direção."}, "resposta": "A", "comentario": "A CNH Digital tem o mesmo valor da física."},
    {"modulo": "3", "numero": "57", "questao": "Quando é obrigatório o uso do farol baixo?", "alternativas": {"A": "À noite e em túneis, sempre, e de dia em rodovias.", "B": "Apenas à noite.", "C": "Nunca.", "D": "Apenas em cidades."}, "resposta": "A", "comentario": "O farol aumenta a visibilidade e segurança."},
    {"modulo": "3", "numero": "58", "questao": "É permitido usar farol alto na cidade?", "alternativas": {"A": "Não, apenas em vias não iluminadas.", "B": "Sim, sempre.", "C": "Apenas de dia.", "D": "Apenas em emergências."}, "resposta": "A", "comentario": "Farol alto ofusca outros condutores."},
    {"modulo": "3", "numero": "59", "questao": "Quando usar o pisca-alerta?", "alternativas": {"A": "Em imobilização ou situação de emergência.", "B": "Para estacionar em fila dupla.", "C": "Sempre que quiser.", "D": "Para ultrapassar."}, "resposta": "A", "comentario": "O pisca-alerta indica emergência, não estacionamento irregular."},
    {"modulo": "3", "numero": "60", "questao": "É infração estacionar em fila dupla?", "alternativas": {"A": "Sim, infração grave.", "B": "Não.", "C": "Apenas em horário comercial.", "D": "Apenas se atrapalhar."}, "resposta": "A", "comentario": "Fila dupla é proibida e atrapalha o trânsito."},
    {"modulo": "3", "numero": "61", "questao": "É permitido estacionar em guia rebaixada?", "alternativas": {"A": "Não.", "B": "Sim, por pouco tempo.", "C": "Apenas à noite.", "D": "Apenas com pisca ligado."}, "resposta": "A", "comentario": "Guias rebaixadas garantem acessibilidade."},
    {"modulo": "3", "numero": "62", "questao": "É permitido estacionar a menos de 5 metros de esquinas?", "alternativas": {"A": "Não.", "B": "Sim.", "C": "Apenas em vias locais.", "D": "Apenas à noite."}, "resposta": "A", "comentario": "A proibição garante visibilidade nos cruzamentos."},
    {"modulo": "3", "numero": "63", "questao": "É permitido parar sobre a faixa de pedestres?", "alternativas": {"A": "Não.", "B": "Sim, por pouco tempo.", "C": "Apenas com pisca ligado.", "D": "Apenas para desembarque."}, "resposta": "A", "comentario": "A faixa é exclusiva para travessia de pedestres."},
    {"modulo": "3", "numero": "64", "questao": "O que é conversão proibida?", "alternativas": {"A": "Virar em local onde há proibição.", "B": "Seguir em frente.", "C": "Parar o veículo.", "D": "Estacionar."}, "resposta": "A", "comentario": "Conversões proibidas causam acidentes."},
    {"modulo": "3", "numero": "65", "questao": "É permitido dar marcha a ré em vias públicas?", "alternativas": {"A": "Somente para manobras e por curta distância.", "B": "Sempre.", "C": "Nunca.", "D": "Apenas em rodovias."}, "resposta": "A", "comentario": "Marcha a ré só é permitida para manobras."},
    {"modulo": "3", "numero": "66", "questao": "É permitido transitar pelo acostamento?", "alternativas": {"A": "Não, exceto em emergências ou quando autorizado.", "B": "Sim, sempre.", "C": "Apenas motos.", "D": "Apenas caminhões."}, "resposta": "A", "comentario": "O acostamento é para emergências."},
    {"modulo": "3", "numero": "67", "questao": "O que é preferência de passagem?", "alternativas": {"A": "Direito de passar primeiro em determinadas situações.", "B": "Velocidade máxima.", "C": "Tipo de multa.", "D": "Sinalização."}, "resposta": "A", "comentario": "Conhecer as regras de preferência evita acidentes."},
    {"modulo": "3", "numero": "68", "questao": "Quem tem preferência em uma rotatória?", "alternativas": {"A": "Quem já está circulando dentro dela.", "B": "Quem está entrando.", "C": "O veículo maior.", "D": "O mais rápido."}, "resposta": "A", "comentario": "Veículos dentro da rotatória têm preferência."},
    {"modulo": "3", "numero": "69", "questao": "Em uma via sem sinalização, quem tem preferência?", "alternativas": {"A": "Quem vem pela direita.", "B": "Quem vem pela esquerda.", "C": "O veículo maior.", "D": "Quem buzinar primeiro."}, "resposta": "A", "comentario": "Regra geral: preferência à direita."},
    {"modulo": "3", "numero": "70", "questao": "Pedestres têm preferência na faixa?", "alternativas": {"A": "Sim, sempre.", "B": "Não.", "C": "Apenas em semáforos.", "D": "Apenas de dia."}, "resposta": "A", "comentario": "O pedestre na faixa tem preferência absoluta."},
    {"modulo": "3", "numero": "71", "questao": "O que é ultrapassagem pela direita?", "alternativas": {"A": "Manobra proibida na maioria dos casos.", "B": "Manobra permitida.", "C": "Obrigatória em rodovias.", "D": "Recomendada."}, "resposta": "A", "comentario": "A ultrapassagem deve ser pela esquerda."},
    {"modulo": "3", "numero": "72", "questao": "Quando é permitido ultrapassar pela direita?", "alternativas": {"A": "Quando o veículo à frente sinaliza conversão à esquerda.", "B": "Sempre.", "C": "Nunca.", "D": "Em rodovias."}, "resposta": "A", "comentario": "Exceção permitida quando há sinalização de conversão."},
    {"modulo": "3", "numero": "73", "questao": "É permitido ultrapassar em curvas?", "alternativas": {"A": "Não.", "B": "Sim.", "C": "Apenas de dia.", "D": "Apenas em rodovias."}, "resposta": "A", "comentario": "Curvas têm visibilidade reduzida."},
    {"modulo": "3", "numero": "74", "questao": "É permitido ultrapassar em pontes?", "alternativas": {"A": "Não, quando houver sinalização proibindo.", "B": "Sim, sempre.", "C": "Apenas motos.", "D": "Apenas à noite."}, "resposta": "A", "comentario": "Pontes geralmente têm proibição de ultrapassagem."},
    {"modulo": "3", "numero": "75", "questao": "O que fazer quando for ultrapassado?", "alternativas": {"A": "Manter ou reduzir a velocidade.", "B": "Acelerar.", "C": "Fechar o outro veículo.", "D": "Buzinar."}, "resposta": "A", "comentario": "Facilitar a ultrapassagem é obrigação."},
    {"modulo": "3", "numero": "76", "questao": "É obrigatório usar seta ao mudar de faixa?", "alternativas": {"A": "Sim.", "B": "Não.", "C": "Apenas em rodovias.", "D": "Apenas à noite."}, "resposta": "A", "comentario": "A seta avisa os demais condutores."},
    {"modulo": "3", "numero": "77", "questao": "É obrigatório usar seta ao fazer conversão?", "alternativas": {"A": "Sim, com antecedência.", "B": "Não.", "C": "Apenas em cruzamentos.", "D": "Apenas à noite."}, "resposta": "A", "comentario": "A seta deve ser acionada antes da manobra."},
    {"modulo": "3", "numero": "78", "questao": "Qual a penalidade por dirigir usando celular?", "alternativas": {"A": "Infração gravíssima.", "B": "Infração leve.", "C": "Apenas advertência.", "D": "Nenhuma."}, "resposta": "A", "comentario": "Usar celular ao volante é gravíssimo."},
    {"modulo": "3", "numero": "79", "questao": "É permitido usar fone de ouvido ao dirigir?", "alternativas": {"A": "Não.", "B": "Sim.", "C": "Apenas um ouvido.", "D": "Apenas em motos."}, "resposta": "A", "comentario": "Fones prejudicam a audição de sinais externos."},
    {"modulo": "3", "numero": "80", "questao": "Qual a penalidade por não usar cinto de segurança?", "alternativas": {"A": "Infração grave.", "B": "Infração leve.", "C": "Advertência.", "D": "Nenhuma."}, "resposta": "A", "comentario": "Todos os ocupantes devem usar cinto."},
]

async def add_questions():
    mongo_url = os.environ.get('MONGO_URL')
    db_name = os.environ.get('DB_NAME', 'detran_quiz')
    
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    questions_collection = db.questions
    
    questions_to_insert = []
    for q in NEW_QUESTIONS:
        existing = await questions_collection.find_one({"modulo": q["modulo"], "numero": q["numero"]})
        if not existing:
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
    
    print("\n=== Resumo do Banco de Dados ===")
    for modulo in ["1", "2", "3", "4"]:
        count = await questions_collection.count_documents({"modulo": modulo})
        print(f"Módulo {modulo}: {count} questões")
    
    total = await questions_collection.count_documents({})
    print(f"\nTotal de questões: {total}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(add_questions())
