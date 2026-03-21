#!/usr/bin/env python3
"""
Script to complete Module 1 and add more Module 3 questions
"""

import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

NEW_QUESTIONS = [
    # Completando MÓDULO 1 (faltam 56 questões: 211-256, 294-303)
    {"modulo": "1", "numero": "211", "questao": "Por que existem diferentes tipos de placas?", "alternativas": {"A": "Para organizar informações por função: regulamentar, advertir, indicar.", "B": "Para decorar as vias.", "C": "Apenas por tradição.", "D": "Por economia."}, "resposta": "A", "comentario": "Cada tipo tem função específica na comunicação viária."},
    {"modulo": "1", "numero": "212", "questao": "Qual a cor de fundo das placas de regulamentação?", "alternativas": {"A": "Branca.", "B": "Amarela.", "C": "Verde.", "D": "Azul."}, "resposta": "A", "comentario": "Fundo branco com orla vermelha indica regulamentação."},
    {"modulo": "1", "numero": "213", "questao": "Qual a cor de fundo das placas de advertência?", "alternativas": {"A": "Amarela.", "B": "Branca.", "C": "Verde.", "D": "Azul."}, "resposta": "A", "comentario": "Amarelo alerta para perigos ou situações especiais."},
    {"modulo": "1", "numero": "214", "questao": "Qual o formato das placas de regulamentação?", "alternativas": {"A": "Circular.", "B": "Quadrada.", "C": "Triangular.", "D": "Retangular."}, "resposta": "A", "comentario": "Formato circular é padrão para regulamentação."},
    {"modulo": "1", "numero": "215", "questao": "Qual o formato das placas de advertência?", "alternativas": {"A": "Quadrada com diagonal para cima (losango).", "B": "Circular.", "C": "Triangular.", "D": "Retangular."}, "resposta": "A", "comentario": "Losango amarelo indica advertência."},
    {"modulo": "1", "numero": "216", "questao": "O que significa placa com círculo e barra diagonal vermelha?", "alternativas": {"A": "Proibição.", "B": "Obrigação.", "C": "Advertência.", "D": "Indicação."}, "resposta": "A", "comentario": "A barra diagonal indica proibição total."},
    {"modulo": "1", "numero": "217", "questao": "Por que as placas são padronizadas?", "alternativas": {"A": "Para que motoristas entendam em qualquer lugar do país.", "B": "Por economia.", "C": "Por tradição.", "D": "Sem motivo específico."}, "resposta": "A", "comentario": "Padronização garante compreensão universal."},
    {"modulo": "1", "numero": "218", "questao": "O que indica placa com seta curva para direita?", "alternativas": {"A": "Curva à direita à frente.", "B": "Retorno obrigatório.", "C": "Proibido virar.", "D": "Conversão à esquerda."}, "resposta": "A", "comentario": "Seta indica direção da curva."},
    {"modulo": "1", "numero": "219", "questao": "O que indica placa com duas setas em sentidos opostos?", "alternativas": {"A": "Via de mão dupla.", "B": "Retorno.", "C": "Ultrapassagem permitida.", "D": "Bifurcação."}, "resposta": "A", "comentario": "Setas opostas = dois sentidos de circulação."},
    {"modulo": "1", "numero": "220", "questao": "O que indica placa com símbolo de caminhão em aclive?", "alternativas": {"A": "Subida íngreme, veículos pesados devem ter cuidado.", "B": "Proibido caminhões.", "C": "Estacionamento de caminhões.", "D": "Posto de pesagem."}, "resposta": "A", "comentario": "Alerta para subida acentuada."},
    {"modulo": "1", "numero": "221", "questao": "O que indica placa com símbolo de carro caindo na água?", "alternativas": {"A": "Cais ou ribanceira, risco de queda.", "B": "Balsa disponível.", "C": "Lavagem de carros.", "D": "Posto de combustível."}, "resposta": "A", "comentario": "Alerta para proximidade de água."},
    {"modulo": "1", "numero": "222", "questao": "O que indica placa com símbolo de avião?", "alternativas": {"A": "Proximidade de aeroporto.", "B": "Voo proibido.", "C": "Área militar.", "D": "Heliponto."}, "resposta": "A", "comentario": "Indica acesso a aeroporto."},
    {"modulo": "1", "numero": "223", "questao": "O que indica placa com símbolo de âncora?", "alternativas": {"A": "Porto ou atracadouro próximo.", "B": "Praia.", "C": "Pesca proibida.", "D": "Área naval."}, "resposta": "A", "comentario": "Indica área portuária."},
    {"modulo": "1", "numero": "224", "questao": "O que indica placa com símbolo de trem?", "alternativas": {"A": "Passagem de nível ferroviária.", "B": "Estação de trem.", "C": "Metrô.", "D": "Museu ferroviário."}, "resposta": "A", "comentario": "Alerta para cruzamento com trilhos."},
    {"modulo": "1", "numero": "225", "questao": "O que indica cruz de Santo André?", "alternativas": {"A": "Passagem de nível sem barreira.", "B": "Cruzamento comum.", "C": "Igreja próxima.", "D": "Hospital."}, "resposta": "A", "comentario": "Cruz em X indica cruzamento ferroviário."},
    {"modulo": "1", "numero": "226", "questao": "O que indica placa com símbolo de bonde?", "alternativas": {"A": "Trânsito de bondes na via.", "B": "Museu de transportes.", "C": "Estacionamento.", "D": "Ponto turístico."}, "resposta": "A", "comentario": "Alerta para presença de bondes."},
    {"modulo": "1", "numero": "227", "questao": "O que indica placa com símbolo de ventos?", "alternativas": {"A": "Vento lateral forte.", "B": "Área de ventilação.", "C": "Fábrica.", "D": "Posto de gasolina."}, "resposta": "A", "comentario": "Risco de desestabilização por vento."},
    {"modulo": "1", "numero": "228", "questao": "O que indica placa com símbolo de chuva?", "alternativas": {"A": "Pista escorregadia quando molhada.", "B": "Lavagem de carros.", "C": "Área alagável.", "D": "Reservatório."}, "resposta": "A", "comentario": "Alerta para cuidado em dias de chuva."},
    {"modulo": "1", "numero": "229", "questao": "O que indica placa com símbolo de pedras caindo?", "alternativas": {"A": "Risco de queda de pedras.", "B": "Pedreira.", "C": "Construção.", "D": "Montanha."}, "resposta": "A", "comentario": "Comum em áreas de encosta."},
    {"modulo": "1", "numero": "230", "questao": "O que indica placa com símbolo de ponte estreita?", "alternativas": {"A": "Estreitamento da pista em ponte.", "B": "Ponte em construção.", "C": "Pedágio.", "D": "Mirante."}, "resposta": "A", "comentario": "Alerta para redução de largura."},
    {"modulo": "1", "numero": "231", "questao": "O que indica placa de área com desmoronamento?", "alternativas": {"A": "Risco de deslizamento de terra.", "B": "Área de escavação.", "C": "Mina.", "D": "Construção."}, "resposta": "A", "comentario": "Comum em encostas instáveis."},
    {"modulo": "1", "numero": "232", "questao": "O que indica placa de projeção de cascalho?", "alternativas": {"A": "Risco de pedras sendo lançadas por outros veículos.", "B": "Pedreira.", "C": "Brita à venda.", "D": "Construção."}, "resposta": "A", "comentario": "Manter distância em vias não pavimentadas."},
    {"modulo": "1", "numero": "233", "questao": "O que indica placa de pista irregular?", "alternativas": {"A": "Pavimento em más condições.", "B": "Pista nova.", "C": "Obras concluídas.", "D": "Via expressa."}, "resposta": "A", "comentario": "Reduzir velocidade devido a buracos ou ondulações."},
    {"modulo": "1", "numero": "234", "questao": "O que indica placa de largura limitada?", "alternativas": {"A": "Veículos acima da largura indicada não podem passar.", "B": "Via larga à frente.", "C": "Estacionamento.", "D": "Retorno."}, "resposta": "A", "comentario": "Similar à altura limitada, mas para largura."},
    {"modulo": "1", "numero": "235", "questao": "O que indica placa de comprimento limitado?", "alternativas": {"A": "Veículos acima do comprimento indicado não podem passar.", "B": "Via curta.", "C": "Estacionamento para veículos longos.", "D": "Área de carga."}, "resposta": "A", "comentario": "Restrição para veículos longos."},
    {"modulo": "1", "numero": "236", "questao": "O que indica placa de peso por eixo?", "alternativas": {"A": "Limite de peso máximo por eixo do veículo.", "B": "Balança próxima.", "C": "Posto de pesagem.", "D": "Área de carga."}, "resposta": "A", "comentario": "Protege estrutura de pontes e vias."},
    {"modulo": "1", "numero": "237", "questao": "O que indica placa de estacionamento regulamentado?", "alternativas": {"A": "Estacionamento permitido conforme condições indicadas.", "B": "Estacionamento proibido.", "C": "Estacionamento livre.", "D": "Área privada."}, "resposta": "A", "comentario": "Pode ter horários e tempo limitado."},
    {"modulo": "1", "numero": "238", "questao": "O que indica placa de ponto de parada?", "alternativas": {"A": "Local autorizado para parada de ônibus ou táxi.", "B": "Parada obrigatória.", "C": "Estacionamento.", "D": "Área de descanso."}, "resposta": "A", "comentario": "Embarque e desembarque de passageiros."},
    {"modulo": "1", "numero": "239", "questao": "O que indica placa de área de estacionamento?", "alternativas": {"A": "Estacionamento disponível.", "B": "Proibido estacionar.", "C": "Garagem privada.", "D": "Área de manobras."}, "resposta": "A", "comentario": "Símbolo P indica local para estacionar."},
    {"modulo": "1", "numero": "240", "questao": "O que indica placa de número de faixas?", "alternativas": {"A": "Quantidade de faixas disponíveis à frente.", "B": "Velocidade por faixa.", "C": "Largura da via.", "D": "Comprimento do túnel."}, "resposta": "A", "comentario": "Informa sobre configuração da via."},
    {"modulo": "1", "numero": "241", "questao": "O que indica placa de confluência à esquerda?", "alternativas": {"A": "Entrada de veículos pela esquerda.", "B": "Saída pela esquerda.", "C": "Curva à esquerda.", "D": "Retorno."}, "resposta": "A", "comentario": "Atenção para veículos entrando."},
    {"modulo": "1", "numero": "242", "questao": "O que indica placa de confluência à direita?", "alternativas": {"A": "Entrada de veículos pela direita.", "B": "Saída pela direita.", "C": "Curva à direita.", "D": "Retorno."}, "resposta": "A", "comentario": "Atenção para veículos entrando."},
    {"modulo": "1", "numero": "243", "questao": "O que indica placa de entroncamento oblíquo?", "alternativas": {"A": "Junção de via em ângulo oblíquo.", "B": "Curva fechada.", "C": "Retorno.", "D": "Bifurcação."}, "resposta": "A", "comentario": "Via lateral entrando em ângulo."},
    {"modulo": "1", "numero": "244", "questao": "O que indica placa de pista dividida?", "alternativas": {"A": "Via passará a ter canteiro central.", "B": "Via terminando.", "C": "Mão dupla.", "D": "Obras."}, "resposta": "A", "comentario": "Separação física entre sentidos."},
    {"modulo": "1", "numero": "245", "questao": "O que indica placa de fim de pista dividida?", "alternativas": {"A": "Término da separação física entre sentidos.", "B": "Início de túnel.", "C": "Pedágio.", "D": "Retorno."}, "resposta": "A", "comentario": "Atenção para tráfego em sentido oposto."},
    {"modulo": "1", "numero": "246", "questao": "O que indica placa de estreitamento de pista à esquerda?", "alternativas": {"A": "Redução de largura pelo lado esquerdo.", "B": "Curva à esquerda.", "C": "Saída à esquerda.", "D": "Retorno."}, "resposta": "A", "comentario": "Ajustar posição na pista."},
    {"modulo": "1", "numero": "247", "questao": "O que indica placa de estreitamento de pista à direita?", "alternativas": {"A": "Redução de largura pelo lado direito.", "B": "Curva à direita.", "C": "Saída à direita.", "D": "Estacionamento."}, "resposta": "A", "comentario": "Ajustar posição na pista."},
    {"modulo": "1", "numero": "248", "questao": "O que indica placa de alargamento de pista à esquerda?", "alternativas": {"A": "Aumento de largura pelo lado esquerdo.", "B": "Nova faixa.", "C": "Retorno permitido.", "D": "Estacionamento."}, "resposta": "A", "comentario": "Via ficará mais larga."},
    {"modulo": "1", "numero": "249", "questao": "O que indica placa de alargamento de pista à direita?", "alternativas": {"A": "Aumento de largura pelo lado direito.", "B": "Nova faixa.", "C": "Acostamento.", "D": "Saída."}, "resposta": "A", "comentario": "Via ficará mais larga."},
    {"modulo": "1", "numero": "250", "questao": "O que indica placa de fim de faixa à esquerda?", "alternativas": {"A": "Faixa esquerda terminando, mudar de faixa.", "B": "Saída à esquerda.", "C": "Retorno.", "D": "Curva."}, "resposta": "A", "comentario": "Preparar para mudança de faixa."},
    {"modulo": "1", "numero": "251", "questao": "O que indica placa de fim de faixa à direita?", "alternativas": {"A": "Faixa direita terminando, mudar de faixa.", "B": "Saída à direita.", "C": "Estacionamento.", "D": "Curva."}, "resposta": "A", "comentario": "Preparar para mudança de faixa."},
    {"modulo": "1", "numero": "252", "questao": "O que indica placa de faixa adicional de subida?", "alternativas": {"A": "Nova faixa para veículos lentos em aclive.", "B": "Ultrapassagem livre.", "C": "Acostamento.", "D": "Retorno."}, "resposta": "A", "comentario": "Veículos lentos devem usar faixa adicional."},
    {"modulo": "1", "numero": "253", "questao": "O que indica placa de faixa de desaceleração?", "alternativas": {"A": "Faixa para reduzir velocidade antes de sair.", "B": "Faixa de ultrapassagem.", "C": "Acostamento.", "D": "Estacionamento."}, "resposta": "A", "comentario": "Preparar para saída da via principal."},
    {"modulo": "1", "numero": "254", "questao": "O que indica placa de faixa de aceleração?", "alternativas": {"A": "Faixa para ganhar velocidade antes de entrar na via principal.", "B": "Faixa de ultrapassagem.", "C": "Acostamento.", "D": "Retorno."}, "resposta": "A", "comentario": "Acelerar antes de se integrar ao fluxo."},
    {"modulo": "1", "numero": "255", "questao": "O que indica placa de cruzamento em desnível?", "alternativas": {"A": "Vias se cruzam sem interseção direta (viaduto/túnel).", "B": "Cruzamento comum.", "C": "Semáforo.", "D": "Rotatória."}, "resposta": "A", "comentario": "Vias em níveis diferentes."},
    {"modulo": "1", "numero": "256", "questao": "O que indica placa de área de escape?", "alternativas": {"A": "Local para veículos sem freio pararem em emergência.", "B": "Saída de emergência.", "C": "Área de descanso.", "D": "Posto de serviço."}, "resposta": "A", "comentario": "Comum em descidas longas."},
    {"modulo": "1", "numero": "294", "questao": "O que indica seta branca no pavimento apontando para frente?", "alternativas": {"A": "Obrigação de seguir em frente.", "B": "Estacionamento.", "C": "Área de manobra.", "D": "Retorno."}, "resposta": "A", "comentario": "Movimento obrigatório indicado pela seta."},
    {"modulo": "1", "numero": "295", "questao": "O que indica seta branca curva no pavimento?", "alternativas": {"A": "Conversão obrigatória na direção indicada.", "B": "Ultrapassagem.", "C": "Estacionamento.", "D": "Retorno proibido."}, "resposta": "A", "comentario": "Seguir direção da seta."},
    {"modulo": "1", "numero": "296", "questao": "O que indica linha branca tracejada?", "alternativas": {"A": "Permitido mudar de faixa ou ultrapassar.", "B": "Proibido mudar de faixa.", "C": "Faixa de pedestres.", "D": "Estacionamento."}, "resposta": "A", "comentario": "Linha tracejada permite manobras."},
    {"modulo": "1", "numero": "297", "questao": "O que indica linha branca contínua?", "alternativas": {"A": "Proibido mudar de faixa.", "B": "Permitido ultrapassar.", "C": "Faixa de pedestres.", "D": "Estacionamento."}, "resposta": "A", "comentario": "Linha contínua proíbe mudança."},
    {"modulo": "1", "numero": "298", "questao": "O que indica linha amarela tracejada?", "alternativas": {"A": "Permitido ultrapassar com cuidado.", "B": "Proibido ultrapassar.", "C": "Faixa exclusiva.", "D": "Estacionamento."}, "resposta": "A", "comentario": "Amarela tracejada = ultrapassagem permitida."},
    {"modulo": "1", "numero": "299", "questao": "O que indica linha amarela contínua?", "alternativas": {"A": "Proibido ultrapassar.", "B": "Permitido ultrapassar.", "C": "Faixa de ônibus.", "D": "Estacionamento."}, "resposta": "A", "comentario": "Amarela contínua = proibição absoluta."},
    {"modulo": "1", "numero": "300", "questao": "O que indica linha amarela no bordo da via?", "alternativas": {"A": "Proibido parar ou estacionar.", "B": "Estacionamento permitido.", "C": "Faixa de pedestres.", "D": "Ciclovia."}, "resposta": "A", "comentario": "Bordo amarelo = parada proibida."},
    {"modulo": "1", "numero": "301", "questao": "O que indica linha vermelha no bordo da via?", "alternativas": {"A": "Proibido estacionar (pode parar rapidamente).", "B": "Estacionamento livre.", "C": "Faixa de ônibus.", "D": "Ciclovia."}, "resposta": "A", "comentario": "Vermelha permite parada breve, proíbe estacionamento."},
    {"modulo": "1", "numero": "302", "questao": "O que indica marcação de faixa de pedestres?", "alternativas": {"A": "Local de travessia de pedestres.", "B": "Estacionamento.", "C": "Área de manobra.", "D": "Ciclovia."}, "resposta": "A", "comentario": "Pedestres têm preferência na faixa."},
    {"modulo": "1", "numero": "303", "questao": "O que indica marcação de ciclofaixa?", "alternativas": {"A": "Faixa exclusiva para ciclistas.", "B": "Estacionamento de bicicletas.", "C": "Área de pedestres.", "D": "Via compartilhada."}, "resposta": "A", "comentario": "Espaço exclusivo para bicicletas."},
    
    # Mais do MÓDULO 3 (131-200)
    {"modulo": "3", "numero": "131", "questao": "O que é credencial de estacionamento para idoso?", "alternativas": {"A": "Autorização para usar vagas especiais.", "B": "Desconto no estacionamento.", "C": "Isenção de multas.", "D": "Passe livre."}, "resposta": "A", "comentario": "Obtida no órgão de trânsito."},
    {"modulo": "3", "numero": "132", "questao": "Quem tem direito à credencial de idoso?", "alternativas": {"A": "Pessoas com 60 anos ou mais.", "B": "Qualquer pessoa.", "C": "Apenas aposentados.", "D": "Apenas deficientes."}, "resposta": "A", "comentario": "Estatuto do Idoso garante o direito."},
    {"modulo": "3", "numero": "133", "questao": "O que é credencial de estacionamento para deficiente?", "alternativas": {"A": "Autorização para usar vagas especiais.", "B": "Desconto.", "C": "Isenção.", "D": "Passe livre."}, "resposta": "A", "comentario": "Para pessoas com deficiência."},
    {"modulo": "3", "numero": "134", "questao": "O que é CNH especial?", "alternativas": {"A": "Habilitação com restrições ou adaptações para deficientes.", "B": "CNH internacional.", "C": "CNH provisória.", "D": "CNH digital."}, "resposta": "A", "comentario": "Permite dirigir com adaptações no veículo."},
    {"modulo": "3", "numero": "135", "questao": "Deficiente pode dirigir qualquer veículo?", "alternativas": {"A": "Apenas veículo adaptado conforme a deficiência.", "B": "Sim, qualquer um.", "C": "Não pode dirigir.", "D": "Apenas automático."}, "resposta": "A", "comentario": "Adaptação deve constar na CNH e no veículo."},
    {"modulo": "3", "numero": "136", "questao": "O que são adaptações veiculares?", "alternativas": {"A": "Modificações para permitir direção por deficientes.", "B": "Acessórios de som.", "C": "Rodas esportivas.", "D": "Insulfilm."}, "resposta": "A", "comentario": "Devem ser homologadas pelo DETRAN."},
    {"modulo": "3", "numero": "137", "questao": "É obrigatório comunicar adaptação ao DETRAN?", "alternativas": {"A": "Sim, deve constar no documento.", "B": "Não.", "C": "Apenas para venda.", "D": "Opcional."}, "resposta": "A", "comentario": "Alteração de característica exige comunicação."},
    {"modulo": "3", "numero": "138", "questao": "O que é isenção de IPVA para deficientes?", "alternativas": {"A": "Dispensa do pagamento do imposto.", "B": "Desconto.", "C": "Parcelamento.", "D": "Adiamento."}, "resposta": "A", "comentario": "Benefício previsto em lei."},
    {"modulo": "3", "numero": "139", "questao": "Deficiente tem isenção automática de IPVA?", "alternativas": {"A": "Não, deve solicitar e comprovar.", "B": "Sim, automática.", "C": "Não existe isenção.", "D": "Apenas para motos."}, "resposta": "A", "comentario": "Requer processo administrativo."},
    {"modulo": "3", "numero": "140", "questao": "O que é CNH de categoria ACC?", "alternativas": {"A": "Autorização para Conduzir Ciclomotor.", "B": "CNH para caminhão.", "C": "CNH provisória.", "D": "CNH internacional."}, "resposta": "A", "comentario": "Para veículos de até 50cc."},
    {"modulo": "3", "numero": "141", "questao": "Qual a idade mínima para ACC?", "alternativas": {"A": "18 anos.", "B": "16 anos.", "C": "21 anos.", "D": "14 anos."}, "resposta": "A", "comentario": "Mesma idade da CNH."},
    {"modulo": "3", "numero": "142", "questao": "O que é ciclomotor?", "alternativas": {"A": "Veículo de 2 ou 3 rodas com até 50cc.", "B": "Bicicleta elétrica.", "C": "Moto grande.", "D": "Triciclo."}, "resposta": "A", "comentario": "Popularmente chamado de cinquentinha."},
    {"modulo": "3", "numero": "143", "questao": "Ciclomotor pode circular em qualquer via?", "alternativas": {"A": "Não, há restrições em vias de trânsito rápido.", "B": "Sim, todas.", "C": "Apenas em ciclovias.", "D": "Apenas em estradas."}, "resposta": "A", "comentario": "Limitação de velocidade restringe uso."},
    {"modulo": "3", "numero": "144", "questao": "O que é motoneta?", "alternativas": {"A": "Scooter, moto com plataforma para os pés.", "B": "Moto esportiva.", "C": "Triciclo.", "D": "Quadriciclo."}, "resposta": "A", "comentario": "Popular em deslocamentos urbanos."},
    {"modulo": "3", "numero": "145", "questao": "O que é motocicleta?", "alternativas": {"A": "Veículo de 2 rodas com motor acima de 50cc.", "B": "Bicicleta.", "C": "Ciclomotor.", "D": "Triciclo."}, "resposta": "A", "comentario": "Requer CNH categoria A."},
    {"modulo": "3", "numero": "146", "questao": "É obrigatório usar capacete em motocicleta?", "alternativas": {"A": "Sim, condutor e passageiro.", "B": "Apenas o condutor.", "C": "Apenas em rodovias.", "D": "Não é obrigatório."}, "resposta": "A", "comentario": "Segurança obrigatória por lei."},
    {"modulo": "3", "numero": "147", "questao": "É obrigatório usar capacete em ciclomotor?", "alternativas": {"A": "Sim.", "B": "Não.", "C": "Apenas em rodovias.", "D": "Opcional."}, "resposta": "A", "comentario": "Mesma regra da motocicleta."},
    {"modulo": "3", "numero": "148", "questao": "Qual a penalidade por não usar capacete?", "alternativas": {"A": "Infração gravíssima.", "B": "Infração leve.", "C": "Advertência.", "D": "Nenhuma."}, "resposta": "A", "comentario": "Capacete salva vidas."},
    {"modulo": "3", "numero": "149", "questao": "É permitido transportar criança em moto?", "alternativas": {"A": "Apenas se tiver mais de 7 anos e usar capacete.", "B": "Sim, qualquer idade.", "C": "Não.", "D": "Apenas com cadeirinha."}, "resposta": "A", "comentario": "Criança deve alcançar os pedais."},
    {"modulo": "3", "numero": "150", "questao": "É permitido pilotar moto de chinelo?", "alternativas": {"A": "Não, é infração.", "B": "Sim.", "C": "Apenas em cidade.", "D": "Apenas de dia."}, "resposta": "A", "comentario": "Calçado adequado é obrigatório."},
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
