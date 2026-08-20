import streamlit as st
from pathlib import Path

# Configuração da página
st.set_page_config(
    page_title="Toolbox Data App (M3)",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Injeção de CSS Material Design 3
css_file = Path(__file__).parent / "styles" / "m3_streamlit.css"
if css_file.exists():
    with open(css_file, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("📊 Toolbox Data App — Material Design 3")
st.markdown("Aplicação de dados com tema e componentes baseados no **Material Design 3 (M3)**.")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Pipelines Ativos", value="12", delta="+2")
with col2:
    st.metric(label="Taxa de Sucesso", value="99.8%", delta="+0.4%")
with col3:
    st.metric(label="Tempo Médio (ms)", value="142ms", delta="-15ms")

st.divider()

if st.button("Executar Análise"):
    st.success("Análise processada com sucesso no padrão M3!")
