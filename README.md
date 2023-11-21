
# IMBD MICROSERVICE
***

## Communication Contract

Ground rules:
- a. The primary form of communication is through Discord. Email will be the backup if needed.
- b. Partners are expected to response within 24 hours.
- c. Partners must notify as soon as possible if they will be unavailable. (Ie. Out sick/vacation)
- d. Code sharing will be on Git (github/gitlab/bitbucket)
- e. Document sharing will be on Google Drive 

***

## Set up of microservice

No set up needed. Data is taken from imbd.csv file
***

## File Structure

**game_microservice.py** is the microservice <br>
**example.py** is the example file that shows how to interact with the microservice <br>
**imbd_videogame_reviews.csv** is the file containing the dataset
***

## How to request and receive data from microservice

### To start the microservice

You need to start the microservice using zmq by doing typing into the terminal <br>
```
python game_microservice.py 5556 # port number
```
<br>

### Once started
On your main.py program, you will send a Json with the constraints <br>
```
data = {
    'genres': "xxxx",
    'startYear': "xxxx",
    'averageRating': x,
    'numVotes': x,
    'isAdult': x
}
```
<br>
Similar to the example and the microservice will be running on a loop until it gets a request
<br>
### Request and response

When the microservice takes the request, it will generate a response in the form of a JSON and send it back as a response. <br>
For example, this could be a response when taking a request: <br>

```
Received reply: {'primaryTitle': 'Treasure Quest', 'genres': 'Adventure,Fantasy,Musical', 'startYear': '1996', 'averageRating': 7.0, 'numVotes': 17.0, 'isAdult': 0}
```
<br>
***

