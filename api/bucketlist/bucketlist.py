#from api.auth import auth
from api.auth.auth import auth
from api import app
from flask import request, abort, jsonify, g
from api.models import Bucketlist, db, User, Item
from flask_httpauth import HTTPTokenAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature

auth = HTTPTokenAuth(scheme='Bearer')

db.create_all()


@auth.verify_token
def verify_auth_token(token):
    if not token:
        return jsonify({"message": "supply token"}), 401
    user_id = User.verify_auth_token(token=token)
    if not token:
        return False
    g.user = db.session.query(User).filter_by(id=user_id).first()
    return True


@app.route("/bucketlists/", methods=["POST"])
@auth.login_required
def add_new_bucketlist():
    name = request.json.get('name')
    description = request.json.get('description')
    if not name or not description:
        return jsonify({'message': 'Please provide a bucketlist name and decription'})
    bucketlist = Bucketlist(
        name=name, description=description, created_by=g.user.id)
    db.session.add(bucketlist)
    db.session.commit()
    return jsonify({'message': 'Bucketlist created successfully'})


@app.route("/bucketlists/", methods=["GET"])
@auth.login_required
def get_bucketlists():
    blist = db.session.query(Bucketlist).filter_by(created_by=g.user.id).all()
    list_bucketlist = []
    for row in blist:
        list_bucketlist.append(row.print_data())
    return jsonify(list_bucketlist), 200


@app.route("/bucketlists/<id>", methods=["GET"])
@auth.login_required
def get_bucketlist(id):
    result = db.session.query(Bucketlist).filter_by(id=id).first()
    return jsonify(result.print_data())


@app.route("/bucketlists/<id>", methods=["PUT"])
@auth.login_required
def update_bucketlist(id):
    name = request.json.get('name')
    description = request.json.get('description')
    if name is None or description is None:
        return jsonify({'message': 'Enter a name and the description'})
    b = db.session.query(Bucketlist).filter_by(
        id=id, created_by=g.user.id).first()
    if b is None:
        return jsonify({'message': 'The bucketlist does not exist'})
    b.name = name
    b.description = description
    db.session.commit()
    return jsonify({'message': 'Bucketlist updated!'})


@app.route("/bucketlists/<id>", methods=["DELETE"])
@auth.login_required
def delete_bucketlist(id):
    b = db.session.query(Bucketlist).filter_by(id=id, created_by=g.user.id).first()
    if b is None:
        return jsonify({'message': 'The bucketlist does not exist'})
    db.session.delete(b)
    db.session.commit()
    return jsonify({'message': 'Bucketlist deleted!'})


@app.route("/bucketlists/<id>/items/", methods=["POST"])
@auth.login_required
def add_item(id):
    name = request.json.get('name')

    if name is None:
        return jsonify({'message': 'please provide item name'})
    b = db.session.query(Bucketlist).filter_by(
        id=id, created_by=g.user.id)
    if b is None:
        return jsonify({'message': 'Bucketlist does not exist'})
    item = db.session.query(Item).filter_by(bucketlist_id=id,
                                  name=name).first()
    if item:
        return jsonify({'message': 'Item exists'})

    item = Item(name=name, bucketlist_id=id )
    db.session.add(item)
    db.session.commit()

    return jsonify({'message': 'Item added successfully'})


@app.route("/bucketlists/<id>/<items>/<item_id>", methods=["PUT"])
@auth.login_required
def update_item(id, items, item_id):

    done = request.json.get('done')
    name = request.json.get('name')
    if done is None or name is None:
        return jsonify({'message': 'Please enter item status and name'})

    b = db.session.query(Bucketlist).filter_by(
        id=id, created_by=g.user.id).first()
    if b is None:
        return jsonify({'message': 'Bucketlist does not exist'})

    item = db.session.query(Item).filter_by(id=item_id).first()
    if item is None:
        return jsonify({'message': 'Item does not exist'})

    Item.name = name
    Item.done = done

    db.session.commit()

    return jsonify({'message': 'Item updated Successsfully'})


@app.route("/bucketlists/<id>/items/<item_id>", methods=["DELETE"])
@auth.login_required
def delete_item(id, item_id):

    # b = db.session.query(Bucketlist).filter_by(
    #     id=id, created_by=g.user.id).first()
    # if not b:
    #     return jsonify({'message': 'Bucketlist does not exist'})

    item = db.session.query(Item).filter_by(id=item_id, bucketlist_id=id).first()
    if not item:
        return jsonify({'message': 'Item does not exist'})

    db.session.delete(item)
    db.session.commit()

    return jsonify({'message': 'Item Deleted'}), 200
