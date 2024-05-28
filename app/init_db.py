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
            Manufacturer(manufacturer_name='Texas Instruments'),
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
            Product(id=1, title='Macbook Pro M1 2022', barcode='099555050509', quantity_total=1, price_when_bought=2000.0, description='The MacBook Pro M1 2022 is a powerful laptop designed for professionals. It features the latest M1 chip from Apple, providing blazing-fast performance and incredible battery life. With its sleek design and stunning Retina display, this laptop is perfect for all your productivity needs.', url='https://apple.com/macbook-pro-m1-2022', documentation='https://example.com/products/A001', notes='This is a note about the product.', quantity_unavailable=0, manufacturer_id=1, category_id=2, vendor_id=3),
            Product(id=2, title='iPhone 14 Pro', barcode='051111407592', quantity_total=10, price_when_bought=1200.0, description='The iPhone 14 Pro is the latest flagship smartphone from Apple. It features a stunning Super Retina XDR display, powerful A16 chip, and advanced camera system. With 5G connectivity and iOS 16, this phone delivers the ultimate mobile experience.', url='https://apple.com/iphone-14-pro', documentation='https://example.com/products/A002', notes='This is a note about the product.', quantity_unavailable=0, manufacturer_id=1, category_id=1, vendor_id=3),
            Product(id=3, title='Samsung Galaxy Tab S8', barcode='787099257798', quantity_total=0, price_when_bought=800.0, description='The Samsung Galaxy Tab S8 is a premium Android tablet with a stunning AMOLED display and powerful Snapdragon processor. With S Pen support and DeX mode, this tablet is perfect for work or play.', url='https://samsung.com/galaxy-tab-s8', documentation='https://example.com/products/A003', notes='This is a note about the product.', quantity_unavailable=0, manufacturer_id=2, category_id=3, vendor_id=4),
            Product(id=4, title='Dell XPS 15 2023', barcode='076950450479', quantity_total=4, price_when_bought=1800.0, description='The Dell XPS 15 2023 is a high-performance laptop with a stunning InfinityEdge display and powerful Intel processor. With up to 32GB of RAM and NVIDIA graphics, this laptop is perfect for creative professionals.', url='https://dell.com/xps-15-2023', documentation='https://example.com/products/A004', notes='This is a note about the product.', quantity_unavailable=0, manufacturer_id=3, category_id=2, vendor_id=5),
            Product(id=5, title='Sony Alpha A7 IV', barcode='7854123698541236', quantity_total=8, price_when_bought=2500.0, description='The Sony Alpha A7 IV is a full-frame mirrorless camera with 33MP resolution and 4K video recording. With advanced autofocus and image stabilization, this camera delivers stunning results in any situation.', url='https://sony.com/alpha-a7-iv', documentation='https://example.com/products/A005', notes='This is a note about the product.', quantity_unavailable=0, manufacturer_id=4, category_id=4, vendor_id=6),
            Product(id=6, title='Microsoft Surface Pro 8', barcode='6325874196325874', quantity_total=18, price_when_bought=1500.0, description='The Microsoft Surface Pro 8 is a versatile 2-in-1 laptop with a detachable keyboard and pen support. With the latest Intel processor and Windows 11, this device is perfect for productivity on the go.', url='https://microsoft.com/surface-pro-8', documentation='https://example.com/products/A006', notes='This is a note about the product.', quantity_unavailable=0, manufacturer_id=5, category_id=2, vendor_id=7),
            Product(id=7, title='V2 UNIT AI.CAMERA', barcode='U078-D', quantity_total=1, price_when_bought=75.0, description='The LG OLED C1 65" 4K TV offers stunning picture quality with OLED technology and 4K resolution. With support for Dolby Vision and Dolby Atmos, this TV delivers an immersive viewing experience.', url='https://lg.com/oled-c1-65', documentation='https://example.com/products/A007', notes='This is a note about the product.', quantity_unavailable=0, manufacturer_id=6, category_id=5, vendor_id=8),
            Product(id=8, title='BG-4 Tripod power bank grip', barcode='6972436382866', quantity_total=1, price_when_bought=30.0, description='The Google Pixel 7 is a flagship smartphone with a stunning display and advanced camera system. With Googles latest AI features and Android 13, this phone offers a seamless user experience.', url='https://google.com/pixel-7', documentation='https://example.com/products/A008', notes='This is a note about the product.', quantity_unavailable=0, manufacturer_id=7, category_id=1, vendor_id=9),
            Product(id=9, title='M5-WATCH Stickc plus', barcode='K016-H', quantity_total=1, price_when_bought=25.0, description='M5StickC PLUS is powered by ESP32-PICO-D4 with Wi-Fi and is an upgrade of the original M5StickC with a bigger screen .It is a portable, easy-to-use, open source, IoT development board. This tiny device will enable you to realize your ideas, enrich your creativity, and speed up your IoT prototyping. Developing with M5StickC PLUS takes away a lot of the pains from the development process. M5StickC Plus is one of the core devices in M5Stacks product series. The compact body is integrated with rich hardware resources, such as infrared, RTC, Microphone, LED, IMU, Buttons, PMU,etc. Improvements from the regular StickC are a buzzer, bigger screen (1.14-inch, 135 * 240 resolution LCD Screen) and more stable hardware design. This revision increases the display area by 18.7%, and the battery capacity from 95mAh to 120mAh. It also supports the HAT and Unit family of products. Power switch operation: Power on :Press power button for 2 seconds Power off :Press power button for 6 seconds', quantity_unavailable=0, manufacturer_id=8, category_id=2, vendor_id=10),
            Product(id=10, title='Battery Module 13.2', barcode='M120', quantity_total=1, price_when_bought=19.90, description='Battery 13.2 Module is a 1500mAh high-capacity lithium polymer battery expansion module in the M5Stack stacking module series. It\'s high-quality material guaranteed with a delicate protection board. With higher protection voltage to prevent overcharging/over-discharging failures and to ensure the safety of operation. Supports for multiple battery modules stacked. This module is the best solution for adding an autonomous and stable power supply to your devices that require long-lasting energy sources.', url='https://shop.m5stack.com/products/battery-module-13-2-1500mah', documentation='https://example.com/products/A010', notes='This is a note about the product.', quantity_unavailable=0, manufacturer_id=9, category_id=4, vendor_id=11),
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