from data.models import User

def get_current_user(request):
    return User.get_user('pwh')

