from crypt import methods
from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from sqlalchemy import desc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(300), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.cli.command("init-db")
def init_db():
    db.create_all()
    print("Database tables created successfully.")

@app.route('/',methods=['GET','POST'])
def to_do_interface():
    if request.method == 'POST':
        title = (request.form['title'])
        desc = (request.form['desc'])
        todo = Todo(title=title, desc=desc)                         # type: ignore
        db.session.add(todo)
        db.session.commit()
        
    alltodo = Todo.query.all()
    return render_template('index.html', alltodo=alltodo)

@app.route('/update/<int:sno>', methods=['GET','POST'])             # type: ignore
def update_todo(sno):
    if request.method == 'POST':
        title = (request.form['title'])
        desc = (request.form['desc'])
        todo = Todo.query.filter_by(sno=sno).first()                        # type: ignore
        todo.title = title                                          # type: ignore
        todo.desc = desc                                            # type: ignore 
        db.session.add(todo)
        db.session.commit()
        return redirect('/')    
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)
        
@app.route('/delete/<int:sno>')                                     # type: ignore
def delete_todo(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)