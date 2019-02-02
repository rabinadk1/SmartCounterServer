import json
from create import *
from flask import jsonify, request, session
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash

# from flask_socketio import SocketIO, emit

# Configure session to use file system
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
# socketio = SocketIO(app)
Session(app)

filename = "buses.json"
with open(filename, 'r') as outfile:
    data = json.loads(outfile.read())  # converts json to dict

# def notfound(errortype="busid not found"):
#     return jsonify(message="failure", info=errortype)


@app.route('/api', methods=['GET'])
def api():
    # if 'busid' in request.args:
    #     busid = int(request.args['busid'])
    #     return jsonify(data["Counter1"][busid])
    return jsonify(data)


@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return "JSON not found!!"
    username = request.json.get("username", None)
    if username is None:
        return "error"
    userinfo = Users.query.filter_by(username=username).one_or_none()
    if userinfo is None:
        return "User not registered"
    password = request.json.get("password", None)
    if check_password_hash(userinfo.password, password):
        return "Password doesn't match"
    session["username"] = username
    return "Logged in successfully!!"


@app.route('/register', methods=['POST'])
def register():
    if "username" not in session:
        if not request.is_json:
            return "JSON not found!"
        username = request.json.get("username", None)
        if username is None:
            return "error"
        if Users.query.filter_by(username=username).count():
            return "Username already exists"
        password = generate_password_hash(request.json.get("password"))
        counter = request.json.get("counter")
        email = request.json.get("email")
        user = Users(username=username, password=password, counter=counter, email=email)
        db.session.add(user)
        db.session.commit()
    return "Success!!"


@app.route('/logout')
def logout():
    try:
        session.pop("username")
    except KeyError:
        return "Not logged it yet!"
    finally:
        return "Successfully logged in!"


@app.route('/api/UpdateSeat', methods=['POST'])
def updateseat():
    if "username" not in session:
        return "Please login first"
    if not request.is_json:
        return "JSON not found!!"
    busid = int(request.json.get("busid"))
    customername = request.json.get("CustomerName", None)
    contact = request.json.get("Contact", None)
    seats = request.json.get("seats", None)
    if customername is None or seats is None:
        return "Customer name or seats are not specified"
    for seatid in seats:
        seat = data['Counter1'][busid]['Seats'][seatid]
        seat.CustomerName = customername
        seat.Contact = contact
        seat.isPacked = True
    with open('buses.json', 'w') as outfile:
        json.dump(data, outfile)


# @socketio.on("update json")
# def updatejson():
#     emit("download json", broadcast=True)


# @app.route('/api/CustomerInfo', methods=['GET'])
# def customerinfo():
#     if 'busid' not in request.args or 'seatid' not in request.args:
#         return notfound("busid or seatid not found")
#
#     busid = int(request.args['busid'])
#     seatid = int(request.args['seatid'])
#     return jsonify(data['Counter1'][busid]['Seats'][seatid])
#
#
# @app.route('/api/<info>', methods=['GET'])
# def businfo(info):
#     if 'busid' not in request.args:
#         return notfound()
#     busid = int(request.args['busid'])
#     submit = data['Counter1'][busid]
#     if info not in submit:
#         return notfound("%s parameter not found" % info)
#     return jsonify(submit[info])


if __name__ == "__main__":
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
