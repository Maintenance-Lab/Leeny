from datetime import datetime, timedelta
import os
import shutil
import subprocess

from apps import create_app, db
from apps.config import config_dict
from apps.webapp.models import Manufacturer, Product, ProductCategory, Vendor, Ordered, Borrowed, Order
from apps.authentication.models import Users

def create_and_return_app(config_mode):
    app_config = config_dict[config_mode.capitalize()]
    app = create_app(app_config)
    app.config['DATABASE_DIR'] = app.config['SQLALCHEMY_DATABASE_URI'].split("sqlite:///")[1]
    return app, app_config

def insert_dummy_data():
    print('Inserting dummy data...')
    if not os.path.exists(sql_uri):
        initialize_database()

    with app.app_context():

        users = [
            Users(id='1', fullname='AmberAdmin', email='amber@a.nl', uid_1='44032007048a3e12796a80', role='admin'),
            Users(id='2', fullname='StudentAmber', email='amber@hva.nl', uid_1='02001804d7919327', role='student'),
            Users(id='3', fullname='Donna', email='donna@donna.nl', uid_1='440008070499d1aa3e3e80', role='admin', password='1'),
        ]


        vendors = [
            Vendor(vendor_name='KIWI Electronics'),
            Vendor(vendor_name='Distrelec'),
            Vendor(vendor_name='Conrad'),
            Vendor(vendor_name='SOS solutions'),
            Vendor(vendor_name='Toolstation'),
            Vendor(vendor_name='HBM'),
            Vendor(vendor_name='Digikey Electronics'),
            Vendor(vendor_name='Vanallesenmeer.nl'),
            Vendor(vendor_name='Bol.com'),
            Vendor(vendor_name='Amazon'),
            Vendor(vendor_name='AliExpress'),
            Vendor(vendor_name='eBay'),
            Vendor(vendor_name='Newegg'),
            Vendor(vendor_name='Mouser'),
            Vendor(vendor_name='RS Components'),
            Vendor(vendor_name='Farnell'),
            Vendor(vendor_name='TME'),
            Vendor(vendor_name='Digi-Key'),
            Vendor(vendor_name='Element14'),
            Vendor(vendor_name='Mouser Electronics'),
            ]

        categories = [
            ProductCategory(category_name='Microcontrollers'),
            ProductCategory(category_name='Sensors'),
            ProductCategory(category_name='Displays'),
            ProductCategory(category_name='Motors'),
            ProductCategory(category_name='Power'),
            ProductCategory(category_name='Connectivity'),
            ProductCategory(category_name='Tools'),
            ProductCategory(category_name='Cables'),
            ProductCategory(category_name='Components'),
            ProductCategory(category_name='Robotics'),
            ProductCategory(category_name='Audio'),
            ProductCategory(category_name='Other'),
            ProductCategory(category_name='Category 1'),
            ProductCategory(category_name='Category 2'),
            ProductCategory(category_name='Category 3'),
            ProductCategory(category_name='Category 4'),
            ProductCategory(category_name='Category 5'),
            ProductCategory(category_name='Category 6'),
            ProductCategory(category_name='Category 7'),
            ProductCategory(category_name='Category 8'),
            ProductCategory(category_name='Category 9'),
            ProductCategory(category_name='Category 10'),
            ProductCategory(category_name='Category 11'),
            ProductCategory(category_name='Category 12'),
            ProductCategory(category_name='Category 13'),
            ProductCategory(category_name='Category 14'),
            ProductCategory(category_name='Category 15'),
            ProductCategory(category_name='Category 16'),
            ProductCategory(category_name='Category 17'),
            ProductCategory(category_name='Category 18'),
            ProductCategory(category_name='Category 19'),
            ProductCategory(category_name='Category 20'),
        ]

        manufacturers = [
            Manufacturer(manufacturer_name='M5stack'),
            Manufacturer(manufacturer_name='Arduino'),
            Manufacturer(manufacturer_name='Raspberry Pi'),
            Manufacturer(manufacturer_name='Seeed Studio'),
            Manufacturer(manufacturer_name='NVidia'),
            Manufacturer(manufacturer_name='Intel'),
            Manufacturer(manufacturer_name='STMicroelectronics'),
            Manufacturer(manufacturer_name='Logitech'),
            Manufacturer(manufacturer_name='Microchip'),
            Manufacturer(manufacturer_name='NXP Semiconductors'),
            Manufacturer(manufacturer_name='Maxim Integrated'),
            Manufacturer(manufacturer_name='Analog Devices'),
            Manufacturer(manufacturer_name='On Semiconductor'),
            Manufacturer(manufacturer_name='Infineon Technologies'),
            Manufacturer(manufacturer_name='Cypress Semiconductor'),
            Manufacturer(manufacturer_name='Dialog Semiconductor'),
            Manufacturer(manufacturer_name='Samsung'),
            Manufacturer(manufacturer_name='Sony'),
            Manufacturer(manufacturer_name='LG Electronics'),
            Manufacturer(manufacturer_name='Sharp')
        ]

        products = [
            Product(id=7, title='V2 UNIT AI.CAMERA', barcode='U078-D', quantity_total=1, price_when_bought=75.0, description='The LG OLED C1 65" 4K TV offers stunning picture quality with OLED technology and 4K resolution. With support for Dolby Vision and Dolby Atmos, this TV delivers an immersive viewing experience.', url='https://lg.com/oled-c1-65', documentation='https://example.com/products/A007', notes='', quantity_unavailable=0, manufacturer_id=1, category_id=5, vendor_id=8),
            Product(id=8, title='BG-4 Tripod power bank grip', barcode='6972436382866', quantity_total=1, price_when_bought=30.0, description='The Google Pixel 7 is a flagship smartphone with a stunning display and advanced camera system. With Googles latest AI features and Android 13, this phone offers a seamless user experience.', url='https://google.com/pixel-7', documentation='https://example.com/products/A008', notes='', quantity_unavailable=0, manufacturer_id=7, category_id=1, vendor_id=9),
            Product(id=9, title='M5-WATCH Stickc plus', barcode='K016-H', quantity_total=1, price_when_bought=25.0, description='M5StickC PLUS is powered by ESP32-PICO-D4 with Wi-Fi and is an upgrade of the original M5StickC with a bigger screen .It is a portable, easy-to-use, open source, IoT development board. This tiny device will enable you to realize your ideas, enrich your creativity, and speed up your IoT prototyping. Developing with M5StickC PLUS takes away a lot of the pains from the development process. M5StickC Plus is one of the core devices in M5Stacks product series. The compact body is integrated with rich hardware resources, such as infrared, RTC, Microphone, LED, IMU, Buttons, PMU,etc. Improvements from the regular StickC are a buzzer, bigger screen (1.14-inch, 135 * 240 resolution LCD Screen) and more stable hardware design. This revision increases the display area by 18.7%, and the battery capacity from 95mAh to 120mAh. It also supports the HAT and Unit family of products. Power switch operation: Power on :Press power button for 2 seconds Power off :Press power button for 6 seconds', quantity_unavailable=0, manufacturer_id=1, category_id=2, vendor_id=10),
            Product(id=10, title='Battery Module 13.2', barcode='M120', quantity_total=2, price_when_bought=19.90, description='Battery 13.2 Module is a 1500mAh high-capacity lithium polymer battery expansion module in the M5Stack stacking module series. It\'s high-quality material guaranteed with a delicate protection board. With higher protection voltage to prevent overcharging/over-discharging failures and to ensure the safety of operation. Supports for multiple battery modules stacked. This module is the best solution for adding an autonomous and stable power supply to your devices that require long-lasting energy sources.', url='https://shop.m5stack.com/products/battery-module-13-2-1500mah', documentation='https://example.com/products/A010', notes='', quantity_unavailable=0, manufacturer_id=1, category_id=4, vendor_id=11),
            Product(id=11, title='Rasberry Pi USB-C Power Supply', barcode='644824914886', quantity_total=1, price_when_bought=8.95, description='This black official Raspberry Pi USB-C Power Supply is specifically designed for the Raspberry Pi 4 Model B and Raspberry Pi 400 computers. Featuring a 1.5m captive USB cable, this reliable, high-quality power supply provides an output of 5.1V / 3.0A DC via a USB-C connector, for all the power your Raspberry Pi 4 or 400 will need.', url='https://www.kiwi-electronics.com/en/raspberry-pi-4-usb-c-power-supply-black-eu-4270?country=NL', documentation='https://datasheets.raspberrypi.com/power-supply/15w-usb-c-power-supply-product-brief.pdf', notes='', quantity_unavailable=0, manufacturer_id=3, category_id=4, vendor_id=11),
            Product(id=12, title='Rasberry Pi 5', barcode='5056561803319', quantity_total=1, price_when_bought=87.95, description='Raspberry Pi 5 builds on the phenomenal success of Raspberry Pi 4. In comparison with its predecessor, it delivers a 2-3x increase in CPU performance, and a significant uplift in GPU performance, alongside improvements to camera, display, and USB interfacing.These interfacing improvements are delivered by the RP1 I/O controller chip, designed in-house at Raspberry Pi. For the first time, Raspberry Pi`s silicon is used on a flagship product.Raspberry Pi 5 has some neat improvements and additions compared Raspberry Pi 4:', url='https://www.kiwi-electronics.com/nl/raspberry-pi-5-8gb-11580?country=NL&utm_term=11580&gad_source=1&gclid=CjwKCAjwgdayBhBQEiwAXhMxtmOBQ6_lxymQCmAPtQjZczkEgWgEjcO_eq3M8LImKLA3d65HFeY1zBoCfxAQAvD_BwE', documentation='https://datasheets.raspberrypi.com/rpi5/raspberry-pi-5-product-brief.pdf', notes='', quantity_unavailable=0, manufacturer_id=3, category_id=4, vendor_id=11),
            Product(id=13, title='M5Stack Core 2', barcode='K010-V11', quantity_total=1, price_when_bought=47.00, description='M5Core2 is the second generation core device in the M5Stack iot development kit series, which further enhances the functions of the original generation of cores. The MCU is an ESP32 kits  model D0WDQ6-V3 and has dual core Xtensa® 32-bit 240Mhz LX6 processors that can be controlled separately. Wi-Fi are supported as standard and it includes an on board 16MB Flash and 8MB PSRAM, USB TYPE-C interface for charging, downloading of programs and serial communication, a 2.0-inch integrated capacitive touch screen, and a built-in vibration motor. M5Core2 also features a built-in RTC module which can provide accurate timing. The power supply is managed by an AXP192 power management chip, which can effectively control the power consumption of the base and a built-in green LED power indicator helps to notify the user of battery level. The battery capacity has been upgraded to 390mAh, which can power the core for much longer than the previous model.', url='https://shop.m5stack.com/products/m5stack-core2-esp32-iot-development-kit', documentation='https://docs.m5stack.com/en/core/core2', notes='', quantity_unavailable=0, manufacturer_id=1, category_id=4, vendor_id=11),
            Product(id=14, title='Logitech K400+ Keyboard', barcode=None, quantity_total=1, price_when_bought=39.95, description='The Logitech K400 Plus is a wireless keyboard that allows you to control your TV within a radius of 10 meters. Watch videos, surf the web and chat with friends without leaving the couch. The all-in-one keyboard with touchpad eliminates the hassle and clutter of multiple devices. The large, built-in 3.5-inch touchpad serves as an integrated mouse, while you can easily control the volume with the shortcut keys. It is possible to scroll vertically and horizontally and thus operate your PC, laptop or TV with just a few touches. You can install this keyboard easily and quickly via Plug and Play: simply connect the small wireless receiver to a USB port and the K400 Plus is ready for use! The battery lasts up to 18 months.', url='https://www.mediamarkt.nl/nl/product/_logitech-k400-plus-wireless-touch-keyboard-zwart-1390858.html?utm_source=google&utm_medium=cpc&utm_campaign=Shopping+-+NB.+-+NL+-+Thuiskantoor+inrichten&utm_term=&utm_content=1390858&gclsrc=aw.ds&gad_source=1&gclid=CjwKCAjwgdayBhBQEiwAXhMxtnHqIWWGSuX-7shSbZpZ2g76S2FV9lAoe33PIJXkAMlljubksMvsehoCsLEQAvD_BwE', documentation='https://support.logi.com/hc/nl/articles/360024695014--Downloads-Wireless-Touch-Keyboard-K400-Plus', notes='', quantity_unavailable=0, manufacturer_id=8, category_id=4, vendor_id=11),
            Product(id=15, title='Portenta Machine Control', barcode='7630049202955', quantity_total=1, price_when_bought=359.00, description='The Portenta Machine Control is a fully centralized, energy-efficient, industrial control unit that can control equipment and machinery. It can be programmed using the Arduino framework, or other embedded development platforms. Thanks to its computing power, the Portenta Machine Control makes it possible to carry out a wide range of predictive maintenance and AI projects. It enables the collection of real-time data from the factory environment and supports remote control of equipment, even from the cloud if desired.', url='https://www.elektor.nl/products/arduino-pro-portenta-machine-control', documentation='https://docs.arduino.cc/resources/datasheets/AKX00032-datasheet.pdf', notes='', quantity_unavailable=0, manufacturer_id=2, category_id=4, vendor_id=11),
            Product(id=16, title='Watchy de Raspberry Pi Camera', barcode=None, quantity_total=1, price_when_bought=99.00, description='Watchy is a complete Rasberry Pi with Camera Module. It is a Rasberry Pi 4 Model B with a 6mm IR CCTV Lens. This camera has a resolution of 3MP.', url='https://www.kiwi-electronics.com/nl/6mm-3mp-lens-voor-rpi-hq-camera-cs-mount-9986', documentation='https://projects.raspberrypi.org/en/projects/getting-started-with-picamera', notes='', quantity_unavailable=0, manufacturer_id=3, category_id=4, vendor_id=11),
            Product(id=17, title='V2 UNIT AI.CAMERA', barcode='U078-D', quantity_total=1, price_when_bought=75.0, description='The LG OLED C1 65" 4K TV offers stunning picture quality with OLED technology and 4K resolution. With support for Dolby Vision and Dolby Atmos, this TV delivers an immersive viewing experience.', url='https://lg.com/oled-c1-65', documentation='https://example.com/products/A007', notes='', quantity_unavailable=0, manufacturer_id=1, category_id=5, vendor_id=8),
            Product(id=18, title='BG-4 Tripod power bank grip', barcode='6972436382866', quantity_total=1, price_when_bought=30.0, description='The Google Pixel 7 is a flagship smartphone with a stunning display and advanced camera system. With Googles latest AI features and Android 13, this phone offers a seamless user experience.', url='https://google.com/pixel-7', documentation='https://example.com/products/A008', notes='', quantity_unavailable=0, manufacturer_id=7, category_id=1, vendor_id=9),
            Product(id=19, title='M5-WATCH Stickc plus', barcode='K016-H', quantity_total=1, price_when_bought=25.0, description='M5StickC PLUS is powered by ESP32-PICO-D4 with Wi-Fi and is an upgrade of the original M5StickC with a bigger screen .It is a portable, easy-to-use, open source, IoT development board. This tiny device will enable you to realize your ideas, enrich your creativity, and speed up your IoT prototyping. Developing with M5StickC PLUS takes away a lot of the pains from the development process. M5StickC Plus is one of the core devices in M5Stacks product series. The compact body is integrated with rich hardware resources, such as infrared, RTC, Microphone, LED, IMU, Buttons, PMU,etc. Improvements from the regular StickC are a buzzer, bigger screen (1.14-inch, 135 * 240 resolution LCD Screen) and more stable hardware design. This revision increases the display area by 18.7%, and the battery capacity from 95mAh to 120mAh. It also supports the HAT and Unit family of products. Power switch operation: Power on :Press power button for 2 seconds Power off :Press power button for 6 seconds', quantity_unavailable=0, manufacturer_id=1, category_id=2, vendor_id=10),
            Product(id=20, title='Battery Module 13.2', barcode='M120', quantity_total=2, price_when_bought=19.90, description='Battery 13.2 Module is a 1500mAh high-capacity lithium polymer battery expansion module in the M5Stack stacking module series. It\'s high-quality material guaranteed with a delicate protection board. With higher protection voltage to prevent overcharging/over-discharging failures and to ensure the safety of operation. Supports for multiple battery modules stacked. This module is the best solution for adding an autonomous and stable power supply to your devices that require long-lasting energy sources.', url='https://shop.m5stack.com/products/battery-module-13-2-1500mah', documentation='https://example.com/products/A010', notes='', quantity_unavailable=0, manufacturer_id=1, category_id=4, vendor_id=11),
            Product(id=21, title='Rasberry Pi USB-C Power Supply', barcode='644824914886', quantity_total=1, price_when_bought=8.95, description='This black official Raspberry Pi USB-C Power Supply is specifically designed for the Raspberry Pi 4 Model B and Raspberry Pi 400 computers. Featuring a 1.5m captive USB cable, this reliable, high-quality power supply provides an output of 5.1V / 3.0A DC via a USB-C connector, for all the power your Raspberry Pi 4 or 400 will need.', url='https://www.kiwi-electronics.com/en/raspberry-pi-4-usb-c-power-supply-black-eu-4270?country=NL', documentation='https://datasheets.raspberrypi.com/power-supply/15w-usb-c-power-supply-product-brief.pdf', notes='', quantity_unavailable=0, manufacturer_id=3, category_id=4, vendor_id=11),
            Product(id=22, title='Rasberry Pi 5', barcode='5056561803319', quantity_total=1, price_when_bought=87.95, description='Raspberry Pi 5 builds on the phenomenal success of Raspberry Pi 4. In comparison with its predecessor, it delivers a 2-3x increase in CPU performance, and a significant uplift in GPU performance, alongside improvements to camera, display, and USB interfacing.These interfacing improvements are delivered by the RP1 I/O controller chip, designed in-house at Raspberry Pi. For the first time, Raspberry Pi`s silicon is used on a flagship product.Raspberry Pi 5 has some neat improvements and additions compared Raspberry Pi 4:', url='https://www.kiwi-electronics.com/nl/raspberry-pi-5-8gb-11580?country=NL&utm_term=11580&gad_source=1&gclid=CjwKCAjwgdayBhBQEiwAXhMxtmOBQ6_lxymQCmAPtQjZczkEgWgEjcO_eq3M8LImKLA3d65HFeY1zBoCfxAQAvD_BwE', documentation='https://datasheets.raspberrypi.com/rpi5/raspberry-pi-5-product-brief.pdf', notes='', quantity_unavailable=0, manufacturer_id=3, category_id=4, vendor_id=11),
            Product(id=23, title='M5Stack Core 2', barcode='K010-V11', quantity_total=1, price_when_bought=47.00, description='M5Core2 is the second generation core device in the M5Stack iot development kit series, which further enhances the functions of the original generation of cores. The MCU is an ESP32 kits  model D0WDQ6-V3 and has dual core Xtensa® 32-bit 240Mhz LX6 processors that can be controlled separately. Wi-Fi are supported as standard and it includes an on board 16MB Flash and 8MB PSRAM, USB TYPE-C interface for charging, downloading of programs and serial communication, a 2.0-inch integrated capacitive touch screen, and a built-in vibration motor. M5Core2 also features a built-in RTC module which can provide accurate timing. The power supply is managed by an AXP192 power management chip, which can effectively control the power consumption of the base and a built-in green LED power indicator helps to notify the user of battery level. The battery capacity has been upgraded to 390mAh, which can power the core for much longer than the previous model.', url='https://shop.m5stack.com/products/m5stack-core2-esp32-iot-development-kit', documentation='https://docs.m5stack.com/en/core/core2', notes='', quantity_unavailable=0, manufacturer_id=1, category_id=4, vendor_id=11),
            Product(id=24, title='Logitech K400+ Keyboard', barcode=None, quantity_total=1, price_when_bought=39.95, description='The Logitech K400 Plus is a wireless keyboard that allows you to control your TV within a radius of 10 meters. Watch videos, surf the web and chat with friends without leaving the couch. The all-in-one keyboard with touchpad eliminates the hassle and clutter of multiple devices. The large, built-in 3.5-inch touchpad serves as an integrated mouse, while you can easily control the volume with the shortcut keys. It is possible to scroll vertically and horizontally and thus operate your PC, laptop or TV with just a few touches. You can install this keyboard easily and quickly via Plug and Play: simply connect the small wireless receiver to a USB port and the K400 Plus is ready for use! The battery lasts up to 18 months.', url='https://www.mediamarkt.nl/nl/product/_logitech-k400-plus-wireless-touch-keyboard-zwart-1390858.html?utm_source=google&utm_medium=cpc&utm_campaign=Shopping+-+NB.+-+NL+-+Thuiskantoor+inrichten&utm_term=&utm_content=1390858&gclsrc=aw.ds&gad_source=1&gclid=CjwKCAjwgdayBhBQEiwAXhMxtnHqIWWGSuX-7shSbZpZ2g76S2FV9lAoe33PIJXkAMlljubksMvsehoCsLEQAvD_BwE', documentation='https://support.logi.com/hc/nl/articles/360024695014--Downloads-Wireless-Touch-Keyboard-K400-Plus', notes='', quantity_unavailable=0, manufacturer_id=8, category_id=4, vendor_id=11),
            Product(id=25, title='Portenta Machine Control', barcode='7630049202955', quantity_total=1, price_when_bought=359.00, description='The Portenta Machine Control is a fully centralized, energy-efficient, industrial control unit that can control equipment and machinery. It can be programmed using the Arduino framework, or other embedded development platforms. Thanks to its computing power, the Portenta Machine Control makes it possible to carry out a wide range of predictive maintenance and AI projects. It enables the collection of real-time data from the factory environment and supports remote control of equipment, even from the cloud if desired.', url='https://www.elektor.nl/products/arduino-pro-portenta-machine-control', documentation='https://docs.arduino.cc/resources/datasheets/AKX00032-datasheet.pdf', notes='', quantity_unavailable=0, manufacturer_id=2, category_id=4, vendor_id=11),
            Product(id=26, title='Watchy de Raspberry Pi Camera', barcode=None, quantity_total=1, price_when_bought=99.00, description='Watchy is a complete Rasberry Pi with Camera Module. It is a Rasberry Pi 4 Model B with a 6mm IR CCTV Lens. This camera has a resolution of 3MP.', url='https://www.kiwi-electronics.com/nl/6mm-3mp-lens-voor-rpi-hq-camera-cs-mount-9986', documentation='https://projects.raspberrypi.org/en/projects/getting-started-with-picamera', notes='', quantity_unavailable=0, manufacturer_id=3, category_id=4, vendor_id=11),
        ]

        borrowed = [
            Borrowed(product_id=1, user_id=1, quantity=2, returned=0, estimated_return_date=int((datetime.now() + timedelta(days=7)).timestamp()), project="Test"),
            Borrowed(product_id=2, user_id=1, quantity=1, returned=0, estimated_return_date=int((datetime.now() + timedelta(days=3)).timestamp()), project="Test"),
            Borrowed(product_id=3, user_id=2, quantity=3, returned=0, estimated_return_date=int((datetime.now() + timedelta(days=5)).timestamp()), project="Test"),
            Borrowed(product_id=4, user_id=3, quantity=1, returned=0, estimated_return_date=int((datetime.now() + timedelta(days=7)).timestamp()), project="Test"),
            Borrowed(product_id=5, user_id=2, quantity=2, returned=0, estimated_return_date=int((datetime.now() + timedelta(days=10)).timestamp()), project="Test"),
            Borrowed(product_id=1, user_id=2, quantity=1, returned=0, estimated_return_date=int((datetime.now() + timedelta(days=2)).timestamp()), project="Test"),
            Borrowed(product_id=3, user_id=3, quantity=1, returned=0, estimated_return_date=int((datetime.now() + timedelta(days=7)).timestamp()), project="Test"),
            Borrowed(product_id=2, user_id=3, quantity=2, returned=0, estimated_return_date=int((datetime.now() + timedelta(days=3)).timestamp()), project="Test"),
            Borrowed(product_id=4, user_id=1, quantity=1, returned=0, estimated_return_date=int((datetime.now() + timedelta(days=5)).timestamp()), project="Test"),
            Borrowed(product_id=5, user_id=1, quantity=2, returned=0, estimated_return_date=int((datetime.now() + timedelta(days=10)).timestamp()), project="Test"),
        ]

        ordered = [
        Ordered(title='Macbook Pro M1 2022', quantity=1, url='https://apple.com/macbook-pro-m1-2022', price_when_bought=2000.0, order_id='1', status=2),
        Ordered(title='iPhone 13 Pro', quantity=1, url='https://apple.com/iphone-13-pro', price_when_bought=1200.0, order_id='2'),
        Ordered(title='Samsung Galaxy S22 Ultra', quantity=1, url='https://samsung.com/galaxy-s22-ultra', price_when_bought=1500.0, order_id='3', status=3),
        Ordered(title='Sony PlayStation 5', quantity=1, url='https://sony.com/playstation-5', price_when_bought=500.0, order_id='4'),
        Ordered(title='Macbook Pro M1 20221', quantity=1, url='https://apple.com/macbook-pro-m1-2022', price_when_bought=2000.0, order_id='1'),
        Ordered(title='iPhone 13 Pro1', quantity=1, url='https://apple.com/iphone-13-pro', price_when_bought=1200.0, order_id='2'),
        Ordered(title='Samsung Galaxy S22 Ultra1', quantity=1, url='https://samsung.com/galaxy-s22-ultra', price_when_bought=1500.0, order_id='3'),
        Ordered(title='Sony PlayStation 51', quantity=1, url='https://sony.com/playstation-5', price_when_bought=500.0, order_id='4'),
        Ordered(title='Macbook Pro M1 20222', quantity=1, url='https://apple.com/macbook-pro-m1-2022', price_when_bought=2000.0, order_id='1', status=2),
        Ordered(title='iPhone 13 Pro2', quantity=1, url='https://apple.com/iphone-13-pro', price_when_bought=1200.0, order_id='2'),
        Ordered(title='Samsung Galaxy S22 Ultra2', quantity=1, url='https://samsung.com/galaxy-s22-ultra', price_when_bought=1500.0, order_id='3', status=-1),
        Ordered(title='Sony PlayStation 52', quantity=1, url='https://sony.com/playstation-5', price_when_bought=500.0, order_id='4', status=3)
        ]

        order = [
        Order(user_id=2, project="Uitleensysteem", students=""),
        Order(user_id=1, project="Vriezer", students=""),
        Order(user_id=3, project="Digital Twin", students=""),
        Order(user_id=1, project="Vriezer", students="")
        ]

        db.session.bulk_save_objects(vendors)
        db.session.bulk_save_objects(categories)
        db.session.bulk_save_objects(manufacturers)
        db.session.bulk_save_objects(products)
        db.session.bulk_save_objects(ordered)
        db.session.bulk_save_objects(borrowed)
        db.session.bulk_save_objects(order)
        db.session.bulk_save_objects(users)
        db.session.commit()
        print('Dummy data inserted')

def clear_database():
    print('> Clearing database...')
    with app.app_context():
        db.drop_all()
        db.create_all()
        print('> Database cleared')

def log_database():
    with app.app_context():
        print(f"{'Model':<15}{'Count':>10}")
        print('-' * 25)
        for model in [Vendor, ProductCategory, Manufacturer, Product, Ordered, Borrowed, Order, Users]:
            count = model.query.count()
            print(f"{model.__name__:<15}{count:>10}")

def initialize_database():
    print('> Initializing database...')
    with app.app_context():
        db.init_app(app)
        db.create_all()
        print('> Database initialized')

def migrate_database():
    print('> Migrating database...')
    subprocess.run(['flask', 'db', 'init'])
    subprocess.run(['flask', 'db', 'migrate'])
    subprocess.run(['flask', 'db', 'upgrade'])
    print('> Database migrated')

def remove_migrations_folder(reset_migrations_folder = True):
    if os.path.exists('migrations') and reset_migrations_folder == True:
        shutil.rmtree('migrations')
        print('- Removed: migrations folder')

def remove_database_file():
    if os.path.exists(sql_uri):
        os.remove(sql_uri)
        print('- Removed database file:\n' + sql_uri)

def reset_database(repopulate_database = True):
    print('Resetting database...')
    remove_database_file()
    remove_migrations_folder()

    if repopulate_database:
        print('Repopulating database...')
        initialize_database()
        migrate_database()
        insert_dummy_data()

        log_database()
        print('Database repopulated')

    print('Database reset')

if __name__ == '__main__':
    config_mode = 'Debug'
    app, config = create_and_return_app(config_mode)
    sql_uri = app.config['DATABASE_DIR']

    reset_database(repopulate_database=True) # BE VERY CAUTIOUS WITH THIS