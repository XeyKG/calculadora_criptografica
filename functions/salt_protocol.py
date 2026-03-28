"""
Módulo: Protocolo SALT
Genera hashes seguros de contraseñas con SALT para MD5, SHA-256 y SHA-512.
Muestra cómo un mismo password produce hashes diferentes con distintos salts.
"""
import hashlib
import os
import secrets


def _generar_salt(longitud: int = 16) -> str:
    """Genera un SALT aleatorio seguro de `longitud` bytes en hexadecimal."""
    return secrets.token_hex(longitud)

def _hash_con_salt(password: str, salt: str, algoritmo: str) -> dict:
    """Calcula hash(salt + password) con el algoritmo especificado."""
    combinado     = (salt + password).encode("utf-8")
    h             = hashlib.new(algoritmo)
    h.update(combinado)
    return {
        "salt": salt,
        "password": password,
        "combinado": salt + password,
        "hash": h.hexdigest(),
        "algoritmo": algoritmo.upper(),
    }

def _multiples_hashes_con_salt(password: str, algoritmo: str, n_salts: int = 5) -> dict:
    """
    Genera `n_salts` salts aleatorios y calcula el hash para cada uno.
    Demuestra que el mismo password produce hashes distintos con distintos salts.
    """
    resultados = []
    for i in range(n_salts):
        salt = _generar_salt()
        res  = _hash_con_salt(password, salt, algoritmo)
        res["#"] = i + 1
        resultados.append(res)

    pasos = [
        f"Password: {repr(password)}",
        f"Algoritmo: {algoritmo.upper()}",
        f"Se generaron {n_salts} SALTs aleatorios independientes.",
        "Observación: aunque el password es idéntico, cada SALT produce un hash completamente diferente.",
        "Esto protege contra ataques de tabla arcoíris (rainbow tables).",
    ]
    return {"resultados": resultados, "pasos": pasos}


# ── 6.1 Hash MD5 + SALT ─────────────────────────────────────
def salt_md5(password: str, n_salts: int = 5, salt_manual: str = "") -> dict:
    """Genera hashes MD5 con SALTs (automáticos o manual)."""
    if salt_manual:
        return {"unico": True, "resultado": _hash_con_salt(password, salt_manual, "md5")}
    return _multiples_hashes_con_salt(password, "md5", n_salts)


# ── 6.2 Hash SHA-256 + SALT ─────────────────────────────────
def salt_sha256(password: str, n_salts: int = 5, salt_manual: str = "") -> dict:
    """Genera hashes SHA-256 con SALTs (automáticos o manual)."""
    if salt_manual:
        return {"unico": True, "resultado": _hash_con_salt(password, salt_manual, "sha256")}
    return _multiples_hashes_con_salt(password, "sha256", n_salts)


# ── 6.3 Hash SHA-512 + SALT ─────────────────────────────────
def salt_sha512(password: str, n_salts: int = 5, salt_manual: str = "") -> dict:
    """Genera hashes SHA-512 con SALTs (automáticos o manual)."""
    if salt_manual:
        return {"unico": True, "resultado": _hash_con_salt(password, salt_manual, "sha512")}
    return _multiples_hashes_con_salt(password, "sha512", n_salts)
