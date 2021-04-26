from enum import Enum, auto

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flask-user:<password>@localhost/lab6flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class OriginCountry(Enum):
    UKRAINE = auto()
    GERMANY = auto()
    USA = auto()
    CHINA = auto()
    SPAIN = auto()
    FRANCE = auto()


class DeviceType(Enum):
    MECHANICS = auto()
    ELECTRICITY_AND_MAGNETISM = auto()
    MOLECULAR_PHYSICS_AND_THERMODYNAMICS = auto()
    OPTICS = auto()


class Equipment(Enum):
    FOR_DEMONSTRATION = auto()
    FOR_LABORATORY = auto()


class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    origin_country: OriginCountry = db.Column(db.Enum(OriginCountry), nullable=False)
    price: float = db.Column(db.Float(10), nullable=False)
    weight_in_grams: float = db.Column(db.Float(10), nullable=True)
    material: str = db.Column(db.String(20), nullable=False)
    category: Equipment = db.Column(db.Enum(Equipment), nullable=False)
    type: DeviceType = db.Column(db.Enum(DeviceType), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '<Loom %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def post():
    if request.method == 'POST':
        origin_country = request.form['origin_country']
        price = request.form['price']
        weight_in_grams = request.form['weight_in_grams']
        material = request.form['material']
        category = request.form['category']
        type = request.form['type']
        new_device = Device(origin_country=origin_country,
                            price=price,
                            weight_in_grams=weight_in_grams,
                            material=material,
                            category=category,
                            type=type)

        try:
            db.session.add(new_device)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your device'

    else:
        devices = Device.query.order_by(Device.date_created).all()
        return render_template('index.html', devices=devices)


@app.route('/delete/<int:id>')
def delete(id):
    device_to_delete = Device.query.get_or_404(id)

    try:
        db.session.delete(device_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting a that device'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    device = Device.query.get_or_404(id)

    if request.method == 'POST':
        device.origin_country = request.form['origin_country']
        device.price = request.form['price']
        device.weight_in_grams = request.form['weight_in_grams']
        device.material = request.form['material']
        device.category = request.form['category']
        device.type = request.form['type']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your device'

    else:
        return render_template('update.html', device=device)


if __name__ == '__main__':
    app.run(debug=True)
