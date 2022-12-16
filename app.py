from flask import Flask, render_template, flash, redirect, render_template, request, jsonify
from models import db, connect_db, Cupcake
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config["SECRET_KEY"] = "oh-so-secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///cupcakes"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

connect_db(app)

@app.route('/')
def homepage():
    """Return JSON for homepage"""

    return render_template('index.html')

    
@app.route('/api/cupcakes')
def list_cupcakes():
    """Returns JSON w/ all cupcakes"""
    all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=all_cupcakes)



@app.route('/api/cupcakes/<int:id>')
def get_cupcake(id):
    """Returns JSON for one cupcake in particular"""
    cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake=cupcake.serialize())




@app.route('/api/cupcakes', methods = ['POST'])
def post_cupcake():
    """Return JSON for adding a new cupcake"""

    data = request.json
    cupcake = Cupcake(
        flavor = data['flavor'],
        rating = data['rating'],
        size = data['size'],
        image = data['image'] or None
    )

    db.session.add(cupcake)
    db.session.commit()

    return(jsonify(cupcake = cupcake.serialize()),201)



@app.route('/api/cupcakes/<int:id>',methods = ['PATCH'])

def patch_cupcake(id):
    """Return JSON for editing a cupcake"""
    data = request.json

    cupcake = Cupcake.query.get_or_404(id)

    cupcake.flavor = data['flavor']
    cupcake.rating = data['rating']
    cupcake.size = data['size']
    cupcake.image = data['image']

    db.session.add(cupcake)
    db.session.commit()

    return jsonify(cupcake=cupcake.serialize())



@app.route('/api/cupcakes/<int:id>', methods = ['DELETE'])

def delete_cupcake(id):
    """Return JSON for removing a cupcake"""
    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message = 'Cupcake Deleted')

    

