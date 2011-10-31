.. robotsoccer-python documentation master file, created by
   sphinx-quickstart on Sat Oct 29 11:59:17 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

RobotSoccer Python Client
=========================

Installing
----------

::

    python setup.py install


Using
-----

.. code-block:: python

    from robotsoccer import SoccerClient
    sc = SoccerClient()
    sc.connect(host, port)
    while True:
        force_left_motor = 1
        force_right_motor = 1
        sc.act(force_left_motor, force_right_motor)


TLFN Client
-----------

.. code-block:: python

    from robotsoccer import TLFNClient
    sc = TLFNClient('weightfile.wts')
    sc.connect(host, port)
    sc.run()


API
---

.. automodule:: robotsoccer.client
    :synopsis:
    :members:
    :undoc-members:

.. automodule:: robotsoccer.tlfn
    :synopsis:
    :members:
    :undoc-members:


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

