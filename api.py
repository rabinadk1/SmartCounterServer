import json
from create import *
from flask import jsonify, request, session
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash

# from flask_socketio import SocketIO, emit
# Configure session to use file system
app.config.update(
    SECRET_KEY="aed1edbd6976ba59b1f746958e3867e2",
    SESSION_PERMANENT=False,
    SESSION_TYPE="filesystem"
)
# socketio = SocketIO(app)
Session(app)

# filename = "buses.json"
# with open(filename, 'r') as outfile:
#     data = json.loads(outfile.read())  # converts json to dict

session = {"admin": False}


# def notfound(errortype="busid not found"):
#     return jsonify(message="failure", info=errortype)

def errormessage(info="Error occurred!!"):
    return jsonify(message="failure", info=info)


def successmessage(info="Successfully done!!"):
    return jsonify(message="success", info=info)


@app.route('/api', methods=['GET'])
def api():
    # if "username" not in session:
    #     return errormessage("Please login first!")

    # NOTE: Don't delete the commented code below
    # if 'busid' in request.args:
    #     busid = int(request.args['busid'])
    #     return jsonify(data["Counter1"][busid])
    if "username" in session:
        busCounters = {}
        counterInfo = []
        counterid = session["counterid"]
        # counterid = 1
        buses = Buses.query.filter((Buses.sourceid == counterid) | (Buses.destinationid == counterid)).all()
        busesid = []
        for bus in buses:
            busesid.append(bus.id)
        customerinfo = CustomerInfo.query.filter(CustomerInfo.busid.in_(busesid)).all()
        for bus in buses:
            busSource = Counters.query.get(bus.sourceid)
            busDestination = Counters.query.get(bus.destinationid)
            BusDetails = {"BusNumber": bus.busnumber, "DepartureTime": bus.departuretime, "BusSource": busSource.name,
                          "BusDestination": busDestination.name, "BusId": bus.id}
            seats = []

            for seat in bus.seats:
                seatsInfo = {"isPacked": False, "CustomerName": "", "contact": 0, "seatName": seat}
                for customer in customerinfo:
                    for seatno in customer.seats:
                        if seatno == seat:
                            seatsInfo["isPacked"] = True
                            seatsInfo["CustomerName"] = customer.name
                            seatsInfo["contact"] = customer.contact
                seats.append(seatsInfo)
            BusDetails["Seats"] = seats
            counterInfo.append(BusDetails)
        busCounters["Counter"] = counterInfo
        # this is done this way as we only have one counter as for now
        # the json structure must be altered a bit differently if more counters are added
        return jsonify(busCounters)
    return errormessage("Please login first!")


@app.route('/admin/getcounters', methods=['GET'])
def getcounters():
    if session["admin"]:
        counters = []
        counterlist = Counters.query.all()
        for counter in counterlist:
            counters.append(
                {
                    "CounterName": counter.name,
                    "CounterAddress": counter.address
                }
            )
        return jsonify(Counters=counters)
    return errormessage("Operation not permitted!")


@app.route('/login', methods=['POST'])
def login():
    if "username" not in session:
        if not request.is_json:
            return errormessage("JSON not found!!")
        username = request.json.get("Username", None)
        if not username:
            return errormessage("Username not provided!")
        userinfo = Users.query.filter_by(username=username).one_or_none()
        if not userinfo:
            return errormessage("User not registered")
        password = request.json.get("Password", None)
        if not check_password_hash(userinfo.password, password):
            return errormessage("Password doesn't match")
        session["username"] = username
        session["counterid"] = userinfo.counterid
    return successmessage("Logged in successfully!!")


@app.route('/admin/adduser', methods=['POST'])
def adduser():
    if session["admin"]:
        if not request.is_json:
            return errormessage("JSON not found!")
        username = request.json.get("Username", None)
        if not username:
            return errormessage("Username not provided!")
        if Users.query.filter_by(username=username).count():
            return errormessage("Username already exists")
        password = request.json.get("Password", None)
        counterid = request.json.get("CounterId", None)
        contact = request.json.get("Contact", None)
        if not (password and counterid and contact):
            return errormessage("Incomplete info provided!")
        user = Users(username=username, password=generate_password_hash(password), counterid=counterid, contact=contact)
        db.session.add(user)
        db.session.commit()
        return successmessage("Successfully registered!")
    return errormessage("Operation not permitted!")


# @app.route('/logout', methods=['GET'])
# def logout():
#     if "username" not in session:
#         return errormessage("Not logged in yet!")
#     session = {"admin": False}
#     return "Successfully logged out!"


@app.route('/updateseat', methods=['POST'])
def updateseat():
    if "username" not in session:
        return errormessage("Please login first")
    if not request.is_json:
        return errormessage("The requested method is not of JSON type.")
    busid = request.json.get("BusId", None)
    customername = request.json.get("CustomerName", None)
    contact = request.json.get("Contact", None)
    seats = request.json.get("Seats", None)
    if not (customername and seats and contact and busid):
        return errormessage("Incomplete info provided!")
    # for seatid in seats:
    #     print(f'"{seatid}"')
    #     seat = data['Counter1'][busid]['Seats'][int(seatid[-1]) - 1]
    #     seat["CustomerName"] = customername
    #     seat["Contact"] = contact
    #     seat["isPacked"] = True
    # with open('buses.json', 'w') as outfile:
    #     json.dump(data, outfile)
    customer = CustomerInfo(name=customername, contact=contact, seats=seats, busid=int(busid))
    db.session.add(customer)
    db.session.commit()
    return successmessage("Data updated successfully!")


@app.route('/admin/login', methods=['POST'])
def loginadmin():
    if not session["admin"]:
        if not request.is_json:
            return errormessage("JSON not found!!")
        username = request.json.get("Username", None)
        if not username:
            return errormessage("Username not provided!")
        admininfo = Admins.query.filter_by(username=username).one_or_none()
        if not admininfo:
            return errormessage("Admin not registered")
        password = request.json.get("Password", None)
        if not check_password_hash(admininfo.password, password):
            return errormessage("Password doesn't match")
        session["username"] = username
        session["admin"] = True
    return successmessage("Logged in successfully!!")


@app.route('/admin/addbus', methods=['POST'])
def addbus():
    if session["admin"]:
        if not request.is_json:
            return errormessage("The requested method is not of JSON type.")
        busnumber = request.json.get("BusNumber", None)
        source = request.json.get("Source", None)
        destination = request.json.get("Destination", None)
        seats = request.json.get("Seats", None)
        departuretime = request.json.get("DepartureTime", None)
        if not (busnumber and source and destination and seats and departuretime):
            return errormessage("Incomplete info provided!")
        sourceid = Counters.query.filter_by(name=source).one_or_none()
        destinationid = Counters.query.filter_by(name=destination).one_or_none()
        if not (sourceid and destinationid):
            return errormessage("Invalid source or destination!")
        sourceid = sourceid.id
        destinationid = destinationid.id
        bus = Buses(busnumber=busnumber, sourceid=sourceid, destinationid=destinationid, seats=seats,
                    departuretime=departuretime)
        db.session.add(bus)
        db.session.commit()
        return successmessage("Added bus successfully!!")
    return errormessage("Operation not permitted!")


@app.route('/admin/updatebus', methods=['POST'])
def updatebus():
    if session["admin"]:
        if not request.is_json:
            return errormessage("The requested method is not of JSON type.")
        busnumber = request.json.get("BusNumber", None)
        source = request.json.get("Source", None)
        destination = request.json.get("Destination", None)
        departuretime = request.json.get("DepartureTime", None)
        if not (busnumber and (source or destination or departuretime)):
            return errormessage("Incomplete info provided!")
        bus = Buses.query.filter_by(busnumber=busnumber).one_or_none()
        if bus is None:
            return errormessage("Invalid BusNumber!")
        if source:
            sourceid = Counters.query.filter_by(name=source).one_or_none()
            if sourceid is None:
                return errormessage("Invalid Source!")
            bus.sourceid = sourceid.id
        if destination:
            destinationid = Counters.query.filter_by(name=destination).one_or_none()
            if destinationid is None:
                return errormessage("Invalid Destination!")
            bus.destinationid = destinationid.id
        if departuretime:
            bus.departuretime = departuretime
        db.session.commit()
        return successmessage("Updated bus successfully!!")
    return errormessage("Operation not permitted!")


@app.route('/admin/addcounter', methods=['POST'])
def addcounter():
    if session["admin"]:
        if not request.is_json:
            return errormessage("JSON not found!!")
        countername = request.json.get("CounterName", None)
        counteraddress = request.json.get("CounterAddress", None)
        if not (countername and counteraddress):
            return errormessage("Information incomplete!")
        counter = Counters(name=countername, address=counteraddress)
        db.session.add(counter)
        db.session.commit()
        return successmessage("Data added successfully!")
    return errormessage("Operation not permitted!")


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
