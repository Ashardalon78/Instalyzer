from instagrapi import Client
#from instagrapi.types import Usertag, Location
from class_instagram_client import InstagramClient


username = 'ashardalon78'
#cl = InstagramClient.from_api(username, '****')
#cl.save_obj_as_pickle(cl.df_user_data, f'saved_data/{username}_instadata.pkl')

cl = InstagramClient.from_pickle(f'saved_data/{username}_instadata.pkl')
print(cl.df_user_data)
