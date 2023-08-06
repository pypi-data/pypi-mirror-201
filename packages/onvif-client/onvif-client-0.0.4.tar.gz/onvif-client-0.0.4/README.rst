============
onvif-client
============

|python| |pypi| |license|

.. |python| image:: https://img.shields.io/pypi/pyversions/onvif-client
   :target: https://www.python.org/

.. |pypi| image:: https://img.shields.io/pypi/v/onvif-client?color=blue
   :target: https://pypi.org/project/onvif-client/

.. |license| image:: https://img.shields.io/pypi/l/onvif-client?color=blue
   :target: https://github.com/hasimoka/onvif-client/blob/main/LICENSE

**WS-Discovery and Simple ONVIF camera client library.**

=====
Usage
=====
An example of using WsDiscoveryClient class

.. code-block:: python

    from onvif import WsDiscoveryClient

    wsd_client = WsDiscoveryClient()
    nvts = wsd_client.search()
    for nvt in nvts:
        print(nvt)
    wsd_client.dispose()

An example of using OnvifClient class

.. code-block:: python
    
    from onvif import OnvifClient
    
    onvif_client = OnvifClient('192.168.0.10', 80, 'user', 'password')
    profile_tokens = onvif_client.get_profile_tokens()
    for profile_token in profile_tokens:
        print(profile_token)

============
Requirements
============
onvif-client 0.0.1 Requirements

* Python >= 3.9
* WSDiscovery >= 2.0.0 
* onvif2-zeep >= 0.3.4

=======================
Installing onvif-client
=======================
Use pip to install the binary wheels on `PyPI <https://pypi.org/project/onvif-client/>`__

.. code-block:: console
    
    $  pip install onvif-client

=======
Support
=======
Bugs may be reported at https://github.com/hasimoka/onvif-client/issues