from instagrapi import Client
import pickle
import pandas as pd
import time
import random

class InstagramClient():
    def __init__(self, datadict):

        self.datadict = datadict

    @classmethod
    def from_api(cls, username, password):
        client = Client()
        client.login(username, password)
        user_info = client.user_info_by_username(username)
        user_id = user_info.pk
        medias = client.user_medias(user_id)[::-1]

        df_user_data = cls.get_user_data(medias)
        comments_all_media = cls.get_comments(medias, client, username, password)
        client.logout()

        datadict = {'userdata': df_user_data, 'comments': comments_all_media}

        return cls(datadict)

    @classmethod
    def from_pickle(cls, filename):
        with open(filename, 'rb') as filein:
            df = pickle.load(filein)

        #return cls(df)

    @classmethod
    def get_user_data(cls, medias):
        df_user_data = pd.DataFrame()
        df_user_data['Datetime'] = [media.taken_at for media in medias]  # [::-1]
        df_user_data['Type'] = [media.media_type for media in medias]  # [::-1]
        df_user_data['Views'] = [media.view_count for media in medias]  # [::-1]
        df_user_data['Likes'] = [media.like_count for media in medias]  # [::-1]
        df_user_data['Comments'] = [media.comment_count for media in medias]  # [::-1]

        return df_user_data


    @classmethod
    def get_comments(cls, medias, client, username, password):
        comments_all_media = []
        for media in medias:
            print(media.comment_count)
            if media.comment_count:
                try:
                    comments_all_media.append(client.media_comments(media.id))
                except:
                    print('Try Login')
                    time.sleep(random.randint(1, 5))
                    client = Client()
                    client.login(username, password)
                    comments_all_media.append(client.media_comments(media.id))

            else:
                comments_all_media.append([])

        return comments_all_media

    def save_obj_as_pickle(self, obj, filename):
        with open(filename, 'wb') as fileout:
            pickle.dump(obj, fileout)
