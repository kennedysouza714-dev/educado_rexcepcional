#!/usr/bin/env python3
"""
Script to add more Module 3 questions (151-300)
"""

import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

NEW_QUESTIONS = [
    # MÓDULO 3 (151-300)
    {"modulo": "3", "numero": "151", "questao": "É obrigatório usar viseira ou óculos de proteção em moto?", "alternativas": {"A": "Sim.", "B": "Não.", "C": "Apenas à noite.", "D": "Apenas em rodovias."}, "resposta": "A", "comentario": "Proteção dos olhos é obrigatória."},
    {"modulo": "3", "numero": "152", "questao": "É permitido pilotar moto com farol apagado de dia?", "alternativas": {"A": "Não, farol deve estar sempre aceso.", "B": "Sim.", "C": "Apenas em cidade.", "D": "Apenas em rodovias."}, "resposta": "A", "comentario": "Farol aceso aumenta visibilidade."},
    {"modulo": "3", "numero": "153", "questao": "O que é motofrete?", "alternativas": {"A": "Transporte de mercadorias por motocicleta.", "B": "Transporte de passageiros.", "C": "Aluguel de motos.", "D": "Corrida de motos."}, "resposta": "A", "comentario": "Atividade regulamentada."},
    {"modulo": "3", "numero": "154", "questao": "O que é mototáxi?", "alternativas": {"A": "Transporte de passageiros por motocicleta.", "B": "Transporte de cargas.", "C": "Aluguel de motos.", "D": "Escola de pilotagem."}, "resposta": "A", "comentario": "Requer autorização específica."},
    {"modulo": "3", "numero": "155", "questao": "Mototaxista precisa de curso especial?", "alternativas": {"A": "Sim, curso de formação específico.", "B": "Não.", "C": "Apenas experiência.", "D": "Apenas CNH A."}, "resposta": "A", "comentario": "Curso obrigatório para exercer a profissão."},
    {"modulo": "3", "numero": "156", "questao": "É permitido transportar carga em moto acima da capacidade?", "alternativas": {"A": "Não.", "B": "Sim.", "C": "Apenas em cidade.", "D": "Apenas de dia."}, "resposta": "A", "comentario": "Compromete estabilidade e segurança."},
    {"modulo": "3", "numero": "157", "questao": "O que é garupa?", "alternativas": {"A": "Assento traseiro da moto para passageiro.", "B": "Bagageiro.", "C": "Para-lama.", "D": "Escapamento."}, "resposta": "A", "comentario": "Local onde o passageiro se senta."},
    {"modulo": "3", "numero": "158", "questao": "É permitido mais de um passageiro na garupa?", "alternativas": {"A": "Não, apenas um.", "B": "Sim, dois.", "C": "Depende da moto.", "D": "Em rodovias sim."}, "resposta": "A", "comentario": "Moto comporta apenas condutor e um passageiro."},
    {"modulo": "3", "numero": "159", "questao": "O que acontece se transportar passageiro sem capacete?", "alternativas": {"A": "Infração gravíssima para o condutor.", "B": "Apenas advertência.", "C": "Multa para o passageiro.", "D": "Nada."}, "resposta": "A", "comentario": "Condutor é responsável pela segurança."},
    {"modulo": "3", "numero": "160", "questao": "É obrigatório usar colete refletivo em moto?", "alternativas": {"A": "Obrigatório apenas para motofretistas.", "B": "Para todos.", "C": "Nunca.", "D": "Apenas à noite."}, "resposta": "A", "comentario": "Profissionais devem usar colete."},
    {"modulo": "3", "numero": "161", "questao": "O que é antena corta-pipa?", "alternativas": {"A": "Dispositivo de segurança contra linhas cortantes.", "B": "Antena de rádio.", "C": "GPS.", "D": "Alarme."}, "resposta": "A", "comentario": "Protege motociclistas de cerol."},
    {"modulo": "3", "numero": "162", "questao": "É obrigatório antena corta-pipa?", "alternativas": {"A": "Não é obrigatório, mas recomendado.", "B": "Sim, obrigatório.", "C": "Apenas em algumas cidades.", "D": "Proibido."}, "resposta": "A", "comentario": "Equipamento de segurança opcional."},
    {"modulo": "3", "numero": "163", "questao": "O que é triciclo?", "alternativas": {"A": "Veículo de três rodas.", "B": "Bicicleta.", "C": "Moto.", "D": "Quadriciclo."}, "resposta": "A", "comentario": "Pode ser motorizado ou não."},
    {"modulo": "3", "numero": "164", "questao": "Qual CNH para conduzir triciclo motorizado?", "alternativas": {"A": "Categoria A.", "B": "Categoria B.", "C": "Categoria C.", "D": "Não precisa."}, "resposta": "A", "comentario": "Mesma categoria de motocicleta."},
    {"modulo": "3", "numero": "165", "questao": "O que é quadriciclo?", "alternativas": {"A": "Veículo de quatro rodas leve.", "B": "Caminhonete.", "C": "Moto.", "D": "Triciclo."}, "resposta": "A", "comentario": "Comum em áreas rurais e praias."},
    {"modulo": "3", "numero": "166", "questao": "Qual CNH para conduzir quadriciclo?", "alternativas": {"A": "Categoria B.", "B": "Categoria A.", "C": "Categoria C.", "D": "Não precisa."}, "resposta": "A", "comentario": "Considerado veículo automotor de 4 rodas."},
    {"modulo": "3", "numero": "167", "questao": "O que é reboque?", "alternativas": {"A": "Veículo sem motor puxado por outro.", "B": "Guincho.", "C": "Caminhão.", "D": "Carreta."}, "resposta": "A", "comentario": "Depende de outro veículo para se mover."},
    {"modulo": "3", "numero": "168", "questao": "É permitido rebocar veículo com corda?", "alternativas": {"A": "Apenas em emergência e curta distância.", "B": "Sim, sempre.", "C": "Nunca.", "D": "Apenas guincho."}, "resposta": "A", "comentario": "Situação emergencial com cuidados."},
    {"modulo": "3", "numero": "169", "questao": "O que é carreta?", "alternativas": {"A": "Reboque para transporte de cargas.", "B": "Caminhão.", "C": "Ônibus.", "D": "Van."}, "resposta": "A", "comentario": "Acoplada a cavalo mecânico."},
    {"modulo": "3", "numero": "170", "questao": "Qual CNH para conduzir caminhão com carreta?", "alternativas": {"A": "Categoria E.", "B": "Categoria C.", "C": "Categoria D.", "D": "Categoria B."}, "resposta": "A", "comentario": "E para veículos articulados."},
    {"modulo": "3", "numero": "171", "questao": "O que é cavalo mecânico?", "alternativas": {"A": "Parte tratora de um veículo articulado.", "B": "Trator agrícola.", "C": "Caminhão simples.", "D": "Ônibus."}, "resposta": "A", "comentario": "Puxa a carreta ou semirreboque."},
    {"modulo": "3", "numero": "172", "questao": "O que é semirreboque?", "alternativas": {"A": "Reboque que se apoia parcialmente no cavalo mecânico.", "B": "Reboque completo.", "C": "Carroceria.", "D": "Baú."}, "resposta": "A", "comentario": "Diferente do reboque que tem rodas próprias."},
    {"modulo": "3", "numero": "173", "questao": "O que é combinação de veículos?", "alternativas": {"A": "Conjunto de veículo trator e reboque(s).", "B": "Comboio.", "C": "Fila de carros.", "D": "Carreata."}, "resposta": "A", "comentario": "Ex: caminhão com carreta."},
    {"modulo": "3", "numero": "174", "questao": "Qual o comprimento máximo para combinações de veículos?", "alternativas": {"A": "19,80 metros (pode haver exceções com AET).", "B": "30 metros.", "C": "10 metros.", "D": "Sem limite."}, "resposta": "A", "comentario": "Regulamentado pelo CONTRAN."},
    {"modulo": "3", "numero": "175", "questao": "O que é AET?", "alternativas": {"A": "Autorização Especial de Trânsito.", "B": "Auto de Exame Técnico.", "C": "Avaliação de Emissão.", "D": "Atestado de Equipamento."}, "resposta": "A", "comentario": "Para veículos fora das dimensões normais."},
    {"modulo": "3", "numero": "176", "questao": "Quando é necessária AET?", "alternativas": {"A": "Para veículos com dimensões ou peso acima do permitido.", "B": "Para qualquer caminhão.", "C": "Para motos.", "D": "Nunca."}, "resposta": "A", "comentario": "Cargas especiais precisam de autorização."},
    {"modulo": "3", "numero": "177", "questao": "O que é carga indivisível?", "alternativas": {"A": "Carga que não pode ser fracionada sem perda de valor.", "B": "Carga frágil.", "C": "Carga perigosa.", "D": "Carga leve."}, "resposta": "A", "comentario": "Ex: máquinas grandes, estruturas."},
    {"modulo": "3", "numero": "178", "questao": "Como deve ser transportada carga indivisível excedente?", "alternativas": {"A": "Com AET e sinalização especial.", "B": "Normalmente.", "C": "Apenas à noite.", "D": "Não pode ser transportada."}, "resposta": "A", "comentario": "Requer autorização e cuidados."},
    {"modulo": "3", "numero": "179", "questao": "O que é carga perigosa?", "alternativas": {"A": "Produtos que oferecem risco à saúde, segurança ou meio ambiente.", "B": "Carga pesada.", "C": "Carga frágil.", "D": "Carga valiosa."}, "resposta": "A", "comentario": "Químicos, inflamáveis, explosivos."},
    {"modulo": "3", "numero": "180", "questao": "É necessário curso especial para transportar carga perigosa?", "alternativas": {"A": "Sim, curso MOPP.", "B": "Não.", "C": "Apenas para líquidos.", "D": "Apenas para explosivos."}, "resposta": "A", "comentario": "MOPP = Movimentação de Produtos Perigosos."},
    {"modulo": "3", "numero": "181", "questao": "O que é MOPP?", "alternativas": {"A": "Movimentação Operacional de Produtos Perigosos.", "B": "Manual de Operações.", "C": "Módulo de Proteção.", "D": "Medida de Prevenção."}, "resposta": "A", "comentario": "Curso obrigatório para transporte de perigosos."},
    {"modulo": "3", "numero": "182", "questao": "O que é painel de segurança?", "alternativas": {"A": "Placa laranja com números que identifica o produto perigoso.", "B": "Placa de velocidade.", "C": "Placa de proibição.", "D": "Placa de indicação."}, "resposta": "A", "comentario": "Obrigatório em veículos com carga perigosa."},
    {"modulo": "3", "numero": "183", "questao": "O que é rótulo de risco?", "alternativas": {"A": "Símbolo que indica o tipo de perigo da carga.", "B": "Etiqueta de preço.", "C": "Código de barras.", "D": "Nota fiscal."}, "resposta": "A", "comentario": "Losango colorido com símbolo."},
    {"modulo": "3", "numero": "184", "questao": "O que indica rótulo de risco vermelho?", "alternativas": {"A": "Produto inflamável.", "B": "Produto corrosivo.", "C": "Produto tóxico.", "D": "Produto radioativo."}, "resposta": "A", "comentario": "Vermelho = inflamável."},
    {"modulo": "3", "numero": "185", "questao": "O que indica rótulo de risco amarelo?", "alternativas": {"A": "Produto oxidante ou peróxido.", "B": "Inflamável.", "C": "Corrosivo.", "D": "Tóxico."}, "resposta": "A", "comentario": "Amarelo = oxidante."},
    {"modulo": "3", "numero": "186", "questao": "O que indica rótulo de risco branco e preto?", "alternativas": {"A": "Produto corrosivo.", "B": "Inflamável.", "C": "Tóxico.", "D": "Radioativo."}, "resposta": "A", "comentario": "Branco/preto = corrosivo."},
    {"modulo": "3", "numero": "187", "questao": "O que indica rótulo de risco com caveira?", "alternativas": {"A": "Produto tóxico.", "B": "Inflamável.", "C": "Corrosivo.", "D": "Explosivo."}, "resposta": "A", "comentario": "Caveira = tóxico."},
    {"modulo": "3", "numero": "188", "questao": "O que indica rótulo de risco com símbolo radioativo?", "alternativas": {"A": "Material radioativo.", "B": "Material tóxico.", "C": "Material inflamável.", "D": "Material corrosivo."}, "resposta": "A", "comentario": "Trifólio = radioativo."},
    {"modulo": "3", "numero": "189", "questao": "É permitido estacionar veículo com carga perigosa em área residencial?", "alternativas": {"A": "Não.", "B": "Sim.", "C": "Apenas de dia.", "D": "Apenas brevemente."}, "resposta": "A", "comentario": "Restrições de estacionamento."},
    {"modulo": "3", "numero": "190", "questao": "O que fazer em acidente com carga perigosa?", "alternativas": {"A": "Isolar área e acionar Corpo de Bombeiros.", "B": "Tentar limpar.", "C": "Ignorar.", "D": "Continuar viagem."}, "resposta": "A", "comentario": "Especialistas devem atuar."},
    {"modulo": "3", "numero": "191", "questao": "O que é tacógrafo?", "alternativas": {"A": "Equipamento que registra velocidade, tempo e distância.", "B": "Velocímetro.", "C": "GPS.", "D": "Rádio."}, "resposta": "A", "comentario": "Obrigatório em veículos de carga e coletivos."},
    {"modulo": "3", "numero": "192", "questao": "Para que serve o tacógrafo?", "alternativas": {"A": "Controlar jornada do motorista e velocidade.", "B": "Apenas medir velocidade.", "C": "Localizar veículo.", "D": "Comunicação."}, "resposta": "A", "comentario": "Segurança e controle trabalhista."},
    {"modulo": "3", "numero": "193", "questao": "É crime adulterar tacógrafo?", "alternativas": {"A": "Sim.", "B": "Não, apenas infração.", "C": "Depende.", "D": "Não há punição."}, "resposta": "A", "comentario": "Crime previsto no CTB."},
    {"modulo": "3", "numero": "194", "questao": "Qual a validade do disco de tacógrafo?", "alternativas": {"A": "24 horas (um dia).", "B": "Uma semana.", "C": "Um mês.", "D": "Um ano."}, "resposta": "A", "comentario": "Deve ser trocado diariamente."},
    {"modulo": "3", "numero": "195", "questao": "O que é Lei do Descanso?", "alternativas": {"A": "Lei que regula jornada e descanso de motoristas profissionais.", "B": "Lei de trânsito geral.", "C": "Lei de velocidade.", "D": "Lei ambiental."}, "resposta": "A", "comentario": "Lei 13.103/2015."},
    {"modulo": "3", "numero": "196", "questao": "Qual o tempo máximo de direção contínua para motorista profissional?", "alternativas": {"A": "5 horas e 30 minutos.", "B": "8 horas.", "C": "4 horas.", "D": "12 horas."}, "resposta": "A", "comentario": "Após isso, deve descansar."},
    {"modulo": "3", "numero": "197", "questao": "Qual o intervalo mínimo de descanso após 5h30 de direção?", "alternativas": {"A": "30 minutos.", "B": "15 minutos.", "C": "1 hora.", "D": "2 horas."}, "resposta": "A", "comentario": "Pode ser fracionado."},
    {"modulo": "3", "numero": "198", "questao": "Qual o descanso mínimo diário para motorista profissional?", "alternativas": {"A": "11 horas.", "B": "8 horas.", "C": "6 horas.", "D": "4 horas."}, "resposta": "A", "comentario": "Dentro de período de 24 horas."},
    {"modulo": "3", "numero": "199", "questao": "O que é EAR?", "alternativas": {"A": "Exame de Aptidão para Renovação.", "B": "Equipamento de Segurança.", "C": "Escola de Direção.", "D": "Estação de Abastecimento."}, "resposta": "A", "comentario": "Exame para renovar CNH de profissional."},
    {"modulo": "3", "numero": "200", "questao": "O motorista profissional precisa de exame toxicológico?", "alternativas": {"A": "Sim, nas categorias C, D e E.", "B": "Não.", "C": "Apenas categoria E.", "D": "Apenas taxistas."}, "resposta": "A", "comentario": "Obrigatório para profissionais."},
    {"modulo": "3", "numero": "201", "questao": "Qual a validade do exame toxicológico?", "alternativas": {"A": "2 anos e 6 meses.", "B": "1 ano.", "C": "5 anos.", "D": "Permanente."}, "resposta": "A", "comentario": "Deve ser renovado periodicamente."},
    {"modulo": "3", "numero": "202", "questao": "O que acontece se reprovar no exame toxicológico?", "alternativas": {"A": "CNH não é emitida ou renovada.", "B": "Apenas advertência.", "C": "Multa.", "D": "Nada."}, "resposta": "A", "comentario": "Impede exercício da profissão."},
    {"modulo": "3", "numero": "203", "questao": "O que é reciclagem de CNH?", "alternativas": {"A": "Curso obrigatório para infratores ou suspensos.", "B": "Renovação normal.", "C": "Primeira habilitação.", "D": "Mudança de categoria."}, "resposta": "A", "comentario": "Para recuperar direito de dirigir."},
    {"modulo": "3", "numero": "204", "questao": "Quando é obrigatória a reciclagem?", "alternativas": {"A": "Suspensão da CNH ou infrações graves.", "B": "A cada 5 anos.", "C": "Nunca.", "D": "Apenas para idosos."}, "resposta": "A", "comentario": "Penalidade educativa."},
    {"modulo": "3", "numero": "205", "questao": "Qual a carga horária do curso de reciclagem?", "alternativas": {"A": "30 horas.", "B": "15 horas.", "C": "45 horas.", "D": "60 horas."}, "resposta": "A", "comentario": "Curso teórico obrigatório."},
    {"modulo": "3", "numero": "206", "questao": "O que é defesa prévia?", "alternativas": {"A": "Recurso contra autuação antes da multa ser aplicada.", "B": "Defesa em tribunal.", "C": "Advogado de trânsito.", "D": "Pagamento de multa."}, "resposta": "A", "comentario": "Direito do condutor autuado."},
    {"modulo": "3", "numero": "207", "questao": "Qual o prazo para defesa prévia?", "alternativas": {"A": "Indicado na notificação de autuação.", "B": "30 dias sempre.", "C": "10 dias.", "D": "1 ano."}, "resposta": "A", "comentario": "Geralmente 15 dias."},
    {"modulo": "3", "numero": "208", "questao": "O que é JARI?", "alternativas": {"A": "Junta Administrativa de Recursos de Infrações.", "B": "Juizado de Trânsito.", "C": "Junta de Avaliação.", "D": "Justiça Rodoviária."}, "resposta": "A", "comentario": "Primeira instância de recurso."},
    {"modulo": "3", "numero": "209", "questao": "É possível recorrer de decisão da JARI?", "alternativas": {"A": "Sim, ao CETRAN ou CONTRAN.", "B": "Não.", "C": "Apenas em crimes.", "D": "Apenas para multas altas."}, "resposta": "A", "comentario": "Segunda instância administrativa."},
    {"modulo": "3", "numero": "210", "questao": "O que é CETRAN?", "alternativas": {"A": "Conselho Estadual de Trânsito.", "B": "Centro de Treinamento.", "C": "Central de Multas.", "D": "Controle de Estradas."}, "resposta": "A", "comentario": "Órgão estadual de trânsito."},
    {"modulo": "3", "numero": "211", "questao": "O pagamento da multa com desconto implica em quê?", "alternativas": {"A": "Renúncia ao direito de recurso.", "B": "Nada.", "C": "Desconto nos pontos.", "D": "Anulação da infração."}, "resposta": "A", "comentario": "Pagar com desconto = assumir a infração."},
    {"modulo": "3", "numero": "212", "questao": "Qual o desconto para pagamento antecipado de multa?", "alternativas": {"A": "Até 40%.", "B": "10%.", "C": "50%.", "D": "Não há desconto."}, "resposta": "A", "comentario": "Incentivo ao pagamento rápido."},
    {"modulo": "3", "numero": "213", "questao": "O que acontece se não pagar multa?", "alternativas": {"A": "Impede licenciamento e pode ir para dívida ativa.", "B": "Nada.", "C": "Apenas pontos.", "D": "Prisão."}, "resposta": "A", "comentario": "Consequências administrativas e financeiras."},
    {"modulo": "3", "numero": "214", "questao": "Os pontos da multa podem ser transferidos?", "alternativas": {"A": "Sim, para quem realmente cometeu a infração.", "B": "Não.", "C": "Apenas entre familiares.", "D": "Apenas com advogado."}, "resposta": "A", "comentario": "Indicação do real infrator."},
    {"modulo": "3", "numero": "215", "questao": "Qual o prazo para indicar o real condutor infrator?", "alternativas": {"A": "Até o vencimento da notificação.", "B": "1 ano.", "C": "Não há prazo.", "D": "30 dias após multa."}, "resposta": "A", "comentario": "Prazo indicado na notificação."},
    {"modulo": "3", "numero": "216", "questao": "O que é NIC?", "alternativas": {"A": "Notificação de Imposição de Penalidade.", "B": "Número de Infração.", "C": "Norma de Circulação.", "D": "Nota de Identificação."}, "resposta": "A", "comentario": "Documento que aplica a multa."},
    {"modulo": "3", "numero": "217", "questao": "O que é AIT?", "alternativas": {"A": "Auto de Infração de Trânsito.", "B": "Autorização de Tráfego.", "C": "Aviso de Irregularidade.", "D": "Atestado de Inspeção."}, "resposta": "A", "comentario": "Documento da autuação."},
    {"modulo": "3", "numero": "218", "questao": "Qual a diferença entre AIT e NIC?", "alternativas": {"A": "AIT é a autuação, NIC é a penalidade aplicada.", "B": "São iguais.", "C": "NIC vem antes.", "D": "Não há diferença."}, "resposta": "A", "comentario": "AIT inicia o processo, NIC conclui."},
    {"modulo": "3", "numero": "219", "questao": "É possível anular multa por erro de preenchimento?", "alternativas": {"A": "Sim, se o erro for essencial.", "B": "Não.", "C": "Apenas erros de valor.", "D": "Apenas erros de data."}, "resposta": "A", "comentario": "Erros que prejudiquem a defesa anulam."},
    {"modulo": "3", "numero": "220", "questao": "O que é CNH provisória?", "alternativas": {"A": "Permissão para Dirigir válida por 1 ano.", "B": "CNH vencida.", "C": "CNH digital.", "D": "CNH internacional."}, "resposta": "A", "comentario": "Primeiro documento do condutor."},
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
