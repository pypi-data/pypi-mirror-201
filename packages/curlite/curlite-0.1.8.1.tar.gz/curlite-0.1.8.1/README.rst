.. image:: https://github.com/Workfellow-Open-Source/curlite/actions/workflows/test.yml/badge.svg
    :target: https://github.com/Workfellow-Open-Source/curlite/actions/workflows/test.yml

Curlite
=======

`curlite` is a Python library that provides a simple interface to perform HTTP requests using the `curl` command. It exposes a similar interface to the popular `requests` library.
Unlike many other wrappers around `curl`, `curlite` does not require any external dependencies. as the name imply, the wrapper is pretty thin and should not require much maintenance.

This wrapper supports simple usage only. It was implemented to solve edge cases that we faced with `requests` unable to fetch certificate files from windows certificate stores.

Installation
------------

You can install `curlite` using pip:

.. code-block:: console

    $ pip install curlite

Usage
-----

You can use `curlite` to perform HTTP requests using the `curl` command. Here's an example of how to use `curlite.get()` to retrieve data from a website:

.. code-block:: python

    import curlite
    
    response = curlite.get('http://www.example.com')
    
    print(response.text)

Here's an example of how to use `curlite.post()` to send data to a website:

.. code-block:: python

    import curlite
    
    data = {'username': 'foo', 'password': 'bar'}
    response = curlite.post('http://www.example.com/login', json=data)
    
    print(response.text)

You can also use `curlite.request()` to send requests using any HTTP method:

.. code-block:: python

    import curlite
    
    response = curlite.request('PUT', 'http://www.example.com/data', json='new data')
    
    print(response.text)

Contributing
------------

We welcome contributions from the community. If you would like to contribute, please fork the repository and submit a pull request. Before submitting a pull request, please ensure that your changes pass the tests and follow our coding standards.

License
-------

`curlite` is distributed under the MIT license. See `LICENSE` for more information.
`curlite` is maintained as part of Workfellow's open source projects. See https://www.workfellow.ai for more information.

Keywords: curl, requests, http, https, ssl, certificate, windows, curlite, curl wrapper, libcurl, httpx

Home-page: https://github.com/Workfellow-Open-Source/curlite

Project-URL: Bug Tracker, https://github.com/Workfellow-Open-Source/curlite

Project-URL: Documentation, https://github.com/Workfellow-Open-Source/curlite

Requires-Python: >=3.9

Author: Mohammed Salman
