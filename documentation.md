# 📚 Documentación — Calculadora Criptográfica

> Guía técnica detallada de cada menú, función y proceso implementado.

---

## 🗂️ Estructura del Proyecto

```
crypto_calc/
├── app.py                     ← Interfaz Streamlit (punto de entrada)
├── functions/
│   ├── __init__.py
│   ├── modular_math.py        ← Menú 1: Matemática Modular
│   ├── classic_crypto.py      ← Menú 2: Criptografía Clásica
│   ├── modern_crypto.py       ← Menú 3: Criptografía Moderna
│   ├── hash_algorithms.py     ← Menú 4: Algoritmos Hash
│   ├── encoding.py            ← Menú 5: Codificación
│   └── salt_protocol.py       ← Menú 6: Protocolo SALT
└── documentation.md           ← Este archivo
```

**Cómo ejecutar:**
```bash
python -m venv venv
venv\Scripts\activate
pip install streamlit pandas
cd crypto_calc
streamlit run app.py
```

---

## 1. Matemática Modular (`modular_math.py`)

La aritmética modular trabaja con el **residuo de una división entera**. Es la base de la criptografía moderna.

### 1.1 Módulo — `calcular_modulo(a, n)`
**Qué hace:** Calcula `a mod n`, es decir, el residuo de dividir `a` entre `n`.

**Proceso:**
```
a = n × cociente + residuo
17 = 5 × 3 + 2   →   17 mod 5 = 2
```
**Retorna:** resultado, cociente, pasos detallados.

---

### 1.2 Inverso Aditivo — `calcular_inverso_aditivo(a, n)`
**Qué hace:** Encuentra `x` tal que `a + x ≡ 0 (mod n)`.

**Fórmula:** `x = (-a) mod n`

**Ejemplo:**
```
Inverso aditivo de 3 en Z_7:
x = (-3) mod 7 = 4
Verificación: 3 + 4 = 7 ≡ 0 (mod 7) ✓
```

---

### 1.3 Inverso XOR — `calcular_inverso_xor(a, b)`
**Qué hace:** Demuestra que XOR es auto-inverso en GF(2ⁿ).

**Propiedad:** `(a XOR b) XOR b = a`

**Ejemplo:**
```
45 XOR 23 = 58   (cifrado)
58 XOR 23 = 45   (descifrado = original) ✓
```
XOR opera bit a bit. Es la base del cifrado Vernam (OTP).

---

### 1.4 MCD e Inverso Multiplicativo — `calcular_mcd_e_inverso_mult(a, n)`
**Qué hace:** Calcula el MCD usando el Algoritmo de Euclides e indica si existe el inverso multiplicativo.

**Regla:** El inverso multiplicativo de `a` en `Z_n` existe **si y solo si** `MCD(a, n) = 1`.

**Proceso del Algoritmo de Euclides:**
```
MCD(48, 18):
48 = 18 × 2 + 12
18 = 12 × 1 + 6
12 = 6  × 2 + 0
MCD = 6  →  Como 6 ≠ 1, no existe inverso multiplicativo de 48 en Z_18.
```

---

### 1.5 Inverso Multiplicativo Tradicional — `calcular_inverso_mult_tradicional(a, n)`
**Qué hace:** Busca `x` tal que `a × x ≡ 1 (mod n)` probando `x = 1, 2, …, n-1`.

**Proceso (búsqueda exhaustiva):**
```
Inverso de 3 en Z_26:
x=1: 3×1 mod 26 = 3
x=2: 3×2 mod 26 = 6
...
x=9: 3×9 = 27 mod 26 = 1 ✓  →  Inverso = 9
```
**Muestra tabla completa** de todos los productos hasta encontrar el inverso.

---

### 1.6 Inverso Multiplicativo AEE — `calcular_inverso_mult_aee(a, n)`
**Qué hace:** Usa el **Algoritmo Extendido de Euclides** (más eficiente que la búsqueda exhaustiva) para encontrar el inverso multiplicativo.

**Algoritmo:** Encuentra coeficientes de Bezout `x, y` tal que `a·x + n·y = MCD(a, n)`.  
Si MCD = 1, entonces `a·x ≡ 1 (mod n)`, es decir, `x` es el inverso.

**Tabla del AEE:**
| Ronda | r    | q  | s  | t  |
|-------|------|----|----|-----|
| 0     | a    | —  | 1  | 0   |
| 1     | n    | —  | 0  | 1   |
| 2     | r₀-q₂·r₁ | q₂ | s₀-q₂·s₁ | t₀-q₂·t₁ |
| ...   | ...  | ...| ...| ... |

**Muestra el número de rondas y la tabla completa.**

---

## 2. Criptografía Clásica (`classic_crypto.py`)

### 2.1 Cifrado Módulo 27 — `cifrado_mod27(texto, clave, modo)`
**Alfabeto:** 27 letras del español: `A B C D E F G H I J K L M N Ñ O P Q R S T U V W X Y Z`

**Cifrado:** `C = (P + clave) mod 27`  
**Descifrado:** `P = (C - clave) mod 27`

**Ejemplo (clave=3):**
```
H(7) → (7+3) mod 27 = 10 → K
```

---

### 2.2 Cifrado César — `cifrado_cesar(texto, desplazamiento, modo)`
**Qué es:** Cada letra se desplaza `k` posiciones en el alfabeto de 26 letras.

**Cifrado:** `C = (P + k) mod 26`  
**Descifrado:** `P = (C - k) mod 26`

**Ejemplo (k=3):** `A→D, B→E, Z→C`

Preserva mayúsculas/minúsculas. Los caracteres no alfabéticos se mantienen.

---

### 2.3 Cifrado Vernam (OTP) — `cifrado_vernam(texto, clave, modo)`
**Qué es:** Cifrado perfecto basado en XOR byte a byte.

**Proceso:**
```
Texto:    H    o    l    a
UTF-8:   0x48 0x6F 0x6C 0x61
Clave:    K    e    y    K
UTF-8:   0x4B 0x65 0x79 0x4B
XOR:     0x03 0x0A 0x15 0x2A  (texto cifrado)
```
La clave se repite cíclicamente si es más corta. Opera sobre bytes UTF-8.

---

### 2.4 Cifrado ATBASH — `cifrado_atbash(texto)`
**Qué es:** Cifrado de espejo: la primera letra ↔ última, etc.

**Mapeo:** `A↔Z, B↔Y, C↔X, …`  
**Fórmula:** `C = 'Z' - (P - 'A')`

Es simétrico: cifrar y descifrar son la misma operación.

---

### 2.5 Transposición Columnar — `cifrado_transposicion_columnar(texto, clave, modo)`
**Qué es:** Reorganiza las letras escribiéndolas en filas y leyendo por columnas en orden clave.

**Proceso (clave = "CLAVE"):**
```
1. Ordenar columnas por la clave: C(0) L(2) A(1) V(4) E(3) → orden: [2,0,1,4,3]
2. Escribir texto en filas de longitud 5.
3. Leer cada columna en el orden indicado.
```

---

### 2.6 Cifrado Afín — `cifrado_afin(texto, a, b, modo)`
**Fórmula cifrado:** `C = (a·P + b) mod 26`  
**Fórmula descifrado:** `P = a⁻¹·(C - b) mod 26`

**Requisito:** `MCD(a, 26) = 1` (a debe ser coprimo con 26).

**Valores válidos de a:** 1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25

---

### 2.7 Sustitución Simple — `cifrado_sustitucion_simple(texto, clave, modo)`
**Proceso para generar el alfabeto de sustitución:**
1. Tomar la clave, eliminar letras duplicadas.
2. Agregar el resto del alfabeto (no usadas) al final.
3. Esto crea un alfabeto de 26 letras permutado.

**Ejemplo (clave = "CRYPTO"):**
```
Plano:    A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
Cifrado:  C R Y P T O A B D E F G H I J K L M N Q S U V W X Z
```

---

## 3. Criptografía Moderna (`modern_crypto.py`)

### 3.1 Diffie-Hellman — `calcular_diffie_hellman(p, g, a, b)`
**Qué es:** Protocolo de intercambio de claves sobre canal público inseguro.

**Proceso:**
```
Parámetros públicos: p (primo), g (generador)
Alice: a_priv  → A = g^a mod p  (clave pública)
Bob:   b_priv  → B = g^b mod p  (clave pública)
Clave compartida: K = B^a mod p = A^b mod p
```
La seguridad se basa en la dificultad del **logaritmo discreto**.

---

### 3.2 RSA — `calcular_rsa(p, q, e, M)`
**Proceso completo:**
```
1. Elegir primos p y q.
2. n = p × q
3. φ(n) = (p-1)(q-1)
4. Elegir e tal que MCD(e, φ(n)) = 1
5. d = e⁻¹ mod φ(n)   (clave privada)
6. Cifrar:    C = M^e mod n
7. Descifrar: M = C^d mod n
```
**Clave pública:** (e, n) · **Clave privada:** (d, n)

---

### 3.3 Exponenciación Rápida — `exponenciacion_rapida(base, exp, mod)`
**Qué es:** Calcula `base^exp mod n` en O(log exp) multiplicaciones en lugar de O(exp).

**Algoritmo Square and Multiply:**
```
Convertir exponente a binario.
Para cada bit de izquierda a derecha:
  result = result² mod n
  Si bit == 1: result = result × base mod n
```

**Ejemplo: 2^10 mod 1000, exp=10 → binario 1010:**
| Paso | Bit | Cuadrado | ×Base | Result |
|------|-----|----------|-------|--------|
| 1    | 1   | 1        | ×2    | 2      |
| 2    | 0   | 4        | —     | 4      |
| 3    | 1   | 16       | ×2    | 32     |
| 4    | 0   | 1024     | —     | 24     |

---

## 4. Algoritmos Hash (`hash_algorithms.py`)

Un **hash** es una función unidireccional: transforma datos de cualquier tamaño en una cadena de longitud fija.  
Son **deterministas** (mismo input = mismo output) pero **no reversibles**.

### 4.1 MD5 — `calcular_md5(texto)`
- Produce 128 bits (32 caracteres hex).
- Obsoleto para seguridad, útil para verificación de integridad.

### 4.2 SHA-256 — `calcular_sha256(texto)`
- Produce 256 bits (64 caracteres hex).
- Estándar actual para firmas digitales y certificados.

### 4.3 SHA-512 — `calcular_sha512(texto)`
- Produce 512 bits (128 caracteres hex).
- Mayor seguridad, usado en sistemas críticos.

**Proceso general:**
```
texto → codificar a UTF-8 bytes → aplicar función hash → resultado hex
```

---

## 5. Codificación (`encoding.py`)

**Nota:** Todas las funciones soportan UTF-8 completo (emojis, tildes, ñ, etc.).

### 5.1 ASCII / Unicode Decimal
Convierte cada carácter a su valor decimal Unicode.  
`H → 72, o → 111, l → 108, a → 97`

### 5.2 Hexadecimal
Convierte los bytes UTF-8 del texto a representación hexadecimal.  
`"Hola" → 486f6c61`

### 5.3 Binario
Convierte cada byte UTF-8 a su representación en 8 bits.  
`"Hi" → 01001000 01101001`

### 5.4 Base64
Codifica bytes en grupos de 3 usando 64 caracteres (A-Z, a-z, 0-9, +, /).  
Muy usado para transportar datos binarios por canales de texto (email, JSON, URLs).  
`"Hola" → SG9sYQ==`

---

## 6. Protocolo SALT (`salt_protocol.py`)

### ¿Qué es un SALT?
Un **SALT** es una cadena aleatoria que se concatena con el password **antes de hashear**.

### ¿Por qué es necesario?
Sin SALT, dos usuarios con el mismo password tendrían el **mismo hash**, vulnerable a:
- **Ataques de diccionario:** Probar hashes precalculados de palabras comunes.
- **Rainbow tables:** Tablas precomputadas de hash→texto.

**Con SALT:**
```
hash("password")          = "5f4dcc3b..."  (siempre igual → inseguro)
hash("xK9pQ2r_" + "password") = "a1b2c3..."   (único → seguro)
hash("mN7wL4s_" + "password") = "f9e8d7..."   (distinto salt → distinto hash)
```

### 6.1 MD5 + SALT — `salt_md5(password, n_salts, salt_manual)`
### 6.2 SHA-256 + SALT — `salt_sha256(password, n_salts, salt_manual)`
### 6.3 SHA-512 + SALT — `salt_sha512(password, n_salts, salt_manual)`

**Proceso:**
```python
salt       = secrets.token_hex(16)   # 32 caracteres hex aleatorios seguros
combinado  = salt + password
hash_final = hashlib.sha256(combinado.encode("utf-8")).hexdigest()
```

**Opciones:**
- Generar N salts aleatorios y mostrar todos los hashes (demostración).
- Ingresar un salt manual específico.

---

## 🔒 Buenas Prácticas de Seguridad

| Concepto | Recomendación |
|----------|--------------|
| Almacenamiento de passwords | SHA-256/512 + SALT único por usuario |
| Integridad de archivos | SHA-256 |
| Cifrado simétrico | AES-256 (no cubierto aquí, es avanzado) |
| Intercambio de claves | Diffie-Hellman o RSA |
| Verificación rápida (no seguridad) | MD5 |

---

*Documentación generada para uso académico · Calculadora Criptográfica · UTF-8 Compatible*
