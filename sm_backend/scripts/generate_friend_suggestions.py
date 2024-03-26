import os
import sys
from collections import Counter
from datetime import timedelta

import django
from django.utils import timezone

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sm_backend.settings")
django.setup()


from account.models import User

users=User.objects.all()


for user in users:
    # *Clear the suggestion list
    user.people_you_may_know.clear()
    if user.friends_count>0:
        print('Find Friends for: ',user)
    for friend in user.friends.all():
        print('Is friends with ', friend)

        for friendsfriend in friend.friends.all():
            if friendsfriend not in user.friends.all() and friendsfriend!=user:
                user.people_you_may_know.add(friendsfriend)
                
