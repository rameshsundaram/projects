# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 17:22:56 2017

@author: ramsunda1
"""
import pandas as pd
local_songs_data_path="C:\\Users\\ramsunda1\\Desktop\\Work\\Training\\spotify\\"
lyrics_path="T:\MoxieDepts\Technology\Analytics\Clients\Verizon Wireless\CRM\Training\Contests\TomPettyViz\\data\\Lyrics\\"
songs_data_path="T:\MoxieDepts\Technology\Analytics\Clients\Verizon Wireless\CRM\Training\Contests\TomPettyViz\\data\\spotify\\"

track_details=pd.read_csv(songs_data_path+"spotify_track_details.csv", header=0)
track_details.columns
track_details.columns = [str(col) + '_track' for col in track_details.columns ]
track_details=track_details.rename(columns = {'album_id_track':'album_id','id_track':'track_id'})
track_details['Hit']=track_details['popularity_track'].apply(lambda x: 1 if x>39 else 0)


album_details=pd.read_csv(songs_data_path+"spotify_album_details.csv", header=0)
album_details.columns = [str(col) + '_album' for col in album_details.columns ]
album_details=album_details.rename(columns = {'id_album':'album_id'})
album_details.drop(['width_album','height_album'], axis=1, inplace=True)

artist_albums=pd.read_csv(songs_data_path+"spotify_artist_albums.csv", header=0)
artist_albums.columns = [str(col) + '_artist_album' for col in artist_albums.columns ]
artist_albums=artist_albums.rename(columns = {'id_artist_album':'album_id'})
artist_albums.drop(['album_type_artist_album','artists_artist_album','available_markets_artist_album','external_urls.spotify_artist_album','href_artist_album','images_artist_album','name_artist_album','type_artist_album','uri_artist_album'], axis=1, inplace=True)

track_features=pd.read_csv(songs_data_path+"spotify_track_features.csv", header=0)
track_features.columns = [str(col) + '_tf' for col in track_features.columns ]
track_features=track_features.rename(columns = {'id_tf':'track_id'})
track_features.drop(['duration_ms_tf','analysis_url_tf','track_href_tf','type_tf','uri_tf'], axis=1, inplace=True)

track_lyrics=pd.read_csv(lyrics_path+"Lyrics_enriched.csv", header=0)
track_lyrics.columns = [str(col) + '_lyr' for col in track_lyrics.columns ]
track_lyrics=track_lyrics.rename(columns = {'id_lyr':'track_id'})
track_lyrics.drop(['key_lyr', 'artists_lyr', 'available_markets_lyr', 'disc_number_lyr', 'duration_ms_lyr', 'explicit_lyr', 'external_urls.spotify_lyr', 'href_lyr', 'preview_url_lyr', 'track_number_lyr', 'type_lyr', 'uri_lyr', 'album_id_lyr', 'Lyric ID_lyr','name_lyr','Release_Date_lyr','Album_lyr'], axis=1, inplace=True)


ds_track_album=pd.merge(track_details, album_details, how='left', on='album_id')
ds_track_artist_album=pd.merge(ds_track_album, artist_albums, how='left', on='album_id')
ds_track_artist_album_tf=pd.merge(ds_track_artist_album, track_features, how='left', on='track_id')
ds_track_artist_album_tf.to_csv(local_songs_data_path+"Track_Features.csv", sep=',', index=False, encoding="utf-8")
ds_track_artist_album_tf_lyr=pd.merge(ds_track_artist_album_tf, track_lyrics, how='left', on='track_id')

ds_track_artist_album_tf_lyr['lyrical_density']=ds_track_artist_album_tf_lyr['word_count_lyr']*1000/ds_track_artist_album_tf_lyr['duration_ms_track']

#ds_track_artist_album_tf_lyr.to_csv(songs_data_path+"TomPettyDS.csv", sep=',', index=False, encoding="utf-8")
ds_track_artist_album_tf_lyr.to_csv(local_songs_data_path+"TomPettyDS.csv", sep=',', index=False, encoding="utf-8")