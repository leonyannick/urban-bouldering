import os
import datetime
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, request, url_for, send_from_directory
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from helpers import apology, login_required

UPLOAD_FOLDER = 'images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response



# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///boulder.db")


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]

    if request.method == "GET":
        boulders = db.execute("SELECT name, grade, latitude, longitude, image, description from boulder")
        return render_template("index.html", boulders=boulders)

    elif request.method == "POST":
        name = request.form.get("name")
        grade = request.form.get("grade")
        description = request.form.get("description")
        latitude = request.form.get("latitude")
        longitude = request.form.get("longitude")

        #check if boulder name already exists
        rows = db.execute("SELECT * FROM boulder WHERE name = :name",
                          name=name)
        if len(rows) == 1:
            return apology("boulder name already exists")

        #upload image
        # check if the post request has the file part
        if 'file' not in request.files:
            #flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            #directory = os.path.join(app.config['UPLOAD_FOLDER'], name)
            #os.mkdir(directory)
            #print(directory)
            #file.save(os.path.join(directory, filename))
            filename, file_extension = os.path.splitext(filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], name + file_extension)
            file.save(image_path)
            #return redirect(url_for('uploaded_file', filename=filename))

        #add values to database
        time = datetime.datetime.now()
        db.execute("INSERT INTO boulder (id, name, grade, time, latitude, longitude, image, description) VALUES (:id, :name, :grade, :time, :latitude, :longitude, :image, :description)", id = user_id, name = name, grade=grade, time=time, latitude=latitude, longitude=longitude, image=image_path, description=description)


        boulders = db.execute("SELECT name, grade, latitude, longitude, image, description from boulder")

        return render_template("index.html", boulders=boulders)

@app.route('/show_boulder', methods=["GET", "POST"])
def show_boulder():
    if request.method == "POST":
        name = request.form.get("name")
        boulder = db.execute("SELECT name, grade, latitude, longitude, image, description from boulder WHERE name=:name", name=name)
        print(boulder)

    return render_template("index.html", boulders=boulder)



@app.route('/images/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route("/<name>", methods=["GET", "POST"])
@login_required
def boulder_fullscreen(name):
    """Display the boulder on a new Site"""
    if request.method == "GET":
        boulder = db.execute("SELECT name, grade, latitude, longitude, image, description from boulder WHERE name = :name", name=name)


        return render_template("boulder_fullscreen.html", boulder=boulder[0])


@app.route("/history")
@login_required
def history():
    """List of all boulders"""
    user_id = session["user_id"]
    boulders = db.execute("SELECT name, grade, time, description from boulder")

    return render_template("history.html", boulders=boulders)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username")

        elif not request.form.get("password"):
            return apology("must provide password")

        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        if len(rows) == 1:
            return apology("username already taken")

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not (password == confirmation):
            return apology("passwords did not match")

        pw_hash = generate_password_hash(password)
        db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username=username, hash=pw_hash)
        return redirect("/")

    elif request.method == "GET":
        return render_template("register.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
