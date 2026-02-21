#!/usr/bin/env python3
"""
Script to add more questions from Modules 2, 3 and 4
"""

import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

NEW_QUESTIONS = [
    # Mais questões do MÓDULO 2 (71-171)
    {"modulo": "2", "numero": "71", "questao": "O que é atropelamento?", "alternativas": {"A": "Colisão entre veículo e pedestre.", "B": "Colisão entre dois veículos.", "C": "Capotamento.", "D": "Colisão lateral."}, "resposta": "A", "comentario": "Atropelamentos são acidentes graves envolvendo pedestres."},
    {"modulo": "2", "numero": "72", "questao": "Como evitar atropelamentos?", "alternativas": {"A": "Reduzir velocidade em áreas com pedestres e respeitar faixas.", "B": "Buzinar para pedestres saírem.", "C": "Ignorar faixas de pedestres.", "D": "Acelerar em zonas escolares."}, "resposta": "A", "comentario": "Atenção e velocidade adequada protegem pedestres."},
    {"modulo": "2", "numero": "73", "questao": "O que fazer ao se aproximar de uma faixa de pedestres?", "alternativas": {"A": "Reduzir velocidade e dar preferência aos pedestres.", "B": "Acelerar para passar antes deles.", "C": "Buzinar.", "D": "Ignorar."}, "resposta": "A", "comentario": "Pedestres na faixa têm preferência de passagem."},
    {"modulo": "2", "numero": "74", "questao": "Qual o comportamento correto ao ver crianças próximas à via?", "alternativas": {"A": "Reduzir velocidade e ficar atento a movimentos inesperados.", "B": "Manter a velocidade.", "C": "Buzinar para afastá-las.", "D": "Acelerar."}, "resposta": "A", "comentario": "Crianças são imprevisíveis e merecem atenção especial."},
    {"modulo": "2", "numero": "75", "questao": "O que é direção sob influência de substâncias?", "alternativas": {"A": "Dirigir após consumir álcool ou drogas.", "B": "Dirigir cansado.", "C": "Dirigir com pressa.", "D": "Dirigir à noite."}, "resposta": "A", "comentario": "Substâncias psicoativas prejudicam a capacidade de dirigir."},
    {"modulo": "2", "numero": "76", "questao": "Quais são os efeitos das drogas na direção?", "alternativas": {"A": "Alteração de percepção, reflexos e julgamento.", "B": "Aumento da atenção.", "C": "Melhora dos reflexos.", "D": "Nenhum efeito."}, "resposta": "A", "comentario": "Drogas comprometem funções essenciais para dirigir."},
    {"modulo": "2", "numero": "77", "questao": "O que é tempo de reação?", "alternativas": {"A": "Intervalo entre perceber um perigo e agir.", "B": "Tempo para acelerar.", "C": "Tempo de viagem.", "D": "Tempo de frenagem."}, "resposta": "A", "comentario": "O tempo de reação médio é de cerca de 1 segundo."},
    {"modulo": "2", "numero": "78", "questao": "O que aumenta o tempo de reação?", "alternativas": {"A": "Cansaço, álcool, distrações.", "B": "Atenção.", "C": "Descanso.", "D": "Boa visibilidade."}, "resposta": "A", "comentario": "Fatores que prejudicam a atenção aumentam o tempo de reação."},
    {"modulo": "2", "numero": "79", "questao": "O que é distância de frenagem?", "alternativas": {"A": "Distância percorrida desde o início da frenagem até parar.", "B": "Distância de seguimento.", "C": "Distância de ultrapassagem.", "D": "Distância de visibilidade."}, "resposta": "A", "comentario": "A distância de frenagem depende da velocidade e condições da pista."},
    {"modulo": "2", "numero": "80", "questao": "O que aumenta a distância de frenagem?", "alternativas": {"A": "Alta velocidade, pista molhada, pneus gastos.", "B": "Baixa velocidade.", "C": "Pneus novos.", "D": "Pista seca."}, "resposta": "A", "comentario": "Esses fatores reduzem a eficiência da frenagem."},
    {"modulo": "2", "numero": "81", "questao": "O que é distância de parada?", "alternativas": {"A": "Soma da distância de reação e de frenagem.", "B": "Apenas distância de frenagem.", "C": "Distância entre veículos.", "D": "Distância de ultrapassagem."}, "resposta": "A", "comentario": "A distância total considera o tempo de reação e a frenagem."},
    {"modulo": "2", "numero": "82", "questao": "Por que a velocidade duplicada quadruplica a distância de frenagem?", "alternativas": {"A": "Porque a energia cinética aumenta com o quadrado da velocidade.", "B": "Porque os freios são menos eficientes.", "C": "Porque a pista fica mais escorregadia.", "D": "Porque o motorista demora mais para reagir."}, "resposta": "A", "comentario": "Física: E = mv²/2, dobrando v, quadruplica E."},
    {"modulo": "2", "numero": "83", "questao": "O que é condução econômica?", "alternativas": {"A": "Dirigir de forma a economizar combustível.", "B": "Dirigir devagar sempre.", "C": "Usar combustível mais barato.", "D": "Não fazer manutenção."}, "resposta": "A", "comentario": "Condução econômica envolve técnicas para reduzir consumo."},
    {"modulo": "2", "numero": "84", "questao": "Como economizar combustível?", "alternativas": {"A": "Manter velocidade constante e evitar acelerações bruscas.", "B": "Acelerar e frear constantemente.", "C": "Andar sempre em alta rotação.", "D": "Usar o ar-condicionado no máximo."}, "resposta": "A", "comentario": "Dirigir suavemente reduz o consumo de combustível."},
    {"modulo": "2", "numero": "85", "questao": "O que é poluição veicular?", "alternativas": {"A": "Emissão de gases e partículas pelos veículos.", "B": "Barulho do trânsito.", "C": "Sujeira nas ruas.", "D": "Congestionamento."}, "resposta": "A", "comentario": "Veículos emitem CO2, CO, NOx e material particulado."},
    {"modulo": "2", "numero": "86", "questao": "Como reduzir a poluição veicular?", "alternativas": {"A": "Manutenção em dia e condução econômica.", "B": "Acelerar mais.", "C": "Usar gasolina adulterada.", "D": "Não fazer revisões."}, "resposta": "A", "comentario": "Veículos bem regulados poluem menos."},
    {"modulo": "2", "numero": "87", "questao": "O que são primeiros socorros?", "alternativas": {"A": "Atendimento inicial à vítima até chegada de socorro especializado.", "B": "Atendimento apenas em hospitais.", "C": "Remover a vítima sempre.", "D": "Dar medicamentos."}, "resposta": "A", "comentario": "Primeiros socorros são procedimentos básicos de emergência."},
    {"modulo": "2", "numero": "88", "questao": "Qual a primeira atitude ao presenciar um acidente?", "alternativas": {"A": "Sinalizar o local e acionar socorro (SAMU 192).", "B": "Remover as vítimas imediatamente.", "C": "Fugir do local.", "D": "Gritar por ajuda."}, "resposta": "A", "comentario": "Sinalizar evita novos acidentes e o socorro deve ser acionado."},
    {"modulo": "2", "numero": "89", "questao": "Quando mover uma vítima de acidente?", "alternativas": {"A": "Somente se houver risco iminente (fogo, afogamento).", "B": "Sempre, para levá-la ao hospital.", "C": "Nunca.", "D": "Quando ela pedir."}, "resposta": "A", "comentario": "Mover incorretamente pode agravar lesões na coluna."},
    {"modulo": "2", "numero": "90", "questao": "O que fazer se a vítima estiver consciente?", "alternativas": {"A": "Acalmá-la e mantê-la imóvel até o socorro.", "B": "Dar água.", "C": "Fazer ela andar.", "D": "Dar medicamentos."}, "resposta": "A", "comentario": "Manter a calma e aguardar socorro especializado."},
    {"modulo": "2", "numero": "91", "questao": "O que é hemorragia?", "alternativas": {"A": "Perda de sangue por rompimento de vasos.", "B": "Falta de ar.", "C": "Dor de cabeça.", "D": "Tontura."}, "resposta": "A", "comentario": "Hemorragias podem ser internas ou externas."},
    {"modulo": "2", "numero": "92", "questao": "Como controlar uma hemorragia externa?", "alternativas": {"A": "Comprimir o local com pano limpo.", "B": "Lavar com água.", "C": "Aplicar torniquete sempre.", "D": "Ignorar."}, "resposta": "A", "comentario": "A compressão direta é a primeira medida."},
    {"modulo": "2", "numero": "93", "questao": "O que é fratura?", "alternativas": {"A": "Quebra ou trinca em um osso.", "B": "Torção.", "C": "Luxação.", "D": "Contusão."}, "resposta": "A", "comentario": "Fraturas podem ser expostas ou fechadas."},
    {"modulo": "2", "numero": "94", "questao": "O que fazer em caso de suspeita de fratura?", "alternativas": {"A": "Imobilizar o membro e aguardar socorro.", "B": "Tentar colocar o osso no lugar.", "C": "Fazer massagem.", "D": "Movimentar o membro."}, "resposta": "A", "comentario": "Imobilização previne agravamento da lesão."},
    {"modulo": "2", "numero": "95", "questao": "O que é estado de choque?", "alternativas": {"A": "Falência circulatória com risco de morte.", "B": "Susto.", "C": "Nervosismo.", "D": "Cansaço."}, "resposta": "A", "comentario": "O choque é uma emergência médica grave."},
    {"modulo": "2", "numero": "96", "questao": "Quais os sinais de estado de choque?", "alternativas": {"A": "Pele fria, palidez, pulso fraco, confusão.", "B": "Pele quente.", "C": "Agitação.", "D": "Fome."}, "resposta": "A", "comentario": "Reconhecer os sinais ajuda no atendimento."},
    {"modulo": "2", "numero": "97", "questao": "O que fazer com vítima em estado de choque?", "alternativas": {"A": "Deitar com pernas elevadas, manter aquecida.", "B": "Dar água.", "C": "Fazer ela andar.", "D": "Deixar sentada."}, "resposta": "A", "comentario": "Elevar as pernas ajuda o retorno venoso."},
    {"modulo": "2", "numero": "98", "questao": "O que é PCR (Parada Cardiorrespiratória)?", "alternativas": {"A": "Cessação dos batimentos cardíacos e da respiração.", "B": "Dor no peito.", "C": "Falta de ar leve.", "D": "Desmaio simples."}, "resposta": "A", "comentario": "PCR é uma emergência que requer RCP imediata."},
    {"modulo": "2", "numero": "99", "questao": "O que fazer em caso de PCR?", "alternativas": {"A": "Iniciar RCP (compressões torácicas) e chamar socorro.", "B": "Dar água.", "C": "Esperar a vítima acordar.", "D": "Não fazer nada."}, "resposta": "A", "comentario": "RCP precoce aumenta chances de sobrevivência."},
    {"modulo": "2", "numero": "100", "questao": "Qual o ritmo das compressões na RCP?", "alternativas": {"A": "100 a 120 compressões por minuto.", "B": "50 por minuto.", "C": "200 por minuto.", "D": "Qualquer ritmo."}, "resposta": "A", "comentario": "O ritmo adequado otimiza a circulação artificial."},
    
    # MÓDULO 3 - Na Direção da Segurança (21-80)
    {"modulo": "3", "numero": "21", "questao": "O CTB (Código de Trânsito Brasileiro) foi instituído por qual lei?", "alternativas": {"A": "Lei 9.503/1997.", "B": "Lei 8.666/1993.", "C": "Lei 10.406/2002.", "D": "Lei 9.099/1995."}, "resposta": "A", "comentario": "O CTB está em vigor desde 1998."},
    {"modulo": "3", "numero": "22", "questao": "Qual o órgão máximo do Sistema Nacional de Trânsito?", "alternativas": {"A": "CONTRAN - Conselho Nacional de Trânsito.", "B": "DENATRAN.", "C": "DETRAN.", "D": "PRF."}, "resposta": "A", "comentario": "O CONTRAN é o órgão normativo máximo."},
    {"modulo": "3", "numero": "23", "questao": "O que é infração de trânsito?", "alternativas": {"A": "Inobservância de norma do CTB.", "B": "Crime grave.", "C": "Apenas excesso de velocidade.", "D": "Acidente."}, "resposta": "A", "comentario": "Infrações são violações às regras de trânsito."},
    {"modulo": "3", "numero": "24", "questao": "Quais são as naturezas das infrações de trânsito?", "alternativas": {"A": "Leve, média, grave e gravíssima.", "B": "Simples e complexa.", "C": "Pequena e grande.", "D": "Normal e especial."}, "resposta": "A", "comentario": "As infrações são classificadas em quatro categorias."},
    {"modulo": "3", "numero": "25", "questao": "Quantos pontos na CNH uma infração leve gera?", "alternativas": {"A": "3 pontos.", "B": "4 pontos.", "C": "5 pontos.", "D": "7 pontos."}, "resposta": "A", "comentario": "Infração leve = 3 pontos na CNH."},
    {"modulo": "3", "numero": "26", "questao": "Quantos pontos na CNH uma infração média gera?", "alternativas": {"A": "4 pontos.", "B": "3 pontos.", "C": "5 pontos.", "D": "7 pontos."}, "resposta": "A", "comentario": "Infração média = 4 pontos na CNH."},
    {"modulo": "3", "numero": "27", "questao": "Quantos pontos na CNH uma infração grave gera?", "alternativas": {"A": "5 pontos.", "B": "4 pontos.", "C": "3 pontos.", "D": "7 pontos."}, "resposta": "A", "comentario": "Infração grave = 5 pontos na CNH."},
    {"modulo": "3", "numero": "28", "questao": "Quantos pontos na CNH uma infração gravíssima gera?", "alternativas": {"A": "7 pontos.", "B": "5 pontos.", "C": "4 pontos.", "D": "10 pontos."}, "resposta": "A", "comentario": "Infração gravíssima = 7 pontos na CNH."},
    {"modulo": "3", "numero": "29", "questao": "Com quantos pontos o condutor pode ter a CNH suspensa?", "alternativas": {"A": "20 pontos em 12 meses (ou 40 para condutores profissionais).", "B": "10 pontos.", "C": "30 pontos.", "D": "50 pontos."}, "resposta": "A", "comentario": "O limite varia conforme o tipo de condutor."},
    {"modulo": "3", "numero": "30", "questao": "O que é penalidade de advertência por escrito?", "alternativas": {"A": "Comunicação ao condutor sobre infração leve, sem multa.", "B": "Multa.", "C": "Suspensão.", "D": "Cassação."}, "resposta": "A", "comentario": "Aplicada a infrações leves quando o condutor não é reincidente."},
    {"modulo": "3", "numero": "31", "questao": "O que é apreensão do veículo?", "alternativas": {"A": "Recolhimento do veículo ao depósito.", "B": "Retenção temporária.", "C": "Multa.", "D": "Suspensão da CNH."}, "resposta": "A", "comentario": "O veículo é removido para depósito público."},
    {"modulo": "3", "numero": "32", "questao": "O que é cassação da CNH?", "alternativas": {"A": "Cancelamento do direito de dirigir.", "B": "Suspensão temporária.", "C": "Multa grave.", "D": "Advertência."}, "resposta": "A", "comentario": "A cassação exige novo processo de habilitação."},
    {"modulo": "3", "numero": "33", "questao": "Por quanto tempo pode ser suspensa a CNH?", "alternativas": {"A": "De 2 meses a 8 meses.", "B": "1 mês.", "C": "1 ano.", "D": "5 anos."}, "resposta": "A", "comentario": "O período varia conforme a infração."},
    {"modulo": "3", "numero": "34", "questao": "Dirigir sem CNH ou com CNH cassada é crime?", "alternativas": {"A": "Sim, conforme o CTB.", "B": "Não, apenas infração.", "C": "Apenas se causar acidente.", "D": "Nunca."}, "resposta": "A", "comentario": "É crime previsto no art. 309 do CTB."},
    {"modulo": "3", "numero": "35", "questao": "Qual a velocidade máxima em vias locais urbanas?", "alternativas": {"A": "30 km/h.", "B": "40 km/h.", "C": "60 km/h.", "D": "80 km/h."}, "resposta": "A", "comentario": "Vias locais têm limite de 30 km/h."},
    {"modulo": "3", "numero": "36", "questao": "Qual a velocidade máxima em vias coletoras urbanas?", "alternativas": {"A": "40 km/h.", "B": "30 km/h.", "C": "60 km/h.", "D": "80 km/h."}, "resposta": "A", "comentario": "Vias coletoras têm limite de 40 km/h."},
    {"modulo": "3", "numero": "37", "questao": "Qual a velocidade máxima em vias arteriais urbanas?", "alternativas": {"A": "60 km/h.", "B": "40 km/h.", "C": "80 km/h.", "D": "110 km/h."}, "resposta": "A", "comentario": "Vias arteriais têm limite de 60 km/h."},
    {"modulo": "3", "numero": "38", "questao": "Qual a velocidade máxima em vias de trânsito rápido?", "alternativas": {"A": "80 km/h.", "B": "60 km/h.", "C": "110 km/h.", "D": "120 km/h."}, "resposta": "A", "comentario": "Vias de trânsito rápido têm limite de 80 km/h."},
    {"modulo": "3", "numero": "39", "questao": "Qual a velocidade máxima em rodovias para automóveis?", "alternativas": {"A": "110 km/h.", "B": "80 km/h.", "C": "120 km/h.", "D": "60 km/h."}, "resposta": "A", "comentario": "Rodovias de pista dupla permitem até 110 km/h para carros."},
    {"modulo": "3", "numero": "40", "questao": "Qual a velocidade máxima em estradas (rodovias não pavimentadas)?", "alternativas": {"A": "60 km/h.", "B": "80 km/h.", "C": "110 km/h.", "D": "40 km/h."}, "resposta": "A", "comentario": "Estradas de terra têm limite de 60 km/h."},
    {"modulo": "3", "numero": "41", "questao": "O que é habilitação?", "alternativas": {"A": "Autorização legal para conduzir veículos.", "B": "Registro do veículo.", "C": "Seguro obrigatório.", "D": "Licenciamento."}, "resposta": "A", "comentario": "A habilitação comprova aptidão para dirigir."},
    {"modulo": "3", "numero": "42", "questao": "Qual a idade mínima para obter a CNH categoria B?", "alternativas": {"A": "18 anos.", "B": "16 anos.", "C": "21 anos.", "D": "25 anos."}, "resposta": "A", "comentario": "A idade mínima é 18 anos para todas as categorias."},
    {"modulo": "3", "numero": "43", "questao": "O que é a Permissão para Dirigir?", "alternativas": {"A": "Documento provisório válido por 1 ano para novos condutores.", "B": "CNH definitiva.", "C": "Autorização para dirigir caminhões.", "D": "Documento internacional."}, "resposta": "A", "comentario": "Durante o primeiro ano, o condutor tem a PPD."},
    {"modulo": "3", "numero": "44", "questao": "O que acontece se o condutor cometer infração grave durante a Permissão?", "alternativas": {"A": "Deve reiniciar todo o processo de habilitação.", "B": "Recebe apenas multa.", "C": "Nada acontece.", "D": "Recebe advertência."}, "resposta": "A", "comentario": "Infrações graves ou gravíssimas anulam a permissão."},
    {"modulo": "3", "numero": "45", "questao": "Qual categoria de CNH permite dirigir automóvel?", "alternativas": {"A": "B.", "B": "A.", "C": "C.", "D": "D."}, "resposta": "A", "comentario": "Categoria B é para veículos de 4 rodas até 3.500 kg."},
    {"modulo": "3", "numero": "46", "questao": "Qual categoria de CNH permite dirigir motocicleta?", "alternativas": {"A": "A.", "B": "B.", "C": "C.", "D": "D."}, "resposta": "A", "comentario": "Categoria A é para veículos de 2 ou 3 rodas."},
    {"modulo": "3", "numero": "47", "questao": "Qual categoria de CNH permite dirigir caminhão?", "alternativas": {"A": "C.", "B": "B.", "C": "A.", "D": "D."}, "resposta": "A", "comentario": "Categoria C é para veículos de carga acima de 3.500 kg."},
    {"modulo": "3", "numero": "48", "questao": "Qual categoria de CNH permite dirigir ônibus?", "alternativas": {"A": "D.", "B": "C.", "C": "B.", "D": "E."}, "resposta": "A", "comentario": "Categoria D é para veículos de transporte de passageiros."},
    {"modulo": "3", "numero": "49", "questao": "O que é licenciamento anual?", "alternativas": {"A": "Obrigação de renovar a autorização do veículo todo ano.", "B": "Renovação da CNH.", "C": "Seguro do veículo.", "D": "IPVA."}, "resposta": "A", "comentario": "O licenciamento é obrigatório para circular."},
    {"modulo": "3", "numero": "50", "questao": "O que é DPVAT?", "alternativas": {"A": "Seguro obrigatório para vítimas de acidentes de trânsito.", "B": "Imposto sobre veículos.", "C": "Taxa de licenciamento.", "D": "Multa."}, "resposta": "A", "comentario": "O DPVAT cobre despesas médicas e indenizações."},
    
    # MÓDULO 4 - Cuidar, Agir e Preservar (21-36)
    {"modulo": "4", "numero": "21", "questao": "O que é meio ambiente?", "alternativas": {"A": "Conjunto de condições naturais e sociais que influenciam os seres vivos.", "B": "Apenas florestas.", "C": "Apenas animais.", "D": "Apenas o ar."}, "resposta": "A", "comentario": "Meio ambiente inclui todos os elementos naturais e sociais."},
    {"modulo": "4", "numero": "22", "questao": "Como o trânsito afeta o meio ambiente?", "alternativas": {"A": "Através de poluição do ar, sonora e geração de resíduos.", "B": "Não afeta.", "C": "Apenas positivamente.", "D": "Apenas em cidades grandes."}, "resposta": "A", "comentario": "Veículos são fontes significativas de poluição."},
    {"modulo": "4", "numero": "23", "questao": "O que é poluição atmosférica veicular?", "alternativas": {"A": "Emissão de gases poluentes pelos veículos.", "B": "Barulho dos carros.", "C": "Vazamento de óleo.", "D": "Descarte de pneus."}, "resposta": "A", "comentario": "Motores emitem CO, CO2, NOx e hidrocarbonetos."},
    {"modulo": "4", "numero": "24", "questao": "Qual gás veicular contribui para o efeito estufa?", "alternativas": {"A": "CO2 (dióxido de carbono).", "B": "Oxigênio.", "C": "Nitrogênio.", "D": "Hélio."}, "resposta": "A", "comentario": "O CO2 é o principal gás de efeito estufa emitido por veículos."},
    {"modulo": "4", "numero": "25", "questao": "O que é monóxido de carbono (CO)?", "alternativas": {"A": "Gás tóxico emitido por veículos.", "B": "Gás inofensivo.", "C": "Combustível.", "D": "Oxigênio."}, "resposta": "A", "comentario": "O CO é perigoso por ser inodoro e tóxico."},
    {"modulo": "4", "numero": "26", "questao": "Como reduzir a emissão de poluentes do veículo?", "alternativas": {"A": "Manutenção em dia e condução econômica.", "B": "Acelerar mais.", "C": "Usar combustível de baixa qualidade.", "D": "Não fazer revisões."}, "resposta": "A", "comentario": "Veículos bem regulados poluem menos."},
    {"modulo": "4", "numero": "27", "questao": "O que é poluição sonora no trânsito?", "alternativas": {"A": "Ruído excessivo causado por veículos.", "B": "Poluição do ar.", "C": "Vazamento de óleo.", "D": "Descarte de lixo."}, "resposta": "A", "comentario": "Buzinas, motores e escapamentos causam ruído."},
    {"modulo": "4", "numero": "28", "questao": "Quais os efeitos da poluição sonora na saúde?", "alternativas": {"A": "Estresse, perda auditiva, problemas cardiovasculares.", "B": "Nenhum.", "C": "Apenas irritação.", "D": "Melhora do sono."}, "resposta": "A", "comentario": "O ruído excessivo causa diversos problemas de saúde."},
    {"modulo": "4", "numero": "29", "questao": "O que é mobilidade sustentável?", "alternativas": {"A": "Uso de transportes que minimizam impactos ambientais.", "B": "Usar apenas carros.", "C": "Não se locomover.", "D": "Usar apenas avião."}, "resposta": "A", "comentario": "Inclui transporte público, bicicleta e veículos elétricos."},
    {"modulo": "4", "numero": "30", "questao": "Quais alternativas ao carro individual?", "alternativas": {"A": "Transporte público, carona, bicicleta, caminhada.", "B": "Apenas helicóptero.", "C": "Nenhuma.", "D": "Apenas táxi."}, "resposta": "A", "comentario": "Alternativas reduzem congestionamento e poluição."},
    {"modulo": "4", "numero": "31", "questao": "O que é descarte correto de pneus?", "alternativas": {"A": "Entregar em pontos de coleta ou ecopontos.", "B": "Jogar no lixo comum.", "C": "Queimar.", "D": "Abandonar na rua."}, "resposta": "A", "comentario": "Pneus devem ser reciclados ou reutilizados."},
    {"modulo": "4", "numero": "32", "questao": "O que fazer com óleo usado do motor?", "alternativas": {"A": "Entregar em postos de coleta.", "B": "Jogar no ralo.", "C": "Descartar no lixo.", "D": "Enterrar."}, "resposta": "A", "comentario": "Óleo usado é altamente poluente e deve ser reciclado."},
    {"modulo": "4", "numero": "33", "questao": "Por que não jogar lixo pela janela do carro?", "alternativas": {"A": "Polui o ambiente e pode causar acidentes.", "B": "É permitido.", "C": "Não tem problema.", "D": "Apenas é feio."}, "resposta": "A", "comentario": "É infração e prejudica o meio ambiente."},
    {"modulo": "4", "numero": "34", "questao": "O que é direção consciente?", "alternativas": {"A": "Dirigir considerando segurança e impacto ambiental.", "B": "Dirigir rápido.", "C": "Dirigir sem cinto.", "D": "Dirigir alcoolizado."}, "resposta": "A", "comentario": "Combina direção defensiva com responsabilidade ambiental."},
    {"modulo": "4", "numero": "35", "questao": "Como o motorista pode contribuir para um trânsito melhor?", "alternativas": {"A": "Respeitando regras, outros usuários e o meio ambiente.", "B": "Sendo agressivo.", "C": "Ignorando pedestres.", "D": "Buzinando constantemente."}, "resposta": "A", "comentario": "Cidadania no trânsito beneficia a todos."},
    {"modulo": "4", "numero": "36", "questao": "Qual a relação entre trânsito e qualidade de vida?", "alternativas": {"A": "Trânsito seguro e sustentável melhora a saúde e o bem-estar.", "B": "Não há relação.", "C": "Trânsito não afeta a vida.", "D": "Apenas afeta economicamente."}, "resposta": "A", "comentario": "Menos acidentes e poluição significam melhor qualidade de vida."},
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
