"""
Calculadora Criptográfica - Interfaz Streamlit
Autor: Proyecto académico - Sistemas de Información
Requisitos: streamlit, pandas
Ejecutar con: streamlit run app.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
import pandas as pd

# ── Importar módulos de funciones ────────────────────────────
from functions.modular_math   import (calcular_modulo, calcular_inverso_aditivo,
                                       calcular_inverso_xor, calcular_mcd_e_inverso_mult,
                                       calcular_inverso_mult_tradicional, calcular_inverso_mult_aee)
from functions.classic_crypto import (cifrado_mod27, cifrado_cesar, cifrado_vernam,
                                       cifrado_atbash, cifrado_transposicion_columnar,
                                       cifrado_afin, cifrado_sustitucion_simple)
from functions.modern_crypto  import (calcular_diffie_hellman, calcular_rsa,
                                       exponenciacion_rapida)
from functions.hash_algorithms import calcular_md5, calcular_sha256, calcular_sha512
from functions.encoding        import (ascii_codificar, ascii_decodificar,
                                        hex_codificar, hex_decodificar,
                                        binario_codificar, binario_decodificar,
                                        base64_codificar, base64_decodificar)
from functions.salt_protocol   import salt_md5, salt_sha256, salt_sha512


# ══════════════════════════════════════════════════════════════
# CONFIGURACIÓN DE PÁGINA
# ══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Calculadora Criptográfica",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Estilos CSS personalizados ───────────────────────────────
st.markdown("""
<style>
    .main-title   { font-size: 2.2rem; font-weight: 700; color: #1f77b4; }
    .sub-title    { font-size: 1.1rem; color: #555; margin-top: -0.5rem; }
    .result-box   { background:#f0f4ff; border-left:4px solid #1f77b4;
                    padding:1rem; border-radius:6px; font-family:monospace; }
    .step-box     { background:#f9f9f9; border-left:3px solid #4caf50;
                    padding:0.8rem; border-radius:4px; font-family:monospace; font-size:0.9rem; }
    .error-box    { background:#fff0f0; border-left:4px solid #e53935;
                    padding:0.8rem; border-radius:4px; }
    .badge        { display:inline-block; background:#1f77b4; color:white;
                    padding:2px 10px; border-radius:12px; font-size:0.8rem; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# HELPERS DE VISUALIZACIÓN
# ══════════════════════════════════════════════════════════════
def mostrar_pasos(pasos: list):
    """Muestra los pasos de una operación en un bloque formateado."""
    st.markdown("**📋 Proceso paso a paso:**")
    st.markdown('<div class="step-box">' + "<br>".join(pasos) + '</div>', unsafe_allow_html=True)

def mostrar_resultado(valor, etiqueta: str = "Resultado"):
    """Muestra el resultado principal destacado."""
    st.markdown(f'<div class="result-box">✅ <strong>{etiqueta}:</strong> <code>{valor}</code></div>',
                unsafe_allow_html=True)

def mostrar_error(msg: str):
    """Muestra un mensaje de error formateado."""
    st.markdown(f'<div class="error-box">❌ <strong>Error:</strong> {msg}</div>', unsafe_allow_html=True)

def mostrar_tabla(datos: list, titulo: str = ""):
    """Muestra una lista de diccionarios como tabla de pandas."""
    if datos:
        if titulo:
            st.markdown(f"**{titulo}**")
        st.dataframe(pd.DataFrame(datos), use_container_width=True)


# ══════════════════════════════════════════════════════════════
# SIDEBAR – NAVEGACIÓN
# ══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🔐 Calculadora Criptográfica")
    st.markdown("---")
    menu_principal = st.selectbox("📂 Menú Principal", [
        "1. Matemática Modular",
        "2. Criptografía Clásica",
        "3. Criptografía Moderna",
        "4. Algoritmos Hash",
        "5. Codificación",
        "6. Protocolo SALT",
    ])
    st.markdown("---")
    st.caption("Calculadora académica · UTF-8 · Streamlit")


# ══════════════════════════════════════════════════════════════
# SECCIÓN 1 – MATEMÁTICA MODULAR
# ══════════════════════════════════════════════════════════════
if menu_principal.startswith("1"):
    st.markdown('<p class="main-title">🔢 Matemática Modular</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Operaciones de aritmética modular con proceso detallado.</p>', unsafe_allow_html=True)

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
    st.markdown('<p class="main-title">📜 Criptografía Clásica</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Cifrados históricos con visualización del proceso letra a letra.</p>', unsafe_allow_html=True)

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
        st.info("⚠️ El cifrado y descifrado Vernam son la misma operación XOR. Para descifrar ingresa el texto cifrado (en hex) y la misma clave.")
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
        st.info("ATBASH es simétrico: cifrar y descifrar son la misma operación.")
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
                    st.info(f"Inverso multiplicativo de a={int(a)} en Z_26: a⁻¹ = {res['a_inv']}")
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
    st.markdown('<p class="main-title">🛡️ Criptografía Moderna</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Diffie-Hellman, RSA y exponenciación rápida con proceso completo.</p>', unsafe_allow_html=True)

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
                st.info(f"🔓 Clave pública: (e={res['e']}, n={res['n']})   |   🔒 Clave privada: (d={res['d']}, n={res['n']})")
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
    st.markdown('<p class="main-title">🔍 Algoritmos Hash</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Calcula hashes criptográficos. Soporta cualquier texto UTF-8.</p>', unsafe_allow_html=True)

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
    st.markdown('<p class="main-title">📡 Codificación / Decodificación</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Convierte textos entre distintas representaciones. Soporte UTF-8 completo.</p>', unsafe_allow_html=True)

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
    st.markdown('<p class="main-title">🧂 Protocolo SALT</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Demuestra cómo el uso de SALT evita ataques de tabla arcoíris.</p>', unsafe_allow_html=True)

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
            st.info("🔍 Observa que el mismo password con distintos SALTs produce hashes completamente diferentes.")
