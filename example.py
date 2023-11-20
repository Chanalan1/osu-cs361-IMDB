
import zmq
def query_server(data):
    context = zmq.Context()

    # Socket to talk to server
    print("Connecting to the video game server...")
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5556")

    # Send the JSON data
    socket.send_json(data)

    # Get the reply.
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