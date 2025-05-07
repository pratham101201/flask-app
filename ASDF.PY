from flask import Flask,render_template,request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db=SQLAlchemy(app)


# Create the database
with app.app_context():
    db.create_all()

# Create a database model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"User('{self.name}', '{self.email}')"

@app.route('/',methods=['GET','POST'])
def hello_world():
    if request.method == 'POST':
        # Handle form submission here
        name = request.form.get('name')
        return render_template('index.html', name=name)
    return render_template('index.html',name=None)
  

@app.route('/hello')
def hello():
    return 'Hello! This is a Flask app.'

@app.route('/goodbye')
def goodbye():
    return 'Goodbye! This is a Flask app.'

@app.route('/about')
def about():
    return render_template('about.html')

@app.route("/add", methods=["POST"])
def add_user():
    name = request.form.get("name")
    email = request.form.get("email")

    if name and email:
        new_user = User(name=name, email=email)
        db.session.add(new_user)
        db.session.commit()
    
    return redirect("/")


@app.route("/index")
def index():
    users = User.query.all()  # Get all users from the database
    return render_template("index.html", users=users)


if __name__ == '__main__':
    app.run(debug=True)