import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def calcular_imc(peso: float, altura: float) -> float:
    """Calcula o Índice de Massa Corporal."""
    if peso <= 0 or altura <= 0:
        raise ValueError("Peso e altura devem ser maiores que zero.")
    return peso / (altura ** 2)


def classificar_imc(imc: float) -> dict:
    """Retorna a classificação, ícone e cor de fundo com base no IMC."""
    if imc < 18.5:
        return {"classificacao": "Baixo peso", "cor": "🔵", "cor_bg": "#bbdefb"}
    elif imc < 25:
        return {"classificacao": "Peso normal", "cor": "🟢", "cor_bg": "#c8e6c9"}
    elif imc < 30:
        return {"classificacao": "Sobrepeso", "cor": "🟡", "cor_bg": "#fff9c4"}
    else:
        return {"classificacao": "Obesidade", "cor": "🔴", "cor_bg": "#ffcdd2"}


def recomendacao_imc(imc: float) -> dict:
    """Retorna tipo e texto de recomendação com base no IMC."""
    if imc < 18.5:
        return {"tipo": "info", "texto": "Considere consultar um nutricionista para ganhar peso de forma saudável."}
    elif imc < 25:
        return {"tipo": "success", "texto": "Parabéns! Você está no peso ideal. Mantenha uma alimentação balanceada e pratique exercícios."}
    elif imc < 30:
        return {"tipo": "warning", "texto": "Considere reduzir o consumo de alimentos calóricos e aumentar a atividade física."}
    else:
        return {"tipo": "error", "texto": "Recomenda-se consultar um médico ou nutricionista para um plano de perda de peso saudável."}


def main():
    # Configuração da página
    st.set_page_config(
        page_title="Calculadora de IMC",
        page_icon="🩺",
        layout="centered",
        initial_sidebar_state="collapsed"
    )

    # CSS customizado para identidade visual única e responsividade
    st.markdown("""
    <style>
    /* Identidade visual - paleta de cores */
    :root {
        --primary: #0d6efd;
        --bg-card: #f8f9fa;
    }
    .main .block-container {
        max-width: 720px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    /* Header */
    .app-header {
        text-align: center;
        padding: 1.5rem 0 0.5rem;
    }
    .app-header h1 {
        font-size: 2.2rem;
        font-weight: 700;
        color: #0d6efd;
        margin-bottom: 0.25rem;
    }
    .app-header p {
        color: #6c757d;
        font-size: 1.05rem;
    }
    /* Resultado card */
    .result-card {
        background: var(--bg-card);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 5px solid var(--primary);
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    .result-card h2 {
        margin: 0;
        font-size: 2rem;
        color: #212529;
    }
    .result-card .label {
        font-size: 0.9rem;
        color: #6c757d;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    /* Footer */
    .app-footer {
        text-align: center;
        color: #adb5bd;
        font-size: 0.85rem;
        padding-top: 1rem;
    }
    /* Botões */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown("""
    <div class="app-header">
        <h1>🩺 Calculadora de IMC</h1>
        <p>Índice de Massa Corporal — Calcule seu IMC de forma rápida e fácil!</p>
    </div>
    """, unsafe_allow_html=True)

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

    # Inicializar session_state
    if "historico" not in st.session_state:
        st.session_state.historico = []
    if "ultimo_imc" not in st.session_state:
        st.session_state.ultimo_imc = None

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
            imc = calcular_imc(peso, altura)
            st.session_state.ultimo_imc = {
                "peso": peso,
                "altura": altura,
                "imc": imc,
                **classificar_imc(imc),
            }
        else:
            st.error("Por favor, insira valores válidos para peso e altura.")
            st.session_state.ultimo_imc = None

    # Exibir resultado persistido na session_state
    resultado = st.session_state.ultimo_imc
    if resultado:
        imc = resultado["imc"]
        classificacao = resultado["classificacao"]
        cor = resultado["cor"]
        cor_bg = resultado["cor_bg"]

        # Card de resultado
        st.markdown(f"""
        <div class="result-card">
            <span class="label">Seu IMC</span>
            <h2>{imc:.2f}</h2>
            <span style="font-size:1.3rem;">{cor} {classificacao}</span>
        </div>
        """, unsafe_allow_html=True)

        # Barra de progresso visual
        st.markdown("#### Visualização do IMC")
        progress = min(imc / 40, 1.0)
        st.progress(progress)

        # Gráfico simples
        fig, ax = plt.subplots(figsize=(6, 2))
        ax.barh(["Seu IMC"], [imc], color=cor_bg, edgecolor="#495057")
        ax.set_xlim(0, 40)
        ax.set_xlabel("IMC")
        ax.set_title("Seu Índice de Massa Corporal")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

        # Recomendações
        rec = recomendacao_imc(imc)
        st.markdown("#### 💡 Recomendações")
        _alert = {"info": st.info, "success": st.success, "warning": st.warning, "error": st.error}
        _alert[rec["tipo"]](rec["texto"])

    # Histórico
    st.markdown("---")
    st.subheader("📊 Histórico de Cálculos")

    if st.button("Salvar este cálculo", use_container_width=True, help="Adiciona o cálculo atual ao histórico"):
        if resultado:
            st.session_state.historico.append({
                "Peso": resultado["peso"],
                "Altura": resultado["altura"],
                "IMC": round(resultado["imc"], 2),
                "Classificação": resultado["classificacao"],
                "Data": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M"),
            })
            st.success("Cálculo salvo no histórico!")
        else:
            st.warning("Calcule o IMC primeiro antes de salvar.")

    if st.session_state.historico:
        df = pd.DataFrame(st.session_state.historico)
        st.dataframe(df, use_container_width=True)

        if len(df) > 1:
            st.line_chart(df.set_index("Data")["IMC"])

        if st.button("Limpar histórico", use_container_width=True):
            st.session_state.historico = []
            st.rerun()
    else:
        st.info("Nenhum cálculo salvo ainda. Calcule seu IMC e clique em 'Salvar este cálculo'.")

    # Footer
    st.markdown("---")
    st.markdown('<div class="app-footer">Desenvolvido com ❤️ usando Streamlit</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()