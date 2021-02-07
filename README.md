# Messy
A simple messaging app written with Django and re-frame 

## Installation and starting the servers
If you have [Poetry](https://github.com/python-poetry/poetry/) installed then simply run
```
poetry install
```
Otherwise, I've supplied the requirements.txt that's output from Poetry. Install those requirements by running
```
pip install -r requirements.txt
```
Start the Django server by running 
```
python manage.py runserver
```
The API should now be availible at `localhost:8000`

Start the clojure development server by running
```
lein watch
```
inside the `messy-cljs` server. The frontend is then available at `localhost:8280`.

## API
###Data:
The shape of a `Message` is the following
```json
{
    "content": "I wrote the funniest joke in the world!",
    "created_at": "2021-02-06T15:21:13.632452Z",
    "id": 1,
    "retrieved_at": "2021-02-06T15:36:21.625787Z",
    "recipient": "wensleydale",
    "sender": null
}
```
`"recipient"` and `"sender"` is the username of the recipient/sender. Note that they're case sensitive.

When creating a new message the `"recipient"` and `"content"` fields are mandatory, `"sender"` is optional.
All other fields are ignored if submitted.

###Endpoints:
```
POST /message/ - Create a new message
GET /message/<id>/ - Get specific message
DELETE /message/<id>/ - Delete specific message
GET /message/range/<from>/<to>/ - Get a range of messages where ``from <= message.id <= to``
POST /message/new/ - Get new messages, that is all messages that hasn't been retrieved from 
this endpoint before
```