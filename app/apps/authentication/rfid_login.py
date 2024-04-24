import time
# pip install pyserial
import serial
import struct
import binascii
import sys
import glob


# Scanner class
class Scanner:
    def __init__(self):
        self.port = self.serial_ports()[0]
        self.ser = self.open_serial()

    def serial_ports(self):
        # https://stackoverflow.com/questions/12090503/listing-available-com-ports-with-python
        """ Lists serial port names

            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result

    # Open serial port
    def open_serial(self):
        ser = serial.Serial(self.port, 115200, timeout=0.1, stopbits=1, bytesize=8)
        return ser

    def piccactivate(self):
        ''' Define the HEX code
            ACK;Length;Length;CMD;Data;XOR-Checksum
            PICCACTIVATE = 0x22
            Input:
                ucRst_1ms: Refer to PiccReset command, if set, the antenna
                           will close for ucRst_1ms(ms) first and then Open
                ucReqCode: 0x26 IDLE,0x52 ALL
        '''
        hex_code = b'\x50\x00\x02\x22\x10\x26\x46'

        print(f"HEX code: {hex_code}")

        try:
            # Write the HEX code to the serial port
            self.ser.write(hex_code)

            # Wait for a short time to allow the RFID reader to respond
            time.sleep(0.1)

            # ACK;Length;CMD;Data;XOR
            # Read the response from the RFID reader
            response = self.ser.read(self.ser.in_waiting)

            hex_response = binascii.hexlify(response)

            # Print the response
            print(f"Response from RFID reader: {response}")
            print(f"Response from RFID reader (hex): {hex_response}")

            return hex_response

        except Exception as e:
            print(f"Error: {e}")

    # third byte is the length of the data without the header and xor
    def response_parse(self, res):
        # Third byte. Length in bytes
        length = res[2:6]
        # Hex to int
        length = int(length, 16) * 2
        print(f"Data length (amount of hex chars): {length}")

        # Option 1: Grab the UID  from the back
        # res1 = res[:-2]
        # uid = res1[-22:]
        # print(f"UID: {uid}")

        # Option 2: Remove the header
        res2 = res[8:]
        # Grab the data
        data = res2[:length]
        # print(f"Data: {data}")
        return data

    def set_led(self):
        '''
        SET_LED = 0x03
        Input:
            ucRates: Shine keeping times will be ucRates*50 ms and go out (500- ucRates*50)ms
            ucTimes: Flicker ucTimes times
        '''
        hex_code = b'\x50\x00\x02\x03\x05\x01\x55'
        # print(f"HEX code: {hex_code}")

        try:
            # Write the HEX code to the serial port
            self.ser.write(hex_code)
            print("SET LED")

            # Wait for a short time to allow the RFID reader to respond
            time.sleep(0.1)

            # ACK;Length;CMD;Data;XOR
            # Read the response from the RFID reader
            response = self.ser.read(self.ser.in_waiting)

            hex_response = binascii.hexlify(response)

            # Print the response
            # print(f"Response from RFID reader: {response}")
            print(f"Response from RFID reader (hex): {hex_response}")

            return hex_response

        except Exception as e:
            print(f"Error: {e}")

    def set_buzzer(self):
        '''
        SET_BUZZER = 0x02
        Input:
            ucRates: beep keeping times will be ucRates*50 ms and silence(500-ucRates*50)ms
            ucTimes: beep ucTimes times.
        '''
        hex_code = b'\x50\x00\x02\x02\x03\x01\x52'
        # print(f"HEX code: {hex_code}")

        try:
            # Write the HEX code to the serial port
            self.ser.write(hex_code)
            print("SET BUZZER")

            # Wait for a short time to allow the RFID reader to respond
            time.sleep(0.1)

            # ACK;Length;CMD;Data;XOR
            # Read the response from the RFID reader
            response = self.ser.read(self.ser.in_waiting)

            hex_response = binascii.hexlify(response)

            # Print the response
            # print(f"Response from RFID reader: {response}")
            print(f"Response from RFID reader (hex): {hex_response}")

            return hex_response

        except Exception as e:
            print(f"Error: {e}")


def main():
    uid = None
    scanner = Scanner()

    print("START SCANNING:\n")
    while True:
        if scanner.ser.is_open is False:
            # print("Serial port is closed. Opening serial port...")
            scanner.open_serial()

        print("SCAN ROUND:")
        picca_res = scanner.piccactivate()
        if picca_res.startswith(b'50'):
            uid = scanner.response_parse(picca_res)
            print(f"\nUID: {uid}\n")

            scanner.set_led()
            scanner.set_buzzer()
        print("END SCAN ROUND:\n")

        if uid:
            print("UID found. Exiting...")
            break

        time.sleep(0.3)

    # close serial
    scanner.ser.close()


if __name__ == "__main__":
    main()
