"""
Calculadora Criptográfica - Interfaz Streamlit
Autor: Proyecto académico - Sistemas de Información
Requisitos: streamlit, pandas
Ejecutar con: streamlit run app.py
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
import pandas as pd

from functions.modular_math   import (calcular_modulo, calcular_inverso_aditivo,
                                       calcular_inverso_xor, calcular_mcd_e_inverso_mult,
                                       calcular_inverso_mult_tradicional, calcular_inverso_mult_aee)
from functions.classic_crypto import (cifrado_mod27, cifrado_cesar, cifrado_vernam,
                                       cifrado_atbash, cifrado_transposicion_columnar,
                                       cifrado_afin, cifrado_sustitucion_simple)
from functions.modern_crypto  import (calcular_diffie_hellman, calcular_rsa, exponenciacion_rapida)
from functions.hash_algorithms import calcular_md5, calcular_sha256, calcular_sha512
from functions.encoding        import (ascii_codificar, ascii_decodificar, hex_codificar,
                                        hex_decodificar, binario_codificar, binario_decodificar,
                                        base64_codificar, base64_decodificar)
from functions.salt_protocol   import salt_md5, salt_sha256, salt_sha512

# ══════════════════════════════════════════════════════════════
# CONFIG
# ══════════════════════════════════════════════════════════════
st.set_page_config(page_title="CryptoLab", page_icon="🟣", layout="wide",
                   initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@400;500;600;700&family=Orbitron:wght@700;900&display=swap');

/* ── BASE ─────────────────────────────────────────────────── */
html, body, [class*="css"] {
  font-family: 'Rajdhani', sans-serif !important;
  font-size: 15px;
}
.stApp {
  background-color: #080810;
  background-image:
    linear-gradient(rgba(124,58,237,0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(124,58,237,0.04) 1px, transparent 1px);
  background-size: 40px 40px;
}

/* ── SIDEBAR ──────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
  background: #0a0a18 !important;
  border-right: 2px solid #7c3aed !important;
}
section[data-testid="stSidebar"]::before {
  content: "";
  position: absolute; top: 0; left: 0; right: 0; height: 3px;
  background: linear-gradient(90deg, #7c3aed, #10b981, #7c3aed);
  background-size: 200% 100%;
  animation: shimmer 3s linear infinite;
}
@keyframes shimmer { 0%{background-position:200% 0} 100%{background-position:-200% 0} }

section[data-testid="stSidebar"] * { color: #c4b5fd !important; }
section[data-testid="stSidebar"] .stSelectbox > div > div {
  background: rgba(124,58,237,0.12) !important;
  border: 1px solid #7c3aed !important;
  border-radius: 6px !important;
  color: #e9d5ff !important;
}

/* ── BLOQUE PRINCIPAL ─────────────────────────────────────── */
.block-container { padding: 1.2rem 2rem 3rem !important; }

/* ── LOGO SIDEBAR ─────────────────────────────────────────── */
.sb-logo { padding: 1rem 0 0.5rem; text-align: center; }
.sb-logo .brand {
  font-family: 'Orbitron', monospace !important;
  font-size: 1.15rem; font-weight: 900;
  color: #a855f7 !important;
  text-shadow: 0 0 18px rgba(168,85,247,0.7);
  letter-spacing: 0.12em;
}
.sb-logo .tagline { font-size: 0.7rem; color: #4ade80 !important; letter-spacing: 0.15em; margin-top: 2px; }
.sb-logo .dot { display:inline-block; width:8px; height:8px;
  background:#10b981; border-radius:50%; margin-right:6px;
  box-shadow: 0 0 8px #10b981; animation: blink 1.4s infinite; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }

/* ── HERO HEADER ──────────────────────────────────────────── */
.hero {
  position: relative;
  border: 1px solid rgba(124,58,237,0.5);
  border-top: 3px solid #a855f7;
  border-radius: 0 0 12px 12px;
  background: linear-gradient(135deg,#0f0a1e 0%,#0d1a0d 100%);
  padding: 1.4rem 1.8rem 1.2rem;
  margin-bottom: 1.6rem;
  overflow: hidden;
}
.hero::after {
  content:"";
  position:absolute; top:0; right:0; bottom:0; width:40%;
  background: radial-gradient(ellipse at right, rgba(16,185,129,0.07) 0%, transparent 70%);
  pointer-events:none;
}
.hero-eyebrow {
  font-family: 'Share Tech Mono', monospace;
  font-size: 0.68rem; color: #4ade80;
  letter-spacing: 0.2em; text-transform: uppercase;
  margin-bottom: 0.35rem;
}
.hero-eyebrow span { color: #7c3aed; }
.hero-title {
  font-family: 'Orbitron', monospace;
  font-size: 1.6rem; font-weight: 900;
  color: #fff; margin: 0 0 0.3rem;
  text-shadow: 0 0 30px rgba(168,85,247,0.4);
}
.hero-title em { color: #4ade80; font-style: normal; }
.hero-desc { font-size: 0.9rem; color: #6b7280; line-height: 1.5; margin: 0; }

/* ── TERMINAL RESULTADO ───────────────────────────────────── */
.terminal {
  background: #030b03;
  border: 1px solid #166534;
  border-left: 4px solid #4ade80;
  border-radius: 8px;
  padding: 1rem 1.25rem;
  margin: 0.8rem 0;
  box-shadow: 0 0 20px rgba(74,222,128,0.1), inset 0 0 30px rgba(0,0,0,0.5);
  position: relative;
}
.terminal::before {
  content: "OUTPUT";
  position:absolute; top:-9px; left:14px;
  background:#030b03; padding: 0 6px;
  font-family: 'Share Tech Mono', monospace;
  font-size: 0.62rem; color: #4ade80;
  letter-spacing: 0.15em;
}
.terminal-label { font-size: 0.7rem; color: #16a34a; font-family: 'Share Tech Mono', monospace; letter-spacing: 0.1em; margin-bottom: 0.35rem; }
.terminal-value {
  font-family: 'Share Tech Mono', monospace;
  font-size: 1.05rem; color: #4ade80;
  text-shadow: 0 0 8px rgba(74,222,128,0.5);
  word-break: break-all; line-height: 1.5;
}
.terminal-value::before { content: "> "; color: #16a34a; }

/* ── PANEL DE PASOS ───────────────────────────────────────── */
.step-panel {
  background: #0a0014;
  border: 1px solid rgba(124,58,237,0.4);
  border-left: 4px solid #7c3aed;
  border-radius: 8px;
  padding: 0.9rem 1.1rem;
  margin: 0.7rem 0;
  box-shadow: 0 0 16px rgba(124,58,237,0.08);
}
.step-panel-title {
  font-family: 'Share Tech Mono', monospace;
  font-size: 0.65rem; color: #a855f7;
  letter-spacing: 0.18em; text-transform: uppercase;
  margin-bottom: 0.5rem;
}
.step-panel-body {
  font-family: 'Share Tech Mono', monospace;
  font-size: 0.82rem; color: #d8b4fe; line-height: 1.9;
}

/* ── ERROR PANEL ──────────────────────────────────────────── */
.err-panel {
  background: #140008;
  border: 1px solid rgba(220,38,38,0.5);
  border-left: 4px solid #dc2626;
  border-radius: 8px;
  padding: 0.85rem 1.1rem; margin: 0.7rem 0;
}
.err-panel-title { font-size: 0.68rem; font-family:'Share Tech Mono',monospace; color:#f87171; letter-spacing:.12em; margin-bottom:.25rem; }
.err-panel-body  { font-size: 0.9rem; color: #fca5a5; }

/* ── INFO PANEL ───────────────────────────────────────────── */
.info-panel {
  background: rgba(124,58,237,0.07);
  border: 1px solid rgba(124,58,237,0.3);
  border-left: 3px solid #a855f7;
  border-radius: 8px;
  padding: 0.7rem 1rem; margin: 0.5rem 0;
  font-size: 0.87rem; color: #c4b5fd;
  font-family: 'Rajdhani', sans-serif;
}

/* ── BOTONES ──────────────────────────────────────────────── */
.stButton > button {
  font-family: 'Orbitron', monospace !important;
  font-size: 0.75rem !important;
  font-weight: 700 !important;
  letter-spacing: 0.12em !important;
  text-transform: uppercase !important;
  background: transparent !important;
  color: #4ade80 !important;
  border: 2px solid #4ade80 !important;
  border-radius: 6px !important;
  padding: 0.5rem 1.6rem !important;
  transition: all 0.2s !important;
  box-shadow: 0 0 10px rgba(74,222,128,0.2), inset 0 0 10px rgba(74,222,128,0.02) !important;
}
.stButton > button:hover {
  background: rgba(74,222,128,0.1) !important;
  box-shadow: 0 0 22px rgba(74,222,128,0.5), inset 0 0 14px rgba(74,222,128,0.05) !important;
  color: #86efac !important;
  transform: translateY(-1px) !important;
}

/* ── INPUTS ───────────────────────────────────────────────── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stNumberInput > div > div > input {
  background: #0a0a18 !important;
  border: 1px solid rgba(124,58,237,0.4) !important;
  border-radius: 6px !important;
  color: #e9d5ff !important;
  font-family: 'Share Tech Mono', monospace !important;
  font-size: 0.88rem !important;
  caret-color: #4ade80;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus,
.stNumberInput > div > div > input:focus {
  border-color: #7c3aed !important;
  box-shadow: 0 0 0 3px rgba(124,58,237,0.18), 0 0 12px rgba(124,58,237,0.2) !important;
}
.stTextInput label, .stNumberInput label, .stTextArea label, .stSelectbox label {
  font-family: 'Share Tech Mono', monospace !important;
  font-size: 0.72rem !important; color: #6b7280 !important;
  letter-spacing: 0.08em; text-transform: uppercase;
}

/* ── SELECTBOX ────────────────────────────────────────────── */
.stSelectbox > div > div {
  background: #0a0a18 !important;
  border: 1px solid rgba(124,58,237,0.4) !important;
  border-radius: 6px !important; color: #e9d5ff !important;
}

/* ── RADIO ────────────────────────────────────────────────── */
.stRadio > div { gap: 0.3rem !important; flex-wrap: wrap !important; }
.stRadio > div > label {
  background: #0a0014 !important;
  border: 1px solid rgba(124,58,237,0.3) !important;
  border-radius: 6px !important;
  padding: 0.3rem 0.75rem !important;
  font-family: 'Share Tech Mono', monospace !important;
  font-size: 0.78rem !important; color: #a78bfa !important;
  transition: all 0.15s !important; cursor: pointer !important;
}
.stRadio > div > label:hover {
  border-color: #4ade80 !important; color: #4ade80 !important;
  box-shadow: 0 0 8px rgba(74,222,128,0.2) !important;
}

/* ── MÉTRICAS ─────────────────────────────────────────────── */
[data-testid="stMetricValue"] {
  font-family: 'Orbitron', monospace !important;
  font-size: 1.25rem !important; font-weight: 700 !important;
  color: #4ade80 !important;
  text-shadow: 0 0 12px rgba(74,222,128,0.5) !important;
}
[data-testid="stMetricLabel"] {
  font-family: 'Share Tech Mono', monospace !important;
  font-size: 0.65rem !important; color: #6b7280 !important;
  letter-spacing: 0.1em; text-transform: uppercase;
}
[data-testid="metric-container"] {
  background: #050510 !important;
  border: 1px solid rgba(124,58,237,0.3) !important;
  border-top: 2px solid #7c3aed !important;
  border-radius: 8px !important; padding: 0.8rem 1rem !important;
  box-shadow: 0 0 12px rgba(124,58,237,0.08) !important;
}

/* ── DATAFRAME ────────────────────────────────────────────── */
[data-testid="stDataFrame"] {
  border: 1px solid rgba(124,58,237,0.25) !important;
  border-radius: 8px !important; overflow: hidden;
}
.stDataFrame thead th {
  background: rgba(124,58,237,0.2) !important;
  color: #a855f7 !important;
  font-family: 'Share Tech Mono', monospace !important;
  font-size: 0.75rem !important; letter-spacing: 0.08em;
}
.stDataFrame tbody td {
  color: #c4b5fd !important;
  font-family: 'Share Tech Mono', monospace !important;
  font-size: 0.8rem !important;
  background: #05050f !important;
}
.stDataFrame tbody tr:nth-child(even) td { background: #0a0a1a !important; }
.stDataFrame tbody tr:hover td { background: rgba(74,222,128,0.04) !important; }

/* ── SLIDER ───────────────────────────────────────────────── */
.stSlider > div > div > div > div { background: #7c3aed !important; }
.stSlider > div > div > div { background: rgba(124,58,237,0.2) !important; }

/* ── DIVIDER ──────────────────────────────────────────────── */
hr { border: none !important; border-top: 1px solid rgba(124,58,237,0.2) !important; }

/* ── st.code ──────────────────────────────────────────────── */
.stCode, pre { background: #030b03 !important; border-radius: 8px !important; }
.stCode code, pre code {
  font-family: 'Share Tech Mono', monospace !important;
  color: #4ade80 !important; text-shadow: 0 0 6px rgba(74,222,128,0.3);
}

/* ── PILL ─────────────────────────────────────────────────── */
.menu-pill {
  display:inline-block;
  font-family:'Share Tech Mono',monospace;
  font-size:0.62rem; letter-spacing:0.15em; text-transform:uppercase;
  background:rgba(74,222,128,0.08);
  border:1px solid rgba(74,222,128,0.3);
  color:#4ade80; padding:2px 10px; border-radius:20px; margin-bottom:0.5rem;
}

/* ── PASSWORD INPUT ───────────────────────────────────────── */
input[type="password"] {
  background: #0a0a18 !important;
  color: #4ade80 !important;
  font-family: 'Share Tech Mono', monospace !important;
}

/* ── SCROLLBAR ────────────────────────────────────────────── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #080810; }
::-webkit-scrollbar-thumb { background: #7c3aed; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #a855f7; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════
def mostrar_resultado(valor, etiqueta: str = "Resultado"):
    st.markdown(
        f'''<div class="terminal">
          <div class="terminal-label">// {etiqueta}</div>
          <div class="terminal-value">{valor}</div>
        </div>''', unsafe_allow_html=True)

def mostrar_pasos(pasos: list):
    body = "<br>".join(pasos)
    st.markdown(
        f'''<div class="step-panel">
          <div class="step-panel-title">[ proceso paso a paso ]</div>
          <div class="step-panel-body">{body}</div>
        </div>''', unsafe_allow_html=True)

def mostrar_error(msg: str):
    st.markdown(
        f'''<div class="err-panel">
          <div class="err-panel-title">!! ERROR</div>
          <div class="err-panel-body">{msg}</div>
        </div>''', unsafe_allow_html=True)

def mostrar_info(msg: str):
    st.markdown(f'<div class="info-panel">◈ {msg}</div>', unsafe_allow_html=True)

def mostrar_tabla(datos: list, titulo: str = ""):
    if datos:
        if titulo:
            st.markdown(
                f'<div style="font-family:monospace;font-size:0.65rem;color:#a855f7;letter-spacing:.12em;text-transform:uppercase;margin:0.8rem 0 0.3rem">[ {titulo} ]</div>',
                unsafe_allow_html=True)
        st.dataframe(pd.DataFrame(datos), use_container_width=True)

def hero(icono: str, titulo: str, subtitulo: str, pill: str = ""):
    pill_html = f'<div class="menu-pill">// {pill}</div><br>' if pill else ""
    titulo_parts = titulo.split(" ", 1)
    titulo_html = f'<em>{titulo_parts[0]}</em> {titulo_parts[1]}' if len(titulo_parts) > 1 else titulo
    st.markdown(
        f'''<div class="hero">
          {pill_html}
          <div class="hero-eyebrow"><span>></span> cryptolab <span>/</span> {pill.lower()}</div>
          <div class="hero-title">{icono} {titulo_html}</div>
          <p class="hero-desc">{subtitulo}</p>
        </div>''', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown('''<div class="sb-logo">
      <div class="brand">CRYPTO<br>LAB</div>
      <div class="tagline"><span class="dot"></span>ONLINE · UNAB</div>
    </div>''', unsafe_allow_html=True)
    st.markdown("---")

    menu_opciones = {
        "[ 01 ]  Matemática Modular":   "1. Matemática Modular",
        "[ 02 ]  Criptografía Clásica": "2. Criptografía Clásica",
        "[ 03 ]  Criptografía Moderna": "3. Criptografía Moderna",
        "[ 04 ]  Algoritmos Hash":      "4. Algoritmos Hash",
        "[ 05 ]  Codificación":         "5. Codificación",
        "[ 06 ]  Protocolo SALT":       "6. Protocolo SALT",
    }
    menu_label = st.selectbox("_", list(menu_opciones.keys()), label_visibility="collapsed")
    menu_principal = menu_opciones[menu_label]

    st.markdown("---")
    st.markdown('''<div style="font-family:'Share Tech Mono',monospace;font-size:0.65rem;color:#374151;text-align:center;line-height:1.8;letter-spacing:0.08em">
      CALCULADORA ACADÉMICA<br>UTF-8 · STREAMLIT · PYTHON<br>
      <span style="color:#4ade80">■</span> SISTEMA ACTIVO
    </div>''', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# SECCIÓN 1 – MATEMÁTICA MODULAR
# ══════════════════════════════════════════════════════════════
if menu_principal.startswith("1"):
    hero('🔢', 'Matemática Modular', 'Operaciones de aritmética modular con proceso detallado.', 'Menú 1')

    sub = st.radio("Selecciona la operación:", [
        "1.1 · Módulo (a mod n)",
        "1.2 · Inverso Aditivo",
        "1.3 · Inverso XOR",
        "1.4 · MCD e Inverso Multiplicativo (existencia)",
        "1.5 · Inverso Multiplicativo – Método Tradicional",
        "1.6 · Inverso Multiplicativo – AEE (con tabla)",
    ], horizontal=False)

    st.markdown("---")

    # ── 1.1 Módulo ──────────────────────────────────────────
    if sub.startswith("1.1"):
        c1, c2 = st.columns(2)
        a = c1.number_input("Valor de a", value=17, step=1)
        n = c2.number_input("Módulo n", value=5, min_value=1, step=1)
        if st.button("Calcular", key="mod"):
            res = calcular_modulo(int(a), int(n))
            if "error" in res:
                mostrar_error(res["error"])
            else:
                mostrar_resultado(res["resultado"], f"{int(a)} mod {int(n)}")
                mostrar_pasos(res["pasos"])

    # ── 1.2 Inverso Aditivo ─────────────────────────────────
    elif sub.startswith("1.2"):
        c1, c2 = st.columns(2)
        a = c1.number_input("Valor de a", value=3, step=1)
        n = c2.number_input("Módulo n", value=7, min_value=1, step=1)
        if st.button("Calcular", key="inv_ad"):
            res = calcular_inverso_aditivo(int(a), int(n))
            if "error" in res:
                mostrar_error(res["error"])
            else:
                mostrar_resultado(res["resultado"], f"Inverso aditivo de {int(a)} en Z_{int(n)}")
                mostrar_pasos(res["pasos"])

    # ── 1.3 Inverso XOR ─────────────────────────────────────
    elif sub.startswith("1.3"):
        c1, c2 = st.columns(2)
        a = c1.number_input("Valor a (entero)", value=45, min_value=0, step=1)
        b = c2.number_input("Clave b (entero)", value=23, min_value=0, step=1)
        if st.button("Calcular", key="xor"):
            res = calcular_inverso_xor(int(a), int(b))
            col1, col2 = st.columns(2)
            col1.metric("a XOR b (cifrado)", res["cifrado"])
            col2.metric("cifrado XOR b (descifrado)", res["descifrado"])
            mostrar_pasos(res["pasos"])

    # ── 1.4 MCD e Inverso Multiplicativo ────────────────────
    elif sub.startswith("1.4"):
        c1, c2 = st.columns(2)
        a = c1.number_input("Valor de a", value=3, min_value=1, step=1)
        n = c2.number_input("Módulo n", value=26, min_value=2, step=1)
        if st.button("Calcular", key="mcd"):
            res = calcular_mcd_e_inverso_mult(int(a), int(n))
            col1, col2 = st.columns(2)
            col1.metric("MCD", res["mcd"])
            col2.metric("¿Inverso existe?", "✅ SÍ" if res["existe_inverso"] else "❌ NO")
            mostrar_pasos(res["pasos"])

    # ── 1.5 Inverso Multiplicativo Tradicional ──────────────
    elif sub.startswith("1.5"):
        c1, c2 = st.columns(2)
        a = c1.number_input("Valor de a", value=3, min_value=1, step=1)
        n = c2.number_input("Módulo n", value=26, min_value=2, step=1)
        if st.button("Calcular", key="inv_trad"):
            res = calcular_inverso_mult_tradicional(int(a), int(n))
            if not res["existe"]:
                mostrar_error(res["pasos"][0])
            else:
                mostrar_resultado(res["resultado"], f"Inverso multiplicativo de {int(a)} en Z_{int(n)}")
                mostrar_pasos(res["pasos"])
                mostrar_tabla(res["tabla"], "📊 Tabla de búsqueda")

    # ── 1.6 Inverso Multiplicativo AEE ──────────────────────
    elif sub.startswith("1.6"):
        c1, c2 = st.columns(2)
        a = c1.number_input("Valor de a", value=3, min_value=1, step=1)
        n = c2.number_input("Módulo n", value=26, min_value=2, step=1)
        if st.button("Calcular", key="inv_aee"):
            res = calcular_inverso_mult_aee(int(a), int(n))
            if not res["existe"]:
                mostrar_error(res["pasos"][0])
            else:
                col1, col2 = st.columns(2)
                col1.metric("Inverso multiplicativo", res["inverso"])
                col2.metric("Rondas AEE", res["total_rondas"])
                mostrar_pasos(res["pasos"])
                mostrar_tabla(res["tabla"], "📊 Tabla AEE (Algoritmo Extendido de Euclides)")


# ══════════════════════════════════════════════════════════════
# SECCIÓN 2 – CRIPTOGRAFÍA CLÁSICA
# ══════════════════════════════════════════════════════════════
elif menu_principal.startswith("2"):
    hero('📜', 'Criptografía Clásica', 'Cifrados históricos con visualización del proceso letra a letra.', 'Menú 2')

    sub = st.radio("Selecciona el cifrado:", [
        "2.1 · Módulo 27 (alfabeto español)",
        "2.2 · César",
        "2.3 · Vernam (OTP / XOR)",
        "2.4 · ATBASH",
        "2.5 · Transposición Columnar Simple",
        "2.6 · Afín",
        "2.7 · Sustitución Simple",
    ], horizontal=False)

    st.markdown("---")

    modo_opciones = ["cifrar", "descifrar"]

    # ── 2.1 Módulo 27 ────────────────────────────────────────
    if sub.startswith("2.1"):
        texto = st.text_input("Texto", value="HOLA MUNDO")
        c1, c2 = st.columns(2)
        clave  = c1.number_input("Clave (entero)", value=3, step=1)
        modo   = c2.selectbox("Modo", modo_opciones)
        if st.button("Ejecutar", key="m27"):
            res = cifrado_mod27(texto, int(clave), modo)
            mostrar_resultado(res["resultado"])
            mostrar_tabla(res["tabla"], "📊 Tabla de sustitución (Alfabeto español 27 letras)")

    # ── 2.2 César ─────────────────────────────────────────────
    elif sub.startswith("2.2"):
        texto = st.text_input("Texto", value="HOLA MUNDO")
        c1, c2 = st.columns(2)
        desp  = c1.number_input("Desplazamiento", value=3, step=1)
        modo  = c2.selectbox("Modo", modo_opciones)
        if st.button("Ejecutar", key="cesar"):
            res = cifrado_cesar(texto, int(desp), modo)
            mostrar_resultado(res["resultado"])
            mostrar_tabla(res["tabla"], "📊 Proceso letra a letra")

    # ── 2.3 Vernam ────────────────────────────────────────────
    elif sub.startswith("2.3"):
        texto = st.text_input("Texto", value="Hola")
        c1, c2 = st.columns(2)
        clave  = c1.text_input("Clave", value="Key")
        modo   = c2.selectbox("Modo", modo_opciones)
        mostrar_info("⚠️ El cifrado y descifrado Vernam son la misma operación XOR. Para descifrar ingresa el texto cifrado (en hex) y la misma clave.")
        if st.button("Ejecutar", key="vernam"):
            res = cifrado_vernam(texto, clave, modo)
            if "error" in res:
                mostrar_error(res["error"])
            else:
                st.markdown(f"**Resultado (hex):** `{res['resultado_hex']}`")
                st.markdown(f"**Resultado (texto/utf-8):** `{res['resultado']}`")
                mostrar_tabla(res["tabla"], "📊 Tabla XOR byte a byte")

    # ── 2.4 ATBASH ────────────────────────────────────────────
    elif sub.startswith("2.4"):
        texto = st.text_input("Texto", value="HOLA MUNDO")
        mostrar_info("ATBASH es simétrico: cifrar y descifrar son la misma operación.")
        if st.button("Ejecutar", key="atbash"):
            res = cifrado_atbash(texto)
            mostrar_resultado(res["resultado"])
            mostrar_tabla(res["tabla"], "📊 Proceso letra a letra")

    # ── 2.5 Transposición Columnar ────────────────────────────
    elif sub.startswith("2.5"):
        texto = st.text_input("Texto", value="ATACAR MAÑANA AL AMANECER")
        c1, c2 = st.columns(2)
        clave  = c1.text_input("Clave columnar", value="CLAVE")
        modo   = c2.selectbox("Modo", modo_opciones)
        if st.button("Ejecutar", key="trans"):
            res = cifrado_transposicion_columnar(texto, clave.upper(), modo)
            mostrar_resultado(res["resultado"])
            mostrar_pasos(res["pasos"])
            if res.get("filas"):
                st.markdown("**📊 Matriz de transposición:**")
                df_filas = pd.DataFrame(
                    [list(f.ljust(len(clave))) for f in res["filas"]],
                    columns=list(clave.upper()[:len(res["filas"][0])])
                )
                st.dataframe(df_filas, use_container_width=True)

    # ── 2.6 Afín ─────────────────────────────────────────────
    elif sub.startswith("2.6"):
        texto = st.text_input("Texto", value="HOLA")
        c1, c2, c3 = st.columns(3)
        a    = c1.number_input("Parámetro a (coprimo con 26)", value=5, step=1)
        b    = c2.number_input("Parámetro b", value=8, step=1)
        modo = c3.selectbox("Modo", modo_opciones)
        if st.button("Ejecutar", key="afin"):
            res = cifrado_afin(texto, int(a), int(b), modo)
            if "error" in res:
                mostrar_error(res["error"])
            else:
                mostrar_resultado(res["resultado"])
                if modo == "descifrar":
                    mostrar_info("Inverso multiplicativo de a={int(a)} en Z_26: a⁻¹ = {res['a_inv']}")
                mostrar_tabla(res["tabla"], "📊 Proceso letra a letra")

    # ── 2.7 Sustitución Simple ───────────────────────────────
    elif sub.startswith("2.7"):
        texto = st.text_input("Texto", value="HOLA MUNDO")
        c1, c2 = st.columns(2)
        clave  = c1.text_input("Clave (palabra)", value="CRYPTO")
        modo   = c2.selectbox("Modo", modo_opciones)
        if st.button("Ejecutar", key="sust"):
            res = cifrado_sustitucion_simple(texto, clave, modo)
            mostrar_resultado(res["resultado"])
            alfa_df = pd.DataFrame({
                "Alfabeto plano": list(res["alfabeto_plano"]),
                "Alfabeto cifrado": list(res["alfabeto_sust"]),
            })
            st.markdown("**📊 Tabla de sustitución:**")
            st.dataframe(alfa_df.T, use_container_width=True)
            mostrar_tabla(res["tabla"], "📊 Proceso letra a letra")


# ══════════════════════════════════════════════════════════════
# SECCIÓN 3 – CRIPTOGRAFÍA MODERNA
# ══════════════════════════════════════════════════════════════
elif menu_principal.startswith("3"):
    hero('🛡️', 'Criptografía Moderna', 'Diffie-Hellman, RSA y exponenciación rápida con proceso completo.', 'Menú 3')

    sub = st.radio("Selecciona el algoritmo:", [
        "3.1 · Diffie-Hellman",
        "3.2 · RSA",
        "3.3 · Exponenciación Rápida (Square & Multiply)",
    ], horizontal=False)

    st.markdown("---")

    # ── 3.1 Diffie-Hellman ───────────────────────────────────
    if sub.startswith("3.1"):
        st.markdown("**Parámetros públicos:**")
        c1, c2 = st.columns(2)
        p = c1.number_input("Primo p", value=23, min_value=2, step=1)
        g = c2.number_input("Generador g", value=5, min_value=2, step=1)
        st.markdown("**Claves privadas:**")
        c3, c4 = st.columns(2)
        a_priv = c3.number_input("Clave privada Alice (a)", value=6, min_value=1, step=1)
        b_priv = c4.number_input("Clave privada Bob (b)", value=15, min_value=1, step=1)
        if st.button("Calcular DH", key="dh"):
            res = calcular_diffie_hellman(int(p), int(g), int(a_priv), int(b_priv))
            if "error" in res:
                mostrar_error(res["error"])
            else:
                col1, col2, col3 = st.columns(3)
                col1.metric("Clave pública Alice (A)", res["A"])
                col2.metric("Clave pública Bob (B)", res["B"])
                col3.metric("🔑 Clave compartida K", res["clave_compartida"])
                mostrar_pasos(res["pasos"])

    # ── 3.2 RSA ──────────────────────────────────────────────
    elif sub.startswith("3.2"):
        st.markdown("**Parámetros:**")
        c1, c2 = st.columns(2)
        p = c1.number_input("Primo p", value=61, min_value=2, step=1)
        q = c2.number_input("Primo q", value=53, min_value=2, step=1)
        c3, c4 = st.columns(2)
        e = c3.number_input("Exponente público e", value=17, min_value=2, step=1)
        M = c4.number_input("Mensaje M (entero)", value=65, min_value=0, step=1)
        if st.button("Calcular RSA", key="rsa"):
            res = calcular_rsa(int(p), int(q), int(e), int(M))
            if "error" in res:
                mostrar_error(res["error"])
            else:
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("n (módulo)", res["n"])
                col2.metric("φ(n)", res["phi"])
                col3.metric("d (clave privada)", res["d"])
                col4.metric("✅ Descifrado", res["descifrado"])
                mostrar_info(f"🔓 Clave pública: (e={res['e']}, n={res['n']})")
                mostrar_pasos(res["pasos"])

    # ── 3.3 Exponenciación Rápida ────────────────────────────
    elif sub.startswith("3.3"):
        c1, c2, c3 = st.columns(3)
        base = c1.number_input("Base", value=2, min_value=0, step=1)
        exp  = c2.number_input("Exponente", value=10, min_value=0, step=1)
        mod  = c3.number_input("Módulo (0 = sin módulo)", value=1000, min_value=0, step=1)
        if mod == 0:
            mod = 10**18
        if st.button("Calcular", key="exp_rap"):
            res = exponenciacion_rapida(int(base), int(exp), int(mod))
            if "error" in res:
                mostrar_error(res["error"])
            else:
                col1, col2 = st.columns(2)
                col1.metric("Resultado", res["resultado"])
                col2.metric("Exponente en binario", res["exp_binario"])
                mostrar_pasos(res["pasos"])
                mostrar_tabla(res["tabla"], "📊 Tabla de pasos (Square & Multiply)")


# ══════════════════════════════════════════════════════════════
# SECCIÓN 4 – ALGORITMOS HASH
# ══════════════════════════════════════════════════════════════
elif menu_principal.startswith("4"):
    hero('🔍', 'Algoritmos Hash', 'Calcula hashes criptográficos. Soporta cualquier texto UTF-8.', 'Menú 4')

    sub = st.radio("Selecciona el algoritmo:", [
        "4.1 · MD5 (128 bits)",
        "4.2 · SHA-256 (256 bits)",
        "4.3 · SHA-512 (512 bits)",
    ], horizontal=False)

    st.markdown("---")
    texto = st.text_area("Texto a hashear", value="Hola Mundo 🔐", height=100)

    funciones_hash = {"4.1": calcular_md5, "4.2": calcular_sha256, "4.3": calcular_sha512}
    clave_fn = sub[:3]

    if st.button("Calcular Hash", key="hash"):
        res = funciones_hash[clave_fn](texto)
        st.markdown(f"**Algoritmo:** `{res['algoritmo']}`  |  **Bits:** `{res['bits']}`")
        st.code(res["hash_hex"], language="text")
        mostrar_pasos(res["pasos"])
        st.markdown("**🔬 Hash en grupos de 8 hex:**")
        hex_s = res["hash_hex"]
        grupos = [hex_s[i:i+8] for i in range(0, len(hex_s), 8)]
        st.markdown("  ".join(f"`{g}`" for g in grupos))


# ══════════════════════════════════════════════════════════════
# SECCIÓN 5 – CODIFICACIÓN
# ══════════════════════════════════════════════════════════════
elif menu_principal.startswith("5"):
    hero('📡', 'Codificación / Decodificación', 'Convierte textos entre distintas representaciones. Soporte UTF-8 completo.', 'Menú 5')

    sub = st.radio("Selecciona la codificación:", [
        "5.1 · ASCII / Unicode decimal",
        "5.2 · Hexadecimal",
        "5.3 · Binario",
        "5.4 · Base64",
    ], horizontal=False)

    st.markdown("---")
    modo_cod = st.radio("Modo:", ["Codificar", "Decodificar"], horizontal=True)

    # ── 5.1 ASCII ────────────────────────────────────────────
    if sub.startswith("5.1"):
        if modo_cod == "Codificar":
            texto = st.text_input("Texto a codificar", value="Hola 🔐")
            if st.button("Codificar ASCII", key="asc_enc"):
                res = ascii_codificar(texto)
                mostrar_resultado(res["resultado"], "Valores decimales")
                mostrar_tabla(res["tabla"], "📊 Tabla ASCII")
        else:
            nums = st.text_input("Valores decimales (separados por espacios)", value="72 111 108 97")
            if st.button("Decodificar ASCII", key="asc_dec"):
                res = ascii_decodificar(nums)
                if "error" in res:
                    mostrar_error(res["error"])
                else:
                    mostrar_resultado(res["resultado"])
                    mostrar_tabla(res["tabla"], "📊 Tabla ASCII")

    # ── 5.2 Hex ──────────────────────────────────────────────
    elif sub.startswith("5.2"):
        if modo_cod == "Codificar":
            texto = st.text_input("Texto a codificar", value="Hola")
            if st.button("Codificar Hex", key="hex_enc"):
                res = hex_codificar(texto)
                mostrar_resultado(res["resultado"], "Hexadecimal")
                mostrar_tabla(res["tabla"], "📊 Tabla de bytes")
        else:
            hex_in = st.text_input("Cadena hexadecimal", value="486f6c61")
            if st.button("Decodificar Hex", key="hex_dec"):
                res = hex_decodificar(hex_in)
                if "error" in res:
                    mostrar_error(res["error"])
                else:
                    mostrar_resultado(res["resultado"])
                    mostrar_tabla(res["tabla"], "📊 Tabla de bytes")

    # ── 5.3 Binario ──────────────────────────────────────────
    elif sub.startswith("5.3"):
        if modo_cod == "Codificar":
            texto = st.text_input("Texto a codificar", value="Hi")
            if st.button("Codificar Binario", key="bin_enc"):
                res = binario_codificar(texto)
                mostrar_resultado(res["resultado"], "Binario (bytes 8 bits)")
                mostrar_tabla(res["tabla"], "📊 Tabla de bytes")
        else:
            bin_in = st.text_input("Binario (bytes de 8 bits separados por espacio)", value="01001000 01101001")
            if st.button("Decodificar Binario", key="bin_dec"):
                res = binario_decodificar(bin_in)
                if "error" in res:
                    mostrar_error(res["error"])
                else:
                    mostrar_resultado(res["resultado"])
                    mostrar_tabla(res["tabla"], "📊 Tabla de bytes")

    # ── 5.4 Base64 ───────────────────────────────────────────
    elif sub.startswith("5.4"):
        if modo_cod == "Codificar":
            texto = st.text_area("Texto a codificar", value="Hola Mundo 🔐", height=80)
            if st.button("Codificar Base64", key="b64_enc"):
                res = base64_codificar(texto)
                mostrar_resultado(res["resultado"], "Base64")
                mostrar_pasos(res["pasos"])
        else:
            b64_in = st.text_area("Cadena Base64", value="SG9sYSBNdW5kbyDwn5KQ", height=80)
            if st.button("Decodificar Base64", key="b64_dec"):
                res = base64_decodificar(b64_in)
                if "error" in res:
                    mostrar_error(res["error"])
                else:
                    mostrar_resultado(res["resultado"])
                    mostrar_pasos(res["pasos"])


# ══════════════════════════════════════════════════════════════
# SECCIÓN 6 – PROTOCOLO SALT
# ══════════════════════════════════════════════════════════════
elif menu_principal.startswith("6"):
    hero('🧂', 'Protocolo SALT', 'Demuestra cómo el uso de SALT evita ataques de tabla arcoíris.', 'Menú 6')

    sub = st.radio("Selecciona el algoritmo:", [
        "6.1 · MD5 + SALT",
        "6.2 · SHA-256 + SALT",
        "6.3 · SHA-512 + SALT",
    ], horizontal=False)

    st.markdown("---")

    funciones_salt = {
        "6.1": salt_md5,
        "6.2": salt_sha256,
        "6.3": salt_sha512,
    }
    clave_fn = sub[:3]

    password = st.text_input("Contraseña (password)", value="MiClave123", type="password")
    n_salts  = st.slider("Número de SALTs a generar", min_value=2, max_value=10, value=5)
    salt_man = st.text_input("SALT manual (opcional, dejar vacío para aleatorios)", value="")

    if st.button("Generar Hashes con SALT", key="salt_btn"):
        res = funciones_salt[clave_fn](password, n_salts, salt_man)
        if res.get("unico"):
            r = res["resultado"]
            st.success(f"**Algoritmo:** {r['algoritmo']}")
            st.markdown(f"**SALT:** `{r['salt']}`")
            st.markdown(f"**Combinado (SALT+password):** `{r['combinado']}`")
            st.code(r["hash"], language="text")
        else:
            mostrar_pasos(res["pasos"])
            st.markdown("### 📊 Hashes generados con distintos SALTs")
            tabla_display = [{
                "#": r["#"],
                "SALT (hex)": r["salt"],
                "Algoritmo": r["algoritmo"],
                "Hash resultante": r["hash"],
            } for r in res["resultados"]]
            st.dataframe(pd.DataFrame(tabla_display), use_container_width=True)
            mostrar_info("🔍 Observa que el mismo password con distintos SALTs produce hashes completamente diferentes.")
            
