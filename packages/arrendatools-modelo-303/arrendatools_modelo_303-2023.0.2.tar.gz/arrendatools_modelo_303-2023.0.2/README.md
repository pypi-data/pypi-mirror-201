# ArrendaTools Modelo 303
![License](https://img.shields.io/github/license/hokus15/ArrendaToolsModelo303)
[![Build Status](https://github.com/hokus15/ArrendaToolsModelo303/actions/workflows/main.yml/badge.svg)](https://github.com/hokus15/ArrendaToolsModelo303/actions)
![GitHub last commit](https://img.shields.io/github/last-commit/hokus15/ArrendaToolsModelo303?logo=github)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/hokus15/ArrendaToolsModelo303?logo=github)

Módulo de Python que genera un string para la importación de datos en el modelo 303 de la Agencia Tributaria de España del año 2023 (PRE 303 - Servicio ayuda modelo 303). El string generado se puede guardar en un fichero para importarlo en el modelo 303 para la presentación trimestral del IVA.

## Limitaciones

Este módulo está diseñado específicamente para facilitar la presentación del IVA trimestral de arrendadores de locales y viviendas urbanos que no realicen ninguna otra actividad. **No es válido para otros casos**, por lo que se recomienda su uso exclusivamente en el contexto mencionado.

Es importante tener en cuenta que este módulo no es aplicable en los siguientes casos:

- Si durante el trimestre se han realizado:
  - Ventas de inmuebles
  - Arrendamientos con opción de compra
  - Servicios complementarios de hostelería
  - Adquisiciones de bienes o servicios a proveedores extranjeros o establecidos en Canarias, Ceuta o Melilla (a excepción de obras realizadas por extranjeros).
- En declaraciones mensuales.
- En el régimen simplificado.
- En el Régimen Especial del Criterio de Caja.
- Si el % atribuible a la Administración del Estado es distinto de 100%.
- En el IVA a la importación liquidado por la Aduana pendiente de ingreso.
- En autoliquidaciones complementarias (opción y número de justificante).
- En casos en los que el volumen de operaciones anual sea igual a 0.
- Cuando existan cuotas pendientes de compensar de periodos anteriores.
- En la cuenta corriente tributaria - ingreso.
- En la cuenta corriente tributaria - devolución.
- En devoluciones por transferencia al extranjero.

Por lo tanto, se recomienda al usuario verificar que se cumplen todas las condiciones necesarias antes de utilizar este módulo para la presentación del IVA trimestral.

## Descargo de responsabilidad

Este módulo proporciona una opción para generar un archivo con la información necesaria para el modelo 303 de la Agencia Tributaria española en un formato legible por su servicio de ayuda. Sin embargo, es importante tener en cuenta que la correcta generación, presentación e introducción de los datos, así como la veracidad del contenido, son responsabilidad exclusiva del usuario. **El usuario es siempre el último responsable de verificar que los datos introducidos son correctos y cumplen con los requisitos de la Agencia Tributaria.**

Es importante destacar que **el autor del módulo está exento de cualquier tipo de responsabilidad derivada del uso de la información generada por este módulo**. La veracidad y exactitud de los datos contenidos generados es responsabilidad exclusiva del usuario, y cualquier sanción que pudiera derivarse de un uso correcto o incorrecto o fraudulento del los datos generados por este módulo será responsabilidad exclusiva del usuario.

Por tanto, se recomienda al usuario **revisar cuidadosamente la información generada antes de presentarla en la web de la Agencia Tributaria y asegurarse de que cumple con los requisitos y está libre de errores**.

## Requisitos

Este módulo requiere Python 3.7 o superior.

## Uso

El módulo cuenta con un objeto llamado Modelo303 que proporciona una interfaz para generar los datos del modelo 303 de la Agencia Tributaria. Este objeto cuenta con un método llamado `generar()` que permite crear un string, que guardado en un fichero de texto, es importable en la web de la Agencia Tributaria con los datos del modelo 303.

Para crear un objeto Modelo303, se deben proporcionar los datos necesarios para generar el modelo, como el nombre y NIF del del contribuyente, la información de facturación y los importes correspondientes. Es importante tener en cuenta que la Agencia Tributaria realiza validaciones adicionales, como verificar que el nombre y NIF coinciden con los del certificado que se usa para la presentación, que el IBAN es correcto, que la letra del NIF es correcta, entre otros.

A continuación se muestra un ejemplo de cómo crear un objeto Modelo303 y generar un archivo con los datos del modelo:

```python
from arrendatools_modelo_303.modelo_303 import Modelo303
from arrendatools_modelo_303.periodos import Periodo

periodo = Periodo.P1T
nif_empresa_desarrollo = "12345678X"
version = "v1.0"
nombre_fiscal_contribuyente = "DE LOS PALOTES PERICO"
nif_contribuyente = "98765432X"
iban = "ES0012341234123412341234"
base_imponible = 2000.0
gastos_bienes_servicios = 1000.0
iva_gastos_bienes_servicios = 210.0
adquisiciones_bienes_inversion = 2000.0
iva_adquisiciones_bienes_inversion = 420.0
volumen_anual_operaciones = 6000.0

datos_modelo = Modelo303(
    periodo=periodo,
    nif_empresa_desarrollo=nif_empresa_desarrollo,
    version=version,
    nombre_fiscal_contribuyente=nombre_fiscal_contribuyente,
    nif_contribuyente=nif_contribuyente,
    iban=iban,
    base_imponible=base_imponible,
    gastos_bienes_servicios=gastos_bienes_servicios,
    iva_gastos_bienes_servicios=iva_gastos_bienes_servicios,
    adquisiciones_bienes_inversion=adquisiciones_bienes_inversion,
    iva_adquisiciones_bienes_inversion=iva_adquisiciones_bienes_inversion,
    volumen_anual_operaciones=volumen_anual_operaciones
)

datos_fichero = datos_modelo.generar()
print(datos_fichero)

with open(f"{nif_contribuyente}_2023_{periodo.value}.303", "w") as archivo:
    archivo.write(datos_fichero)
```

Es importante tener en cuenta que, aunque el ejemplo anterior es funcional, es posible que la importación en la web de la Agencia Tributaria falle en las validaciones adicionales que esta realiza, por lo que se deben proporcionar los datos correctos para poder importar correctamente el modelo en la web de la Agencia Tributaria. 