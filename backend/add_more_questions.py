#!/usr/bin/env python3
"""
Script to add more questions - Module 1 (remaining) and Module 3
"""

import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

NEW_QUESTIONS = [
    # Completando MÓDULO 1 (331-371)
    {"modulo": "1", "numero": "331", "questao": "O que indica uma placa verde com nome de cidade e distância?", "alternativas": {"A": "Direção e distância até a cidade indicada.", "B": "Velocidade máxima.", "C": "Proibição de entrada.", "D": "Área de pedágio."}, "resposta": "A", "comentario": "Placas verdes orientam sobre destinos."},
    {"modulo": "1", "numero": "332", "questao": "O que indica uma placa azul com símbolo de avião?", "alternativas": {"A": "Aeroporto nas proximidades.", "B": "Zona de voo proibido.", "C": "Heliponto.", "D": "Base militar."}, "resposta": "A", "comentario": "Indica acesso a aeroporto."},
    {"modulo": "1", "numero": "333", "questao": "O que indica uma placa marrom com símbolo de ruínas?", "alternativas": {"A": "Sítio arqueológico ou histórico.", "B": "Área de demolição.", "C": "Zona de perigo.", "D": "Construção abandonada."}, "resposta": "A", "comentario": "Placas marrons indicam atrativos turísticos."},
    {"modulo": "1", "numero": "334", "questao": "O que é placa de identificação de rodovia?", "alternativas": {"A": "Placa que mostra o número e nome da rodovia.", "B": "Placa de velocidade.", "C": "Placa de proibição.", "D": "Placa de advertência."}, "resposta": "A", "comentario": "Ex: BR-101, SP-330."},
    {"modulo": "1", "numero": "335", "questao": "O que indica a placa de marco quilométrico?", "alternativas": {"A": "A distância percorrida desde o início da rodovia.", "B": "Velocidade máxima.", "C": "Proibição.", "D": "Pedágio próximo."}, "resposta": "A", "comentario": "Ajuda na localização em rodovias."},
    {"modulo": "1", "numero": "336", "questao": "O que é placa de serviços auxiliares?", "alternativas": {"A": "Indica serviços disponíveis como posto, hospital, telefone.", "B": "Indica proibições.", "C": "Indica velocidade.", "D": "Indica destinos."}, "resposta": "A", "comentario": "Fundo azul com símbolos de serviços."},
    {"modulo": "1", "numero": "337", "questao": "O que significa placa com símbolo de chave inglesa?", "alternativas": {"A": "Oficina mecânica próxima.", "B": "Ferramentas à venda.", "C": "Proibido parar.", "D": "Área industrial."}, "resposta": "A", "comentario": "Indica serviço de mecânica."},
    {"modulo": "1", "numero": "338", "questao": "O que indica placa com símbolo de mala?", "alternativas": {"A": "Hotel ou hospedagem.", "B": "Loja de malas.", "C": "Guarda-volumes.", "D": "Aeroporto."}, "resposta": "A", "comentario": "Indica local de hospedagem."},
    {"modulo": "1", "numero": "339", "questao": "Qual a cor das placas de obras?", "alternativas": {"A": "Laranja.", "B": "Amarela.", "C": "Verde.", "D": "Azul."}, "resposta": "A", "comentario": "Laranja indica sinalização temporária de obras."},
    {"modulo": "1", "numero": "340", "questao": "O que indica uma placa laranja?", "alternativas": {"A": "Obra ou situação temporária na via.", "B": "Perigo permanente.", "C": "Serviço de emergência.", "D": "Área de lazer."}, "resposta": "A", "comentario": "Placas laranjas são temporárias."},
    {"modulo": "1", "numero": "341", "questao": "O que fazer ao ver placas de obras?", "alternativas": {"A": "Reduzir velocidade e seguir as orientações.", "B": "Acelerar para passar rápido.", "C": "Ignorar.", "D": "Buzinar."}, "resposta": "A", "comentario": "Obras exigem atenção redobrada."},
    {"modulo": "1", "numero": "342", "questao": "O que indica placa com operário trabalhando?", "alternativas": {"A": "Obras na pista.", "B": "Área de pedestres.", "C": "Escola próxima.", "D": "Fábrica."}, "resposta": "A", "comentario": "Alerta para presença de trabalhadores."},
    {"modulo": "1", "numero": "343", "questao": "O que indica placa de desvio?", "alternativas": {"A": "Caminho alternativo devido a bloqueio.", "B": "Atalho mais rápido.", "C": "Via preferencial.", "D": "Retorno obrigatório."}, "resposta": "A", "comentario": "Indica rota alternativa temporária."},
    {"modulo": "1", "numero": "344", "questao": "O que é sinalização de canalização em obras?", "alternativas": {"A": "Cones, cavaletes e balizadores que direcionam o fluxo.", "B": "Placas de velocidade.", "C": "Semáforos.", "D": "Faixas de pedestres."}, "resposta": "A", "comentario": "Dispositivos auxiliares organizam o tráfego."},
    {"modulo": "1", "numero": "345", "questao": "O que são balizadores?", "alternativas": {"A": "Dispositivos para delimitar áreas e orientar o fluxo.", "B": "Tipo de placa.", "C": "Semáforos portáteis.", "D": "Radares móveis."}, "resposta": "A", "comentario": "Usados em obras e eventos."},
    {"modulo": "1", "numero": "346", "questao": "O que são cavaletes de sinalização?", "alternativas": {"A": "Suportes para placas temporárias.", "B": "Animais na pista.", "C": "Tipo de veículo.", "D": "Equipamento de resgate."}, "resposta": "A", "comentario": "Sustentam placas de obras."},
    {"modulo": "1", "numero": "347", "questao": "O que indica cone de sinalização?", "alternativas": {"A": "Área interditada ou em obras.", "B": "Estacionamento liberado.", "C": "Velocidade alta.", "D": "Via preferencial."}, "resposta": "A", "comentario": "Cones delimitam áreas de risco."},
    {"modulo": "1", "numero": "348", "questao": "O que é faixa refletiva?", "alternativas": {"A": "Faixa que reflete luz para aumentar visibilidade.", "B": "Faixa de pedestres.", "C": "Faixa de ônibus.", "D": "Linha de bordo."}, "resposta": "A", "comentario": "Melhora visibilidade noturna."},
    {"modulo": "1", "numero": "349", "questao": "Por que a sinalização noturna é diferente?", "alternativas": {"A": "Usa materiais refletivos para compensar a baixa luz.", "B": "É mais colorida.", "C": "Não há diferença.", "D": "É menor."}, "resposta": "A", "comentario": "Refletividade é essencial à noite."},
    {"modulo": "1", "numero": "350", "questao": "O que são tachas refletivas?", "alternativas": {"A": "Dispositivos no pavimento que refletem luz.", "B": "Tipo de pneu.", "C": "Marca de veículo.", "D": "Equipamento de som."}, "resposta": "A", "comentario": "Conhecidas como olhos de gato."},
    {"modulo": "1", "numero": "351", "questao": "Qual a função das tachas refletivas?", "alternativas": {"A": "Delimitar faixas e orientar à noite.", "B": "Decorar a via.", "C": "Reduzir velocidade.", "D": "Indicar pedágio."}, "resposta": "A", "comentario": "Auxiliam na orientação noturna."},
    {"modulo": "1", "numero": "352", "questao": "O que é tachão?", "alternativas": {"A": "Tacha maior usada para separar fluxos.", "B": "Tipo de placa.", "C": "Radar.", "D": "Lombada."}, "resposta": "A", "comentario": "Mais alto que tachas comuns."},
    {"modulo": "1", "numero": "353", "questao": "O que é sonorizador?", "alternativas": {"A": "Faixas no pavimento que fazem barulho ao passar.", "B": "Equipamento de som.", "C": "Tipo de buzina.", "D": "Alarme de carro."}, "resposta": "A", "comentario": "Alerta o motorista desatento."},
    {"modulo": "1", "numero": "354", "questao": "Onde são instalados sonorizadores?", "alternativas": {"A": "Antes de pedágios, curvas perigosas e lombadas.", "B": "Em estacionamentos.", "C": "Em postos de gasolina.", "D": "Em shoppings."}, "resposta": "A", "comentario": "Alertam sobre necessidade de reduzir."},
    {"modulo": "1", "numero": "355", "questao": "O que é guard-rail?", "alternativas": {"A": "Barreira metálica de proteção nas laterais da via.", "B": "Tipo de placa.", "C": "Radar de velocidade.", "D": "Faixa de pedestres."}, "resposta": "A", "comentario": "Protege contra saídas de pista."},
    {"modulo": "1", "numero": "356", "questao": "Qual a função do guard-rail?", "alternativas": {"A": "Absorver impacto e evitar que veículos saiam da pista.", "B": "Decorar a rodovia.", "C": "Indicar velocidade.", "D": "Separar faixas."}, "resposta": "A", "comentario": "Equipamento de segurança passiva."},
    {"modulo": "1", "numero": "357", "questao": "O que é defensa metálica?", "alternativas": {"A": "Outro nome para guard-rail.", "B": "Tipo de placa.", "C": "Semáforo.", "D": "Lombada."}, "resposta": "A", "comentario": "Mesmo equipamento, nomes diferentes."},
    {"modulo": "1", "numero": "358", "questao": "O que é barreira de concreto (New Jersey)?", "alternativas": {"A": "Divisória de concreto entre pistas.", "B": "Tipo de placa.", "C": "Lombada alta.", "D": "Faixa de pedestres."}, "resposta": "A", "comentario": "Separa fluxos opostos em rodovias."},
    {"modulo": "1", "numero": "359", "questao": "Qual a vantagem da barreira New Jersey?", "alternativas": {"A": "Impede invasão de faixa contrária em colisões.", "B": "É mais bonita.", "C": "É mais barata.", "D": "Facilita ultrapassagem."}, "resposta": "A", "comentario": "Reduz gravidade de acidentes."},
    {"modulo": "1", "numero": "360", "questao": "O que é atenuador de impacto?", "alternativas": {"A": "Dispositivo que absorve energia em colisões.", "B": "Tipo de pneu.", "C": "Amortecedor do carro.", "D": "Freio ABS."}, "resposta": "A", "comentario": "Instalado em pontos de risco como pilares."},
    {"modulo": "1", "numero": "361", "questao": "O que indica placa de área escolar?", "alternativas": {"A": "Proximidade de escola, exigindo atenção.", "B": "Proibido crianças.", "C": "Velocidade alta permitida.", "D": "Estacionamento de ônibus."}, "resposta": "A", "comentario": "Crianças podem atravessar."},
    {"modulo": "1", "numero": "362", "questao": "Qual a velocidade em área escolar?", "alternativas": {"A": "Reduzida, geralmente 30 km/h ou menos.", "B": "60 km/h.", "C": "80 km/h.", "D": "Não há limite."}, "resposta": "A", "comentario": "Proteção às crianças é prioridade."},
    {"modulo": "1", "numero": "363", "questao": "O que indica placa de hospital?", "alternativas": {"A": "Proximidade de hospital, silêncio necessário.", "B": "Estacionamento de ambulâncias.", "C": "Velocidade alta.", "D": "Área de obras."}, "resposta": "A", "comentario": "Evitar buzina e barulho."},
    {"modulo": "1", "numero": "364", "questao": "Por que é proibido buzinar perto de hospitais?", "alternativas": {"A": "Para não perturbar pacientes.", "B": "Porque não há necessidade.", "C": "Porque é área de pedágio.", "D": "Porque não há carros."}, "resposta": "A", "comentario": "Silêncio ajuda na recuperação."},
    {"modulo": "1", "numero": "365", "questao": "O que indica placa de área de lazer?", "alternativas": {"A": "Parque ou área recreativa próxima.", "B": "Shopping.", "C": "Rodovia.", "D": "Área industrial."}, "resposta": "A", "comentario": "Atenção a pedestres e ciclistas."},
    {"modulo": "1", "numero": "366", "questao": "O que indica placa de ciclistas?", "alternativas": {"A": "Possível presença de ciclistas na via.", "B": "Proibido bicicletas.", "C": "Loja de bicicletas.", "D": "Oficina de bikes."}, "resposta": "A", "comentario": "Motoristas devem dar espaço."},
    {"modulo": "1", "numero": "367", "questao": "Qual distância mínima ao ultrapassar ciclista?", "alternativas": {"A": "1,5 metro.", "B": "50 centímetros.", "C": "3 metros.", "D": "Não há distância mínima."}, "resposta": "A", "comentario": "Proteção ao ciclista mais vulnerável."},
    {"modulo": "1", "numero": "368", "questao": "O que indica placa de veículos lentos?", "alternativas": {"A": "Possível presença de veículos de baixa velocidade.", "B": "Proibido veículos lentos.", "C": "Via expressa.", "D": "Aceleração obrigatória."}, "resposta": "A", "comentario": "Tratores, carroças podem estar na via."},
    {"modulo": "1", "numero": "369", "questao": "O que indica placa de animais silvestres?", "alternativas": {"A": "Possível travessia de animais silvestres.", "B": "Zoológico.", "C": "Caça permitida.", "D": "Fazenda."}, "resposta": "A", "comentario": "Comum em áreas de preservação."},
    
    # Mais questões do MÓDULO 3 (101-180)
    {"modulo": "3", "numero": "101", "questao": "O que é inspeção veicular?", "alternativas": {"A": "Verificação das condições de segurança do veículo.", "B": "Vistoria policial.", "C": "Lavagem do carro.", "D": "Abastecimento."}, "resposta": "A", "comentario": "Obrigatória em alguns estados."},
    {"modulo": "3", "numero": "102", "questao": "O que é vistoria do DETRAN?", "alternativas": {"A": "Verificação de itens de segurança e identificação do veículo.", "B": "Teste de direção.", "C": "Prova teórica.", "D": "Renovação da CNH."}, "resposta": "A", "comentario": "Necessária para transferência e outras situações."},
    {"modulo": "3", "numero": "103", "questao": "Quando é obrigatória a vistoria?", "alternativas": {"A": "Transferência, mudança de município, alteração de característica.", "B": "Apenas na compra.", "C": "Nunca.", "D": "Apenas para caminhões."}, "resposta": "A", "comentario": "Várias situações exigem vistoria."},
    {"modulo": "3", "numero": "104", "questao": "O que acontece se o veículo reprovar na vistoria?", "alternativas": {"A": "Deve ser regularizado e passar por nova vistoria.", "B": "Pode circular normalmente.", "C": "Recebe multa apenas.", "D": "Nada acontece."}, "resposta": "A", "comentario": "Veículo irregular não pode circular."},
    {"modulo": "3", "numero": "105", "questao": "O que é lacre do veículo?", "alternativas": {"A": "Selo que identifica o chassi e o motor.", "B": "Adesivo decorativo.", "C": "Tipo de trava.", "D": "Alarme."}, "resposta": "A", "comentario": "Lacre violado indica possível adulteração."},
    {"modulo": "3", "numero": "106", "questao": "O que acontece se o lacre estiver violado?", "alternativas": {"A": "Veículo pode ser apreendido para verificação.", "B": "Nada.", "C": "Apenas multa.", "D": "Advertência."}, "resposta": "A", "comentario": "Pode indicar clonagem ou roubo."},
    {"modulo": "3", "numero": "107", "questao": "O que é placa Mercosul?", "alternativas": {"A": "Novo padrão de placas adotado no Brasil.", "B": "Placa antiga.", "C": "Placa de outro país.", "D": "Placa temporária."}, "resposta": "A", "comentario": "Padrão unificado da América do Sul."},
    {"modulo": "3", "numero": "108", "questao": "Quais as características da placa Mercosul?", "alternativas": {"A": "4 letras e 3 números, com QR Code.", "B": "3 letras e 4 números.", "C": "Apenas números.", "D": "Apenas letras."}, "resposta": "A", "comentario": "Formato: ABC1D23."},
    {"modulo": "3", "numero": "109", "questao": "É obrigatório trocar para placa Mercosul?", "alternativas": {"A": "Apenas em situações específicas como transferência.", "B": "Sim, para todos.", "C": "Nunca.", "D": "Apenas para motos."}, "resposta": "A", "comentario": "Troca gradual conforme necessidade."},
    {"modulo": "3", "numero": "110", "questao": "O que é comunicação de venda?", "alternativas": {"A": "Informar ao DETRAN que vendeu o veículo.", "B": "Anúncio de venda.", "C": "Contrato de compra.", "D": "Nota fiscal."}, "resposta": "A", "comentario": "Protege o vendedor de multas futuras."},
    {"modulo": "3", "numero": "111", "questao": "Qual o prazo para comunicar venda?", "alternativas": {"A": "30 dias.", "B": "10 dias.", "C": "60 dias.", "D": "1 ano."}, "resposta": "A", "comentario": "Vendedor deve comunicar em 30 dias."},
    {"modulo": "3", "numero": "112", "questao": "O que acontece se não comunicar a venda?", "alternativas": {"A": "Vendedor continua responsável por multas e impostos.", "B": "Nada.", "C": "Comprador é penalizado.", "D": "Veículo é apreendido."}, "resposta": "A", "comentario": "Comunicação protege o vendedor."},
    {"modulo": "3", "numero": "113", "questao": "Qual o prazo para transferir veículo?", "alternativas": {"A": "30 dias.", "B": "10 dias.", "C": "60 dias.", "D": "1 ano."}, "resposta": "A", "comentario": "Comprador deve transferir em 30 dias."},
    {"modulo": "3", "numero": "114", "questao": "O que acontece se não transferir no prazo?", "alternativas": {"A": "Multa e veículo pode ser apreendido.", "B": "Nada.", "C": "Apenas advertência.", "D": "Desconto no IPVA."}, "resposta": "A", "comentario": "Transferência é obrigatória."},
    {"modulo": "3", "numero": "115", "questao": "O que é baixa do veículo?", "alternativas": {"A": "Retirada do registro quando veículo é sucateado.", "B": "Venda do veículo.", "C": "Transferência.", "D": "Licenciamento."}, "resposta": "A", "comentario": "Veículo deixa de existir legalmente."},
    {"modulo": "3", "numero": "116", "questao": "Quando fazer baixa do veículo?", "alternativas": {"A": "Perda total, sinistro grave, sucateamento.", "B": "Ao vender.", "C": "Todo ano.", "D": "Nunca."}, "resposta": "A", "comentario": "Evita cobranças indevidas."},
    {"modulo": "3", "numero": "117", "questao": "O que é alienação fiduciária?", "alternativas": {"A": "Veículo dado como garantia de financiamento.", "B": "Aluguel de veículo.", "C": "Venda do veículo.", "D": "Doação."}, "resposta": "A", "comentario": "Comum em financiamentos."},
    {"modulo": "3", "numero": "118", "questao": "O que significa veículo alienado?", "alternativas": {"A": "Pertence ao banco até quitação do financiamento.", "B": "Veículo roubado.", "C": "Veículo importado.", "D": "Veículo antigo."}, "resposta": "A", "comentario": "Não pode ser vendido sem quitar."},
    {"modulo": "3", "numero": "119", "questao": "Como remover alienação?", "alternativas": {"A": "Quitar o financiamento e solicitar baixa.", "B": "Não é possível.", "C": "Vender o veículo.", "D": "Ignorar."}, "resposta": "A", "comentario": "Banco libera após quitação."},
    {"modulo": "3", "numero": "120", "questao": "O que é gravame?", "alternativas": {"A": "Registro de restrição financeira no veículo.", "B": "Multa.", "C": "Tipo de placa.", "D": "Modelo de carro."}, "resposta": "A", "comentario": "Aparece na consulta do veículo."},
    {"modulo": "3", "numero": "121", "questao": "O que verificar antes de comprar veículo usado?", "alternativas": {"A": "Débitos, multas, gravames, sinistros, restrições.", "B": "Apenas a cor.", "C": "Apenas o preço.", "D": "Nada especial."}, "resposta": "A", "comentario": "Consulta completa evita problemas."},
    {"modulo": "3", "numero": "122", "questao": "O que é restrição judicial?", "alternativas": {"A": "Bloqueio determinado pela justiça.", "B": "Multa de trânsito.", "C": "IPVA atrasado.", "D": "Licenciamento vencido."}, "resposta": "A", "comentario": "Impede transferência do veículo."},
    {"modulo": "3", "numero": "123", "questao": "O que é restrição administrativa?", "alternativas": {"A": "Bloqueio por débitos ou irregularidades.", "B": "Multa simples.", "C": "Advertência.", "D": "Nada grave."}, "resposta": "A", "comentario": "Deve ser regularizada."},
    {"modulo": "3", "numero": "124", "questao": "O que é bloqueio de circulação?", "alternativas": {"A": "Veículo impedido de transitar.", "B": "Trânsito fechado.", "C": "Rodízio.", "D": "Pedágio."}, "resposta": "A", "comentario": "Por débitos ou irregularidades graves."},
    {"modulo": "3", "numero": "125", "questao": "O que é rodízio de veículos?", "alternativas": {"A": "Restrição de circulação por dia/placa.", "B": "Troca de pneus.", "C": "Revezamento de motoristas.", "D": "Manutenção."}, "resposta": "A", "comentario": "Comum em grandes cidades."},
    {"modulo": "3", "numero": "126", "questao": "Qual a penalidade por desrespeitar rodízio?", "alternativas": {"A": "Multa.", "B": "Apreensão do veículo.", "C": "Suspensão da CNH.", "D": "Nenhuma."}, "resposta": "A", "comentario": "Infração de trânsito."},
    {"modulo": "3", "numero": "127", "questao": "O que é zona azul?", "alternativas": {"A": "Estacionamento rotativo pago.", "B": "Área de lazer.", "C": "Faixa de ônibus.", "D": "Via expressa."}, "resposta": "A", "comentario": "Controla tempo de estacionamento."},
    {"modulo": "3", "numero": "128", "questao": "O que acontece se exceder tempo na zona azul?", "alternativas": {"A": "Multa.", "B": "Apreensão.", "C": "Advertência.", "D": "Nada."}, "resposta": "A", "comentario": "Fiscalização constante."},
    {"modulo": "3", "numero": "129", "questao": "O que é vaga especial?", "alternativas": {"A": "Vaga reservada para idosos, deficientes ou gestantes.", "B": "Vaga maior.", "C": "Vaga coberta.", "D": "Vaga de moto."}, "resposta": "A", "comentario": "Uso exclusivo com credencial."},
    {"modulo": "3", "numero": "130", "questao": "Qual a penalidade por usar vaga especial sem direito?", "alternativas": {"A": "Infração gravíssima.", "B": "Infração leve.", "C": "Advertência.", "D": "Nenhuma."}, "resposta": "A", "comentario": "Respeito às vagas especiais é obrigatório."},
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
        target = {"1": 371, "2": 171, "3": 575, "4": 36}[modulo]
        print(f"Módulo {modulo}: {count}/{target} questões ({count/target*100:.0f}%)")
    
    total = await questions_collection.count_documents({})
    print(f"\nTotal: {total}/1153 questões ({total/1153*100:.1f}%)")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(add_questions())
