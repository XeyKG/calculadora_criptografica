"""
Módulo: Criptografía Clásica
Implementa cifrados históricos y clásicos con soporte UTF-8 donde aplica.
"""
from math import gcd

# Alfabeto español de 27 letras (incluye Ñ)
ALFA27 = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
ALFA26 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


# ── 2.1 Cifrado Módulo 27 ───────────────────────────────────
def cifrado_mod27(texto: str, clave: int, modo: str = "cifrar") -> dict:
    """
    Cifra/descifra usando el alfabeto español de 27 letras.
    Modo: 'cifrar' o 'descifrar'.
    """
    texto_up  = texto.upper()
    resultado = []
    tabla     = []
    for ch in texto_up:
        if ch in ALFA27:
            p = ALFA27.index(ch)
            if modo == "cifrar":
                c = (p + clave) % 27
            else:
                c = (p - clave) % 27
            resultado.append(ALFA27[c])
            tabla.append({"Original": ch, "Pos": p,
                          "Operación": f"({p}{'+'if modo=='cifrar' else '-'}{clave}) mod 27",
                          "Pos resultado": c, "Resultado": ALFA27[c]})
        else:
            resultado.append(ch)
            tabla.append({"Original": ch, "Pos": "—", "Operación": "—", "Pos resultado": "—", "Resultado": ch})
    return {"resultado": "".join(resultado), "tabla": tabla}


# ── 2.2 Cifrado César ───────────────────────────────────────
def cifrado_cesar(texto: str, desplazamiento: int, modo: str = "cifrar") -> dict:
    """
    Cifra/descifra con el cifrado César (desplazamiento sobre 26 letras).
    Preserva mayúsculas/minúsculas y caracteres no alfabéticos.
    """
    resultado = []
    tabla     = []
    for ch in texto:
        if ch.isalpha():
            base  = ord('A') if ch.isupper() else ord('a')
            p     = ord(ch) - base
            if modo == "cifrar":
                c = (p + desplazamiento) % 26
            else:
                c = (p - desplazamiento) % 26
            nuevo = chr(c + base)
            resultado.append(nuevo)
            tabla.append({"Original": ch, "Pos": p,
                          "Operación": f"({p}{'+'if modo=='cifrar'else'-'}{desplazamiento}) mod 26",
                          "Pos resultado": c, "Resultado": nuevo})
        else:
            resultado.append(ch)
            tabla.append({"Original": ch, "Pos": "—", "Operación": "—", "Pos resultado": "—", "Resultado": ch})
    return {"resultado": "".join(resultado), "tabla": tabla}


# ── 2.3 Cifrado Vernam (OTP / XOR) ──────────────────────────
def cifrado_vernam(texto: str, clave: str, modo: str = "cifrar") -> dict:
    """
    Cifra/descifra usando XOR byte a byte sobre la codificación UTF-8.
    La clave se repite cíclicamente si es más corta que el texto.

    - cifrar:    texto (str)  → XOR con clave → resultado_hex (str)
    - descifrar: texto (hex)  → XOR con clave → texto original (str)

    El modo distingue el formato de entrada:
      • En "cifrar"    el parámetro `texto` es una cadena legible.
      • En "descifrar" el parámetro `texto` es la cadena hexadecimal
        devuelta por el cifrado (resultado_hex).
    """
    clave_bytes = clave.encode("utf-8")
    if len(clave_bytes) == 0:
        return {"error": "La clave no puede estar vacía."}

    # ── Obtener los bytes a procesar según el modo ──────────────────────────
    if modo == "descifrar":
        hex_limpio = texto.replace(" ", "").strip()
        if len(hex_limpio) % 2 != 0:
            return {"error": "Hex inválido: longitud impar."}
        try:
            texto_bytes = bytes.fromhex(hex_limpio)
        except ValueError:
            return {"error": "Para descifrar el texto debe estar en formato hexadecimal (ej. 032a35…)."}
    else:  # "cifrar"
        texto_bytes = texto.encode("utf-8")

    # ── XOR byte a byte ─────────────────────────────────────────────────────
    resultado_bytes = bytes(
        tb ^ clave_bytes[i % len(clave_bytes)]
        for i, tb in enumerate(texto_bytes)
    )

    # ── Tabla de proceso ────────────────────────────────────────────────────
    tabla = []
    for i, (tb, rb) in enumerate(zip(texto_bytes, resultado_bytes)):
        kb = clave_bytes[i % len(clave_bytes)]
        tabla.append({
            "Byte #":       i,
            "Texto (dec)":  tb,      "Texto (hex)":  hex(tb),
            "Clave (dec)":  kb,      "Clave (hex)":  hex(kb),
            "XOR (dec)":    rb,      "XOR (hex)":    hex(rb),
        })

    # ── Resultado ───────────────────────────────────────────────────────────
    if modo == "cifrar":
        # El texto cifrado SIEMPRE se devuelve como hex para evitar bytes
        # no imprimibles y garantizar que descifrar funcione correctamente.
        return {
            "resultado":     resultado_bytes.hex(),
            "resultado_hex": resultado_bytes.hex(),
            "tabla":         tabla,
        }
    else:
        # Al descifrar recuperamos la cadena UTF-8 original.
        try:
            resultado_str = resultado_bytes.decode("utf-8")
        except UnicodeDecodeError:
            resultado_str = resultado_bytes.hex()
            return {
                "error":         "El descifrado no produjo UTF-8 válido. Verifica la clave.",
                "resultado":     resultado_str,
                "resultado_hex": resultado_str,
                "tabla":         tabla,
            }
        return {
            "resultado":     resultado_str,
            "resultado_hex": resultado_bytes.hex(),
            "tabla":         tabla,
        }


# ── 2.4 Cifrado ATBASH ──────────────────────────────────────
def cifrado_atbash(texto: str) -> dict:
    """
    Cifra usando ATBASH: A↔Z, B↔Y, … (simétrico, cifrar = descifrar).
    Soporta mayúsculas, minúsculas y caracteres no alfabéticos (sin cambio).
    """
    resultado = []
    tabla     = []
    for ch in texto:
        if ch.isalpha():
            if ch.isupper():
                nuevo = chr(ord('Z') - (ord(ch) - ord('A')))
            else:
                nuevo = chr(ord('z') - (ord(ch) - ord('a')))
            resultado.append(nuevo)
            tabla.append({"Original": ch, "Posición": ord(ch.upper()) - ord('A'),
                          "Espejo": ord(nuevo.upper()) - ord('A'), "Resultado": nuevo})
        else:
            resultado.append(ch)
            tabla.append({"Original": ch, "Posición": "—", "Espejo": "—", "Resultado": ch})
    return {"resultado": "".join(resultado), "tabla": tabla}


# ── 2.5 Transposición Columnar Simple ───────────────────────
def cifrado_transposicion_columnar(texto: str, clave: str, modo: str = "cifrar") -> dict:
    """
    Transpone columnas según el orden lexicográfico de la clave.
    """
    texto_limpio = texto.replace(" ", "_")  # preserva espacios como _
    n_cols   = len(clave)
    orden    = sorted(range(n_cols), key=lambda i: clave[i])
    orden_inv = [0] * n_cols
    for i, o in enumerate(orden):
        orden_inv[o] = i
    pasos = [f"Clave: {clave}",
             f"Orden de columnas (por clave): {orden}",
             f"Número de columnas: {n_cols}"]

    if modo == "cifrar":
        # Rellenar con 'X' si faltan caracteres
        pad = (-len(texto_limpio)) % n_cols
        texto_pad = texto_limpio + "X" * pad
        filas = [texto_pad[i:i+n_cols] for i in range(0, len(texto_pad), n_cols)]
        pasos.append(f"Texto en filas:\n" + "\n".join(filas))
        cifrado = "".join("".join(fila[i] for fila in filas) for i in orden)
        pasos.append(f"Leer columnas en orden {orden}: {cifrado}")
        return {"resultado": cifrado, "filas": filas, "orden": orden, "pasos": pasos}
    else:
        n_filas = -(-len(texto_limpio) // n_cols)
        longitud = len(texto_limpio)
        extra    = n_filas * n_cols - longitud
        len_cols = [n_filas - (1 if orden.index(i) >= (n_cols - extra) else 0) for i in range(n_cols)]
        col_data, pos = [], 0
        for c in orden:
            col_data.append((c, texto_limpio[pos:pos+len_cols[c]]))
            pos += len_cols[c]
        col_data.sort(key=lambda x: x[0])
        filas   = ["".join(col_data[c][1][r] if r < len(col_data[c][1]) else "" for c in range(n_cols))
                   for r in range(n_filas)]
        claro   = "".join(filas).rstrip("X")
        pasos.append(f"Texto descifrado (filas): {'|'.join(filas)}")
        return {"resultado": claro, "filas": filas, "orden": orden, "pasos": pasos}


# ── 2.6 Cifrado Afín ────────────────────────────────────────
def cifrado_afin(texto: str, a: int, b: int, modo: str = "cifrar") -> dict:
    """
    Cifrado afín: C = (a·P + b) mod 26.
    Requiere que MCD(a, 26) = 1.
    """
    if gcd(a, 26) != 1:
        return {"error": f"'a'={a} no es válido: MCD({a}, 26) = {gcd(a, 26)} ≠ 1. 'a' debe ser coprimo con 26."}
    # Inverso multiplicativo de a mod 26
    a_inv = pow(a, -1, 26)
    resultado = []
    tabla     = []
    for ch in texto:
        if ch.isalpha():
            upper = ch.isupper()
            p     = ord(ch.upper()) - ord('A')
            if modo == "cifrar":
                c    = (a * p + b) % 26
                oper = f"({a}×{p}+{b}) mod 26"
            else:
                c    = (a_inv * (p - b)) % 26
                oper = f"({a_inv}×({p}-{b})) mod 26"
            nuevo = chr(c + ord('A'))
            if not upper:
                nuevo = nuevo.lower()
            resultado.append(nuevo)
            tabla.append({"Original": ch, "Pos": p, "Operación": oper, "Pos resultado": c, "Resultado": nuevo})
        else:
            resultado.append(ch)
            tabla.append({"Original": ch, "Pos": "—", "Operación": "—", "Pos resultado": "—", "Resultado": ch})
    return {"resultado": "".join(resultado), "a_inv": a_inv, "tabla": tabla}


# ── 2.7 Cifra de Sustitución Simple ─────────────────────────
def _generar_alfabeto_sustitucion(clave: str) -> str:
    """Genera el alfabeto de sustitución a partir de una clave (elimina duplicados y completa)."""
    clave_up  = clave.upper()
    visto     = []
    for ch in clave_up:
        if ch.isalpha() and ch not in visto:
            visto.append(ch)
    for ch in ALFA26:
        if ch not in visto:
            visto.append(ch)
    return "".join(visto)

def cifrado_sustitucion_simple(texto: str, clave: str, modo: str = "cifrar") -> dict:
    """
    Cifrado de sustitución simple monoalfabética.
    El alfabeto de sustitución se genera desde la clave.
    """
    alfa_sust = _generar_alfabeto_sustitucion(clave)
    resultado = []
    tabla     = []
    for ch in texto:
        upper = ch.isupper()
        ch_up = ch.upper()
        if ch_up in ALFA26:
            if modo == "cifrar":
                idx  = ALFA26.index(ch_up)
                nuevo = alfa_sust[idx]
            else:
                idx  = alfa_sust.index(ch_up)
                nuevo = ALFA26[idx]
            if not upper:
                nuevo = nuevo.lower()
            resultado.append(nuevo)
            tabla.append({"Original": ch, "Índice": ALFA26.index(ch_up) if modo=="cifrar" else alfa_sust.index(ch_up),
                          "Resultado": nuevo})
        else:
            resultado.append(ch)
            tabla.append({"Original": ch, "Índice": "—", "Resultado": ch})
    return {
        "resultado": "".join(resultado),
        "alfabeto_plano": ALFA26,
        "alfabeto_sust": alfa_sust,
        "tabla": tabla,
    }
