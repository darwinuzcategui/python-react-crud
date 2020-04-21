from flask import Flask, jsonify, request
from flask_pymongo import PyMongo,ObjectId
from flask_cors import CORS

app = Flask(__name__)
app.config['MONGO_URI']='mongodb://localhost/pythondb'
mongo = PyMongo(app)
db = mongo.db.users

CORS(app)

@app.route('/users', methods=['POST'])
def crearUser():
    id = db.insert({
        'nombre': request.json['nombre'],
        'email': request.json['email'],
        'clave': request.json['clave']
    })
    return  jsonify(str(ObjectId(id)))

@app.route('/users', methods=['GET'])
def getUsers():
    usuarios =[]
    for doc in db.find():
        usuarios.append({
            "_id": str(ObjectId(doc['_id'])),
            'nombre': doc['nombre'],
            'email': doc['email'], 
            'clave':doc['clave']
        })
    return jsonify(usuarios)

@app.route('/users/<id>', methods=['GET'])
def getUser(id):
  user = db.find_one({'_id': ObjectId(id)})
  print(user)
  return jsonify({
      '_id': str(ObjectId(user['_id'])),
      'nombre': user['nombre'],
      'email': user['email'],
      'clave': user['clave']
  })

@app.route('/users/<id>', methods=['DELETE'])
def eliminarUser(id):
    db.delete_one({'_id':ObjectId(id)})
    print("elimina este usuario con este :"+id)
    return jsonify({'mensaje': 'usuarios eliminado'})

@app.route('/users/<id>', methods=['PUT'])
def actulizarUser(id):
    print("usuario a editar :"+id)
    print(request.json)
    db.update_one({'_id': ObjectId(id)},
    {"$set": {
        'nombre': request.json['nombre'],
        'email': request.json['email'],
        'clave': request.json['clave']
    }})
    return jsonify({'message': 'Usurio Actulizado'})
   
if __name__ == "__main__":
    app.run(debug=True)