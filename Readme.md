# Data Converter

Herramienta Python para conversión entre formatos CSV y JSON con normalización de datos.

## Características

- Conversión bidireccional CSV ↔ JSON
- Normalización automática de texto (minúsculas, sin acentos)
- Limpieza de datos (campos vacíos → "n/a")
- Validación de formatos y manejo de errores
- Soporte UTF-8 para caracteres internacionales

## Requisitos

```txt
# requirements.txt
# Data Converter Requirements
# Python 3.6 or higher required

# No external dependencies needed
# Uses only Python standard library modules

# Required modules:
# - json
# - csv
# - abc
# - typing
# - os
# - unicodedata
# - re
```

## Formatos Soportados

```python
from enum import Enum

class SupportedFormats(Enum):
    CSV = ".csv"
    JSON = ".json"

    # Puedes implemertarlo este codigo si usaras mas formatos
```

## Uso Rápido

```python
from file_converter import FileConverter

# Conversión básica
FileConverter.convert("entrada.csv", "salida.json")
FileConverter.convert("datos.json", "datos.csv")

# Procesamiento manual
from text_normalizer import TextNormalizer
texto_limpio = TextNormalizer.normalizeText("Café au lait")  # → "cafe au lait"
```

## Estructura Principal

- `FileConverter`: Clase principal para conversión
- `DataConverter`: Clase abstracta para implementar nuevos formatos
- `TextNormalizer`: Utilidades de normalización de texto
- `SupportedFormats`: Enum con formatos disponibles 

## Extensión

Para agregar nuevos formatos:

1. Implementar clase que herede de `DataConverter`
2. Agregar formato al enum `SupportedFormats`
3. Registrar en el mapeo de `FileConverter.getConverter()`

## Ejemplo

```csv
Nombre,Edad,Ciudad
Juan Pérez,25,México
```

 Se convierte a ⬇️

```json
[
  {
    "nombre": "juan perez",
    "edad": "25",
    "ciudad": "mexico"
  }
]
```