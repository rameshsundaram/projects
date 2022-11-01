# -*- coding: utf-8 -*-

import pandas as pd
import json
from pandas.io.json import json_normalize
import urllib
file_path="C:\\Users\\ramsunda1\\Desktop\\Work\\Training\\spotify\\"
#share_file_path="T:\\MoxieDepts\\Technology\\Analytics\\Clients\\Verizon Wireless\\CRM\\Training\\Contests\\TomPettyViz\\data\\spotify\\"

OATH_TOKEN = 'BQB6Rgmci0_OvzGgo9JrM8zpksHd-gAhi6UE8iK9sWse5YuGOh9hNeTvGHeBrbA6xwciqgpnEg4f9sdr_8z5_WF7x5nwM_8ngYG0ybkxWVO00f1VMUIIJA-480okr8fX0vQbq7L1-w'
#track_id="1zHlj4dQ8ZAtrayhuDDmkY"
#TRACK_IDS = ['1zHlj4dQ8ZAtrayhuDDmkY']

#artist_id="2UZMlIwnkgAEDBsw1Rejkn"
artist_ids=['2UZMlIwnkgAEDBsw1Rejkn','4tX2TplrkIP4v05BNC903e','2hO4YtXUFJiUYS2uYFvHNK','2xLqrYZxa9GYSCVn0STgxV']

base_api = 'https://api.spotify.com/v1/'

album_exclusions=['5OlEEw6gIk32eMhOqRlfGu','29RVdfPWTEu6atVycxx86s','78OPbUR8fG0poXDdl5H960','5xeMctXQWNmMq4aAjwuR3e','2vcDnqv787PE1q1ym6qvjN','4Qqey3tSd9AaThQRTR2Ydi','6C11NF3olTlW2Y6FyGOg66','1oRF2Yry5g9W8IiiymixGp','2uxG4gg4WnqR5eriMN6ehS','0diDnoCxHOJh9lz6j6rGuK','2VbXEqCO2C06ABWcZ8ymHI','4AKYJAX4Ign3LHWRw4X59x','5HFrCOJWNvPAh43Hbtausa','2SW37CtAla5KfTKnPZ3pDc','0AjY8O7M2WKrbKRIJlbOQi','70zRJisGSqBQhoIUm5RRgE','2aSNahXvY4gtD8vzTzycUC','74CX7xjckNb5bygajdmxO7','21bJVPlnIK2PH4rqQDor8D','7qSN90Ta5W40hdA4xOY2Ww','01mdqLTNOrWIMRIAJUQZgD','3xcXoGZnv9c6ubjkF9Ehio','2mUqVFSr5l4W2Hpm8t3Gfm','0zuIUmEvxMf8tIYZ5wxJHI','4tX2TplrkIP4v05BNC903e','708Whrc4abJEtqBINv9S2b']
#artist endpoints
artist_albums_endpoint="artists/{id}/albums"
artist_toptracks_endpoint="artists/{id}/top-tracks"

#album endpoints
album_endpoint="albums/{id}"
album_tracks_endpoint="albums/{id}/tracks"

#track endpoints
track_detail_endpoint="tracks/{id}"
track_features_endpoint = "audio-features/{id}"
track_audio_analysis_endpoint = "audio-analysis/{id}"

def get_Headers():
    headers = {
        'Accept': 'application/json',
        'Authorization': "Bearer {}".format(OATH_TOKEN)
    }
    return headers
    
def get_artist_top_tracks(artist_id="2UZMlIwnkgAEDBsw1Rejkn"):
    url=base_api + artist_toptracks_endpoint.format(id=artist_id) + "?country=US"
    request=urllib.request.Request(url,headers=get_Headers())
    response=urllib.request.urlopen(request)    
    data = json.loads(response.read())       
    track_list=[]
    type(data)
    for track in data['tracks']:        
        result = json_normalize(track)
        track_list.append(result)
    return pd.concat(track_list)
#df=get_artist_top_tracks("2UZMlIwnkgAEDBsw1Rejkn")



def get_artist_albums(artist_id="4tX2TplrkIP4v05BNC903e"):
    url=base_api + artist_albums_endpoint.format(id=artist_id) + "?market=US"
    request=urllib.request.Request(url,headers=get_Headers())
    response=urllib.request.urlopen(request)
    data = json.loads(response.read())
    type(data)
    for item in data.items():
        if item[0]=='items':
            album_data=item[1]    
    result = json_normalize(album_data)
    result['artist_id']=artist_id
          
    if artist_id=='4tX2TplrkIP4v05BNC903e':
        result['Group_Name']='Tom Petty and the Heartbreakers'
        result['Years_Active']='1976-1987'
        
    elif artist_id=='2hO4YtXUFJiUYS2uYFvHNK':
        result['Group_Name']='Traveling Wilburys'
        result['Years_Active']='1988-1991'
        
    elif artist_id=='2UZMlIwnkgAEDBsw1Rejkn':
        result['Group_Name']='Tom Petty (solo)'
        result['Years_Active']='1989-2006'
        
    elif artist_id=='2xLqrYZxa9GYSCVn0STgxV':
        result['Group_Name']='Mudcrutch'
        result['Years_Active']='2007-2016 (present)'
          
    return result

def get_album_details(album_id="2mUqVFSr5l4W2Hpm8t3Gfm"):
    url=base_api + album_endpoint.format(id=album_id)
    request=urllib.request.Request(url,headers=get_Headers())
    response=urllib.request.urlopen(request)
    data = json.loads(response.read())    
    type(data.keys())
    data_details = {key: data[key] for key in data if key in ["id","release_date","name","popularity","images"]}
    result = json_normalize(data_details, "images",["id","release_date","name","popularity"])
    result_filtered=result.groupby('id').first().reset_index()
    result_filtered.shape
    return result_filtered 
   
def get_albums_tracks(album_id="1CvE8Bp9CDOArk2aL3NuC4"):
    url=base_api + album_tracks_endpoint.format(id=album_id)
    request=urllib.request.Request(url,headers=get_Headers())
    response=urllib.request.urlopen(request)
    data = json.loads(response.read())    
    for item in data.items():
        if item[0]=='items':
            track_data=item[1]    
    result = json_normalize(track_data)
    return result

def get_track_details(track_id="5tVA6TkbaAH9QMITTQRrNv"):
    url=base_api + track_detail_endpoint.format(id=track_id)
    request=urllib.request.Request(url,headers=get_Headers())
    response=urllib.request.urlopen(request)
    data = json.loads(response.read())
    data_details = {key: data[key] for key in data if key in ["id","name","duration_ms","explicit","popularity","album.name"]}    
    type(data_details)
    result = json_normalize(data_details)
    return result

def get_track_features(track_id):
    url=base_api + track_features_endpoint.format(id=track_id)
    request=urllib.request.Request(url,headers=get_Headers())
    response=urllib.request.urlopen(request)
    data = json.loads(response.read())    
    type(data)
    return pd.DataFrame(data,index=[0])


album_list=[]
for artist in artist_ids:    
    album_list.append(get_artist_albums(artist))

df_albums=pd.concat(album_list, ignore_index=True)
df_albums.columns
df_albums_filtered=df_albums[~df_albums['id'].isin(album_exclusions)]


album_detail_list=[]
for index_val, series_val in (df_albums_filtered['id']).iteritems():    
    df_album_details=get_album_details(series_val)        
    album_detail_list.append(df_album_details)
df_album_details=pd.concat(album_detail_list, ignore_index =True)

            
                       
album_track_list=[]
for index_val, series_val in (df_albums_filtered['id']).iteritems():    
    df_album_tracks=get_albums_tracks(series_val)    
    df_album_tracks['album_id']=series_val
    album_track_list.append(df_album_tracks)
    
df_album_tracks=pd.concat(album_track_list, ignore_index =True)


track_details_list=[]
for index_val, track_id, album_id in (df_album_tracks[['id','album_id']]).itertuples():     
    df_track_detail=get_track_details(track_id)    
    df_track_detail['spotify_embed_url']='https://embed.spotify.com/?uri=spotify:track:'+track_id                  
    df_track_detail['album_id']=album_id                   
    track_details_list.append(df_track_detail)                      
#special songs "Mary Jane's" and "Stop Draggin'"
adhoc_songs=[('0Adyxuv3X9l2CtMt0OeY5M','3S404OgKoVQSJ3xXrDVlp8'),('5eYwDBLucWfWI5KsV7oYX2','7ait6chB3O3C1fMGUDJhtu')]    
for track_id, album_id in adhoc_songs:         
    df_track_detail=get_track_details(track_id)    
    df_track_detail['spotify_embed_url']='https://embed.spotify.com/?uri=spotify:track:'+track_id                  
    df_track_detail['album_id']=album_id                   
    track_details_list.append(df_track_detail)                      

df_track_details=pd.concat(track_details_list, ignore_index =True)


trackidlist=df_album_tracks['id'].tolist()
trackidlist.append('0Adyxuv3X9l2CtMt0OeY5M')
trackidlist.append('5eYwDBLucWfWI5KsV7oYX2')
track_features_list=[]
#for index_val, series_val in (df_album_tracks['id']).iteritems():
for series_val in trackidlist:
    print (series_val)    
    track_features_list.append(get_track_features(series_val))
df_track_features=pd.concat(track_features_list, ignore_index =True)

df_albums_filtered.to_csv(file_path+"spotify_artist_albums.csv", sep=',', index=False, encoding="utf-8");    
df_album_tracks.to_csv(file_path+"spotify_album_tracks.csv", sep=',', index=False, encoding="utf-8");    
df_album_details.to_csv(file_path+"spotify_album_details.csv", sep=',', index=False, encoding="utf-8");    
df_track_details.to_csv(file_path+"spotify_track_details.csv", sep=',', index=False, encoding="utf-8");    
df_track_features.to_csv(file_path+"spotify_track_features.csv", sep=',', index=False, encoding="utf-8");    


    