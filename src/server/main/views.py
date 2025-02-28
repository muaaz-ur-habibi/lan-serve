from flask import Blueprint, render_template, request, redirect, flash
import sqlite3 as sql

import os
import time

views = Blueprint("views", __name__)

def init_db():
    print("yo")
    open("main/database/database.db", "w")
    db = sql.connect("main/database/database.db")
    cursor = sql.Cursor(db)

    cursor.execute("""
                    CREATE TABLE USERS(
                    user_id integer PRIMARY KEY,
                    username string NOT NULL,
                    ip_address string NOT NULL
                    )
                    """)
        
    cursor.execute("""
                    CREATE TABLE Messages(
                    message_id integer PRIMARY KEY,
                    sender string NOT NULL,
                    recipient string NOT NULL,
                    message string NOT NULL
                    )
                    """)
    db.commit()
    db.close()

def add_user(ip_address, name):
    conn = sql.connect("main/database/database.db")
    cursor = sql.Cursor(conn)
    cursor.execute(f"""
                    INSERT INTO USERS (username, ip_address) VALUES ('{name}', '{ip_address}')
                    """)

    conn.commit()
    conn.close()

def check_user_in_USERS(ip_address):
    conn = sql.connect("main/database/database.db")
    cursor = sql.Cursor(conn)
    addrs = cursor.execute(f"""
                    SELECT 1 FROM USERS WHERE ip_address = '{ip_address}' LIMIT 1;
                    """).fetchall()

    if addrs == []:
        return False
    else:
        return True

def check_username_exists(username):
    conn = sql.connect("main/database/database.db")
    cursor = sql.Cursor(conn)

    name = cursor.execute(f"""
                        SELECT username FROM USERS WHERE username = '{username}'
                        """)

    if name.fetchall() == []:
        return False
    else:
        return True

def get_name_by_ip(ip_address):
    conn = sql.connect("main/database/database.db")
    cursor = sql.Cursor(conn)

    name = cursor.execute(f"""
                        SELECT username FROM USERS WHERE ip_address = '{ip_address}'
                           """).fetchone()

    return name[0]

def get_ip_by_name(name):
    conn = sql.connect("main/database/database.db")
    cursor = sql.Cursor(conn)
    
    addr = cursor.execute(f"""
                    SELECT ip_address FROM USERS WHERE username = '{name}'
                    """).fetchone()

    return addr[0]

def USERS():
    conn = sql.connect("main/database/database.db")
    cursor = sql.Cursor(conn)

    usrs = cursor.execute("""SELECT username FROM USERS""").fetchall()

    #cursor.close()
    conn.close()

    return usrs


@views.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        if check_user_in_USERS(request.remote_addr):
            return render_template("home.html", is_logged_in=True, uname=get_name_by_ip(request.remote_addr))
        
        else:
            return render_template("home.html", is_logged_in=False)
    
    elif request.method == "POST":
        username = request.form.get("input_name")
        if check_username_exists(username):
            flash("That username already exists on the server. Please enter a new one", "error")
            return render_template("home.html", )
        else:
            add_user(request.remote_addr, username)
            return render_template("home.html", is_logged_in=True, uname=username)


def MESSAGE(sender, recipient, message):
    conn = sql.connect("main/database/database.db")
    cursor = sql.Cursor(conn)
    
    cursor.execute(f"""
                    INSERT INTO Messages (sender, recipient, message) VALUES ('{sender}', '{recipient}', '{message}')
                    """)
    
    print(cursor.execute("SELECT * FROM Messages").fetchall())

    conn.commit()
    conn.close()

@views.route("/messaging", methods=["GET", "POST"])
def messaging_ui():
    if check_user_in_USERS(request.remote_addr):
        if request.method == "GET":
            return render_template("messaging.html", USERS=USERS())
    
        elif request.method == "POST":
            recipient = request.form.get("recipient-holder")
            message_data = request.form.get("message-box")

            MESSAGE(request.remote_addr, get_ip_by_name(recipient), message_data)

            return render_template("messaging.html", USERS=USERS())
    else:
        return redirect("/", 200)
    

def INBOX(inbox_of):
    conn = sql.connect("main/database/database.db")
    cursor = sql.Cursor(conn)

    msgs = cursor.execute(f"""
                          SELECT sender,message FROM Messages WHERE recipient = '{inbox_of}'
                          """).fetchall()
    conn.close()

    return msgs

@views.route("/inbox", methods=["GET"])
def inbox_ui():
    if check_user_in_USERS(request.remote_addr):
        print(INBOX(request.remote_addr))
        return INBOX(request.remote_addr)
    
    else:
        return redirect("/", 200)

@views.route("/ring")
def ring_ui():
    return render_template("ring.html")