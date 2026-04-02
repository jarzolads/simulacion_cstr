import streamlit as st
import base64

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="CSTR Interactive Balance", layout="centered")

def get_svg_base64(file_path):
    """Convierte el SVG a base64 para incrustarlo en HTML."""
    with open(file_path, "rb") as f:
        data = f.read()
        return base64.b64encode(data).decode()

st.title("Reactor CSTR: Balance Interactivo")
st.markdown("Pasa el mouse sobre el reactor para ver los datos del balance en tiempo real.")

# --- SIDEBAR (ENTRADAS) ---
with st.sidebar:
    st.header("Configuración")
    F = st.slider("Flujo (F) [L/min]", 1.0, 100.0, 15.0)
    Ca_in = st.number_input("Conc. Entrada [mol/L]", value=2.5)
    V = st.slider("Volumen (V) [L]", 50, 1000, 200)
    k = st.number_input("Constante k [min⁻¹]", value=0.15)

# --- LÓGICA DEL BALANCE ---
# Ecuación: Ca_out = (F * Ca_in) / (F + k * V)
Ca_out = (F * Ca_in) / (F + (k * V))
conversion = (1 - (Ca_out / Ca_in)) * 100
tau = V / F  # Tiempo de residencia

# --- RENDERIZADO INTERACTIVO (HTML + CSS) ---
try:
    svg_base64 = get_svg_base64("Diagrama en blanco.svg")
    
    # Estilo CSS para el Tooltip
    tooltip_html = f"""
    <style>
        .container {{
            position: relative;
            display: inline-block;
            cursor: crosshair;
        }}
        .overlay-image {{
            display: block;
            width: 100%;
            max-width: 500px;
            height: auto;
        }}
        .tooltip-text {{
            visibility: hidden;
            width: 250px;
            background-color: #262730;
            color: #fff;
            text-align: left;
            border-radius: 8px;
            padding: 15px;
            position: absolute;
            z-index: 1;
            bottom: 10%;
            left: 50%;
            margin-left: -125px;
            opacity: 0;
            transition: opacity 0.3s;
            border: 1px solid #ff4b4b;
            font-family: sans-serif;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.5);
        }}
        .container:hover .tooltip-text {{
            visibility: visible;
            opacity: 1;
        }}
        .data-val {{ color: #ff4b4b; font-weight: bold; }}
    </style>

    <div class="container">
        <img src="data:image/svg+xml;base64,{svg_base64}" class="overlay-image">
        <div class="tooltip-text">
            <strong>📊 Datos del Balance:</strong><br><br>
            • Conc. Salida: <span class="data-val">{Ca_out:.3f} mol/L</span><br>
            • Conversión: <span class="data-val">{conversion:.1f} %</span><br>
            • Residencia (τ): <span class="data-val">{tau:.2f} min</span><br>
            <hr>
            <small>Estado: Estacionario</small>
        </div>
    </div>
    """
    st.components.v1.html(tooltip_html, height=500)

except FileNotFoundError:
    st.error("Archivo 'Diagrama en blanco.svg' no encontrado.")

# --- TABLA DE DATOS ---
st.write("### Resumen de operación")
st.table({{
    "Variable": ["Flujo", "Volumen", "k", "Ca Salida"],
    "Valor": [f"{F} L/min", f"{V} L", f"{k} min⁻¹", f"{Ca_out:.4f} mol/L"]
}})
