from flask import Blueprint, render_template, request, redirect


views = Blueprint("views", __name__)

USERS = []

def add_user(ip_address, name):
    USERS.append({"ip": ip_address, "name": name})

def check_user_in_USERS(ip_address):
    for user in USERS:
        if user["ip"] == ip_address:
            return True
    
    return False

def check_username_exists(username):
    for user in USERS:
        if user["name"] == username:
            return True
        
    return False

def get_name_by_ip(ip_address):
    for user in USERS:
        print(user["ip"])
        if user["ip"] == ip_address:
            return user["name"]
    

@views.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        if check_user_in_USERS(request.remote_addr):
            return render_template("home.html", is_logged_in=True, uname=get_name_by_ip(request.remote_addr), devices=[])
        
        else:
            return render_template("home.html", is_logged_in=False)
    
    elif request.method == "POST":
        username = request.form.get("input_name")
        if check_username_exists(username):
            return render_template("home.html")
        else:
            add_user(request.remote_addr, username)
            return render_template("home.html", is_logged_in=True, uname=username)
    

@views.route("/messaging", methods=["GET", "POST"])
def messaging_ui():
    if request.method == "GET":
        if check_user_in_USERS(request.remote_addr):
            return render_template("messaging.html", USERS=USERS)

        else:
            return redirect("/", 200)
    
    elif request.method == "POST":
        recipient = request.form.get("recipient-holder")
        message_data = request.form.get("message-box")

        print(recipient, message_data)

        return render_template("messaging.html", USERS=USERS)

def message(sender, reciever, message):
    return

@views.route("/ring")
def ring_ui():
    return render_template("ring.html")