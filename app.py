from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# SQLite Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pcos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Table
class Prediction(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))

    age = db.Column(db.Integer)

    weight = db.Column(db.Float)

    height = db.Column(db.Float)

    cycle = db.Column(db.Integer)

    hair_growth = db.Column(db.Integer)

    skin_darkening = db.Column(db.Integer)

    bmi = db.Column(db.Float)

    result = db.Column(db.String(50))

# Home Page
@app.route('/')
def home():
    return render_template('index.html')

# Prediction Page
@app.route('/prediction', methods=['GET', 'POST'])
def prediction():

    if request.method == 'POST':

        name = request.form['name']

        age = int(request.form['age'])

        weight = float(request.form['weight'])

        height = float(request.form['height'])

        height_m = height / 100

        bmi = weight / (height_m ** 2)  

        cycle = int(request.form['cycle'])

        hair_growth = int(request.form['hair_growth'])

        skin_darkening = int(request.form['skin_darkening'])

        # BASIC RISK CALCULATION

        score = 0

        if cycle > 35:
            score += 1

        if hair_growth > 5:
            score += 1

        if skin_darkening > 5:
            score += 1

        if weight > 70:
            score += 1


        if bmi < 18.5:
             bmi_category = "Underweight"

        elif bmi < 25:
            bmi_category = "Normal Weight"

        elif bmi < 30:
            bmi_category = "Overweight"

        else:
            bmi_category = "Obese"

        # FINAL RESULT

        if score >= 2:
            result = "High Risk of PCOS"
        else:
            result = "Low Risk of PCOS"
        
        # SAVE TO DATABASE

        new_data = Prediction(

            name=name,

            age=age,

            weight=weight,

            height=height,

            cycle=cycle,

            hair_growth=hair_growth,

            skin_darkening=skin_darkening,

            bmi=bmi,
            
            result=result
        )

        db.session.add(new_data)

        db.session.commit()

        return render_template(
            'result.html',
            result=result,
             bmi=round(bmi,2),
             bmi_category=bmi_category
        )

    return render_template('prediction.html')

# Dashboard
@app.route('/dashboard')
def dashboard():

    data = Prediction.query.all()

    total_patients = len(data)

    high_risk = len(
        [x for x in data if x.result == "High Risk of PCOS"]
    )

    low_risk = len(
        [x for x in data if x.result == "Low Risk of PCOS"]
    )

    if total_patients > 0:

        average_bmi = round(
            sum(x.bmi for x in data) / total_patients,
            2
        )

    else:
        average_bmi = 0

    return render_template(
        'dashboard.html',
        data=data,
        total_patients=total_patients,
        high_risk=high_risk,
        low_risk=low_risk,
        average_bmi=average_bmi
    )

# Awareness
@app.route('/awareness')
def awareness():
    return render_template('awareness.html')

if __name__ == '__main__':

    with app.app_context():
        db.create_all()

    app.run(debug=True)