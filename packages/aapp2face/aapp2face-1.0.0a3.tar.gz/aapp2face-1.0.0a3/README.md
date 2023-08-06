# 🏛️ AAPP2FACe

**AAPP2FACe** es una librería Python para interactuar con los servicios
web de FACe, el Punto General de Entrada de Facturas de la
Administración General del Estado, desde el lado de las Administraciones
Públicas Españolas.

Está diseñada para ser fácil de usar por desarrolladores y dispone de
una interfaz de línea de comandos (CLI) que también le permite ser usada
por usuarios finales.

---

**Documentación**: <a href="https://antmartinez68.github.io/aapp2face" target="_blank">https://antmartinez68.github.io/aapp2face</a>

**Código fuente**: <a href="https://github.com/antmartinez68/aapp2face" target="_blank">https://github.com/antmartinez68/aapp2face</a>

---

## Requisitos

- Python v3.10

## Instalación

### Como librería

Aunque depende de cómo estés gestionando las dependencias de tu
proyecto, por lo general querrás hacer:

```shell
$ pip install aapp2face
```
### Como aplicación de línea de comandos (CLI)

Si solo pretendes usar la interfaz de línea de comandos, es recomendable
instalar AAPP2FACe usando [pipx](https://pypa.github.io/pipx):

```shell
$ pipx install aapp2face
```

## Uso básico

### Como librería

El siguiente script de ejemplo muestra cómo puedes crear los objetos
necesarios para conectar con FACe y recuperar la información de las
nuevas facturas que están disponibles para su descarga:

```python
>>> from aapp2face import FACeConnection, FACeSoapClient
>>> cliente = FACeSoapClient(
...     "https://se-face-webservice.redsara.es/facturasrcf2?wsdl",
...     "cert.pem",
...     "key.pem"
... )
>>> face = FACeConnection(cliente)
>>> nuevas_facturas = face.solicitar_nuevas_facturas()
>>> for factura in nuevas_facturas:
...    print(
...        factura.numero_registro,
...        factura.fecha_hora_registro,
...        factura.oficina_contable,
...        factura.organo_gestor,
...        factura.unidad_tramitadora,
...    )
...
```
### Como aplicación de línea de comandos (CLI)

La misma operación anterior puedes hacerla usando la CLI. Una vez tienes
configurada la aplicación, basta con que ejecutes el siguiente comando:

```console
$ aapp2face facturas nuevas

Número registro:    202001015624
Fecha registro:     2023-01-19 10:57:38
Oficina contable:   P00000010
Órgano gestor:      P00000010
Unidad tramitadora: P00000010

Número registro:    202001017112
Fecha registro:     2013-01-20 11:05:51
Oficina contable:   P00000010
Órgano gestor:      P00000010
Unidad tramitadora: P00000010

2 nuevas facturas disponibles

```

## Constuir AAPP2FACe desde código fuente

AAPP2FACe usa [Poetry](https://python-poetry.org/) como gestor de
dependencias y empaquetado. Si quieres construirlo desde el código
fuente, puede hacerlo mediante:

```shell
$ git clone https://github.com/antmartinez68/aapp2face
$ cd aapp2face
$ poetry install
$ poetry run pytest
$ poetry build
```

> Nota: La versión inicial de este proyecto forma parte del TFG del
Grado en Ingeniería Informática en [UNIR](https://www.unir.net) de
Antonio Martínez.
