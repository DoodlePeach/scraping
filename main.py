import json
import random
import time
from json import loads

from facebook_scraper import get_profile, set_cookies, exceptions
from neomodel import config
from model import Account
from config import *
from traceback import print_exc

config.DATABASE_URL = DATABASE_URL
set_cookies(COOKIE_FILE)


def scrape(identifier: int or str):
    try:
        content = get_profile(account=str(identifier), friends=True)
    except exceptions.TemporarilyBanned:
        raise exceptions.TemporarilyBanned
    except:
        content = None

    if content is None:
        raise LookupError

    if (type(identifier) is str) or (Account.nodes.first_or_none(profile_id=identifier) is None):
        scraped_account = Account.from_scraped(content).save()
    else:
        scraped_account = Account.nodes.first_or_none(profile_id=identifier)

    friends = content['Friends']

    for friend in friends:
        friend_account = Account.from_friends(friend)

        if Account.nodes.first_or_none(profile_id=friend_account.profile_id) is not None:
            continue

        friend_account.save()
        scraped_account.friends.connect(friend_account)

    return scraped_account


def generate_graph(root_name: str):
    queue = scrape(root_name).friends.all()
    current_level_item_count = len(queue)
    depth = 0

    while depth < DEPTH:
        while current_level_item_count > 0:
            friend = queue.pop(0)
            current_level_item_count -= 1

            time.sleep(random.randrange(SLEEP_INTERVAL[0], SLEEP_INTERVAL[1]))

            try:
                scraped = scrape(identifier=friend.profile_id)
            except LookupError:
                continue

            queue.extend(scraped.friends.all())

        depth += 1
        current_level_item_count = len(queue)


if __name__ == '__main__':
    try:
        generate_graph(root_name=ROOT_NAME)
    except exceptions.TemporarilyBanned:
        print_exc()
        print('EXITING due to exception.')
