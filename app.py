from flask import Flask, flash, render_template, request, redirect, url_for
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

name = "Stefan"
db = SQLAlchemy(app)

class Task(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50))
  description = db.Column(db.Text(), default="No description")
  done = db.Column(db.Boolean)
  due = db.Column(db.String(20), default="Later")

@app.route("/")
def index():
  open_tasks = Task.query.filter_by(done=False)
  done_tasks = Task.query.filter_by(done=True)
  return render_template('tasks.html', name=name, open_tasks=open_tasks, done_tasks=done_tasks)

@app.route("/add", methods=['POST'])
def add():
  name = request.form.get('name')
  description = request.form.get('description')
  due = request.form.get('due')
  new_task = Task(name=name, description=description, due=due, done=False)
  db.session.add(new_task)
  db.session.commit()
  flash('Task added.')
  return redirect(url_for('index'))

@app.route("/update/<int:id>", methods=['POST'])
def update(id):
  task = Task.query.filter_by(id=id).first()
  task.name = request.form.get('name')
  task.description = request.form.get('description')
  task.due = request.form.get('due')
  db.session.commit()
  flash('Task updated.')
  return redirect(url_for('index'))

@app.route("/details/<int:id>")
def details(id):
  task = Task.query.filter_by(id=id).first()
  return render_template('task.html', task=task)

@app.route("/done/<int:id>")
def done(id):
  task = Task.query.filter_by(id=id).first()
  task.done = True
  db.session.commit()
  flash('Task marked as done.')
  return redirect(url_for('index'))

@app.route("/undone/<int:id>")
def undone(id):
  task = Task.query.filter_by(id=id).first()
  task.done = False
  db.session.commit()
  flash('Task marked as open.')
  return redirect(url_for('index'))

@app.route("/delete/<int:id>")
def delete(id):
  task = Task.query.filter_by(id=id).first()
  db.session.delete(task)
  db.session.commit()
  flash('Task deleted')
  return redirect(url_for('index'))

db.create_all()

if __name__ == "__main__":
  app.run(debug=True)
