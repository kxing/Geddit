# Data to be entered into the database, so we don't have to manually enter it
# every time we run sync_db

from data.models import User, Category, Item, Filter, Claim

# Add in categories
girs = Category.create_category('GIRs')
furniture = Category.create_category('Furniture')
clothing = Category.create_category('Clothing')
santorum = Category.create_category('Rainbow-colored Santorum Posters')

kerry = User.create_user('kxing', 'Kerry', 'Xing', 'kxing@mit.edu', '(123)456-7890')
paul = User.create_user('pwh', 'Paul', 'Hemberger', 'pwh@mit.edu', '(234)567-8901')
sean = User.create_user('scockey', 'Sean', 'Cockey', 'scockey@mit.edu', '(345)678-9012')
sarine = User.create_user('sarine', 'Sarine', 'Shahmirian', 'sarine@mit.edu', '(456)789-0123')

kerry.add_item('5.111 Textbook', 'In great condition.', girs)
kerry.add_item('Wooden Chair', 'Slightly worn.', furniture)
kerry.add_item('Santorum Poster', 'Really want to get rid of this...', santorum)

