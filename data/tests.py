"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from data.models import User, Category, Item, Claim, Location, Reservation

class UserTest(TestCase):
    USERNAME = 'asdf1234'
    FIRST_NAME = 'Asdf'
    LAST_NAME = 'Qwerty'
    EMAIL = 'asdf1234@mit.edu'
    PHONE = '(123)456-7890'
    LOCATION = Location.create_location('qwerty', '92.123', '321.29')

    def setUp(self):
        # create a user
        self.user = User.create_user(self.USERNAME, self.FIRST_NAME, \
                self.LAST_NAME, self.EMAIL, self.PHONE, self.LOCATION)

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
    LOCATION = Location.create_location('asdffdasa', '12.345', '54.321')

    TEXTBOOK_CATEGORY = '3.091'
    VIDEOS_CATEGORY = '5.111'
    GIRS_CATEGORY = 'GIRs'

    TEXTBOOK_NAME = '3.091 Textbook'
    TEXTBOOK_DESCRIPTION = 'The textbook for the legendary class ... 3.091!'
    TEXTBOOK_PRICE = '30.00'
    VIDEOS_NAME = '5.111 Video Lecture Series' 
    VIDEOS_DESCRIPTION = 'Watch 5-fun-fun-fun!'
    VIDEOS_PRICE = '100.00'
    CHEAT_SHEET_NAME = '3.091, 5.111, 5.112 Cheat Sheets'
    CHEAT_SHEET_DESCRIPTION = 'Cheat Sheets for all your GIRs'
    CHEAT_SHEET_PRICE = '20.00'

    def setUp(self):
        # create the user
        self.user = User.create_user(self.USERNAME, self.FIRST_NAME, \
                self.LAST_NAME, self.EMAIL, self.PHONE, self.LOCATION)

        # create the categories
        self.textbooks = Category.create_category(self.TEXTBOOK_CATEGORY)
        self.videos = Category.create_category(self.VIDEOS_CATEGORY)
        self.girs = Category.create_category(self.GIRS_CATEGORY)

        # create the items
        self.textbook_3091_1 = Item.create_item(self.user, self.TEXTBOOK_NAME, \
                self.TEXTBOOK_DESCRIPTION, self.textbooks, self.TEXTBOOK_PRICE)
        self.textbook_3091_2 = self.user.add_item(self.TEXTBOOK_NAME, \
                self.TEXTBOOK_DESCRIPTION, self.textbooks, self.TEXTBOOK_PRICE)
        self.video_5111 = self.user.add_item(self.VIDEOS_NAME, \
                self.VIDEOS_DESCRIPTION, self.videos, self.VIDEOS_PRICE)
        self.cheat_sheets = self.user.add_item(self.CHEAT_SHEET_NAME, \
                self.CHEAT_SHEET_DESCRIPTION, self.girs, self.CHEAT_SHEET_PRICE)

    def tearDown(self):
        # delete the items
        Item.delete_item(self.textbook_3091_1)
        Item.delete_item(self.textbook_3091_2)
        Item.delete_item(self.video_5111)
        Item.delete_item(self.cheat_sheets)

        # delete the categories
        Category.delete_category(self.textbooks)
        Category.delete_category(self.videos)
        Category.delete_category(self.girs)

        # delete the user
        User.delete_user(self.user)

    def test_items(self):
        # check to make sure that both ways of getting items work
        for items in [Item.get_items(self.user), self.user.get_items(), Item.get_all_items()]:
            # check the item count
            self.assertEqual(len(items), 4)

            self.assertIn(self.textbook_3091_1, items)
            self.assertIn(self.textbook_3091_2, items)
            self.assertIn(self.video_5111, items)
            self.assertIn(self.cheat_sheets, items)

    def test_get_item_by_id(self):
        self.assertEqual(Item.get_item_by_id(self.textbook_3091_1.id), self.textbook_3091_1)
        self.assertEqual(Item.get_item_by_id(self.textbook_3091_2.id), self.textbook_3091_2)
        self.assertEqual(Item.get_item_by_id(self.video_5111.id), self.video_5111)
        self.assertEqual(Item.get_item_by_id(self.cheat_sheets.id), self.cheat_sheets)

    def test_filter_by_category(self):
        items1 = Item.get_filtered_items(category=self.textbooks)
        self.assertIn(self.textbook_3091_1, items1)
        self.assertIn(self.textbook_3091_2, items1)

        items2 = Item.get_filtered_items(category=self.videos)
        self.assertIn(self.video_5111, items2)

        items3 = Item.get_filtered_items(category=self.girs)
        self.assertIn(self.cheat_sheets, items3)

    def test_filter_by_search(self):
        textbooks = Item.get_filtered_items(search_query='Textbook')
        self.assertIn(self.textbook_3091_1, textbooks)
        self.assertIn(self.textbook_3091_2, textbooks)

        videos = Item.get_filtered_items(search_query='Video')
        self.assertIn(self.video_5111, videos)

        solid_state = Item.get_filtered_items(search_query='3.091')
        self.assertIn(self.textbook_3091_1, solid_state)
        self.assertIn(self.textbook_3091_2, solid_state)
        self.assertIn(self.cheat_sheets, solid_state)

        principles = Item.get_filtered_items(search_query='5.111')
        self.assertIn(self.video_5111, principles)
        self.assertIn(self.cheat_sheets, principles)

class ClaimTest(TestCase):
    BUYER_USERNAME = 'qwerty'
    BUYER_FIRST_NAME = 'Q'
    BUYER_LAST_NAME = 'W'
    BUYER_EMAIL = 'qwerty@mit.edu'
    BUYER_CELL_PHONE = '(123)456-7890'
    BUYER_LOCATION = Location.create_location('asdf', '92.123', '92.321')

    SELLER_USERNAME = 'asdf'
    SELLER_FIRST_NAME = 'A'
    SELLER_LAST_NAME = 'S'
    SELLER_EMAIL = 'asdf@mit.edu'
    SELLER_CELL_PHONE = '(987)654-3210'
    SELLER_LOCATION = Location.create_location('asdf', '55.555', '55.555')

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
                self.BUYER_EMAIL, self.BUYER_CELL_PHONE,
                self.BUYER_LOCATION)
        self.seller = User.create_user(self.SELLER_USERNAME, \
                self.SELLER_FIRST_NAME, self.SELLER_LAST_NAME, \
                self.SELLER_EMAIL, self.SELLER_CELL_PHONE,
                self.SELLER_LOCATION)
        # create the categories
        self.category1 = Category.create_category(self.CATEGORY_1)
        self.category2 = Category.create_category(self.CATEGORY_2)
        # create the items
        self.item1 = Item.create_item(self.seller, self.ITEM_1_NAME, \
                self.ITEM_1_DESCRIPTION, self.category1, self.ITEM_1_PRICE)
        self.item2 = Item.create_item(self.seller, self.ITEM_2_NAME, \
                self.ITEM_2_DESCRIPTION, self.category2, self.ITEM_2_PRICE)

    def tearDown(self):
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
        # check that the items are not claimed
        self.assertFalse(self.item1.claimed)
        self.assertFalse(self.item2.claimed)

        # create the claims
        self.claim1 = Claim.create_claim(self.buyer, self.item1)
        self.claim2 = self.buyer.add_claim(self.item2)

        # check that the items are claimed
        self.assertTrue(self.item1.claimed)
        self.assertTrue(self.item2.claimed)

        for claims in [Claim.get_claims(self.buyer), self.buyer.get_claims()]:
            self.assertIn(self.claim1, claims)
            self.assertIn(self.claim2, claims)
        self.assertEqual(Claim.get_claim(self.buyer, self.item1), self.claim1)

        # delete the second claim and verify that the item is not claimed
        self.buyer.remove_claim(self.item2)
        # refresh self.item2
        self.item2 = Item.get_item_by_id(self.item2.id)
        self.assertFalse(self.item2.claimed)

        # add the claim back
        self.claim2 = self.buyer.add_claim(self.item2)
        self.assertTrue(self.item2.claimed)

        # delete the claims
        Claim.delete_claim(self.claim1)
        Claim.delete_claim(self.claim2)

class ReservationTest(TestCase):
    USERNAME = 'asdf1234'
    FIRST_NAME = 'Asdf'
    LAST_NAME = 'Qwerty'
    EMAIL = 'asdf1234@mit.edu'
    PHONE = '(123)456-7890'
    LOCATION = Location.create_location('asdffdasa', '12.345', '54.321')

    SEARCH_QUERY1 = '8.01'
    SEARCH_QUERY2 = '3.091'
    MAX_PRICE = '69.99'

    GIRS_CATEGORY = 'GIRs'

    PHYSICS_NAME = '8.01 Textbook'
    PHYSICS_DESCRIPTION = 'in great condition'
    PHYSICS_PRICE_1 = '56.78'
    PHYSICS_PRICE_2 = '89.99'

    VIDEO_NAME = 'video'
    VIDEO_DESCRIPTION = 'video'
    VIDEO_PRICE = '12.00'

    def setUp(self):
        self.category = Category.create_category(self.GIRS_CATEGORY)
        self.user = User.create_user(self.USERNAME, self.FIRST_NAME, self.LAST_NAME, \
                self.EMAIL, self.PHONE, self.LOCATION)
        self.item1 = Item.create_item(self.user, self.PHYSICS_NAME, \
                self.PHYSICS_DESCRIPTION, self.category, self.PHYSICS_PRICE_1)
        self.item2 = Item.create_item(self.user, self.PHYSICS_NAME, \
                self.PHYSICS_DESCRIPTION, self.category, self.PHYSICS_PRICE_2)
        self.item3 = Item.create_item(self.user, self.VIDEO_NAME, \
                self.VIDEO_DESCRIPTION, self.category, self.VIDEO_PRICE)
        self.reservation1 = Reservation.create_reservation(self.user, \
                self.SEARCH_QUERY1, self.MAX_PRICE)
        self.reservation2 = self.user.add_reservation(self.SEARCH_QUERY2, self.MAX_PRICE)

    def tearDown(self):
        Reservation.delete_reservation(self.reservation1)
        self.user.remove_reservation(self.reservation2)

        Item.delete_item(self.item1)
        Item.delete_item(self.item2)
        Item.delete_item(self.item3)

        User.delete_user(self.user)
        Category.delete_category(self.category)

    def test_reservations(self):
        for r in Reservation.get_reservations(self.user):
            self.assertIn(r, [self.reservation1, self.reservation2])
        for r in self.user.get_reservations():
            self.assertIn(r, [self.reservation1, self.reservation2])
        self.assertEqual(Reservation.get_reservation_by_id(self.reservation1.id), \
                self.reservation1)
        self.assertEqual(Reservation.get_reservation_by_id(self.reservation2.id), \
                self.reservation2)

    def test_matching_reservations(self):
        # we expect to match the 8.01 reservation
        physics1 = Reservation.get_matching_reservations(self.item1)
        self.assertEqual(len(physics1), 1)
        self.assertIn(self.reservation1, physics1)

        # we expect to match nothing, since the price is too high
        physics2 = Reservation.get_matching_reservations(self.item2)
        self.assertEqual(len(physics2), 0)

        # we don't expect to match anything
        video = Reservation.get_matching_reservations(self.item3)
        self.assertEqual(len(video), 0)
