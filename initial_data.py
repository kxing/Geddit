# Data to be entered into the database, so we don't have to manually enter it
# every time we run sync_db

from data.models import User, Category, Item, Reservation, Claim, Location
import time

# Make location
baker = Location.create_location('Baker Hall', '42.35666', '-71.09582')
bexely = Location.create_location('Bexley Hall', '42.35852604285305', '-71.09368236574556')
burton_conner = Location.create_location('Burton-Conner House', '42.35607', '-71.09811')
east_campus = Location.create_location('East Campus', '42.36026', '-71.08880')
macgregor = Location.create_location('MacGregeor House', '42.35543', '-71.09981')
maseeh = Location.create_location('Maseeh Hall', '42.35764801061463', '-71.09338732275393')
mccormick = Location.create_location('McCormick Hall', '42.35731', '-71.09454')
new_house = Location.create_location('New House', '42.35543', '-71.10023')
next_house = Location.create_location('Next House', '42.354714540813504', '-71.10203476461794')
random_hall = Location.create_location('Random Hall', '42.36191', '-71.09821')
senior = Location.create_location('Senior House', '42.36007', '-71.08689')
simmons = Location.create_location('Simmons Hall', '42.35733', '-71.10105')

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
time.sleep(1.0)
kerry.add_item('Blue Jeans', 'size 30-30. New.', clothing, '30.00')
time.sleep(1.0)
kerry.add_item('3.091 Textbook', 'Simply awesome.', girs, '1000.00')
time.sleep(1.0)
kerry.add_item('Couch', 'Very comfortable.', furniture, '99.99')
time.sleep(1.0)
kerry.add_item('Santorum Poster', 'Don\' know why I have so many of these...', santorum, \
        '0.01')
time.sleep(1.0)
kerry.add_item('DropBox T-shirt', 'Everybody loves DropBox!', clothing, '20.00')

