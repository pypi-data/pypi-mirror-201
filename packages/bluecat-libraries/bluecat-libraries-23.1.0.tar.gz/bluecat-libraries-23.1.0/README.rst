..
    Copyright 2021 BlueCat Networks (USA) Inc. and its affiliates.
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.

BlueCat Libraries
=================

Modules for working with BlueCat products.


Example
-------

.. code-block:: python

    # Fetch all configurations from a BlueCat Address Manager server.

    from bluecat_libraries.address_manager.api import Client
    from bluecat_libraries.address_manager.constants import ObjectType

    with Client(<bam_url>) as client:
        client.login(<username>, <password>)
        configs = client.get_entities(0, ObjectType.CONFIGURATION)
        client.logout()

    for config in configs:
        print(config)


Note
----

Subpackage ``bluecat_libraries.address_manager.api.rest.provisional`` is a deprecated dependency of
BlueCat Gateway, and currently exists while we are still in the pre-deprecation-removal grace
period. It will be removed in the next release of BlueCat Libraries.
