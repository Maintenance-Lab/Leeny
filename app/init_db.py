from datetime import datetime, timedelta
import os
import shutil
import subprocess

from apps import create_app, db
from apps.config import config_dict
from apps.webapp.models import Manufacturer, Product, ProductCategory, Vendor, Ordered, Borrowed, Order, Category

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
        vendors = [
            Vendor(name='KIWI Electronics', website='https://www.kiwi-electronics.com'),
            Vendor(name='Distrelec', website='https://www.distrelec.nl'),
            Vendor(name='Conrad', website='https://www.conrad.nl'),
            Vendor(name='SOS solutions', website='https://www.sossolutions.nl'),
            Vendor(name='Toolstation', website='https://www.toolstation.nl'),
            Vendor(name='HBM', website='https://www.hbm-machines.com'),
            Vendor(name='Digikey Electronics', website='https://www.digikey.nl'),
            Vendor(name='Vanallesenmeer.nl', website='https://www.vanallesenmeer.nl'),
            Vendor(name='Bol.com', website='https://www.bol.com'),
            Vendor(name='Amazon', website='https://www.amazon.com'),
            Vendor(name='AliExpress', website='https://www.aliexpress.com'),
            Vendor(name='eBay', website='https://www.ebay.com'),
            Vendor(name='Newegg', website='https://www.newegg.com'),
            Vendor(name='Mouser', website='https://www.mouser.com'),
            Vendor(name='RS Components', website='https://www.rs-online.com'),
            Vendor(name='Farnell', website='https://www.farnell.com'),
            Vendor(name='TME', website='https://www.tme.eu'),
            Vendor(name='Digi-Key', website='https://www.digikey.com'),
            Vendor(name='Element14', website='https://www.element14.com'),
            Vendor(name='Mouser Electronics', website='https://www.mouser.com'),
        ]

        categories = [
            ProductCategory(name='Microcontrollers'),
            ProductCategory(name='Sensors'),
            ProductCategory(name='Displays'),
            ProductCategory(name='Motors'),
            ProductCategory(name='Power'),
            ProductCategory(name='Connectivity'),
            ProductCategory(name='Tools'),
            ProductCategory(name='Cables'),
            ProductCategory(name='Components'),
            ProductCategory(name='Robotics'),
            ProductCategory(name='Audio'),
            ProductCategory(name='Other'),
            ProductCategory(name='Category 1'),
            ProductCategory(name='Category 2'),
            ProductCategory(name='Category 3'),
            ProductCategory(name='Category 4'),
            ProductCategory(name='Category 5'),
            ProductCategory(name='Category 6'),
            ProductCategory(name='Category 7'),
            ProductCategory(name='Category 8'),
            ProductCategory(name='Category 9'),
            ProductCategory(name='Category 10'),
            ProductCategory(name='Category 11'),
            ProductCategory(name='Category 12'),
            ProductCategory(name='Category 13'),
            ProductCategory(name='Category 14'),
            ProductCategory(name='Category 15'),
            ProductCategory(name='Category 16'),
            ProductCategory(name='Category 17'),
            ProductCategory(name='Category 18'),
            ProductCategory(name='Category 19'),
            ProductCategory(name='Category 20'),
        ]

        manufacturers = [
            Manufacturer(name='M5stack'),
            Manufacturer(name='Arduino'),
            Manufacturer(name='Raspberry Pi'),
            Manufacturer(name='Seeed Studio'),
            Manufacturer(name='NVidia'),
            Manufacturer(name='Intel'),
            Manufacturer(name='STMicroelectronics'),
            Manufacturer(name='Texas Instruments'),
            Manufacturer(name='Microchip'),
            Manufacturer(name='NXP Semiconductors'),
            Manufacturer(name='Maxim Integrated'),
            Manufacturer(name='Analog Devices'),
            Manufacturer(name='On Semiconductor'),
            Manufacturer(name='Infineon Technologies'),
            Manufacturer(name='Cypress Semiconductor'),
            Manufacturer(name='Dialog Semiconductor'),
            Manufacturer(name='Samsung'),
            Manufacturer(name='Sony'),
            Manufacturer(name='LG Electronics'),
            Manufacturer(name='Sharp')
        ]

        products = [
            Product(id=1, title='Macbook Pro M1 2022', barcode='099555050509', quantity_total=1, price_when_bought=2000.0, description='The MacBook Pro M1 2022 is a powerful laptop designed for professionals. It features the latest M1 chip from Apple, providing blazing-fast performance and incredible battery life. With its sleek design and stunning Retina display, this laptop is perfect for all your productivity needs.', url='https://apple.com/macbook-pro-m1-2022', documentation='https://example.com/products/A001', notes='This is a note about the product.', quantity_unavailable=0, manufacturer_id=1, category_id=2, vendor_id=3),
            Product(id=2, title='iPhone 14 Pro', barcode='051111407592', quantity_total=10, price_when_bought=1200.0, description='The iPhone 14 Pro is the latest flagship smartphone from Apple. It features a stunning Super Retina XDR display, powerful A16 chip, and advanced camera system. With 5G connectivity and iOS 16, this phone delivers the ultimate mobile experience.', url='https://apple.com/iphone-14-pro', documentation='https://example.com/products/A002', notes='This is a note about the product.', quantity_unavailable=0, manufacturer_id=1, category_id=1, vendor_id=3),
            Product(id=3, title='Samsung Galaxy Tab S8', barcode='787099257798', quantity_total=0, price_when_bought=800.0, description='The Samsung Galaxy Tab S8 is a premium Android tablet with a stunning AMOLED display and powerful Snapdragon processor. With S Pen support and DeX mode, this tablet is perfect for work or play.', url='https://samsung.com/galaxy-tab-s8', documentation='https://example.com/products/A003', notes='This is a note about the product.', quantity_unavailable=0, manufacturer_id=2, category_id=3, vendor_id=4),
            Product(id=4, title='Dell XPS 15 2023', barcode='076950450479', quantity_total=4, price_when_bought=1800.0, description='The Dell XPS 15 2023 is a high-performance laptop with a stunning InfinityEdge display and powerful Intel processor. With up to 32GB of RAM and NVIDIA graphics, this laptop is perfect for creative professionals.', url='https://dell.com/xps-15-2023', documentation='https://example.com/products/A004', notes='This is a note about the product.', quantity_unavailable=0, manufacturer_id=3, category_id=2, vendor_id=5),
            Product(id=5, title='Sony Alpha A7 IV', barcode='7854123698541236', quantity_total=8, price_when_bought=2500.0, description='The Sony Alpha A7 IV is a full-frame mirrorless camera with 33MP resolution and 4K video recording. With advanced autofocus and image stabilization, this camera delivers stunning results in any situation.', url='https://sony.com/alpha-a7-iv', documentation='https://example.com/products/A005', notes='This is a note about the product.', quantity_unavailable=0, manufacturer_id=4, category_id=4, vendor_id=6),
            Product(id=6, title='Microsoft Surface Pro 8', barcode='6325874196325874', quantity_total=18, price_when_bought=1500.0, description='The Microsoft Surface Pro 8 is a versatile 2-in-1 laptop with a detachable keyboard and pen support. With the latest Intel processor and Windows 11, this device is perfect for productivity on the go.', url='https://microsoft.com/surface-pro-8', documentation='https://example.com/products/A006', notes='This is a note about the product.', quantity_unavailable=0, manufacturer_id=5, category_id=2, vendor_id=7),
            Product(id=7, title='LG OLED C1 65" 4K TV', barcode='3698741258963214', quantity_total=5, price_when_bought=3000.0, description='The LG OLED C1 65" 4K TV offers stunning picture quality with OLED technology and 4K resolution. With support for Dolby Vision and Dolby Atmos, this TV delivers an immersive viewing experience.', url='https://lg.com/oled-c1-65', documentation='https://example.com/products/A007', notes='This is a note about the product.', quantity_unavailable=0, manufacturer_id=6, category_id=5, vendor_id=8),
            Product(id=8, title='Google Pixel 7', barcode='9876543214567890', quantity_total=25, price_when_bought=900.0, description='The Google Pixel 7 is a flagship smartphone with a stunning display and advanced camera system. With Googles latest AI features and Android 13, this phone offers a seamless user experience.', url='https://google.com/pixel-7', documentation='https://example.com/products/A008', notes='This is a note about the product.', quantity_unavailable=0, manufacturer_id=7, category_id=1, vendor_id=9),
            Product(id=9, title='Lenovo ThinkPad X1 Carbon', barcode='7854123698574123', quantity_total=0, price_when_bought=1700.0, description='The Lenovo ThinkPad X1 Carbon is a premium ultrabook with a durable carbon fiber chassis and long battery life. With a vibrant display and powerful performance, this laptop is perfect for business users.', url='https://lenovo.com/thinkpad-x1-carbon', documentation='https://example.com/products/A009', notes='This is a note about the product.', quantity_unavailable=0, manufacturer_id=8, category_id=2, vendor_id=10),
            Product(id=10, title='Canon EOS R5', barcode='1236547893214568', quantity_total=7, price_when_bought=3500.0, description='The Canon EOS R5 is a professional full-frame mirrorless camera with 45MP resolution and 8K video recording. With advanced autofocus and image stabilization, this camera delivers exceptional results for photographers and videographers alike.', url='https://canon.com/eos-r5', documentation='https://example.com/products/A010', notes='This is a note about the product.', quantity_unavailable=0, manufacturer_id=9, category_id=4, vendor_id=11),
        ]

        borrowed = [
            # Borrowed(product_id=1, user_id=1, quantity=2, returned=0, estimated_return_date=int((datetime.now() + timedelta(days=7)).timestamp())),
            # Borrowed(product_id=2, user_id=1, quantity=1, returned=0, estimated_return_date=int((datetime.now() + timedelta(days=3)).timestamp())),
            # Borrowed(product_id=3, user_id=2, quantity=3, returned=0, estimated_return_date=int((datetime.now() + timedelta(days=5)).timestamp())),
            # Borrowed(product_id=4, user_id=3, quantity=1, returned=0, estimated_return_date=int((datetime.now() + timedelta(days=7)).timestamp())),
            # Borrowed(product_id=5, user_id=2, quantity=2, returned=0, estimated_return_date=int((datetime.now() + timedelta(days=10)).timestamp())),
            # Borrowed(product_id=1, user_id=2, quantity=1, returned=0, estimated_return_date=int((datetime.now() + timedelta(days=2)).timestamp())),
            # Borrowed(product_id=3, user_id=3, quantity=1, returned=0, estimated_return_date=int((datetime.now() + timedelta(days=7)).timestamp())),
            # Borrowed(product_id=2, user_id=3, quantity=2, returned=0, estimated_return_date=int((datetime.now() + timedelta(days=3)).timestamp())),
            # Borrowed(product_id=4, user_id=1, quantity=1, returned=0, estimated_return_date=int((datetime.now() + timedelta(days=5)).timestamp())),
            # Borrowed(product_id=5, user_id=1, quantity=2, returned=0, estimated_return_date=int((datetime.now() + timedelta(days=10)).timestamp())),
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
        Order(user_id=2, ordered_id=1, project="Uitleensysteem", students=""),
        Order(user_id=1, ordered_id=2, project="Vriezer", students=""),
        Order(user_id=3, ordered_id=3, project="Digital Twin", students=""),
        Order(user_id=1, ordered_id=4, project="Vriezer", students="")
        ]

        db.session.bulk_save_objects(vendors)
        db.session.bulk_save_objects(categories)
        db.session.bulk_save_objects(manufacturers)
        db.session.bulk_save_objects(products)
        db.session.bulk_save_objects(ordered)
        db.session.bulk_save_objects(borrowed)
        db.session.bulk_save_objects(order)
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
        for model in [Vendor, ProductCategory, Manufacturer, Product, Ordered, Borrowed, Order]:
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