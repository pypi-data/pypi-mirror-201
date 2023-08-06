# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py_dtn7']

package_data = \
{'': ['*']}

install_requires = \
['cbor2>=5.4.3,<6.0.0',
 'requests>=2.27.1,<3.0.0',
 'websocket-client>=1.3.2,<2.0.0']

setup_kwargs = {
    'name': 'py-dtn7',
    'version': '0.3.0a1',
    'description': '',
    'long_description': '# py-dtn7 (Work in Progress -- don\'t use yet)\n\n[![Licence AGPL-3.0](https://img.shields.io/github/license/teschmitt/py-dtn7)](LICENSE)\n\nA Python wrapper library for the DTN7 REST and WebSocket API of [dtn7-rs](https://github.com/dtn7/dtn7-rs).\nThe library includes a fully spec compliant `Bundle` type (but without fragment and CRC support), which allows full\nbundle creation and (de-)serialization.\n\nThe `bundle.py`, `dtn_rest_client.py`, `utils.py` modules/files are Micropython compatible.\nBut, this requires a bit of manual library management.\nPlease refer to the Micropython installation guide below.\n\n### Getting Started\n\nTo use `py-dtn7` in your project, simply install it from PyPI with Poetry:\n\n```shell\n$ poetry install --no-dev py_dtn7\n```\n\n### Development\n\nThis is very much a work-in-progress and by far not complete. The Bundle\nimplementation is very rudimentary and does not support any blocks other\nthan Primary and Payload.\n\nTo generate the API documentation use `pdoc`:\n\n```shell\n$ pdoc ./py_dtn7 --output-directory ./docs\n```\n\n... or check out [py-dtn7.readthedocs.org](https://py-dtn7.readthedocs.org)\n\n\n## Quickstart\n\n```pycon\n>>> from py_dtn7 import DTNRESTClient\n>>> client = DTNRESTClient(host="http://localhost", port=3000)\n>>> d.peers\n{\'box1\': {\'eid\': [1, \'//box1/\'], \'addr\': {\'Ip\': \'10.0.0.42\'}, \'con_type\': \'Dynamic\', \'period\': None, \'cla_list\': [[\'MtcpConvergenceLayer\', 16162]], \'services\': {}, \'last_contact\': 1653316457}}\n>>> d.info\n{\'incoming\': 0, \'dups\': 0, \'outgoing\': 0, \'delivered\': 3, \'broken\': 0}\n```\n\nWhen sending a bundle to a known peer, we can simply supply the peer name and endpoint,\notherwise we use the complete URI:\n\n```pycon\n>>> d.send(payload={"body": "This will be transferred as json"}, peer_name="box1", endpoint="info")\n<Response [200]>\n>>> r = d.send(payload="Is there anybody out there?", destination="dtn://greatunkown/incoming")\n>>> r.content.decode("utf-8")\n\'Sent payload with 27 bytes\'\n```\n\n## Micropython Installation Guide\n\nTo be extended:\n\nThe dummy libraries `__future__.py`, `abc.py`, `typing.py`, the [micropython-cbor](https://github.com/alexmrqt/micropython-cbor/) library (specifically the `cbor.py` module/file) and `urequests` as well as `datetime` are needed:\n\n```shell\n$ mpremote mip install urequests\n$ mpremote mip install datetime\n```\n',
    'author': 'Thomas Schmitt',
    'author_email': 't.e.schmitt@posteo.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/teschmitt/py-dtn7',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
