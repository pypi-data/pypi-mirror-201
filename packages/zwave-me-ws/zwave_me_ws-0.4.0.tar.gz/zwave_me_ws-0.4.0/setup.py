# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zwave_me_ws']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0', 'websocket-client>=1.2.1,<2.0.0']

setup_kwargs = {
    'name': 'zwave-me-ws',
    'version': '0.4.0',
    'description': 'Library, implementing websocket connection to ZWave-Me',
    'long_description': 'ZWave-Me-WS is a websocket connection library for [Z-Wave.Me Z-Way](https://z-wave.me/z-way/) controllers\n\n**Installing**\n\nTo install this package use:\n\n`pip install zwave-me-ws`\n\n**Usage**\n\nTo use the connector initialize the API using:\n\n```\nfrom zwave_me_ws import ZWaveMe, ZWaveMeData\n\nzwave_api = ZWaveMe(\n  on_device_create=on_device_func\n  on_device_update=on_device_update_func,\n  on_new_device=on_device_add_func,\n  token="....", # Z-Way access token in the form .../... (remote) of /... (local)\n  url="...", # wss://find.z-wave.me or ws://IP:8083\n  platforms=[...]\n)\n\ndef on_device_add_func(self, device: ZWaveMeData)\n\ndef on_device_create_func(self, devices: list[ZWaveMeData])\n\ndef on_device_update_func(self, new_info: ZWaveMeData)\n```\n\nHere `platforms` is the list of deviceType fields to handle. Used to filter only types supported by your application. For example, \n`["sensorBinary", "lightMultilevel", "toggleButton", "thermostat", "motor", "fan", "doorlock", "switchMultilevel", "switchBinary", "sensorMultilevel", "siren", "switchRGBW", "switchRGB"]`.\n\nAvailable functions:\n```\ndevices = zwave_api.get_devices()\n\nzwave_api.send_command(device_id, command) # command can be "on", "off", "exact?level=..", "open", "close"\n\nis_connected = zwave_api.get_connection()\n\nzwave_api.close_ws()\n```\n\nDevice (ZWaveMeData) has the following fields:\n```\n  id: str\n  deviceType: str\n  title: str\n  level: Union[str, int, float]\n  deviceIdentifier: str\n  probeType: str\n  scaleTitle: str\n  min: str\n  max: str\n  color: dict\n  isFailed: bool\n  locationName: str\n  manufacturer: str\n  firmware: str\n  tags: list[str]\n  nodeId: str\n  creatorId: str\n```\n',
    'author': 'Dmitry Vlasov',
    'author_email': 'kerbalspacema@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Z-Wave-Me/zwave-me-ws',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
