# spofity

Base inspiration: [I made an AI that suggests you songs better than Spotify’s own AI.](https://medium.com/geekculture/spotifys-song-recommendation-ai-wasnt-good-enough-so-i-made-an-ai-better-than-it-38b8528f14bd)

## Setup
### Recommend using [venv](https://docs.python.org/3/library/venv.html)
- Create a virtual environment
```console
python3 -m venv <env_name>
```
- Activate venv
```console
source <env_name>/bin/activate
```
- Deactivate venv
```console
deactivate
```

### Install required dependencies
```console
pip install -r requirements.txt
```

#### To upgrade your installed packages
```console
pip install --upgrade -r requirements.txt
```

## Setup/retrieve Spotify developer credentials
1. Go to https://developer.spotify.com and login with your Spotify ID.
2. Make a new app.
3. Set the Redirect URL to [http://localhost:8000](http://localhost:8000)
4. Get your client ID and Secret

Once the developer credentials are availabl, run setup `setup.py` file 
- It will loop through and set the required credentials in a `.env` file
If a single credential needs to be updated, run `setup.py` file with one of the following as a parameter:
- `client_id`
- `client_secret`
- `client_username`

