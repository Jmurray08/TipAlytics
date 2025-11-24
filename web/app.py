from flask import Flask, render_template, request
from waitress import serve

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return "This is the TipAlytics web app"

@app.route('/log-shift', methods=['GET'])
def log_shift_form():
    return render_template('log_shift.html')

@app.route('/log-shift', methods=['POST'])
def log_shift_submit():
    #Shift Details
    shift_date = request.form.get('date')
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

    return f"""
        Shift recieved: <br>
        Date: {shift_date} <br>
        Shift Type: {shift_type} <br>
        In: {in_time} Out: {out_time} <br>

        Weather: {low_temp} / {high_temp} ({conditions}) <br><br>

        Tips: {amount} <br> | Spent: {spent}
    """



if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8000)