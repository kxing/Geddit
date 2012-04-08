# Data to be entered into the database, so we don't have to manually enter it
# every time we run sync_db

from data.models import User, Category, Item, Filter, Claim, Location
import time

# Make location
maseeh = Location.create_location('Maseeh Hall', '24.5325235', '95.9283942834')
next_house = Location.create_location('Next House', '12.4234234', '012.1241241')
bexely = Location.create_location('Bexely', '94.124124124', '124.93845345')
print maseeh
# Add in categories
girs = Category.create_category('GIRs')
furniture = Category.create_category('Furniture')
clothing = Category.create_category('Clothing')
santorum = Category.create_category('Rainbow-colored Santorum Posters')

kerry = User.create_user('kxing', 'Kerry', 'Xing', 'kxing@mit.edu', '(123)456-7890', next_house)
paul = User.create_user('pwh', 'Paul', 'Hemberger', 'pwh@mit.edu', '(234)567-8901', maseeh)
sean = User.create_user('scockey', 'Sean', 'Cockey', 'scockey@mit.edu', '(345)678-9012', maseeh)
sarine = User.create_user('sarine', 'Sarine', 'Shahmirian', 'sarine@mit.edu', '(456)789-0123', bexely)

kerry.add_item('5.111 Textbook', 'In great condition.', girs, '30.99')
time.sleep(1.0)
kerry.add_item('Wooden Chair', 'Slightly worn.', furniture, '24.97')
time.sleep(1.0)
kerry.add_item('Santorum Poster', 'Really want to get rid of this...', santorum, '0.01')

