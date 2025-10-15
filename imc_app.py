import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configuração da página
st.set_page_config(
    page_title="Calculadora de IMC",
    page_icon="🩺",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Título
st.title("🩺 Calculadora de IMC")
st.markdown("**Índice de Massa Corporal** - Calcule seu IMC de forma rápida e fácil!")

# Sidebar com informações
with st.sidebar:
    st.header("ℹ️ Sobre o IMC")
    st.markdown("""
    O IMC (Índice de Massa Corporal) é uma medida internacional usada para calcular se uma pessoa está no peso ideal.

    **Classificações:**
    - Abaixo de 18.5: Baixo peso
    - 18.5 - 24.9: Peso normal
    - 25.0 - 29.9: Sobrepeso
    - 30.0 ou mais: Obesidade
    """)

# Entradas do usuário
col1, col2 = st.columns(2)

with col1:
    peso = st.number_input(
        "Peso (kg)",
        min_value=0.0,
        max_value=300.0,
        value=70.0,
        step=0.1,
        help="Digite seu peso em quilogramas"
    )

with col2:
    altura = st.number_input(
        "Altura (m)",
        min_value=0.0,
        max_value=3.0,
        value=1.70,
        step=0.01,
        help="Digite sua altura em metros"
    )

# Botão de cálculo
if st.button("Calcular IMC", type="primary", use_container_width=True):
    if peso > 0 and altura > 0:
        imc = peso / (altura ** 2)

        # Determinar classificação e cor
        if imc < 18.5:
            classificacao = "Baixo peso"
            cor = "🔵"
            cor_bg = "#e3f2fd"
        elif imc < 25:
            classificacao = "Peso normal"
            cor = "🟢"
            cor_bg = "#e8f5e8"
        elif imc < 30:
            classificacao = "Sobrepeso"
            cor = "🟡"
            cor_bg = "#fff9c4"
        else:
            classificacao = "Obesidade"
            cor = "🔴"
            cor_bg = "#ffebee"

        # Resultado
        st.success(f"Seu IMC é: **{imc:.2f}**")
        st.markdown(f"### {cor} Classificação: **{classificacao}**")

        # Barra de progresso visual
        st.markdown("#### Visualização do IMC")
        progress = min(imc / 40, 1.0)  # Normalizar para 0-1
        st.progress(progress)

        # Gráfico simples
        fig, ax = plt.subplots(figsize=(6, 2))
        ax.barh(['Seu IMC'], [imc], color=cor_bg, edgecolor='black')
        ax.set_xlim(0, 40)
        ax.set_xlabel('IMC')
        ax.set_title('Seu Índice de Massa Corporal')
        st.pyplot(fig)

        # Recomendações
        st.markdown("#### 💡 Recomendações")
        if imc < 18.5:
            st.info("Considere consultar um nutricionista para ganhar peso de forma saudável.")
        elif imc < 25:
            st.success("Parabéns! Você está no peso ideal. Mantenha uma alimentação balanceada e pratique exercícios.")
        elif imc < 30:
            st.warning("Considere reduzir o consumo de alimentos calóricos e aumentar a atividade física.")
        else:
            st.error("Recomenda-se consultar um médico ou nutricionista para um plano de perda de peso saudável.")

    else:
        st.error("Por favor, insira valores válidos para peso e altura.")

# Histórico (simulado)
st.markdown("---")
st.subheader("📊 Histórico de Cálculos")

if 'historico' not in st.session_state:
    st.session_state.historico = []

if st.button("Salvar este cálculo", help="Adiciona o cálculo atual ao histórico"):
    if peso > 0 and altura > 0:
        imc = peso / (altura ** 2)
        st.session_state.historico.append({
            'Peso': peso,
            'Altura': altura,
            'IMC': round(imc, 2),
            'Data': pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")
        })
        st.success("Cálculo salvo no histórico!")

if st.session_state.historico:
    df = pd.DataFrame(st.session_state.historico)
    st.dataframe(df, use_container_width=True)

    # Gráfico do histórico
    if len(df) > 1:
        st.line_chart(df.set_index('Data')['IMC'])
else:
    st.info("Nenhum cálculo salvo ainda. Clique em 'Salvar este cálculo' após calcular seu IMC.")

# Footer
st.markdown("---")
st.markdown("*Desenvolvido com ❤️ usando Streamlit*")