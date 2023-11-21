
import zmq
def query_server(data):
    context = zmq.Context()


    print("Connecting to the video game server...")
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5556")


    socket.send_json(data)


    message = socket.recv_json()
    print("Received reply: %s" % message)

# ezxample data used to test microservice
data = {
    'genres': "Fantasy",
    'startYear': "2005",
    'averageRating': 7,
    'numVotes': 1000,
    'isAdult': 0
}

query_server(data)