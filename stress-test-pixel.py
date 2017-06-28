import argparse
import asyncio
import concurrent.futures
import functools
import requests
import time
from bson import ObjectId


parser = argparse.ArgumentParser(description='Stress test the pixel')
parser.add_argument('url', type=str, help='url to test')
parser.add_argument('delay', type=float, help='delay (in ms) between each request')
args = parser.parse_args()


requests_made = 0
num_threads = 50

async def make_request():
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        loop = asyncio.get_event_loop()
        object_ids = [ObjectId() for i in range(num_threads)]
        try:
            futures = [
                loop.run_in_executor(None, functools.partial(requests.get,
                '{0}?active_cart=true&idshopper=4e68f7ab2aa35f12c0000031'
                 '&session_id={1}'.format(args.url, object_ids[i]), verify=False))
                for i in range(num_threads)
            ]
            global requests_made
            for r in await asyncio.gather(*futures):
                requests_made += 1
                print('{0} -- {1}'.format(r.request.url, r.status_code))
                print('Requests made: {0}'.format(requests_made))
        except Exception as e:
            print(e)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    while True:
        loop.run_until_complete(make_request())
        time.sleep(args.delay)
