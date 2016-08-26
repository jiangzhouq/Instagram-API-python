#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Usage: 
python app.py <username>
"""
from app import InstagramScraper
from InstagramAPI import InstagramAPI
from mongotools import MongoTools
import tqdm
import concurrent.futures

InstagramAPI = InstagramAPI("justexplorehaha", "biu1biu2biu3")
MongoTools = MongoTools()
InstagramAPI.login() # login
result = InstagramAPI.getSelfUsersFollowing()
total = 0
while result:
    # with open('measurements.json', 'w') as f:
    #     f.write(json.dumps(InstagramAPI.LastJson, sort_keys=True, indent=4))
    for i in InstagramAPI.LastJson.get('users'):
        MongoTools.insertUser(i)
    count = len(InstagramAPI.LastJson.get('users'))
    total = total + count
    next=InstagramAPI.LastJson.get('next_max_id')
    result = InstagramAPI.getUserFollowings(InstagramAPI.username_id, next)
print(total)

for i in MongoTools.getUsers():
    print(i["username"])
    scraper = InstagramScraper(i["username"])
    scraper.crawl()

    for future in tqdm.tqdm(concurrent.futures.as_completed(scraper.future_to_item), total=len(scraper.future_to_item), desc='Downloading'):
        item = scraper.future_to_item[future]

        if future.exception() is not None:
            print('%r generated an exception: %s') % (item['id'], future.exception())