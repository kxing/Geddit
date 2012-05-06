from data.models import Location, User, Category, Item, Reservation, Claim

backup_file = open('backup', 'w')

for location in Location.objects.all():
    backup_file.write(Location.to_meta_string(location) + '\n')

for user in User.objects.all():
    backup_file.write(User.to_meta_string(user) + '\n')

for category in Category.objects.all():
    backup_file.write(Category.to_meta_string(category) + '\n')

for item in Item.objects.all():
    backup_file.write(Item.to_meta_string(item) + '\n')

for reservation in Reservation.objects.all():
    backup_file.write(Reservation.to_meta_string(reservation) + '\n')

for claim in Claim.objects.all():
    backup_file.write(Claim.to_meta_string(claim) + '\n')

backup_file.close()

