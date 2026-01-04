import streamlit as st
import pandas as pd
from machine_learning import ObesityPredictor

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Prevendo Obesidade", layout="wide")

# --- CSS CUSTOMIZADO (SEU ESTILO + RECOMENDAÇÃO) ---
st.markdown("""
<style>
    /* Força cursor pointer em botões e inputs */
    .stButton button, div[data-baseweb="select"], div[data-baseweb="radio"] {
        cursor: pointer !important;
    }
    
    /* Estilo do botão principal     */
    .stButton button {
        background-color: rgba(61, 213, 109, 0.7);
        color: #fff;
        font-weight: bold;
        border: none;
        width: 100%;
        padding: 10px;
    }
    .stButton button:hover {
        background-color: rgb(61, 157, 243);
    }

    .st-emotion-cache-lpgk4i,   
    .st-emotion-cache-lpgk4i:hover{
        color: white!important;
    }       
            
    .stElementContainer.element-container.st-emotion-cache-zh2fnc.ek2vi381{
        width: 100% !important;     
    }

    /* Container das barras de probabilidade  */
    .bar-chart-container {
        display: flex;
        align-items: flex-end; /* Alinha as barras na base */
        justify-content: space-between;
        height: 280px; /* Altura fixa */
        background-color: #1e1e1e1f; /* Fundo Escuro */
        border-radius: 12px;
        padding: 25px;
        margin-top: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    
    .bar-wrapper {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-end;
        width: 13%; 
        height: 100%;
    }
    
    .probability-text {
        font-weight: bold;
        font-size: 14px;
        margin-bottom: 8px;
        color: #FFFFFF;
        text-shadow: 0px 1px 2px rgba(0,0,0,0.5);
    }
    
    .bar {
        width: 100%;
        border-radius: 6px 6px 0 0;
        transition: height 0.8s ease-in-out;
        box-shadow: 0px 0px 10px rgba(0,0,0,0.5);
    }
    
    .label-text {
        font-size: 11px;
        text-align: center;
        margin-top: 10px;
        color: #E0E0E0;
        font-weight: 500;
        line-height: 1.2;
        font-family: sans-serif;
    }

    .recommendation-box {
        background-color: #f0f2f6;
        border-left: 5px solid rgba(61, 213, 109, 1); /* Verde combinando com botão */
        padding: 15px;
        border-radius: 5px;
        margin-top: 15px;
        font-size: 14px;
        color: #31333F;
        margin-bottom: 40px;
    }
    .recommendation-link {
        color: rgba(61, 213, 109, 1);
        font-weight: bold;
        text-decoration: none;
    }
    .recommendation-link:hover {
        text-decoration: underline;
        color: rgb(61, 157, 243);
    }
    /* Oculta navegação padrão de páginas no sidebar */
    [data-testid="stSidebarNav"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

# --- FUNÇÕES AUXILIARES ---

def get_class_info(classe_ingles):
    # (Nome em Português, Cor Hexadecimal)
    mapa = {
        'Insufficient_Weight': ('Abaixo do Peso', '#00E676'),      # Verde Neon
        'Normal_Weight':       ('Peso Normal',    '#00C853'),      # Verde Forte
        'Overweight_Level_I':  ('Sobrepeso G1',   '#FFD600'),      # Amarelo Ouro
        'Overweight_Level_II': ('Sobrepeso G2',   '#FFAB00'),      # Laranja Vivo
        'Obesity_Type_I':      ('Obesidade G1',   '#FF6D00'),      # Laranja Avermelhado
        'Obesity_Type_II':     ('Obesidade G2',   '#D50000'),      # Vermelho Intenso
        'Obesity_Type_III':    ('Obesidade G3',   '#C51162')       # Magenta/Vinho
    }
    return mapa.get(classe_ingles, (classe_ingles, '#ccc'))

def get_recommendations(classe_pt):
    # Retorna (Texto da recomendação, Texto do Link, URL do Link)
    if 'Obesidade' in classe_pt:
        return (
            "A obesidade é uma doença crônica. Recomendamos buscar orientação médica (endocrinologista) e nutricional para um plano seguro.",
            "Diretrizes Brasileiras de Obesidade (ABESO)",
            "https://abeso.org.br/diretrizes/"
        )
    elif 'Sobrepeso' in classe_pt:
        return (
            "Sinal de alerta. Pequenas mudanças nos hábitos, como aumentar a ingestão de água e caminhar 30min por dia, podem reverter esse quadro.",
            "Guia Alimentar para a População Brasileira",
            "https://bvsms.saude.gov.br/bvs/publicacoes/guia_alimentar_populacao_brasileira_2ed.pdf"
        )
    elif 'Abaixo do Peso' in classe_pt:
        return (
            "Estar abaixo do peso requer atenção para evitar deficiências nutricionais. Consulte um nutricionista para adequar a dieta.",
            "Dicas de Nutrição (Saúde Brasil)",
            "https://www.gov.br/saude/pt-br"
        )
    else: # Peso Normal
        return (
            "Excelente! Para manter seu peso saudável, priorize alimentos in natura e mantenha uma rotina ativa de exercícios.",
            "Recomendações da OMS para Atividade Física",
            "https://www.who.int/news-room/fact-sheets/detail/physical-activity"
        )

def build_clinical_insights(user_data, pred_label):
    """Gera alertas praticos com base no perfil informado e no nivel previsto."""
    severity = {
        'Insufficient_Weight': 0,
        'Normal_Weight': 1,
        'Overweight_Level_I': 2,
        'Overweight_Level_II': 3,
        'Obesity_Type_I': 4,
        'Obesity_Type_II': 5,
        'Obesity_Type_III': 6,
    }.get(pred_label, 0)

    insights = []  # cada item: {"title": str, "lines": [str, ...]}
    gender = user_data.get('Gender')
    age = user_data.get('Age')

    if user_data.get('family_history') == 'yes' and severity >= 4:
        insights.append({
            "title": "Historico familiar",
            "lines": [
                "Pacientes em graus II e III costumam ter historico de obesidade na familia; inclua a triagem familiar no plano de ação.",
                "Considere intervenções que envolvam rotina alimentar e atividade fisica do nucleo familiar."
            ]
        })
    elif user_data.get('family_history') == 'yes':
        insights.append({
            "title": "Historico familiar",
            "lines": [
                "Familia com obesidade aumenta a chance de progressão; acompanhe com revisões periodicas.",
                "Oriente a familia sobre sinais precoces e metas conjuntas."
            ]
        })

    if user_data.get('SCC') == 'no':
        insights.append({
            "title": "Monitoração calórica",
            "lines": [
                "O registro alimentar costuma ser ausente nos graus graves; introduza o uso de um diario/cálculo simples para controle de calorias.",
                "Sugira aplicativos ou planilhas rápidas que somem calorias de forma prática."
            ]
        })

    faf = user_data.get('FAF', 0)
    if faf == 0 and severity >= 4:
        insights.append({
            "title": "Atividade fisica",
            "lines": [
                "O paciente apresenta sedentarismo total com obesidade avançada: iniciar plano supervisionado e progressivo para evitar lesão.",
                "Combine fortalecimento leve + caminhada curta e aumente gradualmente."
            ]
        })
    elif faf <= 1 and severity >= 2:
        insights.append({
            "title": "Atividade fisica",
            "lines": [
                "Baixa atividade: alinhar dieta estruturada e progressão de exercicios para conter ganho.",
                "Metas semanais curtas (ex.: 2-3 sessões leves) ajudam na adesão."
            ]
        })

    if age is not None and age <= 30 and severity >= 3:
        insights.append({
            "title": "Adulto jovem",
            "lines": [
                "Obesidade severa em faixa jovem pede abordagem precoce e intensiva.",
                "Reforce orientações sobre fertilidade, metabolismo e longo prazo."
            ]
        })

    if gender == 'Male' and pred_label == 'Obesity_Type_II':
        insights.append({
            "title": "Perfil masculino",
            "lines": [
                "Homens tendem a aparecer em Grau II; avalie rotina laboral, sono e ingestão proteica.",
                "Cheque circunferência abdominal e risco cardiometabolico."
            ]
        })
    if gender == 'Female' and pred_label == 'Obesity_Type_III':
        insights.append({
            "title": "Perfil feminino",
            "lines": [
                "Mulheres em Grau III se beneficiam de acompanhamento multidisciplinar intensivo.",
                "Inclua suporte psicologico e manejo de deficiências micronutricionais."
            ]
        })

    if user_data.get('FCVC') == 3 and severity >= 4:
        insights.append({
            "title": "Consumo de vegetais",
            "lines": [
                "Mesmo relatando vegetais sempre, o balanco calórico pode estar positivo.",
                "Revise molhos, porções e acompanhamentos calóricos."
            ]
        })

    if user_data.get('CH2O') == 3 and severity >= 4:
        insights.append({
            "title": "Liquidos",
            "lines": [
                "Alto consumo de líquidos pode incluir bebidas calóricas; diferencie água de sucos/refrigerantes.",
                "Estimule água pura e reduza bebidas adoçadas."
            ]
        })

    calc = user_data.get('CALC')
    if calc in ['Sometimes', 'Frequently', 'Always'] and severity >= 3:
        insights.append({
            "title": "Alcool",
            "lines": [
                "Mesmo ocasional, alcool soma calorias vazias e piora controle de apetite.",
                "Negocie redução ou pausas semanais, especialmente em graus elevados."
            ]
        })

    if user_data.get('SMOKE') == 'yes':
        insights.append({
            "title": "Tabagismo",
            "lines": [
                "Apesar de raro, obesidade + tabagismo aumenta risco cardiometabolico.",
                "Ofereça apoio para cessação e ajuste de peso no processo."
            ]
        })

    return insights

@st.cache_resource
def get_model():
    model = ObesityPredictor('Obesity.csv')
    acc = model.train()
    return model, acc

try:
    predictor, accuracy = get_model()
except Exception as e:
    st.error(f"Erro ao carregar modelo. {e}")
    st.stop()

# --- INTERFACE SIDEBAR ---
st.sidebar.header("📋 Dados do Paciente")

gender = st.sidebar.selectbox("Gênero", ["Masculino", "Feminino"])
age = st.sidebar.slider("Idade", 14, 80, 25)
height = st.sidebar.number_input("Altura (m)", 1.40, 2.20, 1.70)
weight = st.sidebar.number_input("Peso (kg)", 30.0, 200.0, 70.0)

st.sidebar.markdown("---")
st.sidebar.subheader("Histórico e Hábitos")

family = st.sidebar.selectbox("Histórico Familiar de Obesidade?", ["Sim", "Não"])
favc = st.sidebar.selectbox("Consome alta caloria frequentemente?", ["Sim", "Não"])
fcvc = st.sidebar.selectbox("Consumo de Vegetais", ["Raramente", "Às Vezes", "Sempre"])
ncp = st.sidebar.slider("Refeições Principais por dia", 1, 4, 3)
caec = st.sidebar.selectbox("Comer entre refeições", ["Não", "Às Vezes", "Frequentemente", "Sempre"])
smoke = st.sidebar.selectbox("Fumante?", ["Sim", "Não"])
ch2o = st.sidebar.selectbox("Água por dia", ["Menos de 1L", "Entre 1L e 2L", "Mais de 2L"])
scc = st.sidebar.selectbox("Monitora Calorias?", ["Sim", "Não"])
faf = st.sidebar.selectbox("Atividade Física Semanal", ["Nenhuma", "1 a 2 dias", "3 a 4 dias", "Mais de 4 dias"])
tue = st.sidebar.selectbox("Tempo em Telas/Dispositivos", ["0-2 horas", "3-5 horas", "Mais de 5 horas"])
calc = st.sidebar.selectbox("Consumo de Álcool", ["Não", "Às Vezes", "Frequentemente", "Sempre"])
mtrans = st.sidebar.selectbox("Transporte Principal", ["Transporte Público", "Caminhada", "Carro", "Moto", "Bicicleta"])

st.sidebar.markdown("---")
botao_diagnostico = st.sidebar.button("🔍 Realizar Diagnóstico")

# Mapeamento Inputs -> Modelo
user_data = {
    'Gender': 'Male' if gender == "Masculino" else 'Female',
    'Age': age, 'Height': height, 'Weight': weight,
    'family_history': 'yes' if family == "Sim" else 'no',
    'FAVC': 'yes' if favc == "Sim" else 'no',
    'FCVC': 1 if fcvc == "Raramente" else 2 if fcvc == "Às Vezes" else 3,
    'NCP': ncp,
    'CAEC': 'no' if caec == "Não" else 'Sometimes' if caec == "Às Vezes" else 'Frequently' if caec == "Frequentemente" else 'Always',
    'SMOKE': 'yes' if smoke == "Sim" else 'no',
    'CH2O': 1 if ch2o == "Menos de 1L" else 2 if ch2o == "Entre 1L e 2L" else 3,
    'SCC': 'yes' if scc == "Sim" else 'no',
    'FAF': 0 if faf == "Nenhuma" else 1 if faf == "1 a 2 dias" else 2 if faf == "3 a 4 dias" else 3,
    'TUE': 0 if tue == "0-2 horas" else 1 if tue == "3-5 horas" else 2,
    'CALC': 'no' if calc == "Não" else 'Sometimes' if calc == "Às Vezes" else 'Frequently' if calc == "Frequentemente" else 'Always',
    'MTRANS': 'Public_Transportation' if mtrans == "Transporte Público" else 'Walking' if mtrans == "Caminhada" else 'Automobile' if mtrans == "Carro" else 'Motorbike' if mtrans == "Moto" else 'Bike'
}

# --- ÁREA PRINCIPAL ---
header_cols = st.columns([4, 1])
with header_cols[0]:
    st.title("🩺 Sistema de Apoio Médico: Obesidade")
    st.markdown("Preencha os dados no menu lateral e clique em **Realizar Diagnóstico**.")
with header_cols[1]:
    if st.button("📈 Análise Exploratória"):
        try:
            st.switch_page("pages/analise_exploratoria.py")
        except Exception:
            st.info("Abra a página 'Análise Exploratória' no menu lateral (modo multipágina).")

if botao_diagnostico:
    
    # 1. Predição
    pred_label, confidence, all_probs = predictor.predict(user_data)
    label_pt, cor_res = get_class_info(pred_label)
    
    # 2. Recomendação
    rec_texto, rec_link_nome, rec_url = get_recommendations(label_pt)
    
    st.divider()
    col_a, col_b = st.columns([3, 1])
    
    with col_a:
        st.subheader("Resultado Indicado:")
        st.markdown(f"<h1 style='color: {cor_res}; margin-top: -20px;'>{label_pt}</h1>", unsafe_allow_html=True)
        
        # --- BOX DE RECOMENDAÇÃO ---
        st.markdown(f"""
        <div class="recommendation-box">
            <b>💡 Recomendação Clínica:</b><br>
            {rec_texto}<br><br>
            <a href="{rec_url}" target="_blank" class="recommendation-link">🔗 {rec_link_nome}</a>
        </div>
        """, unsafe_allow_html=True)
            
    with col_b:
        st.metric("Nível de confiança", f"{confidence:.1%}")

    st.subheader("📊 Análise de Probabilidades por Classe")
    st.markdown("Probabilidade estimada do paciente pertencer a cada grupo:")

    ordem_visual = [
        'Insufficient_Weight', 'Normal_Weight', 
        'Overweight_Level_I', 'Overweight_Level_II',
        'Obesity_Type_I', 'Obesity_Type_II', 'Obesity_Type_III'
    ]
    
    # --- CONSTRUÇÃO DO HTML DAS BARRAS ---
    html_bars = '<div class="bar-chart-container">'
    
    for class_name in ordem_visual:
        prob = all_probs.get(class_name, 0.0)
        nome_pt, cor = get_class_info(class_name)
        
        # Altura da barra
        height_px = max(prob * 100 * 2.5, 4) 
        
        # Se probabilidade < 1%, mostra vazio
        text_display = f"{prob*100:.1f}%" if prob > 0.01 else ""
        
        # HTML sem indentação interna
        html_bars += f'<div class="bar-wrapper">'
        html_bars += f'<span class="probability-text">{text_display}</span>'
        html_bars += f'<div class="bar" style="height: {height_px}px; background-color: {cor};"></div>'
        html_bars += f'<span class="label-text">{nome_pt}</span>'
        html_bars += f'</div>'
    
    html_bars += '</div>'
    
    # RENDERIZAÇÃO FINAL
    st.markdown(html_bars, unsafe_allow_html=True)

    st.subheader("Alertas clínicos orientados por dados")
    clinical_insights = build_clinical_insights(user_data, pred_label)
    if clinical_insights:
        for item in clinical_insights:
            st.markdown(f"### **{item['title']}**")
            for line in item["lines"]:
                st.markdown(f"- {line}")
    else:
        st.markdown("- Perfil sem alertas adicionais relevantes com base na análise exploratória.")

else:
    st.info("👈 Utilize o menu lateral para inserir os dados do paciente.")
    st.markdown(f"**Modelo:** Random Forest | Acurácia Validada: **{accuracy:.1%}**")
