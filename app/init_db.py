from datetime import datetime, timedelta
import os
import shutil
import subprocess

from apps import create_app, db
from apps.config import config_dict
from apps.webapp.models import Manufacturer, Product, ProductCategory, Vendor, Ordered, Borrowed

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
            Product(article_number='A001', model='Model X', quantity=10, price_when_bought=1000.0, description='Sample product description', EAN='1234567890123', url='https://example.com/products/A001', manufacturer_id=1, category_id=1, vendor_id=1),
            Product(article_number='B002', model='Model Y', quantity=5, price_when_bought=750.0, description='Another sample product description', EAN='2345678901234', url='https://example.com/products/B002', manufacturer_id=2, category_id=1, vendor_id=2),
            Product(article_number='C003', model='Model Z', quantity=20, price_when_bought=2000.0, description='Yet another sample product description', EAN='3456789012345', url='https://example.com/products/C003', manufacturer_id=3, category_id=2, vendor_id=3),
            Product(article_number='D004', model='Model A', quantity=15, price_when_bought=1500.0, description='Fourth sample product description', EAN='4567890123456', url='https://example.com/products/D004', manufacturer_id=1, category_id=2, vendor_id=1),
            Product(article_number='E005', model='Model B', quantity=7, price_when_bought=500.0, description='Fifth sample product description', EAN='5678901234567', url='https://example.com/products/E005', manufacturer_id=2, category_id=1, vendor_id=2),
            Product(article_number='F006', model='Model C', quantity=8, price_when_bought=800.0, description='Sixth sample product description', EAN='6789012345678', url='https://example.com/products/F006', manufacturer_id=3, category_id=2, vendor_id=3),
            Product(article_number='G007', model='Model D', quantity=12, price_when_bought=1200.0, description='Seventh sample product description', EAN='7890123456789', url='https://example.com/products/G007', manufacturer_id=1, category_id=1, vendor_id=1),
            Product(article_number='H008', model='Model E', quantity=4, price_when_bought=400.0, description='Eighth sample product description', EAN='8901234567890', url='https://example.com/products/H008', manufacturer_id=2, category_id=2, vendor_id=2),
            Product(article_number='I009', model='Model F', quantity=6, price_when_bought=600.0, description='Ninth sample product description', EAN='9012345678901', url='https://example.com/products/I009', manufacturer_id=3, category_id=1, vendor_id=3),
            Product(article_number='J010', model='Model G', quantity=9, price_when_bought=900.0, description='Tenth sample product description', EAN='0123456789012', url='https://example.com/products/J010', manufacturer_id=1, category_id=2, vendor_id=1),
            Product(article_number='K011', model='Model H', quantity=3, price_when_bought=300.0, description='Eleventh sample product description', EAN='1234567890123', url='https://example.com/products/K011', manufacturer_id=2, category_id=1, vendor_id=2),
            Product(article_number='L012', model='Model I', quantity=11, price_when_bought=1100.0, description='Twelfth sample product description', EAN='2345678901234', url='https://example.com/products/L012', manufacturer_id=3, category_id=2, vendor_id=3),
            Product(article_number='M013', model='Model J', quantity=13, price_when_bought=1300.0, description='Thirteenth sample product description', EAN='3456789012345', url='https://example.com/products/M013', manufacturer_id=1, category_id=1, vendor_id=1),
        ]
        
        borrowed = [
            Borrowed(product_id=1, user_id=1, quantity=2, returned=0, estimated_return_date=int((datetime.now() + timedelta(days=7)).timestamp())),
            Borrowed(product_id=2, user_id=1, quantity=1, returned=0, estimated_return_date=int((datetime.now() + timedelta(days=3)).timestamp())),
            Borrowed(product_id=3, user_id=2, quantity=3, returned=0, estimated_return_date=int((datetime.now() + timedelta(days=5)).timestamp())),
            Borrowed(product_id=4, user_id=3, quantity=1, returned=0, estimated_return_date=int((datetime.now() + timedelta(days=7)).timestamp())),
            Borrowed(product_id=5, user_id=2, quantity=2, returned=0, estimated_return_date=int((datetime.now() + timedelta(days=10)).timestamp())),
            Borrowed(product_id=1, user_id=2, quantity=1, returned=0, estimated_return_date=int((datetime.now() + timedelta(days=2)).timestamp())),
            Borrowed(product_id=3, user_id=3, quantity=1, returned=0, estimated_return_date=int((datetime.now() + timedelta(days=7)).timestamp())),
            Borrowed(product_id=2, user_id=3, quantity=2, returned=0, estimated_return_date=int((datetime.now() + timedelta(days=3)).timestamp())),
            Borrowed(product_id=4, user_id=1, quantity=1, returned=0, estimated_return_date=int((datetime.now() + timedelta(days=5)).timestamp())),
            Borrowed(product_id=5, user_id=1, quantity=2, returned=0, estimated_return_date=int((datetime.now() + timedelta(days=10)).timestamp())),
        ]
        
        ordered = [
            Ordered(product_id=2, vendor_id=3, ordered=True, delivered=False),
            Ordered(product_id=3, vendor_id=4, ordered=True, delivered=True),
            Ordered(product_id=4, vendor_id=5, ordered=True, delivered=False),
            Ordered(product_id=1, vendor_id=6, ordered=True, delivered=False),
            Ordered(product_id=2, vendor_id=7, ordered=True, delivered=False),
            Ordered(product_id=3, vendor_id=8, ordered=True, delivered=True),
            Ordered(product_id=4, vendor_id=9, ordered=True, delivered=False),
            Ordered(product_id=1, vendor_id=10, ordered=True, delivered=False),
            Ordered(product_id=2, vendor_id=3, ordered=False, delivered=False),
            Ordered(product_id=3, vendor_id=5, ordered=False, delivered=False),
        ]

        db.session.bulk_save_objects(vendors)
        db.session.bulk_save_objects(categories)
        db.session.bulk_save_objects(manufacturers)
        db.session.bulk_save_objects(products)
        db.session.bulk_save_objects(ordered)
        db.session.bulk_save_objects(borrowed)
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
        for model in [Vendor, ProductCategory, Manufacturer, Product, Ordered, Borrowed]:
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