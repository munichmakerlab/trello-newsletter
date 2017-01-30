# Trello to Newsletter

MuMaLab people write a newsletter once a week. That was done in a pad so far, and then sent out manually. Not very convinient. Let's automate.

## Setup
* Clone repo
```
git clone git@github.com:munichmakerlab/trello-newsletter.git
cd trello-newsletter
```

* Install py-trello
```
virtualenv env
. env/bin/activate
pip install py-trello
```

* Get Trello API key and secret from https://trello.com/app-key
* Do that OAuth dance
```
export TRELLO_API_KEY=<API_KEY>
export TRELLO_API_SECRET=<API_SECRET>
export TRELLO_EXPIRATION=never
```

* Copy `config.py.sample` and edit it
```
cp config.py.sample config.py
vi config.py
```

* Run the whole thing
```
python newsletter.py
```
