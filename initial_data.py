# Data to be entered into the database, so we don't have to manually enter it
# every time we run sync_db

from data.models import User, Category, Item, Filter, Claim

# Add in categories
Category.create_category('GIRs')
Category.create_category('Furniture')
Category.create_category('Clothing')
Category.create_category('Rainbow-colored Santorum Posters')

