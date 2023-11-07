import streamlit as st
import pickle
import pandas as pd
from IPython.display import Image, display
from PIL import Image as PILImage
import requests
import pickle

games_full_list = pickle.load(open('games_full_list.pkl','rb'))
game_raw = pd.DataFrame(games_full_list)
cosine_sim = pickle.load(open('cosine_sim.pkl','rb'))
def game_recommendation(game):
    movie_id = game_raw.loc[game_raw['Name'] == game, 'serial_number'].values[0]
    similarity_list = cosine_sim[movie_id]
    final_games = sorted(list(enumerate(similarity_list)),key=lambda x: x[1], reverse=True)[1:7]
    rec_games = []
    for i in final_games:
        games_rec = game_raw.loc[game_raw['serial_number']==i[0],'Name'].values[0]
        image_url = game_raw.loc[game_raw['serial_number']==i[0],'Icon URL'].values
        game_link = game_raw.loc[game_raw['serial_number'] == i[0], 'URL'].values
        rec_games.append((games_rec, image_url, game_link))
    return rec_games

st.title('App Store Game Recommendation')
games_list = st.selectbox('Enter the name of the game',game_raw['Name'].values)

if st.button('Search'):
    r = game_recommendation(games_list)

    row1 = st.columns(3)
    row2 = st.columns(3)

    for i, (game_name, image_url, game_link) in enumerate(r):
        img = PILImage.open(requests.get(image_url[0], stream=True).raw)
        img = img.resize((150, 150))

        row = row1 if i < 3 else row2
        col = i if i < 3 else i - 3

        with row[col]:
            st.image(img, caption='')
            game_url = f"{game_link[0]}"
            st.markdown(f"[{game_name}]({game_url})")