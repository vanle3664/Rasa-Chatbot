# Rasa-Chatbot
Reference: https://www.youtube.com/watch?v=hqkfHK7-O08&t=852s

Step to run:

1. Install necessary library

```bash
	pip install rasa_core sklearn_crfsuite spacy rasa_nlu
	python -m spacy download en
```

2. Run it

```bash
	rasa shell #run on terminal
```

Deploy on Messenger

- Create page & app: ĐA HTTT
- Get app secret, page token & paste to credentials.yml
- Run

```bash
	rasa run --endpoints endpoints.yml --credentials credentials.yml
```

- Dowload ngrok, unzip then run ngrok.exe

```bash
	ngrok http 5005
```

- Copy webhook with https protocol into Facebook app
- Start using Messenger Chatbot
