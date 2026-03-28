"""
Módulo: Operaciones de Matemática Modular
Contiene todas las funciones relacionadas con aritmética modular.
"""
from math import gcd


# ── 1.1 Módulo ─────────────────────────────────────────────
def calcular_modulo(a: int, n: int) -> dict:
    """Calcula a mod n y devuelve el resultado con pasos detallados."""
    if n == 0:
        return {"error": "El módulo n no puede ser 0."}
    resultado = a % n
    cociente  = a // n
    pasos = [
        f"Operación: {a} mod {n}",
        f"Dividir {a} ÷ {n} → cociente = {cociente}, residuo = {resultado}",
        f"Fórmula: {a} = {n} × {cociente} + {resultado}",
        f"Resultado: {a} mod {n} = {resultado}",
    ]
    return {"resultado": resultado, "cociente": cociente, "pasos": pasos}


# ── 1.2 Inverso Aditivo ─────────────────────────────────────
def calcular_inverso_aditivo(a: int, n: int) -> dict:
    """Calcula el inverso aditivo de a en Z_n tal que a + (-a) ≡ 0 (mod n)."""
    if n <= 0:
        return {"error": "n debe ser un entero positivo."}
    inverso = (-a) % n
    pasos = [
        f"Inverso aditivo de {a} en Z_{n}",
        f"Fórmula: inverso = (-{a}) mod {n}",
        f"         = {-a} mod {n} = {inverso}",
        f"Verificación: {a} + {inverso} = {a + inverso} ≡ {(a + inverso) % n} (mod {n})  ✓",
    ]
    return {"resultado": inverso, "pasos": pasos}


# ── 1.3 Inverso XOR ─────────────────────────────────────────
def calcular_inverso_xor(a: int, b: int) -> dict:
    """
    XOR es auto-inverso: a XOR b XOR b = a.
    Dado a y b, muestra que (a XOR b) XOR b = a.
    """
    resultado    = a ^ b
    verificacion = resultado ^ b
    pasos = [
        f"XOR es una operación auto-inversa en GF(2^n).",
        f"Paso 1 – Cifrar:    {a} XOR {b} = {resultado}  (binario: {bin(a)} XOR {bin(b)} = {bin(resultado)})",
        f"Paso 2 – Descifrar: {resultado} XOR {b} = {verificacion}  (binario: {bin(resultado)} XOR {bin(b)} = {bin(verificacion)})",
        f"Conclusión: el inverso XOR de {resultado} con clave {b} es {verificacion}  ✓" if verificacion == a else "Error en verificación.",
    ]
    return {"cifrado": resultado, "descifrado": verificacion, "pasos": pasos}


# ── 1.4 MCD e inverso multiplicativo (existencia) ───────────
def calcular_mcd_e_inverso_mult(a: int, n: int) -> dict:
    """Calcula MCD(a, n) usando el algoritmo de Euclides e indica si existe el inverso multiplicativo."""
    # Euclides paso a paso
    pasos_euclides = []
    x, y = a, n
    while y != 0:
        q, r = divmod(x, y)
        pasos_euclides.append(f"MCD({x}, {y}): {x} = {y} × {q} + {r}")
        x, y = y, r
    mcd_val         = x
    existe_inverso  = mcd_val == 1
    conclusion = (
        f"MCD({a}, {n}) = {mcd_val} = 1  →  ✅ El inverso multiplicativo de {a} en Z_{n} EXISTE."
        if existe_inverso else
        f"MCD({a}, {n}) = {mcd_val} ≠ 1  →  ❌ El inverso multiplicativo de {a} en Z_{n} NO EXISTE."
    )
    pasos_euclides.append(conclusion)
    return {"mcd": mcd_val, "existe_inverso": existe_inverso, "pasos": pasos_euclides}


# ── 1.5 Inverso Multiplicativo – método tradicional ─────────
def calcular_inverso_mult_tradicional(a: int, n: int) -> dict:
    """Encuentra el inverso multiplicativo por búsqueda exhaustiva (fuerza bruta)."""
    if gcd(a, n) != 1:
        return {"existe": False, "resultado": None, "tabla": [],
                "pasos": [f"MCD({a}, {n}) ≠ 1  →  No existe inverso multiplicativo."]}
    tabla, resultado = [], None
    for x in range(1, n):
        producto  = (a * x) % n
        es_inv    = producto == 1
        tabla.append({"x": x, f"{a}×x": a * x, f"{a}×x mod {n}": producto, "¿Inverso?": "✓" if es_inv else ""})
        if es_inv and resultado is None:
            resultado = x
    pasos = [
        f"Buscar x ∈ {{1, …, {n-1}}} tal que {a}·x ≡ 1 (mod {n})",
        f"Inverso multiplicativo de {a} en Z_{n} = {resultado}",
        f"Verificación: {a} × {resultado} = {a * resultado} ≡ {(a * resultado) % n} (mod {n})  ✓",
    ]
    return {"existe": True, "resultado": resultado, "tabla": tabla, "pasos": pasos}


# ── 1.6 Inverso Multiplicativo – AEE ────────────────────────
def _aee_tabla(a: int, b: int) -> dict:
    """Ejecuta el Algoritmo Extendido de Euclides y devuelve la tabla completa."""
    filas = []
    r0, r1 = a, b
    s0, s1 = 1, 0
    t0, t1 = 0, 1
    filas.append({"Ronda": 0, "r": r0, "q": "—", "s": s0, "t": t0})
    filas.append({"Ronda": 1, "r": r1, "q": "—", "s": s1, "t": t1})
    ronda = 2
    while r1 != 0:
        q       = r0 // r1
        r0, r1  = r1, r0 - q * r1
        s0, s1  = s1, s0 - q * s1
        t0, t1  = t1, t0 - q * t1
        filas.append({"Ronda": ronda, "r": r1, "q": q, "s": s1, "t": t1})
        ronda += 1
    return {"mcd": r0, "x": s0, "y": t0, "total_rondas": ronda - 2, "tabla": filas}

def calcular_inverso_mult_aee(a: int, n: int) -> dict:
    """Calcula el inverso multiplicativo de a en Z_n usando el AEE."""
    if gcd(a, n) != 1:
        return {"existe": False, "pasos": [f"MCD({a}, {n}) ≠ 1  →  No existe inverso multiplicativo."]}
    res     = _aee_tabla(a, n)
    inverso = res["x"] % n
    pasos   = [
        f"Aplicar AEE({a}, {n})",
        f"Rondas ejecutadas: {res['total_rondas']}",
        f"Ecuación de Bezout: {res['x']}·{a} + {res['y']}·{n} = {res['mcd']}",
        f"Inverso = {res['x']} mod {n} = {inverso}",
        f"Verificación: {a} × {inverso} mod {n} = {(a * inverso) % n}  ✓",
    ]
    return {
        "existe": True, "inverso": inverso,
        "total_rondas": res["total_rondas"],
        "tabla": res["tabla"], "pasos": pasos,
    }
