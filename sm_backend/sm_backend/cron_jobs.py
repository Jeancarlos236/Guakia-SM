import os
import sys
from collections import Counter
from datetime import timedelta

import django
from django.utils import timezone

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sm_backend.settings")
django.setup()

from post.models import Post, Trend
from account.models import User

def extract_hashtags(text, trends):
    for word in text.split():
        if word[0] == '#':
            trends.append(word[1:])
    return trends

def update_trends():
    # Clear existing trends
    Trend.objects.all().delete()

    # Extract hashtags from posts within the last week
    trends = []
    this_week = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=7)

    for post in Post.objects.filter(is_private=False).filter(created_at__gte=this_week):
        extract_hashtags(post.body, trends)

    # Create trends based on extracted hashtags
    for trend in Counter(trends).most_common(10):
        Trend.objects.create(hashtag=trend[0], occurrences=trend[1])

def update_friend_suggestions():
    users = User.objects.all()
    for user in users:
        # Clear the suggestion list
        user.people_you_may_know.clear()
        if user.friends_count > 0:
            print('Finding Friends for: ', user)
        for friend in user.friends.all():
            print('Is friends with ', friend)

            for friendsfriend in friend.friends.all():
                if friendsfriend not in user.friends.all() and friendsfriend != user:
                    user.people_you_may_know.add(friendsfriend)

# Run both functions
update_trends()
update_friend_suggestions()
