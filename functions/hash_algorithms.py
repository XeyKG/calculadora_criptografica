"""
Módulo: Algoritmos Hash
Calcula MD5, SHA-256 y SHA-512 de un texto (soporte UTF-8 completo).
"""
import hashlib


def _hash_info(texto: str, algoritmo: str) -> dict:
    """Calcula el hash del texto con el algoritmo especificado."""
    texto_bytes   = texto.encode("utf-8")
    h             = hashlib.new(algoritmo)
    h.update(texto_bytes)
    digest_hex    = h.hexdigest()
    digest_bytes  = h.digest()
    pasos = [
        f"Texto original: {repr(texto)}",
        f"Codificación:   UTF-8 → {texto_bytes.hex()}",
        f"Algoritmo:      {algoritmo.upper()}",
        f"Longitud hash:  {len(digest_bytes) * 8} bits ({len(digest_hex)} hex chars)",
        f"Hash resultante: {digest_hex}",
    ]
    return {
        "algoritmo": algoritmo.upper(),
        "texto": texto,
        "hash_hex": digest_hex,
        "hash_bytes": digest_bytes.hex(),
        "bits": len(digest_bytes) * 8,
        "pasos": pasos,
    }


# ── 4.1 MD5 ─────────────────────────────────────────────────
def calcular_md5(texto: str) -> dict:
    """Calcula el hash MD5 del texto (128 bits / 32 hex)."""
    return _hash_info(texto, "md5")


# ── 4.2 SHA-256 ─────────────────────────────────────────────
def calcular_sha256(texto: str) -> dict:
    """Calcula el hash SHA-256 del texto (256 bits / 64 hex)."""
    return _hash_info(texto, "sha256")


# ── 4.3 SHA-512 ─────────────────────────────────────────────
def calcular_sha512(texto: str) -> dict:
    """Calcula el hash SHA-512 del texto (512 bits / 128 hex)."""
    return _hash_info(texto, "sha512")
