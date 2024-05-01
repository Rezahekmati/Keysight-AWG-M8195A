"""
Everything related to connection

"""
import socket
import ipaddress
from m8195a_errors import SocketInstrumentError


class M8195Connection:
    """
    This is a class for M8195 connection
    """
    def __init__(self, ip_address, port=5025, time_out=10):
        """
        Opens up a socket connection between an instrument and your PC
        :param ip_address: ip address of the instrument
        :param port: [Optional] socket port of the instrument (default 5025)
        :return: Returns the socket session
        """
        self.port = port
        self.ip_address = ip_address
        self.time_out = time_out
        # self.open_session = []  # ignore it for now

        # ValueError will be raised if ip_address is not IPv4Address; during the test run, I
        # encountered an error because of the following line, so I decided to use the line after.
        # if ipaddress.ip_address(ip_address) is ipaddress.IPv4Address:
        if ipaddress.ip_address(self.ip_address):
            print('connecting to IPv4 address: {self.ip_address}')
        else:
            raise ValueError('Invalid IP address')

        print('Opening socket session and connection ...')
        print('connecting to M8195A ...')
        try:
            # AF_INET: Internet address family for IPv4
            # SOCK_STREAM: Socket type for TCP (the protocol that will be used to transport
            # messages in the network)
            self.open_session = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.open_session.connect((self.ip_address, self.port))
            print('connected to M8195A ...')
        except IOError:
            print('Failed to connect to the instrument, please check your IP address')

        #  setblocking(1) = socket blocking -> it will wait for the operation to complete
        #  setblocking(0) = socket non-blocking -> it will never wait for the operation to complete
        self.open_session.setblocking(True)

        self.open_session.settimeout(self.time_out)

        ## Ignore the next few lines for now. If everything is working, you can do this query later.
        # print('*IDN?: ')
        # inst_query_idn = self.query("*idn?", error_check=False)
        # print(inst_query_idn)
        # if "Keysight Technologies,M8195A" in inst_query_idn:
        #     print('success!')
        # else:
        #     self.session_close()
        #     raise NameError('could not communicate with device, or not a Keysight '
        #                     'Technologies, M8195A')

        ## no need to use return in __init__
        # return self.open_session

    # pylint:disable=fixme
    # TODO: This function potentially could act like a mess. Need to check it in real HW
    # pylint:disable=fixme
    # TODO: Should the "setblocking" be on or off?
    # pylint:disable=fixme
    # TODO: Defined open_session in init. Need to check it in real HW to see how it reacts!

    def session_close(self):
        """
        Closes the socket connection
        :return: TCPIP socket connection
        """
        # if not("open_session" in Running_Session.keys()):
        # raise NameError("there is no running communication session with AWG!")
        # open_session = Running_Session["open_session"]
        print("Closing socket session and connection ...")
        self.open_session.shutdown(socket.SHUT_RDWR)
        self.open_session.close()

    def error_check(self):
        """
        Checks an instrument for errors, print them out, and clears error queue.
        Raises SocketInstrumentError with the info of the error encountered.
        :return: Returns True if any errors are encountered
        """
        err = []
        # Remove whitespaces with strip
        # In socketscpi, replace('+', '') and replace('-', '') are used to remove extra
        # characters before checking
        response = self.query("SYST:ERR?", error_check=False).strip()

        # while int(response[:2]) != 0:
        while '0' not in response:
            err.append(response)
            response = self.query("SYST:ERR?", error_check=False).strip()

        # if int(response[:2]) != 0:
        if err:
            raise SocketInstrumentError(err)

        return err

    #  TODO: Not quite satisfied with the error_check; beside troubleshooting, I need to modify it
    #   in a clever way

    def query(self, command, error_check=False):
        """
        Sends a query to an instrument and reads the output buffer immediately afterward
        :param command: text containing an instrument command (Documented SCPI); Should end with "?"
        :param error_check: [Optional] Check for instrument errors (default False)
        :return: Returns the query response
        """

        if not isinstance(command, str):
            raise SocketInstrumentError('command must be a string.')

        if '?' not in command:
            raise SocketInstrumentError('Query must end with "?"')

        try:
            self.open_session.sendall(str.encode(command + "\n"))
            response = self.read()
            if error_check:
                err = self.error_check()
                if err:
                    response = "<Error>"
                    # not sure about the below one
                    print(f'Query - local: {error_check}, command: {command}')

        except socket.timeout:
            print('Query error:')
            self.error_check()
            response = "<Timeout Error>"

        return response

    def read(self):
        """
        Reads from a socket until a newline is read
        :return: Returns the data read
        """
        response = b''
        # last = len(message)
        # if message(last-1) == "\n":
        #    data = data + message[:-1]
        #    return data
        # else:
        #    data = data + message
        while response[-1:] != b'\n':
            # in socketscpi, 1024 is used
            response += self.open_session.recv(4096)

        # in socketscpi, "latin_1" is used for encoding and decoding
        # strip will remove whitespaces from the beginning and the ending part of the
        # response (not middle part)
        return response.decode().strip()

    def write(self, command, error_check=False):
        """
        Write a command to an instrument
        :param command: text containing an instrument command; i.e. Documented SCPI command
        :param error_check: [Optional] Check for instrument errors (default False)
        :return:
        """
        # not sure if empty "response" is necessary
        # response = ""
        if not isinstance(command, str):
            raise SocketInstrumentError('Argument must be a string.')

        command = f"{command}\n"
        # in socketscpi, "latin_1" is used for encoding and decoding
        # in socketscpi, send is used instead of sendall
        self.open_session.sendall(command.encode())

        if error_check:
            print(f'Send - local: {error_check}, command: {command}')
            self.error_check()


if __name__ == '__main__':
    M8195Connection(ip_address='0.0.0.0', port=5025)
