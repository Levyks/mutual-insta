import os
import sys
from instagrapi import Client
from dotenv import load_dotenv

load_dotenv()

def get_mutual_followers(cl, users):
    mutual_set = {}
    for user in users:
        id = cl.user_id_from_username(user)
        followers = cl.user_followers(id)
        followers_set = set([user.username for user in followers.values()])
        print(f'{user} has {len(followers)} followers')        
        if(len(mutual_set) == 0): 
            mutual_set = followers_set
        else:
            mutual_set = mutual_set.intersection(followers_set)

    return mutual_set

def get_mutual_following(cl, users):
    mutual_set = {}
    for user in users:
        id = cl.user_id_from_username(user)
        following = cl.user_following(id)
        following_set = set([user.username for user in following.values()])
        print(f'{user} follows {len(following)} users')        
        if(len(mutual_set) == 0): 
            mutual_set = following_set
        else:
            mutual_set = mutual_set.intersection(following_set)

    return mutual_set

if 'IG_USERNAME' not in os.environ or 'IG_PASSWORD' not in os.environ:
    print('Please set your Instagram credentials in .env file')
    exit(1)

users = []
mode = 'BOTH'

for i, opt in enumerate(sys.argv):
    if opt == '--following':
        mode = 'FOLLOWING'
    elif opt == '--followers':
        mode = 'FOLLOWERS'
    elif opt == '--both':
        mode = 'BOTH'
    elif i > 0:
        users.append(opt)

if len(users) < 2:
    print('Please provide at least two users')
    exit(1)

cl = Client()

if os.path.exists('./tmp/dump.json'):
    cl.load_settings('./tmp/dump.json')

cl.login(
    os.environ['IG_USERNAME'],
    os.environ['IG_PASSWORD'],
)
cl.dump_settings('./tmp/dump.json')

print("Logged in")

if mode == 'FOLLOWERS' or mode == 'BOTH':
    mutual_followers = get_mutual_followers(cl, users)
    print('Mutual followers:')
    for follower in mutual_followers:
        print(follower)
if mode == 'FOLLOWING' or mode == 'BOTH':
    mutual_following = get_mutual_following(cl, users)
    print('Mutual following:')
    for following in mutual_following:
        print(following)





