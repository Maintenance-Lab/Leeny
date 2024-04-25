# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import sys
import serial
import time
import glob
import binascii
from datetime import datetime
from flask_login import UserMixin

from sqlalchemy.orm import relationship
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin

from apps import db, login_manager

from apps.authentication.util import hash_pass

class Users(db.Model, UserMixin):

    __tablename__ = 'Users'

    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(64), unique=True)
    email         = db.Column(db.String(64), unique=True)
    password      = db.Column(db.LargeBinary)

    uid_1         = db.Column(db.String(64), unique=True, nullable=True)
    uid_2         = db.Column(db.String(64), unique=True, nullable=True)
    uid_3         = db.Column(db.String(64), unique=True, nullable=True)

    oauth_github  = db.Column(db.String(100), nullable=True)

    api_token     = db.Column(db.String(100))
    api_token_ts  = db.Column(db.Integer)    
    created_at_ts = db.Column(db.Integer, default=int(datetime.now().timestamp()))
    updated_at_ts = db.Column(db.Integer, default=int(datetime.now().timestamp()), onupdate=int(datetime.now().timestamp()))

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass(value)  # we need bytes here (not plain str)

            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)


@login_manager.user_loader
def user_loader(id):
    return Users.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = Users.query.filter_by(username=username).first()
    return user if user else None


class OAuth(OAuthConsumerMixin, db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey("Users.id", ondelete="cascade"), nullable=False)
    user = db.relationship(Users)


# RFID Scanner class
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
    