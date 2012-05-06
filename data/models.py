from django.db import models
import smtplib
from email.mime.text import MIMEText
from googlevoice import Voice
from datetime import datetime
from site_specific_constants import SITE_ROOT, GEDDIT_GMAIL, GEDDIT_PASSWORD
import json

USERNAME_MAX_LENGTH = 25
PERSON_NAME_MAX_LENGTH = 25
PHONE_NUMBER_MAX_LENGTH = 20

LOCATION_NAME_MAX_LENGTH=100
class Location(models.Model):
    # The id field is automatically generated by Django
    # id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=LOCATION_NAME_MAX_LENGTH)
    longitude = models.DecimalField(verbose_name="Longitude",
                                    max_digits=20,
                                    decimal_places=17)
    latitude = models.DecimalField(verbose_name="Latitude",
                                   max_digits=20,
                                   decimal_places=17)
    
    @staticmethod
    def to_meta_string(location):
        data = {'class_name': 'Location'}

        data['id'] = location.id
        data['name'] = location.name
        data['longitude'] = str(location.longitude)
        data['latitude'] = str(location.latitude)

        return json.dumps(data)

    @staticmethod
    def from_meta_string(meta_string):
        data = json.loads(meta_string)
        return Location( \
            id=data['id'], \
            name=data['name'], \
            longitude=data['longitude'], \
            latitude=data['latitude'], \
        )

    def __unicode__(self):
        return unicode(self.name)
    
    class Meta:
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'
    
    @staticmethod
    def create_location(locationName, lat, lng):
        l = Location(name=locationName,
                     longitude=lng,
                     latitude=lat)
        l.save()
        return l
    
    @staticmethod
    def get_location(name):
        return Location.objects.get(name=name)
    
class User(models.Model):
    # The id field is automatically generated by Django
    # id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=USERNAME_MAX_LENGTH, unique=True)
    first_name = models.CharField(max_length=PERSON_NAME_MAX_LENGTH)
    last_name = models.CharField(max_length=PERSON_NAME_MAX_LENGTH)
    email = models.EmailField()
    cell_phone = models.CharField(max_length=PHONE_NUMBER_MAX_LENGTH, blank=True, null=True)
    location = models.ForeignKey(Location, blank=True, null=True)

    @staticmethod
    def to_meta_string(user):
        data = {'class_name': 'User'}

        data['id'] = user.id
        data['username'] = user.username
        data['first_name'] = user.first_name
        data['last_name'] = user.last_name
        data['email'] = user.email
        if hasattr(user, 'cell_phone'):
            data['cell_phone'] = user.cell_phone
        if hasattr(user, 'location'):
            data['location'] = user.location.id

        return json.dumps(data)

    @staticmethod
    def from_meta_string(meta_string):
        data = json.loads(meta_string)

        return User( \
            id=data['id'], \
            username=data['username'], \
            first_name=data['first_name'], \
            last_name=data['last_name'], \
            email=data['email'], \
            cell_phone=data.get('cell_phone', None), \
            location=Location.get(id=data['location']) if 'location' in data else None, \
        )

    def __unicode__(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    @staticmethod
    def create_user(username, first_name, last_name, email, cell_phone=None, location=None):
        u = User(username=username, first_name=first_name, \
                last_name=last_name, email=email, cell_phone=cell_phone,
                location=location)
        u.save()
        return u

    @staticmethod
    def get_user(username):
        return User.objects.get(username=username)

    @staticmethod
    def delete_user(user):
        user.delete()
    
    def send_email(self, message, subject):
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = GEDDIT_GMAIL
        msg['To'] = self.email

        s = smtplib.SMTP('localhost')
        s.sendmail(GEDDIT_GMAIL, [self.email], msg.as_string())
        s.quit()

    def send_sms(self, message):
        voice = Voice()
        voice.login(GEDDIT_GMAIL, GEDDIT_PASSWORD)
        voice.send_sms(self.cell_phone, message)

    def add_item(self, name, description, category, price, image=None):
        item = Item.create_item(self, name, description, category, price, image=image)

        # find reservations that match the item
        reservations = Reservation.get_matching_reservations(item)

        # figure out the users to be emailed and SMS-ed
        users = {}
        for reservation in reservations:
            if reservation.user.id in users:
                continue
            users[reservation.user.id] = reservation.user
        # email and SMS
        for uid in users:
            users[uid].send_email('An item has been posted that matches your reservation.\n' + \
                    'Check it out at ' + SITE_ROOT + 'buy?id=' + str(item.id), \
                    '[Geddit] matching reservation')

        return item

    def get_items(self):
        return Item.get_items(self)

    def remove_item(self, item):
        if item.seller_user != self:
            # error, you can't delete someone else's item
            return
        Item.delete_item(item)

    def add_claim(self, item):
        return Claim.create_claim(self, item)

    def remove_claim(self, item):
        claim = Claim.get_claim(item)
        if claim.buyer != self:
            raise AssertionError('Claim does not belong to you')
        Claim.delete_claim(claim)

    def get_claims(self):
        return Claim.get_claims(self)

    def add_reservation(self, search_query, max_price):
        return Reservation.create_reservation(self, search_query, max_price)

    def get_reservations(self):
        return Reservation.get_reservations(self)

    def remove_reservation(self, reservation):
        Reservation.delete_reservation(reservation)

CATEGORY_NAME_MAX_LENGTH = 100

class Category(models.Model):
    # Django will automatically generate this:
    # id = models.IntegerField()
    name = models.CharField(max_length=CATEGORY_NAME_MAX_LENGTH)

    @staticmethod
    def to_meta_string(category):
        data = {'class_name': 'Category'}

        data['id'] = category.id
        data['name'] = category.name

        return json.dumps(data)

    @staticmethod
    def from_meta_string(meta_string):
        data = json.loads(meta_string)

        return Category( \
            id=data['id'], \
            name=data['name'], \
        )

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    @staticmethod
    def create_category(name):
        c = Category(name=name)
        c.save()
        return c

    @staticmethod
    def get_category(name):
        return Category.objects.get(name=name)

    @staticmethod
    def delete_category(category):
        category.delete()

    @staticmethod
    def get_all_categories():
        return Category.objects.all().order_by('name')

ITEM_NAME_MAX_LENGTH = 100
DESCRIPTION_NAME_MAX_LENGTH = 1000

class Item(models.Model):
    # Django will automatically generate this:
    # id = models.IntegerField()
    seller_user = models.ForeignKey(User)
    name = models.CharField(max_length=ITEM_NAME_MAX_LENGTH)
    description = models.CharField(max_length=DESCRIPTION_NAME_MAX_LENGTH)
    claimed = models.BooleanField()
    category = models.ForeignKey(Category)
    upload_time = models.DateTimeField(default=datetime.utcnow)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to="images/%Y/%m/%d/", blank=True, null=True)

    @staticmethod
    def to_meta_string(item):
        data = {'class_name': 'Item'}

        data['id'] = item.id
        data['seller_user'] = item.seller_user.id
        data['name'] = item.name
        data['description'] = item.description
        data['claimed'] = item.claimed
        data['category'] = item.category.id
        data['upload_time'] = str(item.upload_time)
        data['price'] = str(item.price)
        if hasattr(item, 'image') and item.image:
            data['image_path'] = item.image.path
            data['image_url'] = item.image.url

        return json.dumps(data)

    @staticmethod
    def from_meta_string(meta_string):
        data = json.loads(meta_string)

        item = Item( \
            id=data['id'], \
            seller_user=User.get(id=data['seller_user']), \
            name=data['name'], \
            description=data['description'], \
            claimed=data['claimed'], \
            category=Category.get(id=data['claimed']) if 'claimed' in data else None, \
            upload_time=data['upload_time'], \
            price=data['price'], \
        )
        if hasattr(data, 'image_path') and hasattr(data, 'image_url'):
            f = open(data['image_path'])
            item.image.save(data['image_url'], f)
            f.close()

        return item

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'

    @staticmethod
    def create_item(seller_user, name, description, category, price, image=None):
        i = Item(seller_user=seller_user, name=name, description=description, \
                claimed=False, category=category, price=price, image=image)
        i.save()
        return i

    @staticmethod
    def get_item_by_id(id):
        return Item.objects.get(id=id)

    @staticmethod
    def get_items(seller_user):
        return Item.objects.filter(seller_user=seller_user)

    # deprecated
    @staticmethod
    def get_all_items():
        return Item.objects.all().filter(claimed=False).order_by('-upload_time')

    @staticmethod
    def get_filtered_items(category=None, search_query=None, id=None):
        items = Item.objects.all().filter(claimed=False)
        if category is not None:
            items = items.filter(category=category)
        if search_query is not None:
            for keyword in search_query.split():
                items = items.filter(name__icontains=keyword)
        if id is not None:
            items = items.filter(id=id)
        return items.order_by('-upload_time')

    @staticmethod
    def delete_item(item):
        if item.claimed:
            Claim.delete_claim(Claim.get_claim(item))
        item.delete()

    @staticmethod
    def get_item_location(item):
        pass
    
class Reservation(models.Model):
    # Django will automatically generate this:
    # id = models.IntegerField()
    user = models.ForeignKey(User)
    search_query = models.CharField(max_length=DESCRIPTION_NAME_MAX_LENGTH)
    max_price = models.DecimalField(max_digits=8, decimal_places=2)
    timestamp = models.DateTimeField(default=datetime.utcnow)

    @staticmethod
    def to_meta_string(reservation):
        data = {'class_name': 'Reservation'}

        data['id'] = reservation.id
        data['user'] = reservation.user.id
        data['search_query'] = reservation.search_query
        data['max_price'] = str(reservation.max_price)
        data['timestamp'] = str(reservation.timestamp)

        return json.dumps(data)

    @staticmethod
    def from_meta_string(meta_string):
        data = json.loads(meta_string)

        return Reservation( \
            id=data['id'], \
            user=User.get(id=data['user']), \
            search_query=data['search_query'], \
            max_price=data['max_price'], \
            timestamp=data['timestamp'], \
        )

    def __unicode__(self):
        return self.search_query

    class Meta:
        verbose_name = 'Reservation'
        verbose_name_plural = 'Reservations'

    @staticmethod
    def create_reservation(user, search_query, max_price):
        r = Reservation(user=user, search_query=search_query, max_price=max_price)
        r.save()
        return r

    @staticmethod
    def get_all_reservations():
        return Reservation.objects.all().order_by('-timestamp')

    @staticmethod
    def get_reservations(user):
        return Reservation.objects.filter(user=user).order_by('-timestamp')

    @staticmethod
    def get_reservation_by_id(id):
        return Reservation.objects.get(id=id)

    @staticmethod
    def get_matching_reservations(item):
        ''' returns the reservations that match the item '''
        matches = {}

        for keyword in item.name.split():
            reservations = Reservation.objects.filter( \
                    search_query__icontains=keyword, \
                    max_price__gte=item.price)
            for reservation in reservations:
                if reservation.id in matches:
                    continue
                matches[reservation.id] = reservation
        return matches.values()

    @staticmethod
    def delete_reservation(reservation):
        reservation.delete()

class Claim(models.Model):
    # Django will automatically generate this:
    # id = models.IntegerField()
    buyer = models.ForeignKey(User, related_name='buyer')
    item = models.ForeignKey(Item)
    timestamp = models.DateTimeField(default=datetime.utcnow)

    @staticmethod
    def to_meta_string(claim):
        data = {'class_name': 'Claim'}

        data['id'] = claim.id
        data['buyer'] = claim.buyer.id
        data['item'] = claim.item.id
        data['timestamp'] = str(claim.timestamp)

        return json.dumps(data)

    @staticmethod
    def from_meta_string(meta_string):
        data = json.loads(meta_string)

        return Claim( \
            id=data['id'], \
            buyer=User.get(id=data['buyer']), \
            item=Item.get(id=data['item']), \
            timestamp=data['timestamp'], \
        )

    def __unicode__(self):
        return str(self.buyer) + ' ' + str(self.item)

    class Meta:
        verbose_name = 'Claim'
        verbose_name_plural = 'Claims'

    @staticmethod
    def create_claim(buyer, item):
        if item.claimed:
            raise AssertionError('Item already claimed')
        c = Claim(buyer=buyer, item=item)
        c.save()
        item.claimed = True
        item.save()
        return c

    @staticmethod
    def get_claims(buyer):
        return Claim.objects.filter(buyer=buyer).order_by('-timestamp')

    @staticmethod
    def get_claim(item):
        return Claim.objects.get(item=item)

    @staticmethod
    def delete_claim(claim):
        claim.item.claimed = False
        claim.item.save()
        claim.delete()
        

