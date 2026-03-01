#!/usr/bin/env python3
"""
Script to add more questions - completing modules 2 and 3
"""

import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

NEW_QUESTIONS = [
    # Completando MÓDULO 2 (131-171)
    {"modulo": "2", "numero": "131", "questao": "O que é posição lateral de segurança?", "alternativas": {"A": "Posição para vítimas inconscientes que respiram.", "B": "Posição para RCP.", "C": "Posição sentada.", "D": "Posição em pé."}, "resposta": "A", "comentario": "Evita aspiração de vômito."},
    {"modulo": "2", "numero": "132", "questao": "Quando colocar vítima em posição lateral de segurança?", "alternativas": {"A": "Quando inconsciente mas respirando, sem suspeita de trauma.", "B": "Sempre.", "C": "Nunca.", "D": "Quando acordada."}, "resposta": "A", "comentario": "Protege as vias aéreas."},
    {"modulo": "2", "numero": "133", "questao": "O que é politraumatizado?", "alternativas": {"A": "Vítima com múltiplas lesões.", "B": "Vítima com uma lesão.", "C": "Pessoa saudável.", "D": "Doente crônico."}, "resposta": "A", "comentario": "Acidentes graves causam múltiplas lesões."},
    {"modulo": "2", "numero": "134", "questao": "Como tratar vítima politraumatizada?", "alternativas": {"A": "Não mover, estabilizar e aguardar socorro.", "B": "Movê-la imediatamente.", "C": "Dar água.", "D": "Fazer massagem."}, "resposta": "A", "comentario": "O movimento pode agravar lesões."},
    {"modulo": "2", "numero": "135", "questao": "O que são sinais vitais?", "alternativas": {"A": "Respiração, pulso, temperatura e pressão arterial.", "B": "Apenas respiração.", "C": "Apenas pulso.", "D": "Cor da pele."}, "resposta": "A", "comentario": "Os sinais vitais indicam o estado do organismo."},
    {"modulo": "2", "numero": "136", "questao": "Como verificar se a vítima respira?", "alternativas": {"A": "Ver, ouvir e sentir a respiração.", "B": "Apenas olhar.", "C": "Perguntar.", "D": "Não é possível verificar."}, "resposta": "A", "comentario": "Técnica VOS: Ver, Ouvir, Sentir."},
    {"modulo": "2", "numero": "137", "questao": "Onde verificar pulso em adulto?", "alternativas": {"A": "Artéria carótida (pescoço) ou radial (pulso).", "B": "Pé.", "C": "Orelha.", "D": "Não é possível."}, "resposta": "A", "comentario": "Pulso carotídeo é mais confiável em emergências."},
    {"modulo": "2", "numero": "138", "questao": "O que fazer se não houver pulso?", "alternativas": {"A": "Iniciar RCP imediatamente.", "B": "Esperar.", "C": "Dar água.", "D": "Abandonar a vítima."}, "resposta": "A", "comentario": "Sem pulso = parada cardíaca = RCP urgente."},
    {"modulo": "2", "numero": "139", "questao": "O que é DEA?", "alternativas": {"A": "Desfibrilador Externo Automático.", "B": "Documento de emergência.", "C": "Tipo de ambulância.", "D": "Medicamento."}, "resposta": "A", "comentario": "DEA pode salvar vidas em paradas cardíacas."},
    {"modulo": "2", "numero": "140", "questao": "Onde encontrar DEA?", "alternativas": {"A": "Shoppings, aeroportos, estádios, locais públicos.", "B": "Apenas em hospitais.", "C": "Em farmácias.", "D": "Não existe."}, "resposta": "A", "comentario": "DEAs estão cada vez mais disponíveis."},
    {"modulo": "2", "numero": "141", "questao": "Leigos podem usar DEA?", "alternativas": {"A": "Sim, o equipamento dá instruções.", "B": "Não, apenas médicos.", "C": "Apenas enfermeiros.", "D": "Nunca."}, "resposta": "A", "comentario": "O DEA guia o usuário passo a passo."},
    {"modulo": "2", "numero": "142", "questao": "O que é trauma craniano?", "alternativas": {"A": "Lesão na cabeça.", "B": "Lesão no braço.", "C": "Lesão na perna.", "D": "Lesão no tórax."}, "resposta": "A", "comentario": "Traumas cranianos podem ser graves."},
    {"modulo": "2", "numero": "143", "questao": "Sinais de trauma craniano grave:", "alternativas": {"A": "Perda de consciência, vômito, pupilas diferentes.", "B": "Apenas dor de cabeça.", "C": "Fome.", "D": "Sede."}, "resposta": "A", "comentario": "Esses sinais indicam emergência neurológica."},
    {"modulo": "2", "numero": "144", "questao": "O que fazer em trauma craniano?", "alternativas": {"A": "Não mover a cabeça e chamar socorro.", "B": "Sacudir a vítima.", "C": "Dar água.", "D": "Fazer a vítima andar."}, "resposta": "A", "comentario": "Movimentos podem agravar lesões cerebrais."},
    {"modulo": "2", "numero": "145", "questao": "O que é lesão medular?", "alternativas": {"A": "Dano à medula espinhal.", "B": "Dor muscular.", "C": "Cãibra.", "D": "Torção."}, "resposta": "A", "comentario": "Lesões medulares podem causar paralisia."},
    {"modulo": "2", "numero": "146", "questao": "Por que não mover vítima com suspeita de lesão medular?", "alternativas": {"A": "Pode agravar a lesão e causar paralisia permanente.", "B": "Não há motivo.", "C": "Para não sujar a roupa.", "D": "Para não acordar."}, "resposta": "A", "comentario": "A coluna deve ser imobilizada."},
    {"modulo": "2", "numero": "147", "questao": "O que é evisceração?", "alternativas": {"A": "Exposição de órgãos internos.", "B": "Fratura.", "C": "Desmaio.", "D": "Engasgo."}, "resposta": "A", "comentario": "Lesão grave do abdômen."},
    {"modulo": "2", "numero": "148", "questao": "O que fazer em caso de evisceração?", "alternativas": {"A": "Cobrir com pano úmido e não tentar recolocar.", "B": "Empurrar para dentro.", "C": "Lavar com água.", "D": "Ignorar."}, "resposta": "A", "comentario": "Nunca tente recolocar órgãos expostos."},
    {"modulo": "2", "numero": "149", "questao": "O que é amputação traumática?", "alternativas": {"A": "Perda de membro por acidente.", "B": "Cirurgia programada.", "C": "Fratura.", "D": "Luxação."}, "resposta": "A", "comentario": "Emergência com risco de vida."},
    {"modulo": "2", "numero": "150", "questao": "O que fazer com membro amputado?", "alternativas": {"A": "Envolver em pano limpo e colocar em gelo.", "B": "Jogar fora.", "C": "Colocar diretamente no gelo.", "D": "Lavar com álcool."}, "resposta": "A", "comentario": "Pode ser possível reimplantar."},
    {"modulo": "2", "numero": "151", "questao": "O que é objeto encravado?", "alternativas": {"A": "Objeto que penetrou o corpo.", "B": "Objeto no chão.", "C": "Ferramenta.", "D": "Equipamento médico."}, "resposta": "A", "comentario": "Não deve ser removido no local."},
    {"modulo": "2", "numero": "152", "questao": "O que fazer com objeto encravado?", "alternativas": {"A": "Estabilizar sem remover e chamar socorro.", "B": "Puxar imediatamente.", "C": "Girar o objeto.", "D": "Cortar ao redor."}, "resposta": "A", "comentario": "Remover pode causar hemorragia fatal."},
    {"modulo": "2", "numero": "153", "questao": "O que é afogamento secundário?", "alternativas": {"A": "Complicação que ocorre horas após aspirar água.", "B": "Afogamento em piscina.", "C": "Afogamento no mar.", "D": "Não existe."}, "resposta": "A", "comentario": "Por isso toda vítima deve ir ao hospital."},
    {"modulo": "2", "numero": "154", "questao": "O que é hipoglicemia?", "alternativas": {"A": "Baixo nível de açúcar no sangue.", "B": "Alto nível de açúcar.", "C": "Pressão alta.", "D": "Febre."}, "resposta": "A", "comentario": "Comum em diabéticos."},
    {"modulo": "2", "numero": "155", "questao": "Sintomas de hipoglicemia:", "alternativas": {"A": "Tremores, suor, confusão, desmaio.", "B": "Sede intensa.", "C": "Urina frequente.", "D": "Pele seca."}, "resposta": "A", "comentario": "Reconhecer ajuda no socorro."},
    {"modulo": "2", "numero": "156", "questao": "O que fazer em hipoglicemia se consciente?", "alternativas": {"A": "Dar açúcar ou suco.", "B": "Dar água.", "C": "Não fazer nada.", "D": "Dar insulina."}, "resposta": "A", "comentario": "Açúcar rápido reverte a crise."},
    {"modulo": "2", "numero": "157", "questao": "O que é AVC?", "alternativas": {"A": "Acidente Vascular Cerebral.", "B": "Acidente de Veículo.", "C": "Alergia.", "D": "Asma."}, "resposta": "A", "comentario": "AVC é emergência neurológica."},
    {"modulo": "2", "numero": "158", "questao": "Sinais de AVC:", "alternativas": {"A": "Boca torta, fala arrastada, fraqueza em um lado.", "B": "Dor nas costas.", "C": "Dor de barriga.", "D": "Coceira."}, "resposta": "A", "comentario": "SAMU deve ser acionado imediatamente."},
    {"modulo": "2", "numero": "159", "questao": "O que é infarto?", "alternativas": {"A": "Morte de parte do músculo cardíaco.", "B": "Dor muscular.", "C": "Cãibra.", "D": "Gripe."}, "resposta": "A", "comentario": "Emergência cardíaca grave."},
    {"modulo": "2", "numero": "160", "questao": "Sinais de infarto:", "alternativas": {"A": "Dor no peito, falta de ar, suor frio.", "B": "Apenas cansaço.", "C": "Dor de cabeça.", "D": "Coceira."}, "resposta": "A", "comentario": "Tempo é músculo - socorro rápido salva vidas."},
    {"modulo": "2", "numero": "161", "questao": "O que fazer em suspeita de infarto?", "alternativas": {"A": "Chamar SAMU e manter vítima em repouso.", "B": "Fazer a vítima correr.", "C": "Dar café.", "D": "Ignorar."}, "resposta": "A", "comentario": "Repouso reduz demanda cardíaca."},
    {"modulo": "2", "numero": "162", "questao": "O que é reação alérgica grave (anafilaxia)?", "alternativas": {"A": "Reação imunológica severa com risco de morte.", "B": "Alergia leve.", "C": "Coceira simples.", "D": "Espirro."}, "resposta": "A", "comentario": "Anafilaxia é emergência."},
    {"modulo": "2", "numero": "163", "questao": "Sinais de anafilaxia:", "alternativas": {"A": "Inchaço, dificuldade respiratória, queda de pressão.", "B": "Apenas coceira.", "C": "Apenas espirro.", "D": "Dor de barriga."}, "resposta": "A", "comentario": "Pode evoluir rapidamente para parada."},
    {"modulo": "2", "numero": "164", "questao": "O que fazer em anafilaxia?", "alternativas": {"A": "Chamar emergência imediatamente.", "B": "Dar anti-alérgico e esperar.", "C": "Não fazer nada.", "D": "Dar água."}, "resposta": "A", "comentario": "Adrenalina pode ser necessária."},
    {"modulo": "2", "numero": "165", "questao": "O que é picada de animal peçonhento?", "alternativas": {"A": "Picada de animal que injeta veneno.", "B": "Mordida de cachorro.", "C": "Arranhão de gato.", "D": "Picada de mosquito."}, "resposta": "A", "comentario": "Cobras, aranhas, escorpiões."},
    {"modulo": "2", "numero": "166", "questao": "O que fazer em picada de cobra?", "alternativas": {"A": "Lavar, imobilizar e levar ao hospital.", "B": "Chupar o veneno.", "C": "Fazer torniquete.", "D": "Cortar o local."}, "resposta": "A", "comentario": "Não fazer torniquete nem chupar."},
    {"modulo": "2", "numero": "167", "questao": "Por que não fazer torniquete em picada?", "alternativas": {"A": "Pode causar necrose do membro.", "B": "É a melhor opção.", "C": "Não há motivo.", "D": "Ajuda a retirar veneno."}, "resposta": "A", "comentario": "Torniquete concentra o veneno."},
    {"modulo": "2", "numero": "168", "questao": "O que é soro antiofídico?", "alternativas": {"A": "Antídoto contra veneno de cobra.", "B": "Vacina.", "C": "Antibiótico.", "D": "Analgésico."}, "resposta": "A", "comentario": "Aplicado apenas em hospital."},
    {"modulo": "2", "numero": "169", "questao": "Qual a importância do treinamento em primeiros socorros?", "alternativas": {"A": "Permite agir corretamente em emergências salvando vidas.", "B": "Não tem importância.", "C": "Apenas para profissionais.", "D": "É desnecessário."}, "resposta": "A", "comentario": "Conhecimento pode salvar vidas."},
    {"modulo": "2", "numero": "170", "questao": "O que é a regra PAS em primeiros socorros?", "alternativas": {"A": "Prevenir, Alertar, Socorrer.", "B": "Parar, Andar, Sair.", "C": "Pular, Agachar, Sentar.", "D": "Não existe."}, "resposta": "A", "comentario": "Sequência básica de ação."},
    {"modulo": "2", "numero": "171", "questao": "Por que manter a vítima aquecida?", "alternativas": {"A": "Para prevenir hipotermia e estado de choque.", "B": "Para acordar.", "C": "Para dar sede.", "D": "Não é importante."}, "resposta": "A", "comentario": "O frio agrava o estado de choque."},
    
    # Completando MÓDULO 3 (81-150)
    {"modulo": "3", "numero": "81", "questao": "Qual a penalidade por transportar criança sem cadeirinha?", "alternativas": {"A": "Infração gravíssima.", "B": "Infração leve.", "C": "Advertência.", "D": "Nenhuma."}, "resposta": "A", "comentario": "Segurança da criança é prioridade."},
    {"modulo": "3", "numero": "82", "questao": "É permitido transportar criança no banco da frente?", "alternativas": {"A": "Apenas com mais de 10 anos ou em situações especiais.", "B": "Sim, sempre.", "C": "Nunca.", "D": "Apenas bebês."}, "resposta": "A", "comentario": "Airbag pode ser perigoso para crianças."},
    {"modulo": "3", "numero": "83", "questao": "Qual a multa por excesso de velocidade até 20% acima?", "alternativas": {"A": "Infração média.", "B": "Infração leve.", "C": "Infração grave.", "D": "Gravíssima."}, "resposta": "A", "comentario": "Até 20% = média; acima = grave ou gravíssima."},
    {"modulo": "3", "numero": "84", "questao": "Qual a multa por excesso de velocidade de 20% a 50%?", "alternativas": {"A": "Infração grave.", "B": "Infração leve.", "C": "Infração média.", "D": "Advertência."}, "resposta": "A", "comentario": "Excesso significativo é grave."},
    {"modulo": "3", "numero": "85", "questao": "Qual a multa por excesso de velocidade acima de 50%?", "alternativas": {"A": "Infração gravíssima com suspensão.", "B": "Infração média.", "C": "Infração leve.", "D": "Advertência."}, "resposta": "A", "comentario": "Excesso extremo suspende a CNH."},
    {"modulo": "3", "numero": "86", "questao": "O que é direção perigosa?", "alternativas": {"A": "Conduzir de forma a criar risco.", "B": "Dirigir devagar.", "C": "Usar cinto.", "D": "Respeitar placas."}, "resposta": "A", "comentario": "Direção perigosa é infração e pode ser crime."},
    {"modulo": "3", "numero": "87", "questao": "O que é racha?", "alternativas": {"A": "Disputa de corrida em via pública.", "B": "Trinca no para-brisa.", "C": "Tipo de pneu.", "D": "Estilo de direção."}, "resposta": "A", "comentario": "Racha é crime de trânsito."},
    {"modulo": "3", "numero": "88", "questao": "Qual a pena para quem pratica racha?", "alternativas": {"A": "Detenção de 6 meses a 3 anos.", "B": "Apenas multa.", "C": "Advertência.", "D": "Nenhuma."}, "resposta": "A", "comentario": "Racha é crime previsto no CTB."},
    {"modulo": "3", "numero": "89", "questao": "O que é embriaguez ao volante?", "alternativas": {"A": "Dirigir sob efeito de álcool.", "B": "Dirigir cansado.", "C": "Dirigir com sono.", "D": "Dirigir distraído."}, "resposta": "A", "comentario": "Crime de trânsito gravíssimo."},
    {"modulo": "3", "numero": "90", "questao": "Qual a pena para embriaguez ao volante?", "alternativas": {"A": "Detenção de 6 meses a 3 anos e suspensão da CNH.", "B": "Apenas multa.", "C": "Advertência.", "D": "Nenhuma."}, "resposta": "A", "comentario": "Lei Seca é rigorosa."},
    {"modulo": "3", "numero": "91", "questao": "O que é homicídio culposo no trânsito?", "alternativas": {"A": "Matar alguém sem intenção, por imprudência.", "B": "Matar com intenção.", "C": "Ferir alguém.", "D": "Danificar veículo."}, "resposta": "A", "comentario": "Crime grave mesmo sem intenção."},
    {"modulo": "3", "numero": "92", "questao": "Qual a pena para homicídio culposo no trânsito?", "alternativas": {"A": "Detenção de 2 a 4 anos.", "B": "Apenas multa.", "C": "Advertência.", "D": "6 meses."}, "resposta": "A", "comentario": "Pena pode aumentar com agravantes."},
    {"modulo": "3", "numero": "93", "questao": "O que é lesão corporal culposa no trânsito?", "alternativas": {"A": "Ferir alguém sem intenção, por imprudência.", "B": "Ferir com intenção.", "C": "Matar alguém.", "D": "Danificar veículo."}, "resposta": "A", "comentario": "Crime menos grave que homicídio."},
    {"modulo": "3", "numero": "94", "questao": "O que é omissão de socorro no trânsito?", "alternativas": {"A": "Não prestar ajuda à vítima quando possível.", "B": "Chamar ambulância.", "C": "Sinalizar o local.", "D": "Fugir do local."}, "resposta": "A", "comentario": "Omissão é crime."},
    {"modulo": "3", "numero": "95", "questao": "O que é fuga do local de acidente?", "alternativas": {"A": "Deixar o local sem prestar socorro ou identificar-se.", "B": "Estacionar longe.", "C": "Chamar polícia.", "D": "Fotografar."}, "resposta": "A", "comentario": "Fuga agrava a situação legal."},
    {"modulo": "3", "numero": "96", "questao": "O que é adulteração de veículo?", "alternativas": {"A": "Modificar características do veículo ou documentos.", "B": "Lavar o carro.", "C": "Trocar pneus.", "D": "Fazer revisão."}, "resposta": "A", "comentario": "Crime com pena de reclusão."},
    {"modulo": "3", "numero": "97", "questao": "O que acontece se dirigir com CNH de categoria diferente?", "alternativas": {"A": "Infração gravíssima.", "B": "Infração leve.", "C": "Nada.", "D": "Advertência."}, "resposta": "A", "comentario": "Ex: dirigir caminhão com CNH B."},
    {"modulo": "3", "numero": "98", "questao": "O que é veículo clonado?", "alternativas": {"A": "Veículo com placas de outro veículo.", "B": "Veículo novo.", "C": "Veículo importado.", "D": "Veículo elétrico."}, "resposta": "A", "comentario": "Crime grave de adulteração."},
    {"modulo": "3", "numero": "99", "questao": "O que fazer ao comprar veículo usado?", "alternativas": {"A": "Verificar documentação e histórico de multas e sinistros.", "B": "Confiar no vendedor.", "C": "Não verificar nada.", "D": "Apenas pagar."}, "resposta": "A", "comentario": "Evita comprar veículo com problemas."},
    {"modulo": "3", "numero": "100", "questao": "O que é recall?", "alternativas": {"A": "Chamamento para corrigir defeito de fábrica.", "B": "Multa.", "C": "Inspeção obrigatória.", "D": "Licenciamento."}, "resposta": "A", "comentario": "Fabricantes convocam para reparos gratuitos."},
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
    print(f"\nMeta: 1153 questões")
    print(f"Progresso: {total/1153*100:.1f}%")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(add_questions())
