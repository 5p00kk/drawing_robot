import serial

class Accelerometer:
    def __init__(self, serial_port):
        self.serial = serial.Serial(port=serial_port, baudrate=115200)
    
    def extract_accel(self, accel_string):
        try:
            int_list = [int(i) for i in accel_string.rstrip().split(",")]
        except ValueError:
            int_list = [0,0,0]
        
        if len(int_list) != 3:
            int_list = [0,0,0]

        return int_list

    def read_accel(self):
        self.serial.flushInput()
        self.serial.flushOutput()
        accel_string = self.serial.readline().decode('unicode_escape')
        return self.extract_accel(accel_string)