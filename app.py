from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import yaml

app = Flask(__name__)
db_config = yaml.safe_load(open('database.yaml'))
app.config['SQLALCHEMY_DATABASE_URI'] = db_config['uri'] 
db = SQLAlchemy(app)
# CORS(app)

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    age = db.Column(db.String(255))
    
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def __repr__(self):
        return '%s/%s/%s' % (self.id, self.name, self.age)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/data', methods=['POST', 'GET'])
def data():
    
    # POST a data to database
    if request.method == 'POST':
        body = request.json
        name = body['name']
        age = body['age']

        data = User(name, age)
        db.session.add(data)
        db.session.commit()

        return jsonify({
            'status': 'Data is posted to PostgreSQL!',
            'name': name,
            'age': age
        })
    
    # GET all data from database & sort by id
    if request.method == 'GET':
        # data = User.query.all()
        data = User.query.order_by(User.id).all()
        print(data)
        dataJson = []
        for i in range(len(data)):
            # print(str(data[i]).split('/'))
            dataDict = {
                'id': str(data[i]).split('/')[0],
                'name': str(data[i]).split('/')[1],
                'age': str(data[i]).split('/')[2]
            }
            dataJson.append(dataDict)
        return jsonify(dataJson)

@app.route('/data/<string:id>', methods=['GET', 'DELETE', 'PUT'])
def onedata(id):

    # GET a specific data by id
    if request.method == 'GET':
        data = User.query.get(id)
        print(data)
        dataDict = {
            'id': str(data).split('/')[0],
            'name': str(data).split('/')[1],
            'age': str(data).split('/')[2]
        }
        return jsonify(dataDict)
        
    # DELETE a data
    if request.method == 'DELETE':
        delData = User.query.filter_by(id=id).first()
        db.session.delete(delData)
        db.session.commit()
        return jsonify({'status': 'Data '+id+' is deleted from PostgreSQL!'})

    # UPDATE a data by id
    if request.method == 'PUT':
        body = request.json
        newName = body['name']
        newAge = body['age']
        editData = User.query.filter_by(id=id).first()
        editData.name = newName
        editData.age = newAge
        db.session.commit()
        return jsonify({'status': 'Data '+id+' is updated from PostgreSQL!'})

if __name__ == '__main__':

    with app.app_context():
        db.create_all()
    app.debug = True
    # db.create_all()
    app.run()

    
    
    
# from flask import Flask, request, flash, url_for, redirect, render_template
# from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres_user:postgres@172.17.0.2:5432/platformatory_test'
# app.config['SECRET_KEY'] = "random string"

# db = SQLAlchemy(app)

# class students(db.Model):
#    id = db.Column('student_id', db.Integer, primary_key = True)
#    name = db.Column(db.String(100))
#    city = db.Column(db.String(50))
#    addr = db.Column(db.String(200)) 
#    pin = db.Column(db.String(10))

# def __init__(self, name, city, addr,pin):
#    self.name = name
#    self.city = city
#    self.addr = addr
#    self.pin = pin

# @app.route('/')
# def show_all():
#    return render_template('show_all.html', students = students.query.all() )

# @app.route('/new', methods = ['GET', 'POST'])
# def new():
#    if request.method == 'POST':
#       if not request.form['name'] or not request.form['city'] or not request.form['addr']:
#          flash('Please enter all the fields', 'error')
#       else:
#          student = students(request.form['name'], request.form['city'],
#             request.form['addr'], request.form['pin'])
         
#          db.session.add(student)
#          db.session.commit()
#          flash('Record was successfully added')
#          return redirect(url_for('show_all'))
#    return render_template('new.html')

# if __name__ == '__main__':
#    with app.app_context():
#     db.create_all()
#    app.run(debug = True)