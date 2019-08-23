import requests, json

key = 'oqRS1g5qm2egbefRbPB6Q'
secret = '6xbgAO8Cn3QZMZHDb4EPqxukqa4UGElG06ip25ZbOo'

try:
    res = requests.get("https://www.goodreads.com/book/review_counts.json",
                   params={
                       "key": key,
                       "isbns": "00000d0000"
                   })
    print(res.json())
except json.JSONDecodeError as err:
    print(err)

