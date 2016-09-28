from flask import Flask, render_template, request, redirect, flash, session
from mysqlconnection import MySQLConnector
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

app = Flask(__name__)
app.secret_key = 'supersecret'

mysql = MySQLConnector(app, 'frienddb')

@app.route('/')
def index():
    query = "SELECT * FROM friends"
    friends = mysql.query_db(query)
    return render_template("index.html", friendlist = friends)

@app.route('/friends', methods=['POST'])
def create():
    query = "SELECT email FROM friends"
    emails = mysql.query_db(query)
    errors = False
    if len(request.form['email']) < 1:
        errors = True
        flash("e-mail address is empty. Enter e-mail.")
    elif not EMAIL_REGEX.match(request.form['email']):
        errors = True
        flash("Invalid e-mail address. Enter e-mail.")
    elif {'email' : request.form['email']} in emails:
        errors = True
        flash("The e-mail address entered already exists in the database.")
    if errors:
        return redirect('/')
    else:
        query = "INSERT INTO friends (email, firstname, lastname, created_at, updated_at) VALUES(:email, :firstname, :lastname, NOW(),NOW());"
        data = {'email':request.form['email'], 'firstname' :request.form['firstname'], 'lastname' :request.form['lastname']}
        mysql.query_db(query, data)
        return redirect('/')

@app.route('/friends/<id>/edit')
def edit(id):
    query = "SELECT * FROM friends WHERE id = :edit_id"
    data = {'edit_id': id}
    friend = mysql.query_db(query, data)
    return render_template("edit.html", friend = friend)

@app.route('/friends/<id>', methods=['POST'])
def update(id):
    errors = False
    if len(request.form['email']) < 1:
        errors = True
        flash("e-mail address is empty. Enter e-mail.")
    elif not EMAIL_REGEX.match(request.form['email']):
        errors = True
        flash("Invalid e-mail address. Enter e-mail.")
    if errors:
        return redirect('/friends/<id>/edit')
    else:
        query = "UPDATE friends SET email = :email, firstname = :firstname, lastname = :lastname  WHERE id = :id"
        data = {'email':request.form['email'], 'firstname' :request.form['firstname'], 'lastname' :request.form['lastname'], 'id':request.form['id']}
        mysql.query_db(query, data)
        return redirect('/')

@app.route('/friends/<id>/delete', methods=['POST'])
def destroy(id):
    query = "DELETE FROM friends WHERE id = :id"
    data = {'id': id}
    mysql.query_db(query, data)
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
