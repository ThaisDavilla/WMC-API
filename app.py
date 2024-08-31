from flask import Flask, render_template
import urllib.request, json

app = Flask(__name__)

@app.route("/")
def get_list_characters_page():
    url = "https://rickandmortyapi.com/api/character/"
    response = urllib.request.urlopen(url)
    data = response.read()
    dict = json.loads(data)
    
    return render_template("characters.html", characters=dict["results"])


@app.route("/profile/<id>")
def get_profile(id):
    url = "https://rickandmortyapi.com/api/character/" + id
    response = urllib.request.urlopen(url)
    data = response.read()
    character = json.loads(data)

    #Criação do dicionário de episódio, bem como a iteraçaõ sobre episódio.
    #É exatamente a mesma lógica que a demonstração de perfil.

    episodes = []
    for episode_url in character['episode']:
        episode_response = urllib.request.urlopen(episode_url)
        episode_data = episode_response.read()
        episode = json.loads(episode_data)
        episodes.append({
            "id": episode["id"],
            "name": episode["name"],
        })

    # Criação do dicionário para receber todas as informações de perfil.
    profile = {
        "image": character["image"],
        "name": character["name"],
        "status": character["status"],
        "species": character["species"],
        "gender": character["gender"],
        "origin": {
            "name": character["origin"]["name"],
            "url": "/locations/" + str(character["origin"]["url"].split('/')[-1])  
        },
        "location": {
            "name": character["location"]["name"],
            "url": "/locations/" + str(character["location"]["url"].split('/')[-1])
        }, 
        "episodes": episodes
    }    
    
    return render_template("profile.html", profile=profile)
