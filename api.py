import json
from create import *
from flask import jsonify, request, session, abort
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

session = {}


# def notfound(errortype="busid not found"):
#     return jsonify(message="failure", info=errortype)

def errormessage(info="Error occurred!!"):
    return jsonify(message="failure", info=info)


def successmessage(info="Successfully done!!"):
    return jsonify(message="success", info=info)


@app.route('/api', methods=['GET'])
def api():
    # if 'busid' in request.args:
    #     busid = int(request.args['busid'])
    #     return jsonify(data["Counter1"][busid])
    return jsonify(data)


@app.route('/login', methods=['POST'])
def login():
    if "username" not in session:
        if not request.is_json:
            return errormessage("JSON not found!!")
        username = request.json.get("Username", None)
        if username is None:
            return errormessage("Username not provided!")
        userinfo = Users.query.filter_by(username=username).one_or_none()
        if userinfo is None:
            return errormessage("User not registered")
        password = request.json.get("Password", None)
        if not check_password_hash(userinfo.password, password):
            return errormessage("Password doesn't match")
        session["username"] = username
        session["counterid"] = userinfo.counterid
        print("K xa topper?")
    return successmessage("Logged in successfully!!")


@app.route('/register', methods=['POST'])
def register():
    if "username" not in session:
        if not request.is_json:
            return errormessage("JSON not found!")
        username = request.json.get("Username", None)
        if username is None:
            return errormessage("Username not provided!")
        if Users.query.filter_by(username=username).count():
            return errormessage("Username already exists")
        password = generate_password_hash(request.json.get("Password"))
        counterid = request.json.get("CounterId")
        contact = request.json.get("Contact")
        user = Users(username=username, password=password, counterid=counterid, contact=contact)
        db.session.add(user)
        db.session.commit()
    return successmessage("Successfully registered")


@app.route('/logout')
def logout():
    try:
        session.pop("username")
    except KeyError:
        return "Not logged it yet!"
    finally:
        return "Successfully logged in!"


@app.route('/updateseat', methods=['POST'])
def updateseat():
    if "username" not in session:
        return errormessage("Please login first")
    if not request.is_json:
        return errormessage("The requested method is not of JSON type.")
    busid = int(request.json.get("BusId"))
    customername = request.json.get("CustomerName", None)
    contact = request.json.get("Contact", None)
    seats = request.json.get("Seats", None)
    if customername is None or seats is None or contact is None:
        return errormessage("Incomplete info provided!")
    for seatid in seats:
        print(f'"{seatid}"')
        seat = data['Counter1'][busid]['Seats'][int(seatid[-1])-1]
        seat["CustomerName"] = customername
        seat["Contact"] = contact
        seat["isPacked"] = True
    with open('buses.json', 'w') as outfile:
        json.dump(data, outfile)
    ''' The following code works fluently in database but database migration is remaining so commented out!!'''
    # customer = CustomerInfo(name=customername, contact=contact, seats=seats, busid=busid)
    # db.session.add(customer)
    # db.session.commit()
    return successmessage("Data updated successfully")


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
