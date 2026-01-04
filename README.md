# Tech Challenge — Obesidade

Aplicação Streamlit de apoio à decisão clínica que treina um modelo de classificação de obesidade a partir de `Obesity.csv` e exibe probabilidades por classe, recomendações clínicas e alertas orientados por dados exploratórios.

## Dependências
- Python 3.10+ recomendado
- streamlit
- pandas
- scikit-learn
- matplotlib
- seaborn

Instale com:
```bash
pip install -r requirements.txt
```

## Como executar
1) Ative seu ambiente virtual (opcional, mas recomendado).
2) Instale as dependências (`pip install -r requirements.txt`).
3) Rode o app:
```bash
streamlit run app.py
```
4) Abra o link exibido no terminal (geralmente http://localhost:8501) e preencha os dados do paciente na barra lateral.

## Páginas
- `app.py`: sistema de diagnóstico (entrada dos dados do paciente, predição, barras de probabilidade e alertas clínicos).
- `pages/analise_exploratoria.py`: reprodução dos gráficos e textos do notebook de análise exploratória, sem a etapa de ETL exposta, com botão para voltar ao diagnóstico.
