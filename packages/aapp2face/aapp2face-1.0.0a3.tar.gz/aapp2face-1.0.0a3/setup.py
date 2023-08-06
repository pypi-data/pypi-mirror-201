# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aapp2face', 'aapp2face.cli', 'aapp2face.cli.resources', 'aapp2face.lib']

package_data = \
{'': ['*'], 'aapp2face.cli.resources': ['sim-responses/*']}

install_requires = \
['typer[all]>=0.7.0,<0.8.0', 'zeep[xmlsec]>=4.2.1,<5.0.0']

entry_points = \
{'console_scripts': ['aapp2face = aapp2face.cli.main:app']}

setup_kwargs = {
    'name': 'aapp2face',
    'version': '1.0.0a3',
    'description': 'Librería Python para interactuar con los servicios web de FACe desde el lado de las Administraciones Públicas',
    'long_description': '# 🏛️ AAPP2FACe\n\n**AAPP2FACe** es una librería Python para interactuar con los servicios\nweb de FACe, el Punto General de Entrada de Facturas de la\nAdministración General del Estado, desde el lado de las Administraciones\nPúblicas Españolas.\n\nEstá diseñada para ser fácil de usar por desarrolladores y dispone de\nuna interfaz de línea de comandos (CLI) que también le permite ser usada\npor usuarios finales.\n\n---\n\n**Documentación**: <a href="https://antmartinez68.github.io/aapp2face" target="_blank">https://antmartinez68.github.io/aapp2face</a>\n\n**Código fuente**: <a href="https://github.com/antmartinez68/aapp2face" target="_blank">https://github.com/antmartinez68/aapp2face</a>\n\n---\n\n## Requisitos\n\n- Python v3.10\n\n## Instalación\n\n### Como librería\n\nAunque depende de cómo estés gestionando las dependencias de tu\nproyecto, por lo general querrás hacer:\n\n```shell\n$ pip install aapp2face\n```\n### Como aplicación de línea de comandos (CLI)\n\nSi solo pretendes usar la interfaz de línea de comandos, es recomendable\ninstalar AAPP2FACe usando [pipx](https://pypa.github.io/pipx):\n\n```shell\n$ pipx install aapp2face\n```\n\n## Uso básico\n\n### Como librería\n\nEl siguiente script de ejemplo muestra cómo puedes crear los objetos\nnecesarios para conectar con FACe y recuperar la información de las\nnuevas facturas que están disponibles para su descarga:\n\n```python\n>>> from aapp2face import FACeConnection, FACeSoapClient\n>>> cliente = FACeSoapClient(\n...     "https://se-face-webservice.redsara.es/facturasrcf2?wsdl",\n...     "cert.pem",\n...     "key.pem"\n... )\n>>> face = FACeConnection(cliente)\n>>> nuevas_facturas = face.solicitar_nuevas_facturas()\n>>> for factura in nuevas_facturas:\n...\xa0 \xa0 print(\n...\xa0 \xa0 \xa0 \xa0 factura.numero_registro,\n...\xa0 \xa0 \xa0 \xa0 factura.fecha_hora_registro,\n...\xa0 \xa0 \xa0 \xa0 factura.oficina_contable,\n...\xa0 \xa0 \xa0 \xa0 factura.organo_gestor,\n...\xa0 \xa0 \xa0 \xa0 factura.unidad_tramitadora,\n...\xa0 \xa0 )\n...\n```\n### Como aplicación de línea de comandos (CLI)\n\nLa misma operación anterior puedes hacerla usando la CLI. Una vez tienes\nconfigurada la aplicación, basta con que ejecutes el siguiente comando:\n\n```console\n$ aapp2face facturas nuevas\n\nNúmero registro:    202001015624\nFecha registro:     2023-01-19 10:57:38\nOficina contable:   P00000010\nÓrgano gestor:      P00000010\nUnidad tramitadora: P00000010\n\nNúmero registro:    202001017112\nFecha registro:     2013-01-20 11:05:51\nOficina contable:   P00000010\nÓrgano gestor:      P00000010\nUnidad tramitadora: P00000010\n\n2 nuevas facturas disponibles\n\n```\n\n## Constuir AAPP2FACe desde código fuente\n\nAAPP2FACe usa [Poetry](https://python-poetry.org/) como gestor de\ndependencias y empaquetado. Si quieres construirlo desde el código\nfuente, puede hacerlo mediante:\n\n```shell\n$ git clone https://github.com/antmartinez68/aapp2face\n$ cd aapp2face\n$ poetry install\n$ poetry run pytest\n$ poetry build\n```\n\n> Nota: La versión inicial de este proyecto forma parte del TFG del\nGrado en Ingeniería Informática en [UNIR](https://www.unir.net) de\nAntonio Martínez.\n',
    'author': 'Antonio Martínez',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
