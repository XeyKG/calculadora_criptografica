"""
Módulo: Codificación / Decodificación
Soporta ASCII, Hexadecimal, Binario y Base64 con soporte UTF-8 completo.
"""
import base64


# ── 5.1 ASCII ───────────────────────────────────────────────
def ascii_codificar(texto: str) -> dict:
    """Convierte cada carácter a su valor ASCII/Unicode decimal."""
    tabla = [{"Carácter": ch, "Decimal": ord(ch), "Hex": hex(ord(ch))} for ch in texto]
    codificado = " ".join(str(ord(ch)) for ch in texto)
    return {"resultado": codificado, "tabla": tabla}

def ascii_decodificar(numeros: str) -> dict:
    """Convierte valores decimales separados por espacio a texto."""
    try:
        vals  = [int(x) for x in numeros.split()]
        texto = "".join(chr(v) for v in vals)
        tabla = [{"Decimal": v, "Hex": hex(v), "Carácter": chr(v)} for v in vals]
        return {"resultado": texto, "tabla": tabla}
    except Exception as e:
        return {"error": str(e)}


# ── 5.2 Hexadecimal ─────────────────────────────────────────
def hex_codificar(texto: str) -> dict:
    """Codifica texto UTF-8 a hexadecimal."""
    b      = texto.encode("utf-8")
    hex_s  = b.hex()
    tabla  = [{"Carácter": ch, "Bytes UTF-8": texto.encode("utf-8")[i:i+len(ch.encode("utf-8"))].hex()}
              for i, ch in enumerate(texto)]
    return {"resultado": hex_s, "tabla": tabla}

def hex_decodificar(hex_str: str) -> dict:
    """Decodifica una cadena hexadecimal a texto UTF-8."""
    try:
        b     = bytes.fromhex(hex_str.replace(" ", ""))
        texto = b.decode("utf-8")
        tabla = [{"Hex par": hex_str.replace(" ", "")[i:i+2],
                  "Byte dec": int(hex_str.replace(" ", "")[i:i+2], 16)}
                 for i in range(0, len(hex_str.replace(" ", "")), 2)]
        return {"resultado": texto, "tabla": tabla}
    except Exception as e:
        return {"error": str(e)}


# ── 5.3 Binario ─────────────────────────────────────────────
def binario_codificar(texto: str) -> dict:
    """Codifica texto UTF-8 a representación binaria."""
    b      = texto.encode("utf-8")
    bin_s  = " ".join(f"{byte:08b}" for byte in b)
    tabla  = [{"Byte dec": byte, "Binario": f"{byte:08b}"} for byte in b]
    return {"resultado": bin_s, "tabla": tabla}

def binario_decodificar(binario: str) -> dict:
    """Decodifica una cadena binaria (bytes de 8 bits separados por espacio) a texto UTF-8."""
    try:
        partes = binario.split()
        b      = bytes([int(p, 2) for p in partes])
        texto  = b.decode("utf-8")
        tabla  = [{"Binario": p, "Byte dec": int(p, 2)} for p in partes]
        return {"resultado": texto, "tabla": tabla}
    except Exception as e:
        return {"error": str(e)}


# ── 5.4 Base64 ──────────────────────────────────────────────
def base64_codificar(texto: str) -> dict:
    """Codifica texto UTF-8 a Base64."""
    b      = texto.encode("utf-8")
    b64    = base64.b64encode(b).decode("utf-8")
    pasos  = [
        f"Texto original: {repr(texto)}",
        f"Bytes UTF-8: {b.hex()}",
        f"Base64: {b64}",
        f"Longitud original: {len(b)} bytes  →  Base64: {len(b64)} caracteres",
    ]
    return {"resultado": b64, "pasos": pasos}

def base64_decodificar(b64_str: str) -> dict:
    """Decodifica una cadena Base64 a texto UTF-8."""
    try:
        b     = base64.b64decode(b64_str.encode("utf-8"))
        texto = b.decode("utf-8")
        pasos = [
            f"Base64: {b64_str}",
            f"Bytes decodificados: {b.hex()}",
            f"Texto UTF-8: {repr(texto)}",
        ]
        return {"resultado": texto, "pasos": pasos}
    except Exception as e:
        return {"error": str(e)}
