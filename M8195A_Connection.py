"""
Everything related to connection

"""
import socket
import ipaddress
from M8195A_Errors import SocketInstrumentError


class M8195Connection:
    def __init__(self, IPAddress, port=5025, TimeOut=10):
        """
        Opens up a socket connection between an instrument and your PC
        :param IPAddress: ip address of the instrument
        :param port: [Optional] socket port of the instrument (default 5025)
        :return: Returns the socket session
        """
        self.OpenSession = []
        self.port = port
        self.IPAddress = IPAddress
        self.TimeOut = TimeOut

        # ValueError will be raised if IPAddress is not IPv4Address; during the test run, I encountered an error
        # because of the following line, so I decided to use the line after.
        # if ipaddress.ip_address(IPAddress) is ipaddress.IPv4Address:
        if ipaddress.ip_address(self.IPAddress):
            print(f'connecting to IPv4 address: {self.IPAddress}')
        else:
            raise ValueError(f'Invalid IP address')

        # AF_INET: Internet address family for IPv4
        # SOCK_STREAM: Socket type for TCP (the protocol that will be used to transport messages in the network)
        self.OpenSession = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.OpenSession.settimeout(self.TimeOut)

    def OpenSession(self):
        """
        Opens the socket connection
        :return:
        """
        print("Opening socket session and connection ...")
        print(f'connecting to M8195A ...')

        try:
            self.OpenSession.connect((self.IPAddress, self.port))
            print(f'connected to M8195A ...')
        except IOError:
            print(f'Failed to connect to the instrument, please check your IP address')

        #  setblocking(1) = socket blocking -> it will wait for the operation to complete
        #  setblocking(0) = socket non-blocking -> it will never wait for the operation to complete
        self.OpenSession.setblocking(True)
        # TODO: Should the "setblocking" be on or off?

        print(f'*IDN?: ')
        InstQuery_IDN = self.Query("*idn?", error_check=False)
        print(InstQuery_IDN)
        if "Keysight Technologies,M8195A" in InstQuery_IDN:
            print(f'success!')
        else:
            self.CloseSession()
            raise NameError(f'could not communicate with device, or not a Keysight Technologies, M8195A')

    def CloseSession(self):
        """
        Closes the socket connection
        :return: TCPIP socket connection
        """
        # if not("OpenSession" in Running_Session.keys()):
        # raise NameError(f"there is no running communication session with AWG!")
        # OpenSession = Running_Session["OpenSession"]
        print("Closing socket session and connection ...")
        self.OpenSession.shutdown(socket.SHUT_RDWR)
        self.OpenSession.close()

    def ErrorCheck(self):
        """
        Checks an instrument for errors, print them out, and clears error queue.
        Raises SocketInstrumentError with the info of the error encountered.
        :return: Returns True if any errors are encountered
        """
        Err = []
        # Remove whitespaces with strip
        # In socketscpi, replace('+', '') and replace('-', '') are used to remove extra characters before checking
        response = self.Query("SYST:ERR?", error_check=False).strip()

        # while int(response[:2]) != 0:
        while '0' not in response:
            Err.append(response)
            response = self.Query("SYST:ERR?", error_check=False).strip()

        # if int(response[:2]) != 0:
        if Err:
            raise SocketInstrumentError(Err)

    def Query(self, command, error_check=False):
        """
        Sends a query to an instrument and reads the output buffer immediately afterward
        :param command: text containing an instrument command (Documented SCPI); Should end with "?"
        :param error_check: [Optional] Check for instrument errors (default False)
        :return: Returns the query response
        """

        if not isinstance(command, str):
            raise SocketInstrumentError(f'command must be a string.')

        if '?' not in command:
            raise SocketInstrumentError(f'Query must end with "?"')

        try:
            self.OpenSession.sendall(str.encode(command + "\n"))
            response = self.Read()
            if error_check:
                Err = self.ErrorCheck()
                if Err:
                    response = "<Error>"
                    # not sure about the below one
                    print(f'Query - local: {error_check}, command: {command}')

        except socket.timeout:
            print(f'Query error:')
            self.ErrorCheck()
            response = "<Timeout Error>"

        return response

    def Read(self):
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
            response += self.OpenSession.recv(4096)

        # in socketscpi, "latin_1" is used for encoding and decoding
        # strip will remove whitespaces from the beginning and the ending part of the response (not middle part)
        return response.decode().strip()

    def Write(self, command, error_check=False):
        """
        Write a command to an instrument
        :param command: text containing an instrument command; i.e. Documented SCPI command
        :param error_check: [Optional] Check for instrument errors (default False)
        :return:
        """
        # not sure if empty "response" is necessary
        # response = ""
        if not isinstance(command, str):
            raise SocketInstrumentError(f'Argument must be a string.')

        command = '{}\n'.format(command)
        # in socketscpi, "latin_1" is used for encoding and decoding
        # in socketscpi, send is used instead of sendall
        self.OpenSession.sendall(command.encode())

        if error_check:
            print(f'Send - local: {error_check}, command: {command}')
            self.ErrorCheck()


if __name__ == '__main__':
    M8195Connection(IPAddress="192.168.1.1")
