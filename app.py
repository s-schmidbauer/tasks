from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

name = "Stefan"
db = SQLAlchemy(app)

class Task(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100))
  done = db.Column(db.Boolean)
  # due = db.Column(db.DateTime)

@app.route("/")
def index():
  open_tasks = Task.query.filter_by(done=False)
  done_tasks = Task.query.filter_by(done=True)
  return render_template('tasks.html', name=name, open_tasks=open_tasks, done_tasks=done_tasks)

@app.route("/add", methods=['POST'])
def add():
  name = request.form.get('name')
  # due = request.form.get('due')
  new_task = Task(name=name, done=False)
  db.session.add(new_task)
  db.session.commit()
  return redirect(url_for('index'))

@app.route("/done/<int:id>")
def done(id):
  task = Task.query.filter_by(id=id).first()
  task.done = True
  db.session.commit()
  return redirect(url_for('index'))

@app.route("/undone/<int:id>")
def undone(id):
  task = Task.query.filter_by(id=id).first()
  task.done = False
  db.session.commit()
  return redirect(url_for('index'))

@app.route("/delete/<int:id>")
def delete(id):
  task = Task.query.filter_by(id=id).first()
  db.session.delete(task)
  return redirect(url_for('index'))

db.create_all()
app.run(debug=True)
