#!/usr/bin/env python3
"""
Script to add more Module 3 questions (281-430)
"""

import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

NEW_QUESTIONS = [
    # MÓDULO 3 (281-430)
    {"modulo": "3", "numero": "281", "questao": "Permitir que menor dirija é crime?", "alternativas": {"A": "Sim, para quem entrega o veículo.", "B": "Não.", "C": "Apenas infração.", "D": "Depende da idade."}, "resposta": "A", "comentario": "Crime de trânsito."},
    {"modulo": "3", "numero": "282", "questao": "Qual a pena para quem entrega veículo a menor?", "alternativas": {"A": "Detenção de 6 meses a 1 ano.", "B": "Apenas multa.", "C": "Advertência.", "D": "Nenhuma."}, "resposta": "A", "comentario": "Responsabilidade do proprietário."},
    {"modulo": "3", "numero": "283", "questao": "Entregar veículo a pessoa não habilitada é crime?", "alternativas": {"A": "Sim.", "B": "Não.", "C": "Apenas infração.", "D": "Depende."}, "resposta": "A", "comentario": "Crime do CTB."},
    {"modulo": "3", "numero": "284", "questao": "O que é adulteração de chassi?", "alternativas": {"A": "Alterar número de identificação do veículo.", "B": "Pintar o carro.", "C": "Trocar peças.", "D": "Lavar o motor."}, "resposta": "A", "comentario": "Crime grave."},
    {"modulo": "3", "numero": "285", "questao": "Qual a pena para adulteração de chassi?", "alternativas": {"A": "Reclusão de 3 a 6 anos.", "B": "Detenção.", "C": "Apenas multa.", "D": "Advertência."}, "resposta": "A", "comentario": "Crime grave com pena de reclusão."},
    {"modulo": "3", "numero": "286", "questao": "O que é receptação de veículo?", "alternativas": {"A": "Adquirir veículo roubado ou furtado.", "B": "Comprar carro usado.", "C": "Vender carro.", "D": "Alugar veículo."}, "resposta": "A", "comentario": "Crime previsto no Código Penal."},
    {"modulo": "3", "numero": "287", "questao": "Como evitar comprar veículo roubado?", "alternativas": {"A": "Consultar histórico e verificar documentação.", "B": "Confiar no vendedor.", "C": "Não há como.", "D": "Apenas pelo preço."}, "resposta": "A", "comentario": "Consulta ao DETRAN evita problemas."},
    {"modulo": "3", "numero": "288", "questao": "O que é clonagem de veículo?", "alternativas": {"A": "Usar placa de outro veículo.", "B": "Copiar design.", "C": "Fazer réplica.", "D": "Adesivo."}, "resposta": "A", "comentario": "Crime de falsidade."},
    {"modulo": "3", "numero": "289", "questao": "Como identificar veículo clonado?", "alternativas": {"A": "Comparar chassi, motor e documentos.", "B": "Pela cor.", "C": "Pelo modelo.", "D": "Não é possível."}, "resposta": "A", "comentario": "Vistoria detalhada identifica."},
    {"modulo": "3", "numero": "290", "questao": "O que fazer se descobrir que seu veículo foi clonado?", "alternativas": {"A": "Registrar boletim de ocorrência.", "B": "Ignorar.", "C": "Vender o carro.", "D": "Trocar de placa."}, "resposta": "A", "comentario": "Proteger-se de multas indevidas."},
    {"modulo": "3", "numero": "291", "questao": "O que é sinistro de veículo?", "alternativas": {"A": "Acidente ou dano ao veículo.", "B": "Manutenção.", "C": "Revisão.", "D": "Lavagem."}, "resposta": "A", "comentario": "Registrado para fins de seguro."},
    {"modulo": "3", "numero": "292", "questao": "O que é perda total?", "alternativas": {"A": "Quando o custo de reparo excede valor do veículo.", "B": "Roubo.", "C": "Furto.", "D": "Incêndio."}, "resposta": "A", "comentario": "Seguradora considera PT."},
    {"modulo": "3", "numero": "293", "questao": "Veículo com perda total pode voltar a circular?", "alternativas": {"A": "Sim, após recuperação e vistoria especial.", "B": "Nunca.", "C": "Sempre.", "D": "Depende da cor."}, "resposta": "A", "comentario": "Procedimento específico exigido."},
    {"modulo": "3", "numero": "294", "questao": "O que é veículo recuperado de roubo?", "alternativas": {"A": "Veículo roubado encontrado pelas autoridades.", "B": "Carro novo.", "C": "Carro reformado.", "D": "Carro importado."}, "resposta": "A", "comentario": "Retorna ao proprietário ou seguradora."},
    {"modulo": "3", "numero": "295", "questao": "O que é leilão de veículos?", "alternativas": {"A": "Venda pública de veículos apreendidos ou recuperados.", "B": "Feira de carros.", "C": "Concessionária.", "D": "Revenda."}, "resposta": "A", "comentario": "Oportunidade de compra, mas com riscos."},
    {"modulo": "3", "numero": "296", "questao": "Quais cuidados ao comprar em leilão?", "alternativas": {"A": "Verificar histórico, estado e documentação.", "B": "Apenas o preço.", "C": "Nenhum.", "D": "Apenas a cor."}, "resposta": "A", "comentario": "Veículos podem ter problemas ocultos."},
    {"modulo": "3", "numero": "297", "questao": "O que é despachante de trânsito?", "alternativas": {"A": "Profissional que auxilia em processos no DETRAN.", "B": "Fiscal.", "C": "Policial.", "D": "Mecânico."}, "resposta": "A", "comentario": "Facilita trâmites burocráticos."},
    {"modulo": "3", "numero": "298", "questao": "É obrigatório usar despachante?", "alternativas": {"A": "Não, todos os serviços podem ser feitos diretamente.", "B": "Sim.", "C": "Para alguns serviços.", "D": "Apenas para empresas."}, "resposta": "A", "comentario": "Opção do cidadão."},
    {"modulo": "3", "numero": "299", "questao": "O que é vistoria veicular?", "alternativas": {"A": "Inspeção das condições do veículo.", "B": "Lavagem.", "C": "Polimento.", "D": "Revisão mecânica."}, "resposta": "A", "comentario": "Verifica itens de segurança e identificação."},
    {"modulo": "3", "numero": "300", "questao": "Quando é obrigatória a vistoria?", "alternativas": {"A": "Transferência, mudança de município, alteração de características.", "B": "Todo ano.", "C": "Nunca.", "D": "Apenas para motos."}, "resposta": "A", "comentario": "Situações específicas exigem."},
    {"modulo": "3", "numero": "301", "questao": "O que é laudo de vistoria?", "alternativas": {"A": "Documento que atesta condições do veículo.", "B": "Nota fiscal.", "C": "Recibo.", "D": "Contrato."}, "resposta": "A", "comentario": "Necessário para vários procedimentos."},
    {"modulo": "3", "numero": "302", "questao": "Quanto tempo vale o laudo de vistoria?", "alternativas": {"A": "90 dias em geral.", "B": "1 ano.", "C": "Permanente.", "D": "30 dias."}, "resposta": "A", "comentario": "Prazo pode variar por estado."},
    {"modulo": "3", "numero": "303", "questao": "O que é gravame veicular?", "alternativas": {"A": "Restrição financeira sobre o veículo.", "B": "Tipo de placa.", "C": "Modelo de carro.", "D": "Acessório."}, "resposta": "A", "comentario": "Indica financiamento ou alienação."},
    {"modulo": "3", "numero": "304", "questao": "Veículo com gravame pode ser vendido?", "alternativas": {"A": "Apenas com autorização do credor ou quitação.", "B": "Sim, livremente.", "C": "Nunca.", "D": "Apenas para parentes."}, "resposta": "A", "comentario": "Restrição impede transferência normal."},
    {"modulo": "3", "numero": "305", "questao": "O que é restrição judicial?", "alternativas": {"A": "Bloqueio determinado por juiz.", "B": "Multa.", "C": "IPVA.", "D": "Licenciamento."}, "resposta": "A", "comentario": "Impede movimentação do bem."},
    {"modulo": "3", "numero": "306", "questao": "O que é busca e apreensão?", "alternativas": {"A": "Ação judicial para retomar veículo de devedor.", "B": "Fiscalização.", "C": "Blitz.", "D": "Leilão."}, "resposta": "A", "comentario": "Comum em financiamentos inadimplidos."},
    {"modulo": "3", "numero": "307", "questao": "O que acontece se não pagar financiamento?", "alternativas": {"A": "Veículo pode ser retomado pelo credor.", "B": "Nada.", "C": "Apenas negativação.", "D": "Multa apenas."}, "resposta": "A", "comentario": "Alienação fiduciária permite retomada."},
    {"modulo": "3", "numero": "308", "questao": "O que é RENAVAM?", "alternativas": {"A": "Registro Nacional de Veículos Automotores.", "B": "Registro de condutores.", "C": "Número da CNH.", "D": "Placa."}, "resposta": "A", "comentario": "Identificação única do veículo."},
    {"modulo": "3", "numero": "309", "questao": "Para que serve o RENAVAM?", "alternativas": {"A": "Identificar o veículo em todo o país.", "B": "Identificar o condutor.", "C": "Calcular IPVA.", "D": "Registrar multas."}, "resposta": "A", "comentario": "Número nacional de identificação."},
    {"modulo": "3", "numero": "310", "questao": "O que é RENACH?", "alternativas": {"A": "Registro Nacional de Carteira de Habilitação.", "B": "Registro de veículos.", "C": "Número da placa.", "D": "Código de multas."}, "resposta": "A", "comentario": "Identifica condutores."},
    {"modulo": "3", "numero": "311", "questao": "O que é SNT?", "alternativas": {"A": "Sistema Nacional de Trânsito.", "B": "Seguro Nacional.", "C": "Serviço de Notificação.", "D": "Setor de Normas."}, "resposta": "A", "comentario": "Conjunto de órgãos de trânsito."},
    {"modulo": "3", "numero": "312", "questao": "Quais órgãos compõem o SNT?", "alternativas": {"A": "CONTRAN, DENATRAN, DETRANs, PRF, polícias.", "B": "Apenas DETRAN.", "C": "Apenas PRF.", "D": "Apenas CONTRAN."}, "resposta": "A", "comentario": "Sistema integrado nacional."},
    {"modulo": "3", "numero": "313", "questao": "O que é CONTRAN?", "alternativas": {"A": "Conselho Nacional de Trânsito.", "B": "Controle de Transporte.", "C": "Central de Notificações.", "D": "Comitê de Normas."}, "resposta": "A", "comentario": "Órgão máximo normativo."},
    {"modulo": "3", "numero": "314", "questao": "Qual a função do CONTRAN?", "alternativas": {"A": "Estabelecer normas e regulamentar o CTB.", "B": "Aplicar multas.", "C": "Fiscalizar.", "D": "Emitir CNH."}, "resposta": "A", "comentario": "Órgão normativo e consultivo."},
    {"modulo": "3", "numero": "315", "questao": "O que é DENATRAN?", "alternativas": {"A": "Departamento Nacional de Trânsito.", "B": "Delegacia de Trânsito.", "C": "Departamento de Normas.", "D": "Divisão de Educação."}, "resposta": "A", "comentario": "Atual SENATRAN."},
    {"modulo": "3", "numero": "316", "questao": "O que é SENATRAN?", "alternativas": {"A": "Secretaria Nacional de Trânsito.", "B": "Serviço de Notificações.", "C": "Setor de Atendimento.", "D": "Sistema de Registro."}, "resposta": "A", "comentario": "Novo nome do DENATRAN."},
    {"modulo": "3", "numero": "317", "questao": "O que é DETRAN?", "alternativas": {"A": "Departamento Estadual de Trânsito.", "B": "Delegacia de Trânsito.", "C": "Divisão de Transporte.", "D": "Departamento de Estradas."}, "resposta": "A", "comentario": "Órgão estadual executivo."},
    {"modulo": "3", "numero": "318", "questao": "Qual a função do DETRAN?", "alternativas": {"A": "Emitir CNH, registrar veículos, aplicar penalidades.", "B": "Apenas emitir CNH.", "C": "Apenas fiscalizar.", "D": "Apenas multar."}, "resposta": "A", "comentario": "Múltiplas funções executivas."},
    {"modulo": "3", "numero": "319", "questao": "O que é PRF?", "alternativas": {"A": "Polícia Rodoviária Federal.", "B": "Patrulha Rodoviária.", "C": "Polícia de Fronteira.", "D": "Programa Rodoviário."}, "resposta": "A", "comentario": "Fiscaliza rodovias federais."},
    {"modulo": "3", "numero": "320", "questao": "Qual a função da PRF?", "alternativas": {"A": "Fiscalizar rodovias federais.", "B": "Emitir CNH.", "C": "Registrar veículos.", "D": "Aprovar estradas."}, "resposta": "A", "comentario": "Polícia ostensiva nas BRs."},
    {"modulo": "3", "numero": "321", "questao": "O que é DER?", "alternativas": {"A": "Departamento de Estradas de Rodagem.", "B": "Divisão de Registros.", "C": "Delegacia de Estradas.", "D": "Departamento de Emergências."}, "resposta": "A", "comentario": "Cuida das estradas estaduais."},
    {"modulo": "3", "numero": "322", "questao": "O que é DNIT?", "alternativas": {"A": "Departamento Nacional de Infraestrutura de Transportes.", "B": "Delegacia Nacional.", "C": "Divisão de Normas.", "D": "Departamento de Inspeção."}, "resposta": "A", "comentario": "Cuida da infraestrutura rodoviária federal."},
    {"modulo": "3", "numero": "323", "questao": "O que são concessionárias de rodovias?", "alternativas": {"A": "Empresas que administram rodovias mediante pedágio.", "B": "Lojas de carros.", "C": "Postos de gasolina.", "D": "Oficinas."}, "resposta": "A", "comentario": "Concessão para operar rodovias."},
    {"modulo": "3", "numero": "324", "questao": "É obrigatório pagar pedágio?", "alternativas": {"A": "Sim, para usar rodovias pedagiadas.", "B": "Não.", "C": "Apenas para caminhões.", "D": "Opcional."}, "resposta": "A", "comentario": "Contraprestação pelo uso."},
    {"modulo": "3", "numero": "325", "questao": "O que acontece se não pagar pedágio?", "alternativas": {"A": "Multa e cobrança administrativa.", "B": "Nada.", "C": "Prisão.", "D": "Apreensão do veículo."}, "resposta": "A", "comentario": "Infração com penalidade."},
    {"modulo": "3", "numero": "326", "questao": "O que é TAG de pedágio?", "alternativas": {"A": "Dispositivo para pagamento automático.", "B": "Placa especial.", "C": "Tipo de pneu.", "D": "Adesivo decorativo."}, "resposta": "A", "comentario": "Facilita passagem sem parar."},
    {"modulo": "3", "numero": "327", "questao": "O que é sistema free flow?", "alternativas": {"A": "Pedágio sem cancela, com cobrança eletrônica.", "B": "Via livre.", "C": "Estacionamento.", "D": "Rodovia sem pedágio."}, "resposta": "A", "comentario": "Cobrança por câmeras e sensores."},
    {"modulo": "3", "numero": "328", "questao": "O que é rodízio de veículos?", "alternativas": {"A": "Restrição de circulação por dia e final de placa.", "B": "Troca de pneus.", "C": "Rodagem de motor.", "D": "Manutenção."}, "resposta": "A", "comentario": "Medida para reduzir congestionamento."},
    {"modulo": "3", "numero": "329", "questao": "Onde existe rodízio de veículos?", "alternativas": {"A": "Grandes cidades como São Paulo.", "B": "Todo o Brasil.", "C": "Apenas rodovias.", "D": "Zona rural."}, "resposta": "A", "comentario": "Política local de mobilidade."},
    {"modulo": "3", "numero": "330", "questao": "Qual a penalidade por furar rodízio?", "alternativas": {"A": "Multa.", "B": "Apreensão.", "C": "Suspensão da CNH.", "D": "Nenhuma."}, "resposta": "A", "comentario": "Infração de trânsito."},
    {"modulo": "3", "numero": "331", "questao": "O que é inspeção ambiental veicular?", "alternativas": {"A": "Verificação das emissões de poluentes.", "B": "Lavagem ecológica.", "C": "Vistoria de segurança.", "D": "Revisão mecânica."}, "resposta": "A", "comentario": "Controle de poluição."},
    {"modulo": "3", "numero": "332", "questao": "Onde é obrigatória a inspeção ambiental?", "alternativas": {"A": "Em alguns estados e municípios.", "B": "Todo o Brasil.", "C": "Nenhum lugar.", "D": "Apenas rodovias."}, "resposta": "A", "comentario": "Varia conforme legislação local."},
    {"modulo": "3", "numero": "333", "questao": "O que é PCPV?", "alternativas": {"A": "Programa de Controle de Poluição Veicular.", "B": "Plano de Circulação.", "C": "Programa de Capacitação.", "D": "Política de Condutores."}, "resposta": "A", "comentario": "Programa ambiental."},
    {"modulo": "3", "numero": "334", "questao": "O que verifica a inspeção ambiental?", "alternativas": {"A": "Gases do escapamento e ruído.", "B": "Pintura.", "C": "Documentos.", "D": "Pneus."}, "resposta": "A", "comentario": "Emissões e nível de ruído."},
    {"modulo": "3", "numero": "335", "questao": "Veículo reprovado na inspeção pode circular?", "alternativas": {"A": "Não, até ser regularizado.", "B": "Sim.", "C": "Apenas de dia.", "D": "Apenas em cidade."}, "resposta": "A", "comentario": "Deve fazer ajustes e reprovar."},
    {"modulo": "3", "numero": "336", "questao": "O que é catalisador?", "alternativas": {"A": "Dispositivo que reduz poluentes do escapamento.", "B": "Tipo de combustível.", "C": "Filtro de ar.", "D": "Vela de ignição."}, "resposta": "A", "comentario": "Equipamento obrigatório."},
    {"modulo": "3", "numero": "337", "questao": "É crime remover catalisador?", "alternativas": {"A": "Sim, crime ambiental.", "B": "Não.", "C": "Apenas infração.", "D": "Depende."}, "resposta": "A", "comentario": "Adulteração ambiental é crime."},
    {"modulo": "3", "numero": "338", "questao": "O que é escapamento adulterado?", "alternativas": {"A": "Sistema modificado para aumentar ruído ou desempenho.", "B": "Escapamento novo.", "C": "Escapamento original.", "D": "Silenciador."}, "resposta": "A", "comentario": "Infração e crime ambiental."},
    {"modulo": "3", "numero": "339", "questao": "Qual a penalidade por escapamento adulterado?", "alternativas": {"A": "Multa, retenção e possível crime ambiental.", "B": "Apenas multa.", "C": "Nenhuma.", "D": "Advertência."}, "resposta": "A", "comentario": "Penalidades cumulativas."},
    {"modulo": "3", "numero": "340", "questao": "O que é película no vidro?", "alternativas": {"A": "Filme aplicado para escurecer ou proteger.", "B": "Tipo de vidro.", "C": "Trinco.", "D": "Adesivo."}, "resposta": "A", "comentario": "Insulfilm."},
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
