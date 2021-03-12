import socket
import time
from utils import assert_exit

class LineUs:
    """An example class to show how to use the Line-us API"""
    def __init__(self, line_us_name):
        self.__line_us = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__line_us.connect((line_us_name, 1337))
        self.__connected = True
        self.__hello_message = self.__read_response()

    def get_hello_string(self):
        if self.__connected:
            return self.__hello_message.decode()
        else:
            return 'Not connected'

    def disconnect(self):
        """Close the connection to the Line-us"""
        self.__line_us.close()
        self.__connected = False

    def g01(self, x, y, z):
        """Send a G01 (interpolated move), and wait for the response before returning"""
        
        # Offset
        x = x + 650
        y = y - 1000

        if x<650 or x >1775:
            return
        if y<-1000 or y >1000:
            return

        assert_exit(x>=650 and x<=1775)
        assert_exit(y>=-1000 and y<=1000)

        cmd = b'G01 X'
        cmd += str(x).encode()
        cmd += b' Y'
        cmd += str(y).encode()
        cmd += b' Z'
        cmd += str(z).encode()
        self.__send_command(cmd)
        self.__read_response()

    def g94(self, speed):
        """Send a G94 set speed"""
        
        cmd = b'G94 S'
        cmd += str(speed).encode()
        self.__send_command(cmd)
        self.__read_response()

    def __read_response(self):
        """Read from the socket one byte at a time until we get a null"""
        line = b''
        while True:
            char = self.__line_us.recv(1)
            if char != b'\x00':
                line += char
            elif char == b'\x00':
                break
        return line

    def __send_command(self, command):
        """Send the command to Line-us"""
        command += b'\x00'
        self.__line_us.send(command)
