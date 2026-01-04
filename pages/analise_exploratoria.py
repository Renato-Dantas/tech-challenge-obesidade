import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Análise Exploratória", layout="wide")
sns.set_theme(style="whitegrid")

# Paletas conforme notebook
binary_colors = ['#2a08c2', '#d606d0']

# Oculta sidebar e navegação de páginas nesta tela; ajusta padding/topo e largura máxima
st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] { display: none !important; }
        [data-testid="stSidebarNav"] { display: none !important; }
        div[data-testid="collapsedControl"] { display: none !important; }
        .block-container { padding-top: 40px; padding-left: 2rem; padding-right: 2rem; }
        /* Limita largura e centraliza conteúdo em telas largas, com fallback responsivo */
        .block-container { max-width: 1200px; margin: 0 auto; }
        @media (max-width: 768px) {
            .block-container { padding-left: 1rem; padding-right: 1rem; }
        }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def carregar_dados():
    doc = "Obesity.csv"
    df = pd.read_csv(doc)

    novas_colunas = {
        'Gender': 'Genero',
        'Age': 'Idade',
        'Height': 'Altura',
        'Weight': 'Peso',
        'family_history': 'Historico_Familiar',
        'FAVC': 'Consumo_Alta_Caloria',
        'FCVC': 'Freq_Vegetais',
        'NCP': 'Num_Refeicoes',
        'CAEC': 'Comer_Entre_Refeicoes',
        'SMOKE': 'Fumante',
        'CH2O': 'Consumo_Agua',
        'SCC': 'Monitora_Calorias',
        'FAF': 'Freq_Ativ_Fisica',
        'TUE': 'Tempo_Dispositivos',
        'CALC': 'Consumo_Alcool',
        'MTRANS': 'Transporte',
        'Obesity': 'Nivel_Obesidade'
    }
    df = df.rename(columns=novas_colunas)

    traducao_obesidade = {
        'Insufficient_Weight': 'Abaixo do Peso',
        'Normal_Weight': 'Peso Normal',
        'Overweight_Level_I': 'Sobrepeso Grau I',
        'Overweight_Level_II': 'Sobrepeso Grau II',
        'Obesity_Type_I': 'Obesidade Grau I',
        'Obesity_Type_II': 'Obesidade Grau II',
        'Obesity_Type_III': 'Obesidade Grau III'
    }
    traducao_genero = {'Male': 'Masculino', 'Female': 'Feminino'}
    df['Nivel_Obesidade'] = df['Nivel_Obesidade'].replace(traducao_obesidade)
    df['Genero'] = df['Genero'].replace(traducao_genero)

    ordem_obesidade = [
        'Abaixo do Peso', 'Peso Normal',
        'Sobrepeso Grau I', 'Sobrepeso Grau II',
        'Obesidade Grau I', 'Obesidade Grau II', 'Obesidade Grau III'
    ]
    df['Nivel_Obesidade'] = pd.Categorical(df['Nivel_Obesidade'], categories=ordem_obesidade, ordered=True)

    # Demais traduções (mesmo fluxo do notebook)
    df['Historico_Familiar'] = df['Historico_Familiar'].replace({'yes': 'Sim', 'no': 'Não'})
    df['Consumo_Alta_Caloria'] = df['Consumo_Alta_Caloria'].replace({'yes': 'Sim', 'no': 'Não'})
    df['Comer_Entre_Refeicoes'] = df['Comer_Entre_Refeicoes'].replace(
        {'no': 'Não', 'Sometimes': 'Às Vezes', 'Frequently': 'Frequentemente', 'Always': 'Sempre'}
    )
    df['Fumante'] = df['Fumante'].replace({'yes': 'Sim', 'no': 'Não'})
    df['Monitora_Calorias'] = df['Monitora_Calorias'].replace({'yes': 'Sim', 'no': 'Não'})
    df['Consumo_Alcool'] = df['Consumo_Alcool'].replace({
        'no': 'Não bebe',
        'Sometimes': 'Às Vezes',
        'Frequently': 'Frequentemente',
        'Always': 'Sempre'
    })
    df['Transporte'] = df['Transporte'].replace({
        'Public_Transportation': 'Transporte Público',
        'Walking': 'Caminhada',
        'Automobile': 'Carro',
        'Motorbike': 'Moto',
        'Bike': 'Bicicleta'
    })

    # Colunas derivadas usadas nos plots
    df['Freq_Vegetais_Label'] = df['Freq_Vegetais'].map({1: 'Raramente', 2: 'Às Vezes', 3: 'Sempre'})
    df['Consumo_Agua_Label'] = df['Consumo_Agua'].round().astype(int).map({1: 'Menos de 1L', 2: 'Entre 1L e 2L', 3: 'Mais de 2L'})
    df['Freq_Ativ_Fisica_Label'] = df['Freq_Ativ_Fisica'].round().astype(int).map({
        0: 'Nenhuma',
        1: '1 a 2 dias/sem',
        2: '3 a 4 dias/sem',
        3: 'Mais de 4 dias/sem'
    })
    df['Tempo_Dispositivos_Label'] = df['Tempo_Dispositivos'].round().astype(int).map({
        0: '0-2 horas',
        1: '3-5 horas',
        2: 'Mais de 5 horas'
    })

    return df, ordem_obesidade


df, ordem_obesidade = carregar_dados()

top_cols = st.columns([4,1])
with top_cols[0]:
    st.title("📈 Análise exploratória de dados")
    st.markdown("Os plots e textos abaixo replicam a análise original do notebook, mantendo descrições e visualizações.")
with top_cols[1]:
    if st.button("⬅️ Voltar ao sistema de diagnóstico"):
        try:
            st.switch_page("app.py")
        except Exception:
            st.stop()


def render_sec(titulo_md, texto_md, fig):
    st.markdown(titulo_md)
    st.markdown(texto_md)
    st.pyplot(fig)


# 1) Gênero x Obesidade
fig, ax = plt.subplots(figsize=(10, 6))
sns.countplot(data=df, y='Nivel_Obesidade', hue='Genero', palette=binary_colors, order=ordem_obesidade, ax=ax)
ax.set_title('Distribuição dos Níveis de Obesidade por Gênero')
ax.set_xlabel('Quantidade')
ax.set_ylabel('Nível de Obesidade')
ax.legend(title='Gênero')
fig.tight_layout()
render_sec(
    "### 📌 Análise: Gênero x Obesidade",
    "Há uma distinção clara nas categorias severas: a Obesidade Grau II é predominantemente masculina, "
    "enquanto a Obesidade Grau III é massivamente feminina. \nNas demais categorias, há um equilíbrio maior. "
    "Isso torna o gênero uma variável preditora essencial, pois inverte a probabilidade de risco entre os graus mais altos da doença.",
    fig
)

# 2) Histórico Familiar
fig, ax = plt.subplots(figsize=(12, 6))
sns.countplot(data=df, y='Nivel_Obesidade', hue='Historico_Familiar', order=ordem_obesidade, palette=binary_colors, ax=ax)
ax.set_title('Influência do Histórico Familiar na Obesidade')
ax.set_xlabel('Quantidade de Pacientes')
ax.set_ylabel('Nível de Obesidade')
ax.legend(title='Histórico Familiar de Obesidade')
fig.tight_layout()
render_sec(
    "### 📌 Análise: Histórico Familiar",
    "Os dados revelam uma correlação alarmante: a quase totalidade dos pacientes com Obesidade Grau II e III possui histórico familiar de excesso de peso. "
    "Isso sugere que o ambiente familiar e a genética são fatores determinantes para o agravamento do quadro. "
    "Para a estratégia de negócio, isso indica que intervenções focadas na família (e não apenas no indivíduo isolado) são essenciais para prevenir casos severos.",
    fig
)

# 3) Idade x Obesidade
fig, ax = plt.subplots(figsize=(14, 7))
sns.boxplot(data=df, y='Idade', x='Nivel_Obesidade', order=ordem_obesidade, ax=ax)
ax.set_title('Distribuição de Idade por Categoria de Peso')
ax.set_xlabel('Nível de Obesidade')
ax.set_ylabel('Idade (Anos)')
ax.tick_params(axis='x', rotation=45)
render_sec(
    "### 📌 Análise de Idade x Obesidade",
    "Ao analisar a distribuição etária entre as diferentes categorias de peso, observamos os seguintes padrões:\n\n"
    "**Concentração em Jovens Adultos:** A maior parte da base de dados, independentemente da categoria de peso, está concentrada na faixa dos 20 aos 30 anos. "
    "Isso indica que o problema de obesidade severa neste dataset não é exclusivo de pessoas mais velhas.\n\n"
    "**Obesidade Grau II e III (Jovens):** É notável que as medianas (linha central da caixa) dos grupos Obesidade Grau II e Grau III estão situadas em idades muito jovens (aprox. 23-26 anos). "
    "Isso refuta a hipótese de que a obesidade severa só se desenvolve com o avanço da idade.\n\n"
    "**Outliers em \"Peso Normal\":** A categoria Peso Normal apresenta diversos outliers na parte superior (acima de 40/50 anos). "
    "Isso sugere que, embora a maioria dos jovens tenha peso normal, existem indivíduos mais velhos saudáveis, mas eles fogem do padrão geral da amostra (que é majoritariamente jovem).\n\n"
    "**Conclusão para o Modelo:** A idade sozinha pode não ser um separador linear forte (ex: \"quanto mais velho, mais obeso\"), pois temos muitos jovens com obesidade grave. "
    "O modelo precisará combinar Idade com outras variáveis (como hábitos) para ser preciso.",
    fig
)

# 4) Consumo de Vegetais
fig, ax = plt.subplots(figsize=(12, 6))
sns.countplot(
    data=df,
    y='Nivel_Obesidade',
    hue='Freq_Vegetais_Label',
    order=ordem_obesidade,
    hue_order=['Raramente', 'Às Vezes', 'Sempre'],
    palette='Greens',
    ax=ax
)
ax.set_title('Consumo de Vegetais por Nível de Obesidade')
ax.set_xlabel('Quantidade de Pacientes')
ax.set_ylabel('Nível de Obesidade')
ax.legend(title='Consome Vegetais?')
render_sec(
    "### 📌 Análise: Consumo de Vegetais",
    "Os dados apresentam um comportamento inesperado: 100% dos pacientes com Obesidade Grau III relataram consumir vegetais \"Sempre\". "
    "Isso pode indicar dois cenários: viés de autoavaliação (o paciente relata o que \"deveria\" fazer, não o que faz) ou que o consumo de vegetais ocorre em conjunto com uma ingestão calórica total excessiva. "
    "Já nos graus I e II, o consumo moderado (\"Às Vezes\") é predominante. "
    "Este padrão alerta que apenas recomendar \"coma mais vegetais\" pode não ser suficiente para os casos mais graves sem controle calórico global.",
    fig
)

# 5) Consumo de Água
fig, ax = plt.subplots(figsize=(12, 6))
sns.countplot(
    data=df,
    y='Nivel_Obesidade',
    hue='Consumo_Agua_Label',
    order=ordem_obesidade,
    hue_order=['Menos de 1L', 'Entre 1L e 2L', 'Mais de 2L'],
    palette='Blues',
    ax=ax
)
ax.set_title('Consumo Diário de Água por Nível de Obesidade')
ax.set_xlabel('Quantidade de Pacientes')
ax.set_ylabel('Nível de Obesidade')
ax.legend(title='Consumo Diário')
render_sec(
    "### 📌 Análise: Consumo de Água",
    "Ao contrário do esperado, não há uma relação linear onde \"beber pouca água causa obesidade\". "
    "Os dados mostram que o grupo Obesidade Grau III possui uma alta proporção de indivíduos que consomem mais de 2L por dia (aprox. 46%), superior até mesmo a pessoas com Peso Normal. "
    "Isso sugere que a alta ingestão de líquidos neste grupo pode estar associada a bebidas calóricas (não diferenciadas nesta variável específica) ou a uma maior necessidade fisiológica de hidratação devido à massa corporal.",
    fig
)

# 6) Consumo de Álcool
fig, ax = plt.subplots(figsize=(12, 6))
sns.countplot(
    data=df,
    y='Nivel_Obesidade',
    hue='Consumo_Alcool',
    order=ordem_obesidade,
    hue_order=['Não bebe', 'Às Vezes', 'Frequentemente', 'Sempre'],
    palette='Purples',
    ax=ax
)
ax.set_title('Frequência de Consumo de Álcool por Nível de Obesidade')
ax.set_xlabel('Quantidade de Pacientes')
ax.set_ylabel('Nível de Obesidade')
ax.legend(title='Consumo de Álcool')
render_sec(
    "### 📌 Análise: Consumo de Álcool",
    "A variável apresenta baixa variabilidade nos extremos: os casos de consumo \"Frequente\" ou \"Sempre\" são estatisticamente irrelevantes em todas as categorias. "
    "O dado mais impactante é que 99.7% dos pacientes com Obesidade Grau III se classificam como consumidores ocasionais (\"Às Vezes\"), praticamente eliminando o perfil de \"Não bebe\" neste grupo. "
    "Isso sugere que o consumo social de álcool é onipresente nos graus mais altos de obesidade, diferentemente dos grupos de peso normal, onde há uma parcela significativa de abstêmios.",
    fig
)

# 7) Atividade Física
fig, ax = plt.subplots(figsize=(12, 6))
sns.countplot(
    data=df,
    y='Nivel_Obesidade',
    hue='Freq_Ativ_Fisica_Label',
    order=ordem_obesidade,
    hue_order=['Nenhuma', '1 a 2 dias/sem', '3 a 4 dias/sem', 'Mais de 4 dias/sem'],
    palette='Oranges',
    ax=ax
)
ax.set_title('Frequência de Atividade Física Semanal por Nível de Obesidade')
ax.set_xlabel('Quantidade de Pacientes')
ax.set_ylabel('Nível de Obesidade')
ax.legend(title='Frequência Semanal')
render_sec(
    "### 📌 Análise: Atividade Física",
    "A relação entre sedentarismo e obesidade severa fica evidente na categoria Obesidade Grau III, onde aprox. 58% dos pacientes não praticam nenhuma atividade física. "
    "No entanto, é interessante notar que no grupo Obesidade Grau II, a maioria (55%) pratica exercícios levemente (1-2 vezes), superando o sedentarismo total. "
    "Isso reforça que a falta de exercício é um fator crítico, mas não o único, visto que há pessoas com Peso Normal que também declaram atividade \"Nenhuma\" (aprox. 27%).",
    fig
)

# 8) Tabagismo
fig, ax = plt.subplots(figsize=(12, 6))
sns.countplot(
    data=df,
    y='Nivel_Obesidade',
    hue='Fumante',
    order=ordem_obesidade,
    palette={'Sim': '#596275', 'Não': '#dcdde1'},
    ax=ax
)
ax.set_title('Relação: Tabagismo x Obesidade')
ax.set_xlabel('Quantidade de Pacientes')
ax.set_ylabel('Nível de Obesidade')
ax.legend(title='É Fumante?')
render_sec(
    "### 📌 Análise: Tabagismo",
    "A base de dados revela que o tabagismo é extremamente raro neste grupo de estudo, com uma quantidade ínfima de fumantes em todas as categorias. "
    "O destaque, porém, é a quase inexistência de fumantes nos extremos (Abaixo do Peso e Obesidade Grau III, com apenas 1 caso cada).",
    fig
)

# 9) Monitoramento de Calorias
ct_calorias = pd.crosstab(df['Nivel_Obesidade'], df['Monitora_Calorias'], normalize='index') * 100
ct_calorias = ct_calorias.reindex(ordem_obesidade)
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x=ct_calorias.index, y=ct_calorias['Sim'], palette='viridis', order=ordem_obesidade, ax=ax)
ax.set_title('Percentual de Pessoas que Monitoram Calorias por Nível de Obesidade')
ax.set_xlabel('Nível de Obesidade')
ax.set_ylabel('% que Monitora Calorias')
for index, value in enumerate(ct_calorias['Sim']):
    ax.text(index, value + 0.2, f'{value:.1f}%', ha='center', fontweight='bold')
ax.tick_params(axis='x', rotation=15)
render_sec(
    "### 📌 Análise: Monitoramento de Calorias",
    "Este gráfico revela uma correlação negativa quase perfeita. Enquanto cerca de 10% a 12% das pessoas com Peso Normal ou Sobrepeso Leve monitoram ativamente suas calorias, esse hábito desaparece completamente nos graus mais severos de obesidade (caindo para 0% no Grau III e <1% nos Graus I e II).\n\n"
    "Insight de Negócio: Isso sugere que a perda da consciência (ou controle) sobre a ingestão calórica é um marcador crítico da transição para a obesidade. "
    "Ferramentas que reintroduzam esse monitoramento de forma simples podem ser intervenções eficazes, já que o público-alvo atual (Graus II e III) simplesmente não o faz.",
    fig
)

# 10) Tempo de Tela
fig, ax = plt.subplots(figsize=(12, 6))
sns.countplot(
    data=df,
    y='Nivel_Obesidade',
    hue='Tempo_Dispositivos_Label',
    order=ordem_obesidade,
    hue_order=['0-2 horas', '3-5 horas', 'Mais de 5 horas'],
    palette='cool_r',
    ax=ax
)
ax.set_title('Tempo Diário em Dispositivos Eletrônicos por Nível de Obesidade')
ax.set_xlabel('Quantidade de Pacientes')
ax.set_ylabel('Nível de Obesidade')
ax.legend(title='Tempo de Tela')
render_sec(
    "### 📌 Análise: Tempo de Tela",
    "Ao contrário do senso comum, não existe uma correlação direta e linear onde \"mais tempo de tela = mais obesidade\" neste dataset.\n\n"
    "Obesidade Grau III: Este grupo apresenta um comportamento peculiar: 0% dos indivíduos relatam ficar mais de 5 horas em telas (focando-se massivamente na faixa intermediária de 3-5 horas).\n\n"
    "Uso Moderado x Baixo: O uso baixo (0-2 horas) é bastante comum em graus elevados de obesidade (ex: Grau II com aprox. 58%), até mais do que em grupos de Peso Normal.\n\n"
    "Conclusão: O tempo de tela parece ser uma característica geracional ou ocupacional (trabalho/estudo) transversal a todos os grupos de peso, e não um fator discriminante forte para a obesidade severa isoladamente.",
    fig
)

# 11) Relatório Executivo (texto)
st.markdown("## Relatório Executivo: Fatores Determinantes da Obesidade")
st.markdown("**Objetivo:** Apresentar os principais insights extraídos da base de dados histórica para orientar estratégias de prevenção e apoio ao diagnóstico médico.")
st.markdown("""
### 1. O "DNA" da Obesidade (Fatores Críticos)
- A análise revelou que dois fatores são divisores de águas entre pacientes com peso normal e pacientes com obesidade severa:

- Hereditariedade é Mandatória: A influência genética é o preditor mais forte. Quase a totalidade (aprox. 100%) dos pacientes com Obesidade Grau II e III possui histórico familiar de excesso de peso.

- Ação Sugerida: O diagnóstico não deve olhar apenas para o indivíduo, mas realizar a triagem familiar imediata.

- A Falta de Consciência Calórica: Existe uma correlação negativa perfeita no monitoramento de calorias. Enquanto 10-12% das pessoas saudáveis monitoram o que comem, esse hábito é inexistente (0%) nos grupos de obesidade mórbida.

***Insight:*** A perda do controle sobre a ingestão (e não apenas a qualidade do alimento) é um marco comportamental da doença.

### 2. Perfil Demográfico de Risco
Identificamos padrões distintos que exigem abordagens personalizadas:

- **Gênero**: A doença se manifesta de forma diferente entre os sexos nos níveis avançados.

- **Homens**: Predominância massiva na Obesidade Grau II.

- **Mulheres**: Predominância massiva na Obesidade Grau III (Mórbida).

- **Idade (O Mito do Metabolismo)**: A obesidade severa nesta base não é uma doença de idosos. A maior concentração de casos graves está em jovens adultos (20 a 30 anos). Campanhas focadas na terceira idade seriam ineficazes para este perfil.

### 3. Comportamento: Mitos vs. Realidade
Dados que contradizem o senso comum e alertam para vieses de autoavaliação dos pacientes:

- O Paradoxo da "Alimentação Saudável": Curiosamente, pacientes com Obesidade Grau III relatam comer vegetais "Sempre" e beber muita água (>2L).

- Interpretação: Isso sugere que o consumo de alimentos saudáveis não está gerando déficit calórico, possivelmente devido ao volume excessivo ou acompanhamento de molhos/preparos calóricos.

- **Sedentarismo Relativo**: A falta de exercício é crítica no Grau III (58% sedentários), mas o grupo Grau II apresenta tentativas de atividade (1-2x na semana), indicando que o exercício isolado, sem dieta, não está contendo a progressão da doença.

- **Fatores Irrelevantes**: O Tabagismo e o Tempo de Tela (>5h) não mostraram correlação direta com o aumento de peso nesta amostra específica.

## 4. Conclusão para a Estratégia
O modelo preditivo terá alta assertividade pois os padrões são claros. Para a equipe médica, a recomendação baseada em dados é:

Priorizar a anamnese familiar.

Focar a reeducação na consciência calórica (monitoramento) e não apenas na recomendação genérica de "comer vegetais", que os pacientes acreditam já fazer.

Atenção redobrada a mulheres jovens com histórico familiar, que representam o maior grupo de risco para obesidade mórbida.
""")
