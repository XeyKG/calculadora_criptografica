"""
Módulo: Criptografía Moderna
Implementa Diffie-Hellman, RSA y exponenciación rápida con pasos detallados.
"""
from math import gcd, isqrt


# ── Utilidades ───────────────────────────────────────────────
def _es_primo(n: int) -> bool:
    """Prueba de primalidad simple (suficiente para demos educativos)."""
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def _inverso_mod(a: int, m: int) -> int:
    """Retorna el inverso multiplicativo de a mod m usando AEE."""
    g, x, _ = _aee(a, m)
    if g != 1:
        raise ValueError(f"MCD({a}, {m}) = {g} ≠ 1: no existe inverso multiplicativo.")
    return x % m

def _aee(a: int, b: int):
    """Algoritmo Extendido de Euclides. Retorna (mcd, x, y) tal que a*x + b*y = mcd."""
    old_r, r = a, b
    old_s, s = 1, 0
    while r != 0:
        q       = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
    return old_r, old_s, (old_r - old_s * a) // b if b != 0 else 0


# ── 3.1 Diffie-Hellman ───────────────────────────────────────
def calcular_diffie_hellman(p: int, g: int, a_priv: int, b_priv: int) -> dict:
    """
    Intercambio de clave Diffie-Hellman.
    p: número primo público, g: generador público,
    a_priv: clave privada de Alice, b_priv: clave privada de Bob.
    """
    errores = []
    if not _es_primo(p):
        errores.append(f"p={p} no es primo.")
    if errores:
        return {"error": " | ".join(errores)}

    A = pow(g, a_priv, p)   # Clave pública de Alice
    B = pow(g, b_priv, p)   # Clave pública de Bob
    Ka = pow(B, a_priv, p)  # Clave compartida calculada por Alice
    Kb = pow(A, b_priv, p)  # Clave compartida calculada por Bob

    pasos = [
        "=== PARÁMETROS PÚBLICOS ===",
        f"  Primo p = {p}",
        f"  Generador g = {g}",
        "",
        "=== ALICE ===",
        f"  Clave privada a = {a_priv}",
        f"  Clave pública  A = g^a mod p = {g}^{a_priv} mod {p} = {A}",
        "",
        "=== BOB ===",
        f"  Clave privada b = {b_priv}",
        f"  Clave pública  B = g^b mod p = {g}^{b_priv} mod {p} = {B}",
        "",
        "=== CLAVE COMPARTIDA ===",
        f"  Alice calcula: K = B^a mod p = {B}^{a_priv} mod {p} = {Ka}",
        f"  Bob   calcula: K = A^b mod p = {A}^{b_priv} mod {p} = {Kb}",
        f"  ¿Coinciden? {'✅ SÍ' if Ka == Kb else '❌ NO'}  →  Clave compartida K = {Ka}",
    ]
    return {
        "A": A, "B": B, "clave_compartida": Ka,
        "coinciden": Ka == Kb, "pasos": pasos,
    }


# ── 3.2 RSA ─────────────────────────────────────────────────
def calcular_rsa(p: int, q: int, e: int, mensaje: int) -> dict:
    """
    Calcula RSA completo: generación de claves, cifrado y descifrado.
    p, q: primos; e: exponente público; mensaje: entero a cifrar (M < n).
    """
    errores = []
    if not _es_primo(p): errores.append(f"p={p} no es primo.")
    if not _es_primo(q): errores.append(f"q={q} no es primo.")
    if p == q:            errores.append("p y q deben ser distintos.")
    if errores:
        return {"error": " | ".join(errores)}

    n   = p * q
    phi = (p - 1) * (q - 1)

    if gcd(e, phi) != 1:
        return {"error": f"e={e} no es válido: MCD({e}, φ({n})={phi}) = {gcd(e,phi)} ≠ 1."}
    if mensaje >= n:
        return {"error": f"El mensaje M={mensaje} debe ser menor que n={n}."}

    d = _inverso_mod(e, phi)
    C = pow(mensaje, e, n)
    M = pow(C, d, n)

    pasos = [
        "=== GENERACIÓN DE CLAVES ===",
        f"  p = {p},  q = {q}",
        f"  n = p × q = {p} × {q} = {n}",
        f"  φ(n) = (p-1)(q-1) = {p-1} × {q-1} = {phi}",
        f"  e = {e}  →  MCD({e}, {phi}) = {gcd(e, phi)}  ✓",
        f"  d = e⁻¹ mod φ(n) = {e}⁻¹ mod {phi} = {d}",
        f"  Clave pública:  (e={e}, n={n})",
        f"  Clave privada:  (d={d}, n={n})",
        "",
        "=== CIFRADO ===",
        f"  C = M^e mod n = {mensaje}^{e} mod {n} = {C}",
        "",
        "=== DESCIFRADO ===",
        f"  M = C^d mod n = {C}^{d} mod {n} = {M}",
        f"  Verificación: M original = {mensaje}  →  {'✅ Correcto' if M == mensaje else '❌ Error'}",
    ]
    return {
        "n": n, "phi": phi, "e": e, "d": d,
        "clave_publica": (e, n), "clave_privada": (d, n),
        "cifrado": C, "descifrado": M, "pasos": pasos,
    }


# ── 3.3 Exponenciación Rápida (Square and Multiply) ─────────
def exponenciacion_rapida(base: int, exp: int, mod: int) -> dict:
    """
    Calcula base^exp mod (si mod>0) usando el método de cuadrado y multiplicación.
    Muestra tabla con cada paso bit a bit.
    """
    if mod == 0:
        return {"error": "El módulo no puede ser 0."}

    exp_bin = bin(exp)[2:]  # Representación binaria del exponente
    tabla   = []
    result  = 1
    base_r  = base % mod

    for i, bit in enumerate(exp_bin):
        result = (result * result) % mod
        tabla.append({
            "Paso": i + 1, "Bit": bit,
            "Operación": f"result² mod {mod} = {result}",
            "result tras cuadrado": result,
        })
        if bit == '1':
            result = (result * base_r) % mod
            tabla[-1]["Operación"] += f"  →  ×{base_r} mod {mod} = {result}"
        tabla[-1]["result final"] = result

    pasos = [
        f"Calcular {base}^{exp} mod {mod}",
        f"Exponente en binario: {exp} = {exp_bin}₂  ({len(exp_bin)} bits)",
        f"Algoritmo: para cada bit de izquierda a derecha:",
        f"  1. Elevar al cuadrado el resultado acumulado.",
        f"  2. Si el bit es 1, multiplicar por la base.",
        f"Resultado final: {base}^{exp} mod {mod} = {result}",
    ]
    return {
        "resultado": result,
        "exp_binario": exp_bin,
        "tabla": tabla,
        "pasos": pasos,
    }
