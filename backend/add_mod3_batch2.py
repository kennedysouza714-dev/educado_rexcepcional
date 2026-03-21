#!/usr/bin/env python3
"""
Script to add more Module 3 questions (221-370)
"""

import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

NEW_QUESTIONS = [
    # MÓDULO 3 (221-370)
    {"modulo": "3", "numero": "221", "questao": "O que é CNH definitiva?", "alternativas": {"A": "CNH emitida após período de permissão sem infrações graves.", "B": "CNH vitalícia.", "C": "CNH internacional.", "D": "CNH digital."}, "resposta": "A", "comentario": "Após 1 ano sem infrações graves ou gravíssimas."},
    {"modulo": "3", "numero": "222", "questao": "Qual a validade da CNH?", "alternativas": {"A": "5 anos para menores de 50, 3 anos para 50-69, 1 ano para 70+.", "B": "10 anos.", "C": "Vitalícia.", "D": "2 anos."}, "resposta": "A", "comentario": "Validade varia conforme idade."},
    {"modulo": "3", "numero": "223", "questao": "É necessário exame médico para renovar CNH?", "alternativas": {"A": "Sim, exame de aptidão física e mental.", "B": "Não.", "C": "Apenas após 60 anos.", "D": "Apenas para profissionais."}, "resposta": "A", "comentario": "Obrigatório em toda renovação."},
    {"modulo": "3", "numero": "224", "questao": "O que é exame de aptidão física e mental?", "alternativas": {"A": "Avaliação médica para verificar condições de dirigir.", "B": "Prova teórica.", "C": "Prova prática.", "D": "Exame de sangue."}, "resposta": "A", "comentario": "Realizado por médico credenciado."},
    {"modulo": "3", "numero": "225", "questao": "O que é avaliação psicológica?", "alternativas": {"A": "Exame que avalia condições emocionais para dirigir.", "B": "Teste de inteligência.", "C": "Prova de conhecimentos.", "D": "Entrevista."}, "resposta": "A", "comentario": "Obrigatória para primeira habilitação e algumas renovações."},
    {"modulo": "3", "numero": "226", "questao": "Quando é obrigatória a avaliação psicológica?", "alternativas": {"A": "Primeira habilitação, mudança/adição de categoria, algumas renovações.", "B": "Sempre.", "C": "Nunca.", "D": "Apenas para idosos."}, "resposta": "A", "comentario": "Situações específicas exigem avaliação."},
    {"modulo": "3", "numero": "227", "questao": "É possível dirigir com CNH vencida?", "alternativas": {"A": "Não, é infração gravíssima.", "B": "Sim, por 30 dias.", "C": "Apenas em cidade.", "D": "Apenas em emergência."}, "resposta": "A", "comentario": "CNH vencida não autoriza dirigir."},
    {"modulo": "3", "numero": "228", "questao": "Qual a penalidade por dirigir com CNH vencida há mais de 30 dias?", "alternativas": {"A": "Infração gravíssima com retenção do veículo.", "B": "Infração leve.", "C": "Advertência.", "D": "Nenhuma."}, "resposta": "A", "comentario": "Veículo fica retido até apresentar condutor habilitado."},
    {"modulo": "3", "numero": "229", "questao": "O que é adição de categoria?", "alternativas": {"A": "Incluir nova categoria na CNH já existente.", "B": "Trocar categoria.", "C": "Renovar CNH.", "D": "Perder categoria."}, "resposta": "A", "comentario": "Ex: adicionar A (moto) à categoria B."},
    {"modulo": "3", "numero": "230", "questao": "O que é mudança de categoria?", "alternativas": {"A": "Passar para categoria superior.", "B": "Trocar CNH.", "C": "Renovar.", "D": "Perder CNH."}, "resposta": "A", "comentario": "Ex: de B para C (caminhão)."},
    {"modulo": "3", "numero": "231", "questao": "Qual requisito para mudar para categoria C?", "alternativas": {"A": "Ter CNH B há pelo menos 1 ano e sem infrações graves.", "B": "Apenas curso.", "C": "Idade mínima de 25 anos.", "D": "Nenhum requisito."}, "resposta": "A", "comentario": "Experiência prévia é necessária."},
    {"modulo": "3", "numero": "232", "questao": "Qual requisito para mudar para categoria D?", "alternativas": {"A": "Ter 21 anos, CNH B há 2 anos ou C há 1 ano.", "B": "Apenas curso.", "C": "Ter 18 anos.", "D": "Nenhum."}, "resposta": "A", "comentario": "Requisitos mais rigorosos para transporte de passageiros."},
    {"modulo": "3", "numero": "233", "questao": "Qual requisito para mudar para categoria E?", "alternativas": {"A": "Ter CNH C ou D há pelo menos 1 ano.", "B": "Apenas curso.", "C": "Idade mínima de 30 anos.", "D": "Nenhum."}, "resposta": "A", "comentario": "Para veículos articulados."},
    {"modulo": "3", "numero": "234", "questao": "O que é ACC?", "alternativas": {"A": "Autorização para Conduzir Ciclomotor.", "B": "Aceleração.", "C": "Associação de Condutores.", "D": "Avaliação."}, "resposta": "A", "comentario": "Para veículos de até 50cc."},
    {"modulo": "3", "numero": "235", "questao": "Categoria A engloba quais veículos?", "alternativas": {"A": "Motocicletas, motonetas, triciclos motorizados.", "B": "Apenas motos.", "C": "Carros.", "D": "Caminhões."}, "resposta": "A", "comentario": "Veículos de 2 ou 3 rodas."},
    {"modulo": "3", "numero": "236", "questao": "Categoria B engloba quais veículos?", "alternativas": {"A": "Automóveis, camionetes, utilitários até 3.500kg.", "B": "Apenas carros.", "C": "Motos.", "D": "Ônibus."}, "resposta": "A", "comentario": "Veículos de 4 rodas leves."},
    {"modulo": "3", "numero": "237", "questao": "Categoria C engloba quais veículos?", "alternativas": {"A": "Veículos de carga acima de 3.500kg.", "B": "Ônibus.", "C": "Carros.", "D": "Motos."}, "resposta": "A", "comentario": "Caminhões."},
    {"modulo": "3", "numero": "238", "questao": "Categoria D engloba quais veículos?", "alternativas": {"A": "Veículos de transporte de passageiros com mais de 8 lugares.", "B": "Caminhões.", "C": "Carros.", "D": "Motos."}, "resposta": "A", "comentario": "Ônibus, micro-ônibus, vans."},
    {"modulo": "3", "numero": "239", "questao": "Categoria E engloba quais veículos?", "alternativas": {"A": "Combinações de veículos com reboque acima de 6.000kg.", "B": "Apenas carretas.", "C": "Caminhões simples.", "D": "Ônibus articulados."}, "resposta": "A", "comentario": "Veículos articulados pesados."},
    {"modulo": "3", "numero": "240", "questao": "CNH categoria B permite dirigir ambulância?", "alternativas": {"A": "Sim, se for veículo até 3.500kg.", "B": "Não.", "C": "Apenas com curso.", "D": "Apenas em emergência."}, "resposta": "A", "comentario": "Ambulância leve pode ser conduzida com B."},
    {"modulo": "3", "numero": "241", "questao": "CNH categoria B permite rebocar trailer?", "alternativas": {"A": "Sim, se o conjunto não exceder 3.500kg ou o reboque não exceder 750kg.", "B": "Não.", "C": "Sempre.", "D": "Apenas com AET."}, "resposta": "A", "comentario": "Limite de peso total deve ser respeitado."},
    {"modulo": "3", "numero": "242", "questao": "O que é CNH com observação para uso de lentes?", "alternativas": {"A": "Obrigatoriedade de usar óculos ou lentes ao dirigir.", "B": "Proibição de usar óculos.", "C": "Restrição de categoria.", "D": "CNH especial."}, "resposta": "A", "comentario": "Restrição indicada no documento."},
    {"modulo": "3", "numero": "243", "questao": "O que acontece se dirigir sem os óculos obrigatórios?", "alternativas": {"A": "Infração gravíssima.", "B": "Infração leve.", "C": "Advertência.", "D": "Nada."}, "resposta": "A", "comentario": "Equivale a dirigir sem habilitação."},
    {"modulo": "3", "numero": "244", "questao": "O que é EAR?", "alternativas": {"A": "Exercício de Atividade Remunerada.", "B": "Exame de Aptidão.", "C": "Escola de Aprendizado.", "D": "Equipamento de Rodagem."}, "resposta": "A", "comentario": "Indicação na CNH para profissionais."},
    {"modulo": "3", "numero": "245", "questao": "Quando é necessário EAR na CNH?", "alternativas": {"A": "Para trabalhar como motorista profissional.", "B": "Para todos.", "C": "Apenas taxistas.", "D": "Nunca."}, "resposta": "A", "comentario": "Obrigatório para exercer atividade remunerada."},
    {"modulo": "3", "numero": "246", "questao": "O que é CNH estrangeira?", "alternativas": {"A": "Habilitação emitida por outro país.", "B": "CNH internacional.", "C": "CNH digital.", "D": "CNH provisória."}, "resposta": "A", "comentario": "Pode ser aceita no Brasil em algumas situações."},
    {"modulo": "3", "numero": "247", "questao": "Estrangeiro pode dirigir no Brasil com CNH de seu país?", "alternativas": {"A": "Sim, temporariamente, se acompanhada de tradução juramentada.", "B": "Não.", "C": "Sempre.", "D": "Apenas turistas."}, "resposta": "A", "comentario": "Aceita por tempo limitado."},
    {"modulo": "3", "numero": "248", "questao": "O que é PID?", "alternativas": {"A": "Permissão Internacional para Dirigir.", "B": "Plano de Direção.", "C": "Programa de Inspeção.", "D": "Prova de Identificação."}, "resposta": "A", "comentario": "Permite dirigir em outros países."},
    {"modulo": "3", "numero": "249", "questao": "Onde obter a PID?", "alternativas": {"A": "No DETRAN ou despachante.", "B": "Na polícia.", "C": "No consulado.", "D": "Na internet."}, "resposta": "A", "comentario": "Documento emitido pelo órgão de trânsito."},
    {"modulo": "3", "numero": "250", "questao": "Qual a validade da PID?", "alternativas": {"A": "Mesma validade da CNH.", "B": "1 ano.", "C": "5 anos.", "D": "Vitalícia."}, "resposta": "A", "comentario": "Vinculada à CNH nacional."},
    {"modulo": "3", "numero": "251", "questao": "O que são infrações autossuspensivas?", "alternativas": {"A": "Infrações que suspendem a CNH independente de pontos.", "B": "Infrações leves.", "C": "Advertências.", "D": "Infrações canceladas."}, "resposta": "A", "comentario": "Algumas infrações suspendem automaticamente."},
    {"modulo": "3", "numero": "252", "questao": "Dirigir embriagado é infração autossuspensiva?", "alternativas": {"A": "Sim.", "B": "Não.", "C": "Depende do teor alcoólico.", "D": "Apenas para profissionais."}, "resposta": "A", "comentario": "Suspensão imediata da CNH."},
    {"modulo": "3", "numero": "253", "questao": "Participar de racha é infração autossuspensiva?", "alternativas": {"A": "Sim.", "B": "Não.", "C": "Depende.", "D": "Apenas se causar acidente."}, "resposta": "A", "comentario": "Suspensão automática."},
    {"modulo": "3", "numero": "254", "questao": "Recusar teste do bafômetro é infração?", "alternativas": {"A": "Sim, infração gravíssima com penalidade igual a dirigir embriagado.", "B": "Não.", "C": "Apenas advertência.", "D": "Infração leve."}, "resposta": "A", "comentario": "Lei Seca é rigorosa."},
    {"modulo": "3", "numero": "255", "questao": "É obrigatório fazer teste do bafômetro?", "alternativas": {"A": "Não é obrigatório, mas recusa gera mesma penalidade.", "B": "Sim, obrigatório.", "C": "Nunca.", "D": "Apenas em acidentes."}, "resposta": "A", "comentario": "Recusar tem consequências iguais."},
    {"modulo": "3", "numero": "256", "questao": "O que é blitz de trânsito?", "alternativas": {"A": "Operação de fiscalização.", "B": "Acidente.", "C": "Obra na via.", "D": "Evento."}, "resposta": "A", "comentario": "Fiscalização rotineira ou específica."},
    {"modulo": "3", "numero": "257", "questao": "É obrigatório parar em blitz?", "alternativas": {"A": "Sim.", "B": "Não.", "C": "Apenas se for abordado.", "D": "Apenas de dia."}, "resposta": "A", "comentario": "Recusar é infração."},
    {"modulo": "3", "numero": "258", "questao": "O que é Lei Seca?", "alternativas": {"A": "Lei que proíbe dirigir sob efeito de álcool.", "B": "Lei de velocidade.", "C": "Lei de estacionamento.", "D": "Lei de licenciamento."}, "resposta": "A", "comentario": "Tolerância zero para álcool."},
    {"modulo": "3", "numero": "259", "questao": "Qual o limite de álcool no sangue para dirigir?", "alternativas": {"A": "Zero.", "B": "0,2 dg/L.", "C": "0,5 dg/L.", "D": "1,0 dg/L."}, "resposta": "A", "comentario": "Tolerância zero."},
    {"modulo": "3", "numero": "260", "questao": "Qual a multa por dirigir embriagado?", "alternativas": {"A": "R$ 2.934,70 (gravíssima multiplicada por 10).", "B": "R$ 293,47.", "C": "R$ 500,00.", "D": "R$ 1.000,00."}, "resposta": "A", "comentario": "Uma das maiores multas de trânsito."},
    {"modulo": "3", "numero": "261", "questao": "Além da multa, qual outra penalidade por embriaguez?", "alternativas": {"A": "Suspensão da CNH por 12 meses.", "B": "Apenas pontos.", "C": "Advertência.", "D": "Nenhuma."}, "resposta": "A", "comentario": "Penalidades cumulativas."},
    {"modulo": "3", "numero": "262", "questao": "Dirigir embriagado pode ser crime?", "alternativas": {"A": "Sim, se houver concentração de álcool igual ou superior a 6 dg/L.", "B": "Nunca.", "C": "Apenas se causar acidente.", "D": "Apenas para profissionais."}, "resposta": "A", "comentario": "Crime previsto no CTB."},
    {"modulo": "3", "numero": "263", "questao": "Qual a pena para crime de embriaguez ao volante?", "alternativas": {"A": "Detenção de 6 meses a 3 anos.", "B": "Apenas multa.", "C": "Prisão perpétua.", "D": "Trabalho comunitário."}, "resposta": "A", "comentario": "Crime de trânsito."},
    {"modulo": "3", "numero": "264", "questao": "O que é homicídio culposo de trânsito?", "alternativas": {"A": "Matar alguém em acidente sem intenção.", "B": "Matar intencionalmente.", "C": "Atropelamento leve.", "D": "Colisão sem vítimas."}, "resposta": "A", "comentario": "Crime grave mesmo sem dolo."},
    {"modulo": "3", "numero": "265", "questao": "Qual a pena base para homicídio culposo no trânsito?", "alternativas": {"A": "Detenção de 2 a 4 anos.", "B": "6 meses.", "C": "10 anos.", "D": "Apenas multa."}, "resposta": "A", "comentario": "Pena pode ser aumentada com agravantes."},
    {"modulo": "3", "numero": "266", "questao": "O que aumenta a pena do homicídio culposo?", "alternativas": {"A": "Embriaguez, racha, excesso de velocidade.", "B": "Nada.", "C": "Ser primário.", "D": "Ter seguro."}, "resposta": "A", "comentario": "Agravantes específicos do CTB."},
    {"modulo": "3", "numero": "267", "questao": "O que é lesão corporal culposa no trânsito?", "alternativas": {"A": "Ferir alguém em acidente sem intenção.", "B": "Ferimento intencional.", "C": "Dano ao veículo.", "D": "Multa."}, "resposta": "A", "comentario": "Crime menos grave que homicídio."},
    {"modulo": "3", "numero": "268", "questao": "Qual a pena para lesão corporal culposa no trânsito?", "alternativas": {"A": "Detenção de 6 meses a 2 anos.", "B": "Apenas multa.", "C": "5 anos.", "D": "Advertência."}, "resposta": "A", "comentario": "Pena pode aumentar com agravantes."},
    {"modulo": "3", "numero": "269", "questao": "O que é fuga do local de acidente?", "alternativas": {"A": "Deixar o local sem prestar socorro ou se identificar.", "B": "Sair do veículo.", "C": "Chamar polícia.", "D": "Fotografar."}, "resposta": "A", "comentario": "Crime de trânsito."},
    {"modulo": "3", "numero": "270", "questao": "Qual a pena para fuga do local de acidente?", "alternativas": {"A": "Detenção de 6 meses a 1 ano.", "B": "Apenas multa.", "C": "5 anos.", "D": "Advertência."}, "resposta": "A", "comentario": "Crime específico do CTB."},
    {"modulo": "3", "numero": "271", "questao": "O que é omissão de socorro no trânsito?", "alternativas": {"A": "Deixar de socorrer vítima quando possível.", "B": "Prestar socorro.", "C": "Chamar ambulância.", "D": "Sinalizar."}, "resposta": "A", "comentario": "Crime de trânsito."},
    {"modulo": "3", "numero": "272", "questao": "Qual a pena para omissão de socorro no trânsito?", "alternativas": {"A": "Aumenta pela metade as penas de homicídio ou lesão.", "B": "Crime autônomo.", "C": "Apenas multa.", "D": "Nenhuma."}, "resposta": "A", "comentario": "Agravante das penas."},
    {"modulo": "3", "numero": "273", "questao": "O que é direção perigosa?", "alternativas": {"A": "Dirigir de forma a criar perigo de dano.", "B": "Dirigir rápido.", "C": "Dirigir devagar.", "D": "Dirigir à noite."}, "resposta": "A", "comentario": "Pode ser infração ou crime."},
    {"modulo": "3", "numero": "274", "questao": "O que é racha ou pega?", "alternativas": {"A": "Disputa de corrida não autorizada em via pública.", "B": "Competição oficial.", "C": "Ultrapassagem.", "D": "Teste de velocidade."}, "resposta": "A", "comentario": "Crime de trânsito."},
    {"modulo": "3", "numero": "275", "questao": "Qual a pena para participar de racha?", "alternativas": {"A": "Detenção de 6 meses a 3 anos.", "B": "Apenas multa.", "C": "Advertência.", "D": "Prisão perpétua."}, "resposta": "A", "comentario": "Crime grave."},
    {"modulo": "3", "numero": "276", "questao": "Promover racha sem participar é crime?", "alternativas": {"A": "Sim, mesma pena.", "B": "Não.", "C": "Apenas infração.", "D": "Depende."}, "resposta": "A", "comentario": "Organizadores também respondem."},
    {"modulo": "3", "numero": "277", "questao": "O que é velocidade incompatível?", "alternativas": {"A": "Dirigir em velocidade inadequada às condições.", "B": "Apenas excesso de velocidade.", "C": "Dirigir devagar.", "D": "Velocidade normal."}, "resposta": "A", "comentario": "Pode ser crime em certas situações."},
    {"modulo": "3", "numero": "278", "questao": "O que é direção sem habilitação?", "alternativas": {"A": "Dirigir sem CNH ou com CNH cassada/suspensa.", "B": "Dirigir com CNH vencida.", "C": "Dirigir com CNH de outro estado.", "D": "Dirigir sem documentos."}, "resposta": "A", "comentario": "Pode ser crime."},
    {"modulo": "3", "numero": "279", "questao": "Quando dirigir sem habilitação é crime?", "alternativas": {"A": "Quando gerar perigo de dano.", "B": "Sempre.", "C": "Nunca.", "D": "Apenas para menores."}, "resposta": "A", "comentario": "Crime de perigo."},
    {"modulo": "3", "numero": "280", "questao": "Qual a pena para direção sem habilitação com perigo?", "alternativas": {"A": "Detenção de 6 meses a 1 ano.", "B": "Apenas multa.", "C": "5 anos.", "D": "Advertência."}, "resposta": "A", "comentario": "Crime do CTB."},
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
    
    print("\n=== Resumo do Banco de Dados ===")
    for modulo in ["1", "2", "3", "4"]:
        count = await questions_collection.count_documents({"modulo": modulo})
        target = {"1": 371, "2": 171, "3": 575, "4": 36}[modulo]
        status = "✅" if count >= target else "🔄"
        print(f"{status} Módulo {modulo}: {count}/{target} ({count/target*100:.0f}%)")
    
    total = await questions_collection.count_documents({})
    print(f"\n📊 Total: {total}/1153 ({total/1153*100:.1f}%)")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(add_questions())
