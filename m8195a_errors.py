"""
Everything related to errors
(not completed yet)

"""


class SocketInstrumentError(Exception):
    """
    This is a class for socket instrument error
    """
    pass


class GranularityError(Exception):
    """
    Waveform Granularity Exception class
    """
    def __init__(self):
        pass

    def __str__(self):
        return 'Must be a multiplication of Granularity'


if __name__ == '__main__':
    SocketInstrumentError()
