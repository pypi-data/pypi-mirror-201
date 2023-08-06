# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jetblack_fixengine',
 'jetblack_fixengine.acceptor',
 'jetblack_fixengine.admin',
 'jetblack_fixengine.initiator',
 'jetblack_fixengine.managers',
 'jetblack_fixengine.persistence',
 'jetblack_fixengine.transports',
 'jetblack_fixengine.utils']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=23.1,<24.0',
 'aiosqlite>=0.18.0,<0.19.0',
 'jetblack-fixparser>=2.4,<3.0',
 'pytz>=2022.7,<2023.0',
 'tzlocal>=4.3,<5.0']

setup_kwargs = {
    'name': 'jetblack-fixengine',
    'version': '1.0.0a5',
    'description': 'A pure Python implementation of the FIX protocol',
    'long_description': '# jetblack-fixengine\n\nA pure python asyncio FIX engine.\n\n## Status\n\nThis is work in progress.\n\n## Installation\n\nThe package can be install from the pie store.\n\n```bash\npip install jetblack-fixengine\n```\n\n## Overview\n\nThis project provides a pure Python, asyncio implementation of\na FIX engine, supporting both initiators and acceptors.\n\nThe engine uses the [jetblack-fixparser](https://github.com/rob-blackbourn/jetblack-fixparser)\npackage to present the FIX messages a plain Python objects. For example, a `LOGON` message\ncan be sent as follows:\n\n```python\nawait send_message({\n    \'MsgType\': \'LOGON\',\n    \'MsgSeqNum\': 42,\n    \'SenderCompID\': \'ME\',\n    \'TargetCompID\': \'BANK OF SOMEWHERE\',\n    \'SendingTime\': datetime.now(timezone.utc),\n    \'EncryptMethod\': "NONE",\n    \'HeartBtInt\': 30\n})\n```\n\n### FIX Protocols\n\nThe FIX protocol is a combination of *well known* messages (like `LOGON`)\nand *custom* messages (like an order to buy or sell). The protocol\nhas evolved through a number of different versions providing new features.\n\nBecause of this the protocols are provided by config files. Historically\n`XML` was used. While this is supported, `yaml` is preferred and some\nexample protocols are provided in the\n[etc](https://github.com/rob-blackbourn/jetblack-fixengine/tree/master/etc)\nfolder.\n\nCurrently supported versions are 4.0, 4.1, 4.2, 4.3, 4.4.\n\n### Initiators\n\nAn initiator is a class which inherits from `FIXApplication`, and implements a\nfew methods, and has access to `send_message` from the `fix_engine`. Here is an example.\n\n```python\nimport asyncio\nimport logging\nfrom pathlib import Path\nfrom typing import Mapping, Any\n\nfrom jetblack_fixparser import load_yaml_protocol\nfrom jetblack_fixengine import (\n    FileStore,\n    start_initiator,\n    InitiatorConfig,\n    FIXApplication,\n    FIXEngine\n)\n\nLOGGER = logging.getLogger(__name__)\n\n\nclass MyInitiator(FIXApplication):\n    """An instance of the initiator"""\n\n    async def on_logon(\n            self,\n            _message: Mapping[str, Any],\n            fix_engine: FIXEngine\n    ) -> None:\n        LOGGER.info(\'on_logon\')\n\n    async def on_logout(\n            self,\n            _message: Mapping[str, Any],\n            fix_engine: FIXEngine\n    ) -> None:\n        LOGGER.info(\'on_logout\')\n\n    async def on_application_message(\n            self,\n            _message: Mapping[str, Any],\n            fix_engine: FIXEngine\n    ) -> None:\n        LOGGER.info(\'on_application_message\')\n\n\napp = MyInitiator()\nconfig = InitiatorConfig(\n    \'127.0.0.1\',\n    9801,\n    load_yaml_protocol(Path(\'etc\') / \'FIX44.yaml\'),\n    \'INITIATOR1\',\n    \'ACCEPTOR\',\n    FileStore(Path(\'store\'))\n)\n\nlogging.basicConfig(level=logging.DEBUG)\n\nasyncio.run(\n    start_initiator(app, config)\n)\n```\n\n### Acceptor\n\nThe acceptor works in the same way as the initiator. Here is an example:\n\n```python\nimport asyncio\nimport logging\nfrom pathlib import Path\nfrom typing import Mapping, Any\n\nfrom jetblack_fixparser import load_yaml_protocol\nfrom jetblack_fixengine import (\n    FileStore,\n    start_acceptor,\n    AcceptorConfig,\n    FIXApplication,\n    FIXEngine\n)\n\n\nLOGGER = logging.getLogger(__name__)\n\n\nclass MyAcceptor(FIXApplication):\n    """An instance of the acceptor"""\n\n    async def on_logon(\n            self,\n            _message: Mapping[str, Any],\n            _fix_engine: FIXEngine\n    ) -> None:\n        LOGGER.info(\'on_logon\')\n\n    async def on_logout(\n            self,\n            _message: Mapping[str, Any],\n            _fix_engine: FIXEngine\n    ) -> None:\n        LOGGER.info(\'on_logout\')\n\n    async def on_application_message(\n            self,\n            _message: Mapping[str, Any],\n            _fix_engine: FIXEngine\n    ) -> None:\n        LOGGER.info(\'on_application_message\')\n\n\nlogging.basicConfig(level=logging.DEBUG)\n\napp = MyAcceptor()\nconfig = AcceptorConfig(\n    \'0.0.0.0\',\n    9801,\n    load_yaml_protocol(Path(\'etc\') / \'FIX44.yaml\'),\n    \'ACCEPTOR\',\n    \'INITIATOR1\',\n    FileStore(Path("store"))\n)\n\nasyncio.run(\n    start_acceptor(\n        app,\n        config\n    )\n)\n```\n\nNote that throwing the exception `LogonError` from `on_logon` will reject\nthe logon request.\n\n### Stores\n\nThe engines need to store their state. Two stores are currently provided:\na file store (`FileStore`) and sqlite (`SqlStore`).\n\n## Implementation\n\nThe engines are implemented as state machines. This means they can be\ntested without the need for IO.\n',
    'author': 'Rob Blackbourn',
    'author_email': 'rob.blackbourn@googlemail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rob-blackbourn/jetblack-fixengine',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
