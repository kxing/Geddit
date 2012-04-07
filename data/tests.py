"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from data.models import User, Category, Item, Claim

class UserTest(TestCase):
    USERNAME = 'asdf1234'
    FIRST_NAME = 'Asdf'
    LAST_NAME = 'Qwerty'
    EMAIL = 'asdf1234@mit.edu'
    PHONE = '(123)456-7890'

    def setUp(self):
        # create a user
        self.user = User.create_user(self.USERNAME, self.FIRST_NAME, \
                self.LAST_NAME, self.EMAIL, self.PHONE)

    def tearDown(self):
        # delete the user
        User.delete_user(self.user)

    def test_user(self):
        '''
        Tests to make sure that users can be queried
        and that their attributes are correct.
        '''
        # create a user

        # find the user and check it
        u = User.get_user(self.USERNAME)
        self.assertEqual(u, self.user)
        self.assertEqual(u.username, self.USERNAME)
        self.assertEqual(u.first_name, self.FIRST_NAME)
        self.assertEqual(u.last_name, self.LAST_NAME)
        self.assertEqual(u.email, self.EMAIL)
        self.assertEqual(u.cell_phone, self.PHONE)

class CategoryTest(TestCase):
    CATEGORY_NAME = '3.091'
    CATEGORY2_NAME = '1.00'

    def setUp(self):
        # create a category
        self.category = Category.create_category(self.CATEGORY_NAME)
        self.category2 = Category.create_category(self.CATEGORY2_NAME)

    def tearDown(self):
        # delete the category
        Category.delete_category(self.category)
        Category.delete_category(self.category2)

    def test_categories(self):
        '''
        Tests to make sure that categories can be queried
        and that the attributes are correct.
        '''
        # find the category and check it
        c = Category.get_category(self.CATEGORY_NAME)
        self.assertEqual(c, self.category)
        self.assertEqual(c.name, self.CATEGORY_NAME)

        # repeat for category 2
        c2 = Category.get_category(self.CATEGORY2_NAME)
        self.assertEqual(c2, self.category2)
        self.assertEqual(c2.name, self.CATEGORY2_NAME)

        # test to make sure that the list of all categories is sorted
        all_categories = Category.get_all_categories()
        self.assertEqual(all_categories[0], self.category2)
        self.assertEqual(all_categories[1], self.category) 

class ItemTest(TestCase):
    USERNAME = 'asdf1234'
    FIRST_NAME = 'Asdf'
    LAST_NAME = 'Qwerty'
    EMAIL = 'asdf1234@mit.edu'
    PHONE = '(123)456-7890'

    TEXTBOOK_CATEGORY = '3.091'
    VIDEOS_CATEGORY = '5.111'

    TEXTBOOK_NAME = '3.091 Textbook'
    TEXTBOOK_DESCRIPTION = 'The textbook for the legendary class ... 3.091!'
    TEXTBOOK_PRICE = '30.00'
    VIDEOS_NAME = '5.111 Video Lecture Series'
    VIDEOS_DESCRIPTION = 'Watch 5-fun-fun-fun!'
    VIDEOS_PRICE = '100.00'

    def setUp(self):
        # create the user
        self.user = User.create_user(self.USERNAME, self.FIRST_NAME, \
                self.LAST_NAME, self.EMAIL, self.PHONE)

        # create the categories
        self.category1 = Category.create_category(self.TEXTBOOK_CATEGORY)
        self.category2 = Category.create_category(self.VIDEOS_CATEGORY)

        # create the items
        self.item1 = Item.create_item(self.user, self.TEXTBOOK_NAME, \
                self.TEXTBOOK_DESCRIPTION, self.category1, self.TEXTBOOK_PRICE)
        self.item2 = self.user.add_item(self.TEXTBOOK_NAME, \
                self.TEXTBOOK_DESCRIPTION, self.category1, self.TEXTBOOK_PRICE)
        self.item3 = self.user.add_item(self.VIDEOS_NAME, \
                self.VIDEOS_DESCRIPTION, self.category2, self.VIDEOS_PRICE)

    def tearDown(self):
        # delete the items
        Item.delete_item(self.item1)
        Item.delete_item(self.item2)
        Item.delete_item(self.item3)

        # delete the categories
        Category.delete_category(self.category1)
        Category.delete_category(self.category2)

        # delete the user
        User.delete_user(self.user)

    def test_items(self):
        # check to make sure that both ways of getting items work
        for items in [Item.get_items(self.user), self.user.get_items(), Item.get_all_items()]:
            # check the item count
            self.assertEqual(len(items), 3)

            self.assertTrue(self.item1 in items)
            self.assertTrue(self.item2 in items)
            self.assertTrue(self.item3 in items)
        self.assertEqual(Item.get_item_by_id(self.item1.id), self.item1)
        self.assertEqual(Item.get_item_by_id(self.item2.id), self.item2)
        self.assertEqual(Item.get_item_by_id(self.item3.id), self.item3)

class ClaimTest(TestCase):
    BUYER_USERNAME = 'qwerty'
    BUYER_FIRST_NAME = 'Q'
    BUYER_LAST_NAME = 'W'
    BUYER_EMAIL = 'qwerty@mit.edu'
    BUYER_CELL_PHONE = '(123)456-7890'

    SELLER_USERNAME = 'asdf'
    SELLER_FIRST_NAME = 'A'
    SELLER_LAST_NAME = 'S'
    SELLER_EMAIL = 'asdf@mit.edu'
    SELLER_CELL_PHONE = '(987)654-3210'

    CATEGORY_1 = '3.091'
    CATEGORY_2 = '5.111'

    ITEM_1_NAME = '3.091 Textbook'
    ITEM_1_DESCRIPTION = 'Textbook for Professor Sadoway\'s awesome class!'
    ITEM_1_PRICE = '30.00'

    ITEM_2_NAME = '5.111 Video Lectures'
    ITEM_2_DESCRIPTION = 'Professor Klibinov is hilarious!'
    ITEM_2_PRICE = '100.00'

    def setUp(self):
        # create the users
        self.buyer = User.create_user(self.BUYER_USERNAME, \
                self.BUYER_FIRST_NAME, self.BUYER_LAST_NAME, \
                self.BUYER_EMAIL, self.BUYER_CELL_PHONE)
        self.seller = User.create_user(self.SELLER_USERNAME, \
                self.SELLER_FIRST_NAME, self.SELLER_LAST_NAME, \
                self.SELLER_EMAIL, self.SELLER_CELL_PHONE)
        # create the categories
        self.category1 = Category.create_category(self.CATEGORY_1)
        self.category2 = Category.create_category(self.CATEGORY_2)
        # create the items
        self.item1 = Item.create_item(self.seller, self.ITEM_1_NAME, \
                self.ITEM_1_DESCRIPTION, self.category1, self.ITEM_1_PRICE)
        self.item2 = Item.create_item(self.seller, self.ITEM_2_NAME, \
                self.ITEM_2_DESCRIPTION, self.category2, self.ITEM_2_PRICE)
        # create the claims
        self.claim1 = Claim.create_claim(self.buyer, self.item1)
        self.claim2 = self.buyer.add_claim(self.item2)

    def tearDown(self):
        # delete the claims
        Claim.delete_claim(self.claim1)
        Claim.delete_claim(self.claim2)
        # delete the items
        Item.delete_item(self.item1)
        Item.delete_item(self.item2)
        # delete the categories
        Category.delete_category(self.category1)
        Category.delete_category(self.category2)
        # delete the users
        User.delete_user(self.buyer)
        User.delete_user(self.seller)

    def test_claims(self):
        for claims in [Claim.get_claims(self.buyer), self.buyer.get_claims()]:
            self.assertTrue(self.claim1 in claims)
            self.assertTrue(self.claim2 in claims)
