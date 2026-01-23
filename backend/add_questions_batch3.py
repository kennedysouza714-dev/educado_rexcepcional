#!/usr/bin/env python3
"""
Script to add third batch of extracted questions to the database (questions 131-170)
"""

import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

# More questions from Module 1 (131-170)
NEW_QUESTIONS = [
    {"modulo": "1", "numero": "131", "questao": "Paulo conduz seu carro e encontra a placa de sentido obrigatório à direita. O que ele deve fazer?", "alternativas": {"A": "Seguir obrigatoriamente à direita.", "B": "Virar à esquerda.", "C": "Parar o veículo.", "D": "Fazer retorno."}, "resposta": "A", "comentario": "A seta indica o único sentido permitido para o fluxo naquele ponto."},
    {"modulo": "1", "numero": "132", "questao": "Paulo conduz um caminhão-baú e encontra a placa de peso máximo próxima a uma ponte. Por que essa placa foi instalada ali?", "alternativas": {"A": "Para proteger a estrutura da ponte contra sobrepeso.", "B": "Para controlar o fluxo de veículos.", "C": "Para reduzir a velocidade.", "D": "Para indicar pedágio."}, "resposta": "A", "comentario": "O excesso de peso pode comprometer a estrutura de pontes e viadutos, gerando risco de colapso."},
    {"modulo": "1", "numero": "133", "questao": "Paulo dirige pela Avenida Brasil e encontra a placa de proibido retorno. O que ele deve fazer?", "alternativas": {"A": "Seguir em frente até o próximo ponto permitido para retorno.", "B": "Fazer o retorno rapidamente, olhando pelo retrovisor.", "C": "Parar no meio da via e aguardar espaço.", "D": "Utilizar o acostamento para manobrar."}, "resposta": "A", "comentario": "A R-5a proíbe o retorno à esquerda, devendo o condutor seguir até um local autorizado e seguro."},
    {"modulo": "1", "numero": "134", "questao": "Paulo dirige sob chuva intensa. A placa indica 80 km/h. O que ele deve fazer?", "alternativas": {"A": "Reduzir a velocidade, mesmo que abaixo do limite mínimo.", "B": "Manter no mínimo 80 km/h.", "C": "Aumentar a velocidade para evitar aquaplanagem.", "D": "Parar no acostamento."}, "resposta": "A", "comentario": "O limite da placa é o máximo, mas o condutor deve adequar a velocidade às condições da via."},
    {"modulo": "1", "numero": "135", "questao": "Paulo dirige um ônibus com altura de 3,5 metros e encontra a placa de altura máxima 4,5m. Ele pode seguir?", "alternativas": {"A": "Sim, pois está abaixo do limite máximo permitido.", "B": "Não, porque o veículo é grande.", "C": "Apenas se houver espaço lateral.", "D": "Somente se não houver pedágio."}, "resposta": "A", "comentario": "A altura informada na placa é o limite máximo, veículos mais baixos podem transitar normalmente."},
    {"modulo": "1", "numero": "136", "questao": "Por que a placa de sentido proibido é essencial em cruzamentos de mão única?", "alternativas": {"A": "Para evitar que condutores entrem na contramão.", "B": "Para indicar quebra-molas.", "C": "Para permitir estacionamento.", "D": "Para sinalizar pedágio."}, "resposta": "A", "comentario": "Indica o sentido permitido e impede entradas indevidas na pista oposta."},
    {"modulo": "1", "numero": "137", "questao": "Por que é importante diminuir a velocidade ao ver a placa de lombada?", "alternativas": {"A": "Para evitar danos no veículo e garantir conforto e segurança aos ocupantes.", "B": "Para economizar combustível.", "C": "Para manter o motor em rotação alta.", "D": "Porque a pista é de pedágio."}, "resposta": "A", "comentario": "A passagem rápida pode causar pancadas no fundo do carro e acidentes."},
    {"modulo": "1", "numero": "138", "questao": "Por que é importante olhar para ambos os lados ao passar um cruzamento sinalizado com placa de advertência?", "alternativas": {"A": "Porque veículos podem vir em alta velocidade pela via transversal.", "B": "Porque o motorista precisa ver o pôr do sol.", "C": "Porque o retrovisor não funciona.", "D": "Porque o carro pode desligar."}, "resposta": "A", "comentario": "Muitos sinistros ocorrem por falta de observação lateral."},
    {"modulo": "1", "numero": "139", "questao": "Por que é importante que a placa de via sem saída esteja visível logo na entrada da via?", "alternativas": {"A": "Para que o condutor decida antes de entrar, evitando congestionamentos e manobras perigosas.", "B": "Para indicar o limite de velocidade.", "C": "Para alertar pedestres sobre o fluxo de veículos.", "D": "Para informar presença de lombada."}, "resposta": "A", "comentario": "A visibilidade da placa evita situações de risco e manobras de retorno em locais estreitos."},
    {"modulo": "1", "numero": "140", "questao": "Por que é importante reduzir a velocidade ao ver a placa de semáforo à frente?", "alternativas": {"A": "Porque o sinal pode estar fechado logo à frente.", "B": "Porque a placa é obrigatória.", "C": "Porque há buracos na pista.", "D": "Porque a cor amarela significa perigo fixo."}, "resposta": "A", "comentario": "Reduzir dá tempo para parar com segurança se o sinal estiver vermelho."},
    {"modulo": "1", "numero": "141", "questao": "Por que é importante reduzir a velocidade nas lombadas?", "alternativas": {"A": "Para evitar danos no veículo e garantir conforto e segurança aos ocupantes.", "B": "Porque é obrigatório parar totalmente.", "C": "Para economizar combustível.", "D": "Porque a lombada é apenas decorativa."}, "resposta": "A", "comentario": "A alta velocidade pode causar perda de controle ou danos à suspensão."},
    {"modulo": "1", "numero": "142", "questao": "Por que a placa de pista sinuosa é importante em rodovias e serras?", "alternativas": {"A": "Porque avisa o motorista que a estrada tem curvas fechadas seguidas.", "B": "Porque indica local de pedágio.", "C": "Porque mostra um ponto de ultrapassagem.", "D": "Porque sinaliza uma ponte estreita."}, "resposta": "A", "comentario": "Em regiões de serra, o risco de acidente em curvas duplas é maior."},
    {"modulo": "1", "numero": "143", "questao": "Por que a placa de proibido trânsito de pedestres é importante para a segurança viária?", "alternativas": {"A": "Porque evita atropelamentos em locais sem condições seguras de travessia.", "B": "Porque orienta o fluxo de ciclistas.", "C": "Porque indica o limite de velocidade.", "D": "Porque autoriza pedestres a atravessar em qualquer ponto."}, "resposta": "A", "comentario": "Sua função é afastar pedestres de locais de risco e preservar vidas."},
    {"modulo": "1", "numero": "144", "questao": "Qual a atitude correta de um automóvel diante da placa de faixa exclusiva de caminhões?", "alternativas": {"A": "Não circular na faixa ou via sinalizada.", "B": "Manter-se à direita e reduzir a velocidade.", "C": "Seguir normalmente entre os caminhões.", "D": "Estacionar no local."}, "resposta": "A", "comentario": "A via é reservada apenas ao trânsito de caminhões."},
    {"modulo": "1", "numero": "145", "questao": "Qual deve ser a atitude do condutor ao visualizar a placa de curva à direita?", "alternativas": {"A": "Reduzir a velocidade e posicionar o veículo mais à direita da faixa.", "B": "Aumentar a velocidade para sair rápido da curva.", "C": "Manter a marcha e acelerar na entrada da curva.", "D": "Parar antes da curva."}, "resposta": "A", "comentario": "Reduzir a velocidade e ajustar o posicionamento lateral aumenta a estabilidade."},
    {"modulo": "1", "numero": "146", "questao": "Qual deve ser a atitude do condutor de motocicleta ao encontrar a placa de proibido trânsito de motocicletas?", "alternativas": {"A": "Não entrar ou circular no trecho indicado.", "B": "Seguir normalmente, mas com farol baixo.", "C": "Reduzir a velocidade e seguir.", "D": "Parar para embarque e desembarque."}, "resposta": "A", "comentario": "A entrada de motocicletas em área com essa sinalização constitui infração de trânsito."},
    {"modulo": "1", "numero": "147", "questao": "Qual deve ser a atitude do condutor de ônibus ao encontrar a placa de proibido trânsito de ônibus?", "alternativas": {"A": "Não acessar a via sinalizada.", "B": "Seguir pela via, reduzindo a velocidade.", "C": "Utilizar a via apenas para embarque.", "D": "Parar para verificar o motivo da restrição."}, "resposta": "A", "comentario": "O condutor deve respeitar a proibição e buscar rota alternativa."},
    {"modulo": "1", "numero": "148", "questao": "Qual deve ser a atitude do motorista ao ver a placa de semáforo à frente?", "alternativas": {"A": "Reduzir a velocidade e ficar atento às luzes do semáforo.", "B": "Acelerar para passar antes do vermelho.", "C": "Buzinar para avisar os outros.", "D": "Ignorar a placa e seguir normalmente."}, "resposta": "A", "comentario": "A aproximação de um semáforo exige atenção e velocidade moderada."},
    {"modulo": "1", "numero": "149", "questao": "Qual deve ser a atitude do motorista ao ver a placa de máquinas agrícolas?", "alternativas": {"A": "Reduzir a velocidade e redobrar a atenção.", "B": "Ultrapassar o trator rapidamente.", "C": "Acelerar para sair da área rural.", "D": "Ligar o farol alto."}, "resposta": "A", "comentario": "Máquinas agrícolas se movem devagar, exigindo paciência e cuidado dos demais condutores."},
    {"modulo": "1", "numero": "150", "questao": "Qual deve ser a primeira atitude ao ver a placa de cruzamento de vias?", "alternativas": {"A": "Reduzir a velocidade e observar os dois lados.", "B": "Acelerar para passar antes dos outros carros.", "C": "Buzinar e seguir em frente.", "D": "Parar o veículo no meio da pista."}, "resposta": "A", "comentario": "Reduzir e observar garante tempo para evitar colisões."},
    {"modulo": "1", "numero": "151", "questao": "Qual deve ser o comportamento do condutor ao ver a placa de rotatória antes de entrar?", "alternativas": {"A": "Seguir no sentido indicado e ceder passagem a quem já estiver circulando.", "B": "Parar completamente antes de entrar.", "C": "Entrar pela contramão se a via estiver livre.", "D": "Ultrapassar os veículos mais lentos."}, "resposta": "A", "comentario": "O CTB exige respeito à preferência dos veículos que já estão na rotatória."},
    {"modulo": "1", "numero": "152", "questao": "Qual deve ser o comportamento do motociclista na travessia de linha férrea?", "alternativas": {"A": "Reduzir a velocidade e atravessar em linha reta e devagar, evitando derrapagens sobre os trilhos.", "B": "Atravessar em alta velocidade para não ser atingido.", "C": "Parar no meio dos trilhos para olhar melhor.", "D": "Fazer zigue-zague para manter equilíbrio."}, "resposta": "A", "comentario": "Trilhos podem ser escorregadios, a travessia deve ser feita com cuidado e estabilidade."},
    {"modulo": "1", "numero": "153", "questao": "Qual é a conduta segura ao se aproximar da placa de curva?", "alternativas": {"A": "Reduzir levemente a velocidade e manter o veículo na faixa de rolamento.", "B": "Acelerar antes da curva.", "C": "Frear bruscamente dentro da curva.", "D": "Transitar no acostamento."}, "resposta": "A", "comentario": "A antecipação da redução evita perda de aderência e mantém o controle direcional."},
    {"modulo": "1", "numero": "154", "questao": "Qual é a função principal da placa de pista dividida?", "alternativas": {"A": "Advertir sobre o início de divisão física da pista.", "B": "Indicar redução de pista.", "C": "Avisar sobre pedágio.", "D": "Anunciar obra na pista."}, "resposta": "A", "comentario": "A sinalização prepara o condutor para a nova configuração da via."},
    {"modulo": "1", "numero": "155", "questao": "Qual é a função principal da placa de velocidade máxima?", "alternativas": {"A": "Regular a velocidade máxima de segurança para o local.", "B": "Avisar sobre pedágios.", "C": "Indicar radar escondido.", "D": "Identificar a pista da direita."}, "resposta": "A", "comentario": "A placa R-19 busca compatibilizar segurança e fluidez do trânsito."},
    {"modulo": "1", "numero": "156", "questao": "Qual é a principal função da placa de veículos pesados mantenham-se à direita?", "alternativas": {"A": "Organizar o tráfego e reduzir conflitos entre veículos leves e pesados.", "B": "Alertar sobre lombadas.", "C": "Indicar ponto de parada de ônibus.", "D": "Proibir ultrapassagem."}, "resposta": "A", "comentario": "Mantendo veículos pesados à direita, evita lentidão nas faixas de ultrapassagem."},
    {"modulo": "1", "numero": "157", "questao": "Qual é o principal risco ao ignorar a placa de fim de pista dupla?", "alternativas": {"A": "Colisão frontal com veículos em sentido contrário.", "B": "Estouro de pneu.", "C": "Pane elétrica.", "D": "Gasto excessivo de combustível."}, "resposta": "A", "comentario": "A falta de atenção ao fim da pista dupla pode resultar em ultrapassagem perigosa e choque frontal."},
    {"modulo": "1", "numero": "158", "questao": "Qual é o principal risco ao ignorar a placa de mão dupla?", "alternativas": {"A": "Colisão frontal com veículos que trafegam no sentido contrário.", "B": "Não haverá mais sinalização horizontal.", "C": "O tráfego será apenas de pedestres.", "D": "Porque o carro pode desligar."}, "resposta": "A", "comentario": "A desatenção pode levar a acidentes graves por invasão da contramão."},
    {"modulo": "1", "numero": "159", "questao": "Qual é o risco principal em curvas sinuosas como indicado na placa?", "alternativas": {"A": "O motorista perder o controle do carro se estiver muito rápido.", "B": "O carro desligar o motor.", "C": "O consumo de combustível aumentar.", "D": "O farol apagar."}, "resposta": "A", "comentario": "A força centrífuga aumenta nas curvas e pode empurrar o carro para fora da pista."},
    {"modulo": "1", "numero": "160", "questao": "Qual manobra é proibida na presença da placa de proibido virar à esquerda?", "alternativas": {"A": "Virar à esquerda.", "B": "Seguir em frente.", "C": "Virar à direita.", "D": "Parar na via."}, "resposta": "A", "comentario": "A placa proíbe conversão à esquerda e retorno."},
    {"modulo": "1", "numero": "161", "questao": "Qual manobra é proibida onde há a placa de proibido virar à direita?", "alternativas": {"A": "Virar à direita.", "B": "Seguir em frente.", "C": "Virar à esquerda.", "D": "Parar o veículo."}, "resposta": "A", "comentario": "Essa sinalização impede a conversão à direita no ponto indicado."},
    {"modulo": "1", "numero": "162", "questao": "Qual o objetivo principal da placa de sentido obrigatório?", "alternativas": {"A": "Organizar o fluxo e evitar conflitos de tráfego.", "B": "Avisar sobre obras na pista.", "C": "Permitir o estacionamento.", "D": "Indicar pedágio."}, "resposta": "A", "comentario": "Essa sinalização reduz riscos de colisões frontais e garante circulação ordenada."},
    {"modulo": "1", "numero": "163", "questao": "Qual o principal objetivo da placa de faixa exclusiva de ônibus?", "alternativas": {"A": "Garantir prioridade ao transporte coletivo de passageiros.", "B": "Facilitar o trânsito de caminhões.", "C": "Aumentar o fluxo de automóveis.", "D": "Indicar ponto turístico."}, "resposta": "A", "comentario": "A prioridade ao transporte coletivo melhora a mobilidade urbana e reduz o congestionamento."},
    {"modulo": "1", "numero": "164", "questao": "Qual o principal objetivo da placa de ciclovia e via de pedestres?", "alternativas": {"A": "Garantir segurança e organização entre pedestres e ciclistas.", "B": "Indicar um ponto de parada de ônibus.", "C": "Avisar sobre obras na pista.", "D": "Alertar para curva acentuada."}, "resposta": "A", "comentario": "A separação física e visual reduz riscos de atropelamento e colisão lateral."},
    {"modulo": "1", "numero": "165", "questao": "Qual o principal objetivo da placa de via sem saída?", "alternativas": {"A": "Evitar que o motorista entre por engano e tenha dificuldade de sair.", "B": "Indicar rua preferencial.", "C": "Mostrar via de alta velocidade.", "D": "Avisar sobre lombadas."}, "resposta": "A", "comentario": "A sinalização evita confusão, congestionamentos e manobras indevidas."},
    {"modulo": "1", "numero": "166", "questao": "Quando o condutor encontra a placa de sentido obrigatório em frente, ele:", "alternativas": {"A": "Deve seguir em frente, sem realizar conversões.", "B": "Pode virar à direita.", "C": "Deve parar imediatamente.", "D": "Pode fazer retorno."}, "resposta": "A", "comentario": "A placa indica a única direção permitida naquele ponto da via."},
    {"modulo": "1", "numero": "167", "questao": "Quando o condutor encontra a placa de sentido obrigatório à direita, ele deve:", "alternativas": {"A": "Sinalizar e virar à direita no ponto indicado.", "B": "Parar antes da esquina.", "C": "Virar à esquerda.", "D": "Seguir em frente."}, "resposta": "A", "comentario": "A seta define a direção obrigatória a ser seguida pelo veículo."},
    {"modulo": "1", "numero": "168", "questao": "Quando o motorista vê a placa de parada obrigatória à frente, o que deve fazer?", "alternativas": {"A": "Reduzir a velocidade e se preparar para parar.", "B": "Acelerar para passar antes do vermelho.", "C": "Buzinar para avisar os outros.", "D": "Ignorar a placa e seguir normalmente."}, "resposta": "A", "comentario": "A sinalização de advertência serve para antecipar a parada obrigatória."},
    {"modulo": "1", "numero": "169", "questao": "Rafaela dirige e vê a placa de proibido trânsito de veículos automotores antes de uma praça. Por que essa placa foi colocada ali?", "alternativas": {"A": "Para proteger pedestres e evitar riscos em áreas de convivência.", "B": "Porque há radar fixo.", "C": "Porque o piso é de paralelepípedo.", "D": "Porque é área de estacionamento rotativo."}, "resposta": "A", "comentario": "Essa placa é comum em áreas de lazer, praças e calçadões, garantindo segurança aos pedestres."},
    {"modulo": "1", "numero": "170", "questao": "Rita estaciona seu carro em uma vaga sinalizada com placa de estacionamento permitido com limite de 1 hora rotativo. O que ela deve fazer?", "alternativas": {"A": "Permanecer no local por, no máximo, 1 hora.", "B": "Estacionar o dia todo, se houver vaga.", "C": "Deixar o carro à noite sem controle de tempo.", "D": "Usar a vaga apenas se for moradora da rua."}, "resposta": "A", "comentario": "A placa E indica estacionamento permitido, mas a placa auxiliar define as condições, como o tempo máximo de permanência."},
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
