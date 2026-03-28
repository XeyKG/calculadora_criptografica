# 🔐 Calculadora Criptográfica — Streamlit

Calculadora educativa completa con **6 menús principales** y **31 operaciones** de criptografía, matemática modular, codificación y hashing.

## 📋 Características

✅ **6 Menús principales:**
1. **Matemática Modular** — 6 operaciones (módulo, inversos, MCD, AEE)
2. **Criptografía Clásica** — 7 cifrados (César, Vernam, ATBASH, Afín, etc.)
3. **Criptografía Moderna** — Diffie-Hellman, RSA, exponenciación rápida
4. **Algoritmos Hash** — MD5, SHA-256, SHA-512
5. **Codificación** — ASCII, Hex, Binario, Base64
6. **Protocolo SALT** — Demostración de seguridad en hashing

✅ **Características técnicas:**
- 📊 Tablas interactivas paso a paso
- 🔢 Soporte UTF-8 completo (emojis, tildes, ñ)
- 📈 Visualización de procesos detallados
- ✅ Tests automatizados
- 🎨 Interfaz Streamlit moderna
- 💾 Funciones reutilizables y modularizadas

---

## 🚀 Instalación

### Requisitos
- Python 3.8+
- pip

### Pasos

```bash
# 1. Descargar o clonar el proyecto
cd crypto_calc

# 2. Instalar dependencias
pip install streamlit pandas

# 3. Ejecutar la aplicación
streamlit run app.py
```

La aplicación se abrirá en `http://localhost:8501`

---

## 📁 Estructura del Proyecto

```
crypto_calc/
├── app.py                          # Interfaz Streamlit (punto de entrada)
├── documentation.md                # Documentación técnica completa
├── ejemplos.md                     # Ejemplos prácticos paso a paso
├── README.md                       # Este archivo
└── functions/
    ├── __init__.py
    ├── modular_math.py             # Menú 1: Operaciones modulares
    ├── classic_crypto.py           # Menú 2: Cifrados clásicos
    ├── modern_crypto.py            # Menú 3: DH, RSA, Exp. Rápida
    ├── hash_algorithms.py          # Menú 4: MD5, SHA256, SHA512
    ├── encoding.py                 # Menú 5: Codificación/Decodificación
    └── salt_protocol.py            # Menú 6: SALT + Hashing seguro
```

---

## 📖 Ejemplos de Uso

### Desde Streamlit (GUI)
```
1. Ejecutar: streamlit run app.py
2. Seleccionar menú desde la barra lateral
3. Ingresar parámetros
4. Clic en botón "Calcular" o "Ejecutar"
5. Ver resultado y tabla de proceso
```

### Desde Python (como librería)
```python
from functions.modular_math import calcular_inverso_mult_aee
from functions.classic_crypto import cifrado_cesar

# Ejemplo 1: Inverso multiplicativo
resultado = calcular_inverso_mult_aee(3, 26)
print(f"Inverso: {resultado['inverso']}")
print(f"Rondas: {resultado['total_rondas']}")

# Ejemplo 2: Cifrado César
cifrado = cifrado_cesar("HOLA", 3, "cifrar")
print(f"Resultado: {cifrado['resultado']}")
```

---

## 🧮 Menú 1: Matemática Modular

| Operación | Función | Descripción |
|-----------|---------|-------------|
| 1.1 | `calcular_modulo(a, n)` | Calcula a mod n |
| 1.2 | `calcular_inverso_aditivo(a, n)` | Encuentra x tal que a+x≡0(mod n) |
| 1.3 | `calcular_inverso_xor(a, b)` | Demuestra XOR auto-inverso |
| 1.4 | `calcular_mcd_e_inverso_mult(a, n)` | MCD y verifica existencia de inverso |
| 1.5 | `calcular_inverso_mult_tradicional(a, n)` | Búsqueda exhaustiva |
| 1.6 | `calcular_inverso_mult_aee(a, n)` | Algoritmo Extendido de Euclides |

---

## 🔤 Menú 2: Criptografía Clásica

| Cifrado | Función | Parámetros |
|---------|---------|-----------|
| 2.1 | `cifrado_mod27(texto, clave, modo)` | Alfabeto español (27 letras) |
| 2.2 | `cifrado_cesar(texto, des, modo)` | Desplazamiento clásico |
| 2.3 | `cifrado_vernam(texto, clave, modo)` | XOR byte a byte (OTP) |
| 2.4 | `cifrado_atbash(texto)` | Espejo (A↔Z, B↔Y) |
| 2.5 | `cifrado_transposicion_columnar(texto, clave, modo)` | Reordenamiento de columnas |
| 2.6 | `cifrado_afin(texto, a, b, modo)` | C=(a·P+b) mod 26 |
| 2.7 | `cifrado_sustitucion_simple(texto, clave, modo)` | Sustitución monoalfabética |

---

## 🛡️ Menú 3: Criptografía Moderna

| Algoritmo | Función | Complejidad |
|-----------|---------|------------|
| 3.1 | `calcular_diffie_hellman(p, g, a, b)` | O(log a + log b) |
| 3.2 | `calcular_rsa(p, q, e, M)` | O(log e + log d) |
| 3.3 | `exponenciacion_rapida(base, exp, mod)` | O(log exp) |

---

## 🔍 Menú 4: Algoritmos Hash

| Algoritmo | Función | Bits | Hex chars |
|-----------|---------|------|-----------|
| 4.1 | `calcular_md5(texto)` | 128 | 32 |
| 4.2 | `calcular_sha256(texto)` | 256 | 64 |
| 4.3 | `calcular_sha512(texto)` | 512 | 128 |

---

## 📡 Menú 5: Codificación

| Tipo | Codificar | Decodificar |
|------|-----------|-------------|
| ASCII | `ascii_codificar(texto)` | `ascii_decodificar(nums)` |
| Hex | `hex_codificar(texto)` | `hex_decodificar(hex_str)` |
| Binario | `binario_codificar(texto)` | `binario_decodificar(bin_str)` |
| Base64 | `base64_codificar(texto)` | `base64_decodificar(b64_str)` |

---

## 🧂 Menú 6: Protocolo SALT

| Función | Descripción |
|---------|-------------|
| `salt_md5(password, n_salts, salt_manual)` | Hash MD5 + SALT |
| `salt_sha256(password, n_salts, salt_manual)` | Hash SHA-256 + SALT |
| `salt_sha512(password, n_salts, salt_manual)` | Hash SHA-512 + SALT |

Demuestra cómo el mismo password con SALTs distintos produce hashes completamente diferentes.

---

## 📚 Documentación

### `documentation.md`
Guía técnica detallada de cada menú, función, algoritmo y proceso.

### `ejemplos.md`
Ejemplos prácticos paso a paso con entradas, cálculos y salidas para cada operación.

---

## 🧪 Tests

El proyecto incluye tests automatizados para verificar funcionamiento:

```bash
python -m pytest tests/  # Si implementas tests
```

Actualmente, tests inline en el código de ejecución.

---

## 🔒 Consideraciones de Seguridad

⚠️ **Uso educativo:** Esta calculadora es para aprendizaje académico.

❌ **NO usar para:**
- Proteger datos sensibles en producción
- Almacenar passwords reales
- Generar claves criptográficas en sistemas reales

✅ **Usar para:**
- Aprender conceptos de criptografía
- Verificar procesos paso a paso
- Proyectos académicos
- Demostraciones educativas

---

## 🤝 Contribuciones

Este proyecto es parte de un trabajo académico. Para mejoras o reportes de bugs, contacta al autor.

---

## 📝 Licencia

Uso académico y educativo. © 2026

---

## 👨‍💻 Autor

Proyecto desarrollado como herramienta educativa para curso de Seguridad en Sistemas.

**Institución:** Universidad Autónoma de Bucaramanga (UNAB)  
**Programa:** Ingeniería de Sistemas  
**Fecha:** Marzo 2026

---

## 📞 Soporte

Para preguntas sobre el código o funcionamiento, revisar:
1. `documentation.md` — Teoría completa
2. `ejemplos.md` — Ejemplos prácticos
3. Comentarios en el código (`app.py` y `functions/`)

---

## 🎯 Próximas mejoras potenciales

- [ ] Agregar AES (criptografía simétrica moderna)
- [ ] Implementar curvas elípticas (ECDH)
- [ ] Exportar resultados a PDF
- [ ] Gráficos de complejidad
- [ ] Interfaz multidioma
- [ ] API REST para integración

---

**¡Gracias por usar la Calculadora Criptográfica!** 🔐
