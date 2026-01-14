from flask import Flask, render_template, request
from waitress import serve
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:BrodyAussie2020@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db=SQLAlchemy(app)

class Shift(db.Model):
    __tablename__ = "shift"

    id = db.Column(db.Integer, primary_key=True)
    shift_date = db.Column(db.String(10))
    shift_type = db.Column(db.String(10))
    in_time = db.Column(db.String(10))
    out_time = db.Column(db.String(10))

    weather = db.relationship('Weather', backref='shift', uselist=False)
    tips = db.relationship('Tips', backref='shift', uselist=False)

class Weather(db.Model):
    __tablename__ = "weather"

    id = db.Column(db.Integer, primary_key=True)
    low_temp = db.Column(db.Integer)
    high_temp = db.Column(db.Integer)
    condition = db.Column(db.String(10))

    shift_id = db.Column(db.Integer, db.ForeignKey('shift.id'), nullable=False)

class Tips(db.Model):
    __tablename__ = "tips"

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer)
    spent = db.Column(db.Float)

    shift_id = db.Column(db.Integer, db.ForeignKey('shift.id'), nullable=False)

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/view-shifts')
def view_shifts():
    return render_template('view-shifts.html')

@app.route('/analytics')
def analytics():
    return render_template('analytics.html')

@app.route('/log-shift', methods=['GET'])
def log_shift_form():
    return render_template('log_shift.html')

@app.route('/log-shift', methods=['POST'])
def log_shift_submit():
    #Shift Details
    shift_date = request.form.get('shift_date')
    shift_type = request.form.get('shift_type')
    in_time = request.form.get('in_time')
    out_time = request.form.get('out_time')

    #Weather
    low_temp = request.form.get('low_temp')
    high_temp = request.form.get('high_temp')
    conditions = request.form.get('conditions')

    #Tips
    amount = request.form.get('amount')
    spent = request.form.get('spent')

    shift_date_obj = datetime.strptime(shift_date, "%Y-%m-%d").date()
    in_time_obj = datetime.strptime(in_time, "%H:%M").time()
    out_time_obj = datetime.strptime(out_time, "%H:%M").time()

    new_shift = Shift(
        shift_date=shift_date_obj,
        shift_type=shift_type,
        in_time=in_time_obj,
        out_time=out_time_obj
    )

    new_weather = Weather(
        low_temp=low_temp,
        high_temp=high_temp,
        condition=conditions,
        shift=new_shift
    )

    new_tips = Tips(
        amount=amount,
        spent=spent,
        shift=new_shift
    )
    db.session.add_all([new_shift, new_weather, new_tips])
    db.session.commit()

    return render_template('form_success.html')

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8000)