import json
from flask import jsonify, request, Flask
from flask_socketio import SocketIO, emit

app = Flask(__name__)
# app.config["DEBUG"] = False
socketio = SocketIO(app)

filename = "buses.json"
with open(filename, 'r') as outfile:
    data = json.loads(outfile.read())  # converts json to dict
    
def notfound(errortype="busid not found"):
    return jsonify(message="failure", info=errortype)


@app.route('/api', methods=['GET'])
def allData():
    if 'busid' in request.args:
        busid = int(request.args['busid'])
        return jsonify(data["Counter1"][busid])
    return jsonify(data)


@app.route('/api/UpdateSeat', methods=['GET'])
def check():
    if not request.args:
        return notfound("Arguments not found")
    if 'busid' not in request.args or 'seatid' not in request.args:
        return notfound("busid or seatid not found")
    busid = int(request.args['busid'])
    seatid = int(request.args['seatid'])
    changed = False

    if 'isPacked' in request.args:
        isPacked = int(request.args['isPacked'])
        data['Counter1'][busid]['Seats'][seatid]['isPacked'] = isPacked
        changed = True

    if 'fn' in request.args:
        fn = request.args['fn']
        data['Counter1'][busid]['Seats'][seatid]['fn'] = fn
        changed = True

    if 'ln' in request.args:
        ln = request.args['ln']
        data['Counter1'][busid]['Seats'][seatid]['ln'] = ln
        changed = True

    if 'contact' in request.args:
        contact = int(request.args['contact'])
        data['Counter1'][busid]['Seats'][seatid]['contact'] = contact
        changed = True

    if changed:
        with open(filename, 'w') as outfile:
            json.dump(data, outfile)
        return jsonify(message="success", info="Updated successfully")

    return jsonify(message="failure", info="parameters other than busid and seatid needed")


@socketio.on("update json")
def updatejson():
    emit("download json", broadcast=True)


@app.route('/api/CustomerInfo', methods=['GET'])
def CustomerInfo():
    if 'busid' not in request.args or 'seatid' not in request.args:
        return notfound("busid or seatid not found")

    busid = int(request.args['busid'])
    seatid = int(request.args['seatid'])
    return jsonify(data['Counter1'][busid]['Seats'][seatid])


@app.route('/api/<info>', methods=['GET'])
def BusInfo(info):
    if 'busid' not in request.args:
        return notfound()
    busid = int(request.args['busid'])
    submit = data['Counter1'][busid]
    if info not in submit:
        return notfound("%s parameter not found" % info)
    return jsonify(submit[info])


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
