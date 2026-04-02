import streamlit as st
import base64

# --- FUNCIONES DE APOYO ---
def render_svg(svg_path):
    """Codifica y muestra el SVG en la interfaz."""
    with open(svg_path, "r") as f:
        svg = f.read()
        b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
        html = f'<div style="text-align: center;"><img src="data:image/svg+xml;base64,{b64}" width="450"/></div>'
        st.write(html, unsafe_allow_html=True)

# --- CONFIGURACIÓN DE UI ---
st.set_page_config(page_title="Balance CSTR", layout="wide")

st.title("👨‍🔬 Simulador de Balance de Materia")
st.markdown("---")

# --- BARRA LATERAL (ENTRADAS) ---
st.sidebar.header("Parámetros del Proceso")
flow = st.sidebar.slider("Flujo Volumétrico (F) [L/min]", 0.1, 50.0, 10.0)
c_in = st.sidebar.number_input("Conc. Entrada (Ca_in) [mol/L]", value=2.0)
volume = st.sidebar.slider("Volumen (V) [L]", 10, 1000, 500)
k = st.sidebar.number_input("Constante k [min⁻¹]", value=0.1)

# --- LÓGICA DE CÁLCULO ---
# Balance: F*Cin - F*Cout - k*V*Cout = 0
ca_out = (flow * c_in) / (flow + (k * volume))
conversion = (1 - (ca_out / c_in)) * 100

# --- CUERPO PRINCIPAL ---
col_diag, col_res = st.columns([1.5, 1])

with col_diag:
    st.subheader("Esquema del Reactor")
    # Intentar cargar el archivo que ya está en la carpeta
    try:
        render_svg("Diagrama en blanco.svg")
    except FileNotFoundError:
        st.error("Error: 'Diagrama en blanco.svg' no encontrado en la carpeta.")

with col_res:
    st.subheader("Resultados del Balance")
    st.metric("Concentración de Salida", f"{ca_out:.3f} mol/L")
    st.metric("Conversión de A", f"{conversion:.1f} %")
    
    with st.expander("Ver Ecuación"):
        st.latex(r"C_{A,out} = \frac{F \cdot C_{A,in}}{F + k \cdot V}")
