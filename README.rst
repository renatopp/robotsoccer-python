==================
RobotSoccer-Python
==================

Python library for robotsoccer match simulator communication.

**Installing**::

    python setup.py install


**Basic Usage**::

    from robotsoccer import SoccerClient
    sc = SoccerClient()
    sc.connect(host, port)
    while True:
        force_left_motor = 1
        force_right_motor = 1
        sc.act(force_left_motor, force_right_motor)

**TLFN Client**::

    from robotsoccer import TLFNClient
    sc = TLFNClient('weightfile.wts')
    sc.connect(host, port)
    sc.run()


**More Information**:

- http://inf.ufrgs.br/~rppereira/robotsoccer.html