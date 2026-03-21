#!/usr/bin/env python3
"""
Script to add more Module 3 questions (341-500)
"""

import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

NEW_QUESTIONS = [
    # MÓDULO 3 (341-500)
    {"modulo": "3", "numero": "341", "questao": "Qual o limite de película nos vidros dianteiros?", "alternativas": {"A": "75% de transparência mínima.", "B": "50%.", "C": "100% escuro.", "D": "Sem limite."}, "resposta": "A", "comentario": "Vidros dianteiros devem permitir visibilidade."},
    {"modulo": "3", "numero": "342", "questao": "Pode usar película escura nos vidros traseiros?", "alternativas": {"A": "Sim, sem restrição.", "B": "Não.", "C": "Apenas 50%.", "D": "Apenas com laudo."}, "resposta": "A", "comentario": "Traseiros não têm restrição."},
    {"modulo": "3", "numero": "343", "questao": "O que é película espelhada?", "alternativas": {"A": "Película que reflete como espelho.", "B": "Película transparente.", "C": "Película decorativa.", "D": "Película de proteção."}, "resposta": "A", "comentario": "Proibida em todos os vidros."},
    {"modulo": "3", "numero": "344", "questao": "É permitida película espelhada?", "alternativas": {"A": "Não, proibida em qualquer vidro.", "B": "Sim.", "C": "Apenas atrás.", "D": "Apenas na frente."}, "resposta": "A", "comentario": "Infração grave."},
    {"modulo": "3", "numero": "345", "questao": "O que é farol de milha?", "alternativas": {"A": "Farol auxiliar de longo alcance.", "B": "Farol baixo.", "C": "Lanterna.", "D": "Pisca."}, "resposta": "A", "comentario": "Para uso em rodovias escuras."},
    {"modulo": "3", "numero": "346", "questao": "Quando usar farol de milha?", "alternativas": {"A": "Em rodovias escuras sem veículos no sentido contrário.", "B": "Sempre.", "C": "Na cidade.", "D": "Em dias claros."}, "resposta": "A", "comentario": "Evitar ofuscamento."},
    {"modulo": "3", "numero": "347", "questao": "O que é farol de neblina?", "alternativas": {"A": "Farol baixo com feixe amplo para neblina.", "B": "Farol alto.", "C": "Lanterna.", "D": "Pisca-alerta."}, "resposta": "A", "comentario": "Luz amarela ou branca, baixa."},
    {"modulo": "3", "numero": "348", "questao": "Quando usar farol de neblina?", "alternativas": {"A": "Apenas em condições de neblina ou chuva forte.", "B": "Sempre.", "C": "À noite.", "D": "Na cidade."}, "resposta": "A", "comentario": "Uso específico para visibilidade reduzida."},
    {"modulo": "3", "numero": "349", "questao": "É infração usar farol de neblina sem necessidade?", "alternativas": {"A": "Sim.", "B": "Não.", "C": "Depende.", "D": "Apenas em rodovias."}, "resposta": "A", "comentario": "Pode ofuscar outros motoristas."},
    {"modulo": "3", "numero": "350", "questao": "O que é luz de advertência (pisca-alerta)?", "alternativas": {"A": "Acionamento simultâneo dos piscas.", "B": "Farol alto.", "C": "Luz de ré.", "D": "Luz de freio."}, "resposta": "A", "comentario": "Para emergências e imobilização."},
    {"modulo": "3", "numero": "351", "questao": "Quando usar pisca-alerta?", "alternativas": {"A": "Emergência, imobilização, veículo lento.", "B": "Para estacionar em fila dupla.", "C": "Para ultrapassar.", "D": "Na chuva."}, "resposta": "A", "comentario": "Não justifica infrações."},
    {"modulo": "3", "numero": "352", "questao": "Usar pisca-alerta autoriza estacionar irregularmente?", "alternativas": {"A": "Não.", "B": "Sim.", "C": "Por 5 minutos.", "D": "Para desembarque."}, "resposta": "A", "comentario": "Não é salvo-conduto."},
    {"modulo": "3", "numero": "353", "questao": "O que é luz de ré?", "alternativas": {"A": "Luz branca que acende ao engatar marcha à ré.", "B": "Luz de freio.", "C": "Pisca.", "D": "Farol."}, "resposta": "A", "comentario": "Avisa que veículo vai recuar."},
    {"modulo": "3", "numero": "354", "questao": "O que é luz de freio?", "alternativas": {"A": "Luz vermelha que acende ao frear.", "B": "Pisca.", "C": "Luz de ré.", "D": "Farol."}, "resposta": "A", "comentario": "Avisa veículos atrás."},
    {"modulo": "3", "numero": "355", "questao": "É infração circular com luz de freio queimada?", "alternativas": {"A": "Sim, infração média.", "B": "Não.", "C": "Apenas em rodovias.", "D": "Advertência."}, "resposta": "A", "comentario": "Equipamento obrigatório."},
    {"modulo": "3", "numero": "356", "questao": "O que é terceira luz de freio?", "alternativas": {"A": "Luz de freio adicional no centro, geralmente no vidro traseiro.", "B": "Luz de ré.", "C": "Pisca.", "D": "Farol."}, "resposta": "A", "comentario": "Obrigatória em veículos novos."},
    {"modulo": "3", "numero": "357", "questao": "O que são lanternas?", "alternativas": {"A": "Luzes de posição dianteiras e traseiras.", "B": "Faróis.", "C": "Piscas.", "D": "Luz de freio."}, "resposta": "A", "comentario": "Indicam presença do veículo."},
    {"modulo": "3", "numero": "358", "questao": "Quando usar lanternas?", "alternativas": {"A": "À noite e em condições de baixa visibilidade.", "B": "Nunca.", "C": "Apenas de dia.", "D": "Apenas na cidade."}, "resposta": "A", "comentario": "Tornam veículo visível."},
    {"modulo": "3", "numero": "359", "questao": "O que são retrovisores?", "alternativas": {"A": "Espelhos para ver atrás e laterais.", "B": "Vidros.", "C": "Painéis.", "D": "Para-brisas."}, "resposta": "A", "comentario": "Equipamento obrigatório."},
    {"modulo": "3", "numero": "360", "questao": "Quantos retrovisores são obrigatórios?", "alternativas": {"A": "No mínimo dois: interno e externo esquerdo.", "B": "Apenas um.", "C": "Três.", "D": "Nenhum."}, "resposta": "A", "comentario": "Externo direito é obrigatório em novos."},
    {"modulo": "3", "numero": "361", "questao": "É infração circular sem retrovisor?", "alternativas": {"A": "Sim, infração grave.", "B": "Não.", "C": "Apenas advertência.", "D": "Infração leve."}, "resposta": "A", "comentario": "Compromete segurança."},
    {"modulo": "3", "numero": "362", "questao": "O que é para-brisa?", "alternativas": {"A": "Vidro dianteiro do veículo.", "B": "Vidro traseiro.", "C": "Retrovisor.", "D": "Lanterna."}, "resposta": "A", "comentario": "Proteção contra vento e objetos."},
    {"modulo": "3", "numero": "363", "questao": "É infração circular com para-brisa trincado?", "alternativas": {"A": "Sim, se comprometer visibilidade.", "B": "Não.", "C": "Apenas em vistoria.", "D": "Depende do tamanho."}, "resposta": "A", "comentario": "Deve estar em bom estado."},
    {"modulo": "3", "numero": "364", "questao": "O que são limpadores de para-brisa?", "alternativas": {"A": "Dispositivo para limpar água e sujeira do vidro.", "B": "Produto de limpeza.", "C": "Pano.", "D": "Esponja."}, "resposta": "A", "comentario": "Equipamento obrigatório."},
    {"modulo": "3", "numero": "365", "questao": "É infração circular sem limpador funcionando?", "alternativas": {"A": "Sim.", "B": "Não.", "C": "Apenas em dias de chuva.", "D": "Advertência."}, "resposta": "A", "comentario": "Equipamento de segurança."},
    {"modulo": "3", "numero": "366", "questao": "O que é buzina?", "alternativas": {"A": "Dispositivo sonoro de alerta.", "B": "Alarme.", "C": "Rádio.", "D": "Sirene."}, "resposta": "A", "comentario": "Equipamento obrigatório."},
    {"modulo": "3", "numero": "367", "questao": "Quando usar buzina?", "alternativas": {"A": "Apenas para alertar sobre perigo iminente.", "B": "Para cumprimentar.", "C": "Para reclamar.", "D": "Para acelerar trânsito."}, "resposta": "A", "comentario": "Uso deve ser moderado."},
    {"modulo": "3", "numero": "368", "questao": "É infração usar buzina prolongadamente?", "alternativas": {"A": "Sim.", "B": "Não.", "C": "Depende do local.", "D": "Apenas à noite."}, "resposta": "A", "comentario": "Perturbação do sossego."},
    {"modulo": "3", "numero": "369", "questao": "É proibido buzinar em quais locais?", "alternativas": {"A": "Hospitais, escolas, bibliotecas.", "B": "Rodovias.", "C": "Estacionamentos.", "D": "Postos."}, "resposta": "A", "comentario": "Áreas sensíveis ao ruído."},
    {"modulo": "3", "numero": "370", "questao": "O que é freio de serviço?", "alternativas": {"A": "Freio principal acionado pelo pedal.", "B": "Freio de mão.", "C": "Freio motor.", "D": "ABS."}, "resposta": "A", "comentario": "Sistema principal de frenagem."},
    {"modulo": "3", "numero": "371", "questao": "O que é freio de estacionamento?", "alternativas": {"A": "Freio de mão ou pedal para manter veículo parado.", "B": "Freio principal.", "C": "Freio ABS.", "D": "Freio motor."}, "resposta": "A", "comentario": "Para uso com veículo parado."},
    {"modulo": "3", "numero": "372", "questao": "É obrigatório usar freio de estacionamento ao parar?", "alternativas": {"A": "Sim, em paradas e estacionamentos.", "B": "Não.", "C": "Apenas em aclives.", "D": "Apenas em declives."}, "resposta": "A", "comentario": "Evita que veículo se mova."},
    {"modulo": "3", "numero": "373", "questao": "O que é freio ABS?", "alternativas": {"A": "Sistema que evita travamento das rodas.", "B": "Freio de mão.", "C": "Freio motor.", "D": "Freio a disco."}, "resposta": "A", "comentario": "Anti-lock Braking System."},
    {"modulo": "3", "numero": "374", "questao": "Qual a vantagem do freio ABS?", "alternativas": {"A": "Mantém controle da direção durante frenagem.", "B": "Freia mais rápido.", "C": "Economiza combustível.", "D": "Reduz desgaste."}, "resposta": "A", "comentario": "Permite desviar enquanto freia."},
    {"modulo": "3", "numero": "375", "questao": "O que fazer em frenagem com ABS?", "alternativas": {"A": "Pisar firme e manter pressão.", "B": "Bombear o pedal.", "C": "Usar freio de mão.", "D": "Tirar o pé."}, "resposta": "A", "comentario": "Sistema pulsa automaticamente."},
    {"modulo": "3", "numero": "376", "questao": "O que é airbag?", "alternativas": {"A": "Bolsa inflável de proteção em colisões.", "B": "Cinto de segurança.", "C": "Encosto de cabeça.", "D": "Amortecedor."}, "resposta": "A", "comentario": "Equipamento de segurança passiva."},
    {"modulo": "3", "numero": "377", "questao": "O airbag substitui o cinto de segurança?", "alternativas": {"A": "Não, são complementares.", "B": "Sim.", "C": "Em baixa velocidade.", "D": "Em cidade."}, "resposta": "A", "comentario": "Cinto é obrigatório mesmo com airbag."},
    {"modulo": "3", "numero": "378", "questao": "O que é encosto de cabeça?", "alternativas": {"A": "Dispositivo que protege cervical em colisões traseiras.", "B": "Travesseiro.", "C": "Almofada.", "D": "Apoio de braço."}, "resposta": "A", "comentario": "Equipamento de segurança."},
    {"modulo": "3", "numero": "379", "questao": "Como ajustar o encosto de cabeça?", "alternativas": {"A": "Altura na linha dos olhos ou topo da cabeça.", "B": "O mais baixo possível.", "C": "Removê-lo.", "D": "Não importa."}, "resposta": "A", "comentario": "Ajuste correto protege pescoço."},
    {"modulo": "3", "numero": "380", "questao": "O que é extintor de incêndio veicular?", "alternativas": {"A": "Equipamento para combater princípio de incêndio.", "B": "Alarme.", "C": "Kit de primeiros socorros.", "D": "Triângulo."}, "resposta": "A", "comentario": "Era obrigatório, hoje dispensado para carros."},
    {"modulo": "3", "numero": "381", "questao": "Extintor ainda é obrigatório em carros de passeio?", "alternativas": {"A": "Não, foi dispensado.", "B": "Sim.", "C": "Apenas para táxis.", "D": "Apenas para ônibus."}, "resposta": "A", "comentario": "Resolução CONTRAN dispensou."},
    {"modulo": "3", "numero": "382", "questao": "Extintor é obrigatório em ônibus e caminhões?", "alternativas": {"A": "Sim.", "B": "Não.", "C": "Apenas para cargas perigosas.", "D": "Depende do estado."}, "resposta": "A", "comentario": "Veículos de transporte ainda exigem."},
    {"modulo": "3", "numero": "383", "questao": "O que é triângulo de sinalização?", "alternativas": {"A": "Dispositivo refletivo para sinalizar emergência.", "B": "Extintor.", "C": "Macaco.", "D": "Chave de roda."}, "resposta": "A", "comentario": "Obrigatório em todos os veículos."},
    {"modulo": "3", "numero": "384", "questao": "A que distância colocar o triângulo?", "alternativas": {"A": "30m em área urbana, 60m ou mais em rodovias.", "B": "5 metros.", "C": "100 metros sempre.", "D": "Junto ao veículo."}, "resposta": "A", "comentario": "Distância para ser visto a tempo."},
    {"modulo": "3", "numero": "385", "questao": "O que é macaco veicular?", "alternativas": {"A": "Equipamento para levantar veículo.", "B": "Triângulo.", "C": "Extintor.", "D": "Estepe."}, "resposta": "A", "comentario": "Para troca de pneu."},
    {"modulo": "3", "numero": "386", "questao": "O que é estepe?", "alternativas": {"A": "Pneu reserva.", "B": "Macaco.", "C": "Chave de roda.", "D": "Triângulo."}, "resposta": "A", "comentario": "Equipamento obrigatório."},
    {"modulo": "3", "numero": "387", "questao": "Estepe deve estar calibrado?", "alternativas": {"A": "Sim, verificar periodicamente.", "B": "Não.", "C": "Apenas quando usar.", "D": "Depende."}, "resposta": "A", "comentario": "Deve estar pronto para uso."},
    {"modulo": "3", "numero": "388", "questao": "O que é chave de roda?", "alternativas": {"A": "Ferramenta para remover parafusos da roda.", "B": "Chave do carro.", "C": "Macaco.", "D": "Triângulo."}, "resposta": "A", "comentario": "Necessária para trocar pneu."},
    {"modulo": "3", "numero": "389", "questao": "O que é cinto de segurança de três pontos?", "alternativas": {"A": "Cinto que prende ombro, peito e quadril.", "B": "Apenas cinto abdominal.", "C": "Cinto de criança.", "D": "Airbag."}, "resposta": "A", "comentario": "Padrão em veículos modernos."},
    {"modulo": "3", "numero": "390", "questao": "É infração usar cinto de forma incorreta?", "alternativas": {"A": "Sim.", "B": "Não.", "C": "Apenas se causar acidente.", "D": "Advertência."}, "resposta": "A", "comentario": "Deve estar ajustado corretamente."},
    {"modulo": "3", "numero": "391", "questao": "O que é cadeirinha infantil?", "alternativas": {"A": "Dispositivo de retenção para crianças.", "B": "Banco comum.", "C": "Assento de elevação.", "D": "Bebê conforto."}, "resposta": "A", "comentario": "Obrigatória por idade/peso."},
    {"modulo": "3", "numero": "392", "questao": "O que é bebê conforto?", "alternativas": {"A": "Cadeirinha para bebês de até 1 ano.", "B": "Cadeirinha para crianças maiores.", "C": "Assento de elevação.", "D": "Cinto especial."}, "resposta": "A", "comentario": "Deve ficar de costas para o movimento."},
    {"modulo": "3", "numero": "393", "questao": "O que é assento de elevação (booster)?", "alternativas": {"A": "Eleva criança para usar cinto de adulto.", "B": "Bebê conforto.", "C": "Cadeirinha.", "D": "Banco especial."}, "resposta": "A", "comentario": "Para crianças de 4 a 7,5 anos."},
    {"modulo": "3", "numero": "394", "questao": "Até que idade é obrigatório dispositivo de retenção?", "alternativas": {"A": "7 anos e meio.", "B": "5 anos.", "C": "10 anos.", "D": "12 anos."}, "resposta": "A", "comentario": "Depois, apenas banco traseiro com cinto."},
    {"modulo": "3", "numero": "395", "questao": "Com quantos anos criança pode ir no banco da frente?", "alternativas": {"A": "10 anos.", "B": "5 anos.", "C": "7 anos.", "D": "12 anos."}, "resposta": "A", "comentario": "Antes disso, apenas atrás."},
    {"modulo": "3", "numero": "396", "questao": "O que é ISOFIX?", "alternativas": {"A": "Sistema de fixação de cadeirinha no veículo.", "B": "Tipo de cinto.", "C": "Marca de cadeirinha.", "D": "Airbag infantil."}, "resposta": "A", "comentario": "Fixação mais segura."},
    {"modulo": "3", "numero": "397", "questao": "O que é velocímetro?", "alternativas": {"A": "Instrumento que indica velocidade.", "B": "Conta-giros.", "C": "Odômetro.", "D": "Tacômetro."}, "resposta": "A", "comentario": "Equipamento obrigatório."},
    {"modulo": "3", "numero": "398", "questao": "O que é odômetro?", "alternativas": {"A": "Instrumento que conta quilometragem.", "B": "Velocímetro.", "C": "Conta-giros.", "D": "Tacógrafo."}, "resposta": "A", "comentario": "Marca distância percorrida."},
    {"modulo": "3", "numero": "399", "questao": "É crime adulterar odômetro?", "alternativas": {"A": "Sim, fraude.", "B": "Não.", "C": "Apenas infração.", "D": "Depende."}, "resposta": "A", "comentario": "Crime previsto em lei."},
    {"modulo": "3", "numero": "400", "questao": "O que é conta-giros?", "alternativas": {"A": "Instrumento que indica rotação do motor.", "B": "Velocímetro.", "C": "Odômetro.", "D": "Tacógrafo."}, "resposta": "A", "comentario": "Ajuda na economia de combustível."},
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
