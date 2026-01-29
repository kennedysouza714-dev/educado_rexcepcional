#!/usr/bin/env python3
"""
Script to add questions from Modules 2, 3 and 4
"""

import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

# Questions from Module 2 - Escolhas e Consequências (21-100)
NEW_QUESTIONS = [
    # MÓDULO 2 - Escolhas e Consequências
    {"modulo": "2", "numero": "21", "questao": "Ao conduzir em rodovia, qual atitude demonstra direção defensiva?", "alternativas": {"A": "Manter distância segura do veículo à frente.", "B": "Dirigir colado ao veículo da frente.", "C": "Acelerar para ultrapassar rapidamente.", "D": "Usar o celular para verificar mensagens."}, "resposta": "A", "comentario": "A distância de segurança permite tempo de reação em caso de frenagem brusca."},
    {"modulo": "2", "numero": "22", "questao": "O que caracteriza a direção defensiva?", "alternativas": {"A": "Antecipar situações de risco e agir preventivamente.", "B": "Reagir somente após o perigo acontecer.", "C": "Confiar que os outros motoristas sempre seguem as regras.", "D": "Dirigir o mais rápido possível."}, "resposta": "A", "comentario": "Direção defensiva é prever riscos e evitá-los antes que ocorram."},
    {"modulo": "2", "numero": "23", "questao": "Um motorista defensivo deve:", "alternativas": {"A": "Estar sempre atento às condições da via e do trânsito.", "B": "Ignorar os sinais de trânsito quando a via está vazia.", "C": "Confiar apenas em sua habilidade ao volante.", "D": "Ultrapassar sempre que possível."}, "resposta": "A", "comentario": "Atenção constante é um dos pilares da direção defensiva."},
    {"modulo": "2", "numero": "24", "questao": "Qual é a principal causa de acidentes de trânsito?", "alternativas": {"A": "Falha humana.", "B": "Defeito mecânico.", "C": "Condições climáticas.", "D": "Problemas nas vias."}, "resposta": "A", "comentario": "Estudos mostram que a maioria dos acidentes é causada por erros humanos."},
    {"modulo": "2", "numero": "25", "questao": "O que é aquaplanagem?", "alternativas": {"A": "Perda de aderência dos pneus em pista molhada.", "B": "Excesso de velocidade em curvas.", "C": "Falta de combustível.", "D": "Problema no sistema de freios."}, "resposta": "A", "comentario": "A aquaplanagem ocorre quando há uma camada de água entre os pneus e o asfalto."},
    {"modulo": "2", "numero": "26", "questao": "Como evitar a aquaplanagem?", "alternativas": {"A": "Reduzir a velocidade em pista molhada.", "B": "Acelerar para passar rápido pela água.", "C": "Frear bruscamente.", "D": "Manter os pneus carecas."}, "resposta": "A", "comentario": "Velocidade reduzida e pneus em bom estado previnem a aquaplanagem."},
    {"modulo": "2", "numero": "27", "questao": "O que fazer em caso de aquaplanagem?", "alternativas": {"A": "Tirar o pé do acelerador e manter o volante firme.", "B": "Frear bruscamente.", "C": "Acelerar para sair da água.", "D": "Virar o volante rapidamente."}, "resposta": "A", "comentario": "Movimentos suaves ajudam a recuperar o controle do veículo."},
    {"modulo": "2", "numero": "28", "questao": "O cinto de segurança é obrigatório para:", "alternativas": {"A": "Todos os ocupantes do veículo.", "B": "Apenas o motorista.", "C": "Apenas os passageiros do banco da frente.", "D": "Apenas em rodovias."}, "resposta": "A", "comentario": "O CTB exige o uso do cinto por todos os ocupantes em qualquer via."},
    {"modulo": "2", "numero": "29", "questao": "Qual a função do cinto de segurança?", "alternativas": {"A": "Manter o ocupante preso ao banco em caso de colisão.", "B": "Evitar multas.", "C": "Melhorar a postura.", "D": "Reduzir o consumo de combustível."}, "resposta": "A", "comentario": "O cinto distribui a força do impacto e evita que o ocupante seja projetado."},
    {"modulo": "2", "numero": "30", "questao": "Crianças de até 7 anos e meio devem ser transportadas:", "alternativas": {"A": "No banco traseiro com dispositivo de retenção adequado.", "B": "No banco da frente com cinto.", "C": "No colo de um adulto.", "D": "Sem nenhum dispositivo especial."}, "resposta": "A", "comentario": "A legislação exige cadeirinha ou assento de elevação conforme a idade e peso."},
    {"modulo": "2", "numero": "31", "questao": "O que é fadiga ao volante?", "alternativas": {"A": "Cansaço físico ou mental que prejudica a capacidade de dirigir.", "B": "Falta de combustível.", "C": "Problema mecânico no veículo.", "D": "Excesso de velocidade."}, "resposta": "A", "comentario": "A fadiga reduz reflexos e atenção, aumentando o risco de acidentes."},
    {"modulo": "2", "numero": "32", "questao": "Como prevenir a fadiga ao volante?", "alternativas": {"A": "Fazer pausas regulares durante viagens longas.", "B": "Tomar bebidas energéticas.", "C": "Dirigir mais rápido para chegar logo.", "D": "Ligar o ar-condicionado no máximo."}, "resposta": "A", "comentario": "Pausas de 15 a 20 minutos a cada 2 horas ajudam a manter o alerta."},
    {"modulo": "2", "numero": "33", "questao": "Qual o efeito do álcool na direção?", "alternativas": {"A": "Diminui os reflexos e a capacidade de julgamento.", "B": "Aumenta a atenção.", "C": "Melhora a visão noturna.", "D": "Não tem efeito significativo."}, "resposta": "A", "comentario": "O álcool afeta o sistema nervoso central, prejudicando a direção."},
    {"modulo": "2", "numero": "34", "questao": "Qual é o limite de álcool no sangue permitido para condutores?", "alternativas": {"A": "Zero.", "B": "0,2 decigramas por litro.", "C": "0,5 decigramas por litro.", "D": "1,0 decigrama por litro."}, "resposta": "A", "comentario": "A Lei Seca estabelece tolerância zero para álcool no sangue de condutores."},
    {"modulo": "2", "numero": "35", "questao": "O que é visão periférica?", "alternativas": {"A": "Capacidade de ver objetos fora do foco principal.", "B": "Visão com óculos escuros.", "C": "Visão apenas central.", "D": "Visão noturna."}, "resposta": "A", "comentario": "A visão periférica ajuda a perceber movimentos laterais no trânsito."},
    {"modulo": "2", "numero": "36", "questao": "O que acontece com a visão periférica em alta velocidade?", "alternativas": {"A": "Ela diminui, criando o efeito túnel.", "B": "Ela aumenta.", "C": "Não é afetada.", "D": "Melhora a percepção."}, "resposta": "A", "comentario": "Em alta velocidade, o campo de visão se estreita, dificultando ver os lados."},
    {"modulo": "2", "numero": "37", "questao": "Qual a distância mínima de seguimento em condições normais?", "alternativas": {"A": "Dois segundos do veículo à frente.", "B": "Meio segundo.", "C": "Um metro.", "D": "Não há distância mínima."}, "resposta": "A", "comentario": "A regra dos dois segundos garante tempo de reação adequado."},
    {"modulo": "2", "numero": "38", "questao": "Em pista molhada, a distância de seguimento deve ser:", "alternativas": {"A": "Aumentada.", "B": "Mantida igual.", "C": "Diminuída.", "D": "Não importa."}, "resposta": "A", "comentario": "Pista molhada aumenta a distância de frenagem, exigindo maior espaço."},
    {"modulo": "2", "numero": "39", "questao": "O que é ponto cego?", "alternativas": {"A": "Área ao redor do veículo que não é visível pelos espelhos.", "B": "Problema de visão do motorista.", "C": "Local sem sinalização.", "D": "Trecho escuro da via."}, "resposta": "A", "comentario": "O ponto cego deve ser verificado virando a cabeça antes de manobras."},
    {"modulo": "2", "numero": "40", "questao": "Como reduzir os riscos do ponto cego?", "alternativas": {"A": "Ajustar os espelhos corretamente e olhar para os lados.", "B": "Confiar apenas nos espelhos.", "C": "Ignorar os pontos cegos.", "D": "Dirigir mais rápido."}, "resposta": "A", "comentario": "A combinação de espelhos bem ajustados e verificação visual reduz riscos."},
    {"modulo": "2", "numero": "41", "questao": "Ao mudar de faixa, o motorista deve:", "alternativas": {"A": "Sinalizar, verificar espelhos e ponto cego.", "B": "Apenas sinalizar.", "C": "Mudar rapidamente sem avisar.", "D": "Buzinar para os outros saírem."}, "resposta": "A", "comentario": "A sequência correta previne colisões laterais."},
    {"modulo": "2", "numero": "42", "questao": "O que é força centrífuga?", "alternativas": {"A": "Força que empurra o veículo para fora da curva.", "B": "Força que puxa o veículo para dentro da curva.", "C": "Força de frenagem.", "D": "Força do motor."}, "resposta": "A", "comentario": "Em curvas, a força centrífuga tende a jogar o veículo para fora."},
    {"modulo": "2", "numero": "43", "questao": "Como contrapor a força centrífuga em uma curva?", "alternativas": {"A": "Reduzir a velocidade antes da curva.", "B": "Acelerar na curva.", "C": "Frear bruscamente na curva.", "D": "Soltar o volante."}, "resposta": "A", "comentario": "Velocidade adequada mantém a aderência dos pneus na curva."},
    {"modulo": "2", "numero": "44", "questao": "O que é força de inércia?", "alternativas": {"A": "Tendência do corpo em manter seu estado de movimento.", "B": "Força do motor.", "C": "Força dos freios.", "D": "Força do vento."}, "resposta": "A", "comentario": "A inércia faz o corpo continuar em movimento mesmo após a frenagem."},
    {"modulo": "2", "numero": "45", "questao": "Por que usar o cinto de segurança combate a inércia?", "alternativas": {"A": "Impede que o corpo seja projetado para frente em uma frenagem.", "B": "Aumenta a velocidade.", "C": "Reduz o consumo de combustível.", "D": "Melhora a direção."}, "resposta": "A", "comentario": "O cinto mantém o ocupante preso ao banco durante desacelerações bruscas."},
    {"modulo": "2", "numero": "46", "questao": "O que fazer se o veículo apresentar falha nos freios?", "alternativas": {"A": "Usar o freio motor e o freio de estacionamento gradualmente.", "B": "Pular do veículo.", "C": "Acelerar para compensar.", "D": "Fechar os olhos e esperar."}, "resposta": "A", "comentario": "Freio motor e freio de mão ajudam a reduzir a velocidade com segurança."},
    {"modulo": "2", "numero": "47", "questao": "O que é freio motor?", "alternativas": {"A": "Redução de velocidade usando as marchas do câmbio.", "B": "Freio de emergência.", "C": "Freio ABS.", "D": "Freio de estacionamento."}, "resposta": "A", "comentario": "Engatar marchas mais baixas ajuda a desacelerar o veículo."},
    {"modulo": "2", "numero": "48", "questao": "Em descidas longas, o motorista deve:", "alternativas": {"A": "Usar o freio motor para não superaquecer os freios.", "B": "Manter o pé no freio o tempo todo.", "C": "Descer em ponto morto.", "D": "Acelerar para ganhar tempo."}, "resposta": "A", "comentario": "O freio motor preserva o sistema de freios e mantém o controle."},
    {"modulo": "2", "numero": "49", "questao": "O que é ultrapassagem?", "alternativas": {"A": "Manobra de passar à frente de outro veículo.", "B": "Parar atrás de outro veículo.", "C": "Seguir outro veículo.", "D": "Estacionar."}, "resposta": "A", "comentario": "Ultrapassagem é uma manobra que requer cuidado e visibilidade."},
    {"modulo": "2", "numero": "50", "questao": "Quando é permitido ultrapassar?", "alternativas": {"A": "Quando há visibilidade suficiente e sinalização permite.", "B": "Sempre que quiser.", "C": "Apenas em curvas.", "D": "Somente à noite."}, "resposta": "A", "comentario": "A ultrapassagem segura depende de condições adequadas."},
    {"modulo": "2", "numero": "51", "questao": "O que o condutor deve verificar antes de ultrapassar?", "alternativas": {"A": "Se há espaço, tempo e visibilidade suficientes.", "B": "Apenas se o carro é potente.", "C": "Se está com pressa.", "D": "Se o outro motorista permite."}, "resposta": "A", "comentario": "Avaliar as condições evita acidentes durante a ultrapassagem."},
    {"modulo": "2", "numero": "52", "questao": "Por onde deve ser feita a ultrapassagem?", "alternativas": {"A": "Pela esquerda do veículo à frente.", "B": "Pela direita sempre.", "C": "Por qualquer lado.", "D": "Pelo acostamento."}, "resposta": "A", "comentario": "No Brasil, a ultrapassagem deve ser feita pela esquerda."},
    {"modulo": "2", "numero": "53", "questao": "O que é direção evasiva?", "alternativas": {"A": "Manobra para evitar uma colisão iminente.", "B": "Dirigir em alta velocidade.", "C": "Fugir da polícia.", "D": "Estacionar rapidamente."}, "resposta": "A", "comentario": "A direção evasiva é uma técnica de emergência para evitar acidentes."},
    {"modulo": "2", "numero": "54", "questao": "Qual a importância da manutenção preventiva do veículo?", "alternativas": {"A": "Evita falhas mecânicas que podem causar acidentes.", "B": "Apenas deixa o carro bonito.", "C": "Aumenta o consumo de combustível.", "D": "Não tem importância."}, "resposta": "A", "comentario": "Veículos bem mantidos são mais seguros e confiáveis."},
    {"modulo": "2", "numero": "55", "questao": "O que verificar antes de viajar?", "alternativas": {"A": "Pneus, freios, luzes, nível de óleo e água.", "B": "Apenas o combustível.", "C": "Apenas os documentos.", "D": "Nada especial."}, "resposta": "A", "comentario": "Uma verificação completa previne problemas durante a viagem."},
    {"modulo": "2", "numero": "56", "questao": "Pneus carecas aumentam o risco de:", "alternativas": {"A": "Aquaplanagem e perda de controle.", "B": "Economia de combustível.", "C": "Melhor aderência.", "D": "Maior durabilidade."}, "resposta": "A", "comentario": "Pneus sem sulcos não escoam água adequadamente."},
    {"modulo": "2", "numero": "57", "questao": "Qual a pressão correta dos pneus?", "alternativas": {"A": "A indicada pelo fabricante do veículo.", "B": "A máxima permitida pelo pneu.", "C": "A mínima para economizar.", "D": "Qualquer uma serve."}, "resposta": "A", "comentario": "A pressão correta garante segurança, economia e durabilidade."},
    {"modulo": "2", "numero": "58", "questao": "O que pode causar o superaquecimento do motor?", "alternativas": {"A": "Falta de água no radiador ou problema no sistema de arrefecimento.", "B": "Excesso de combustível.", "C": "Pneus novos.", "D": "Uso do ar-condicionado."}, "resposta": "A", "comentario": "O sistema de arrefecimento deve estar sempre em bom estado."},
    {"modulo": "2", "numero": "59", "questao": "O que fazer se o motor superaquecer?", "alternativas": {"A": "Parar em local seguro e esperar esfriar.", "B": "Continuar dirigindo.", "C": "Abrir o reservatório imediatamente.", "D": "Acelerar para ventilar."}, "resposta": "A", "comentario": "Nunca abra o reservatório com o motor quente devido ao risco de queimaduras."},
    {"modulo": "2", "numero": "60", "questao": "O que é hidroplanagem?", "alternativas": {"A": "Outro nome para aquaplanagem.", "B": "Problema no sistema hidráulico.", "C": "Tipo de freio.", "D": "Sistema de direção."}, "resposta": "A", "comentario": "Hidroplanagem e aquaplanagem são sinônimos."},
    {"modulo": "2", "numero": "61", "questao": "Dirigir sob efeito de medicamentos que causam sonolência é:", "alternativas": {"A": "Perigoso e pode ser infração.", "B": "Permitido sempre.", "C": "Recomendado.", "D": "Indiferente."}, "resposta": "A", "comentario": "Medicamentos que afetam a atenção prejudicam a direção segura."},
    {"modulo": "2", "numero": "62", "questao": "O que fazer em caso de sono ao volante?", "alternativas": {"A": "Parar o veículo em local seguro e descansar.", "B": "Tomar café e continuar.", "C": "Ligar o som alto.", "D": "Abrir o vidro e continuar."}, "resposta": "A", "comentario": "O único remédio eficaz contra o sono é parar e descansar."},
    {"modulo": "2", "numero": "63", "questao": "Qual o principal fator de risco em cruzamentos?", "alternativas": {"A": "Não respeitar a sinalização e a preferência.", "B": "Andar devagar demais.", "C": "Usar o cinto.", "D": "Manter distância."}, "resposta": "A", "comentario": "Desrespeitar regras em cruzamentos causa colisões laterais."},
    {"modulo": "2", "numero": "64", "questao": "Em um cruzamento sem sinalização, quem tem preferência?", "alternativas": {"A": "Quem vem pela direita.", "B": "Quem vem pela esquerda.", "C": "Quem chega primeiro.", "D": "Quem buzina primeiro."}, "resposta": "A", "comentario": "A regra geral é dar preferência a quem vem pela direita."},
    {"modulo": "2", "numero": "65", "questao": "O que é colisão frontal?", "alternativas": {"A": "Choque entre veículos que vêm em sentidos opostos.", "B": "Batida na traseira.", "C": "Colisão lateral.", "D": "Capotamento."}, "resposta": "A", "comentario": "Colisões frontais são as mais graves devido à soma das velocidades."},
    {"modulo": "2", "numero": "66", "questao": "Como evitar colisões frontais?", "alternativas": {"A": "Não ultrapassar em locais proibidos.", "B": "Dirigir na contramão.", "C": "Ignorar a sinalização.", "D": "Ultrapassar em curvas."}, "resposta": "A", "comentario": "Respeitar as regras de ultrapassagem previne colisões frontais."},
    {"modulo": "2", "numero": "67", "questao": "O que é colisão traseira?", "alternativas": {"A": "Quando um veículo bate na traseira de outro.", "B": "Batida frontal.", "C": "Colisão lateral.", "D": "Capotamento."}, "resposta": "A", "comentario": "Colisões traseiras geralmente ocorrem por falta de atenção ou distância."},
    {"modulo": "2", "numero": "68", "questao": "Como evitar colisões traseiras?", "alternativas": {"A": "Manter distância segura e atenção.", "B": "Andar colado ao veículo da frente.", "C": "Frear bruscamente sem aviso.", "D": "Não usar luzes de freio."}, "resposta": "A", "comentario": "Distância e atenção são essenciais para evitar bater na traseira."},
    {"modulo": "2", "numero": "69", "questao": "O que é capotamento?", "alternativas": {"A": "Quando o veículo vira de cabeça para baixo.", "B": "Colisão frontal.", "C": "Colisão traseira.", "D": "Atropelamento."}, "resposta": "A", "comentario": "Capotamentos são graves e geralmente causados por excesso de velocidade em curvas."},
    {"modulo": "2", "numero": "70", "questao": "Como evitar capotamentos?", "alternativas": {"A": "Reduzir velocidade em curvas e manter pneus em bom estado.", "B": "Acelerar nas curvas.", "C": "Usar pneus carecas.", "D": "Ignorar lombadas."}, "resposta": "A", "comentario": "Velocidade adequada e pneus bons mantêm a estabilidade."},
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
