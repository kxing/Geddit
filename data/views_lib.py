from data.models import Category
from site_specific_constants import SITE_ROOT
from site_specific_functions import get_current_user

def base_params(request):
    return { \
        'categories': Category.get_all_categories(), \
        'SITE_ROOT': SITE_ROOT, \
        'user': get_current_user(request), \
    }


