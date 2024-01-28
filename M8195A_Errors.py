"""
Everything related to errors
(not completed yet)

"""


class SocketInstrumentError(Exception):
    """

    """
    pass


class GranularityError(Exception):
    """
    Waveform Granularity Exception class
    """
    def __init__(self):
        pass

    def __str__(self):
        return f'Must be a multiplication of Granularity'


if __name__ == '__main__':
    SocketInstrumentError()
