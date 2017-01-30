from api.auth.auth import auth
from flask import request, abort, jsonify, g, Blueprint
from api.models import Bucketlist, db, User, Item
from flask_httpauth import HTTPTokenAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature

auth = HTTPTokenAuth(scheme='Bearer')

bucket_view = Blueprint('bucket_view', __name__, url_prefix='/bucketlists')


@auth.verify_token
def verify_auth_token(token):
    if not token:
        return jsonify({"message": "supply token"}), 401
    user_id = User.verify_auth_token(token=token)
    if not user_id:
        return False
    g.user = db.session.query(User).filter_by(id=user_id).first()
    return True


@bucket_view.route("/", methods=["POST"])
@auth.login_required
def add_new_bucketlist():
    name = request.json.get('name')
    description = request.json.get('description')
    if not name or not description:
        return jsonify({'message': 'Please provide a bucketlist name and decription'}), 400
    check_bucket = db.session.query(Bucketlist).filter_by(name=name).first()
    if check_bucket:
        return jsonify({'message': 'Bucketlist exists'})
    bucketlist = Bucketlist(
        name=name, description=description, created_by=g.user.id)
    db.session.add(bucketlist)
    db.session.commit()
    return jsonify({'message': 'Bucketlist created successfully'}), 201


@bucket_view.route("/", methods=["GET"])
@auth.login_required
def get_bucketlists():
    blist = db.session.query(Bucketlist).filter_by(created_by=g.user.id).all()
    if not blist:
        return jsonify({'message': 'Currently you have no bucketlists'})
    list_bucketlist = []
    for row in blist:
        list_bucketlist.append(row.print_data())
    return jsonify(list_bucketlist), 200


@bucket_view.route("/<id>", methods=["GET"])
@auth.login_required
def get_bucketlist(id):
    result = db.session.query(Bucketlist).filter_by(
        id=id, created_by=g.user.id).first()
    if not result:
        return jsonify({'message': 'Please enter your bucketlist id'}), 400
    return jsonify(result.print_data()), 200


@bucket_view.route("/<id>", methods=["PUT"])
@auth.login_required
def update_bucketlist(id):
    name = request.json.get("name")
    description = request.json.get("description")
    if not name and not description:
        return jsonify({"message": "You need to supply something to modify"})
    bl = db.session.query(Bucketlist).filter_by(
        id=id, created_by=g.user.id).first()

    if not bl:
        return jsonify({"message": "Invalid bucketlist, might exist but doesn't belong to users"})
    if name or description:
        if bl.name == name:
            if bl.description == description:
                return jsonify({"message": "You have entered the same values, nothing to update"})
            else:
                bl.description = description
                db.session.add(bl)
                db.session.commit()
                return jsonify({'message': 'Decription updated!'}), 200
        else:
            if bl.description == description:
                bl.name = name
                db.session.add(bl)
                db.session.commit()
                return jsonify({'message': 'Name updated'}), 200
            else:
                bl.name = name
                bl.decription = description
                db.session.add(bl)
                db.session.commit()
                return jsonify({"message": "Updated"}), 200


@bucket_view.route("/<id>", methods=["DELETE"])
@auth.login_required
def delete_bucketlist(id):
    b = db.session.query(Bucketlist).filter_by(
        id=id, created_by=g.user.id).first()
    if b is None:
        return jsonify({'message': 'The bucketlist does not exist'})
    db.session.delete(b)
    db.session.commit()
    return jsonify({'message': 'Bucketlist deleted!'}), 204


@bucket_view.route("/<id>/items/", methods=["POST"])
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

    item = Item(name=name, bucketlist_id=id)
    db.session.add(item)
    db.session.commit()

    return jsonify({'message': 'Item added successfully'})


@bucket_view.route("/<id>/<items>/<item_id>", methods=["PUT"])
@auth.login_required
def update_item(id, items, item_id):
    bucket_list = db.session.query(Bucketlist).filter_by(
        id=id, created_by=g.user.id)
    if not bucket_list:
        return jsonify({'messsage': 'Please Enter Your Bucketlist id in url'})

    name = request.json.get("name")
    done = request.json.get("done")
    
    if not name and not done:
        return jsonify({"message": "You need to supply something to modify"})

    bl_item = db.session.query(Item).filter_by(
        id=id, bucketlist_id=id).first()

    if not bl_item:
        return jsonify({"message": "Invalid Item Id"})
    if name or done:
        if bl_item.name == name:
            if bl_item.done == done:
                return jsonify({"message": "Same values entered"})
            else:
                db.session.add(bl_item)
                db.session.commit()
                return jsonify({'message': 'Item Status updated!'})
        else:
            if bl_item.done == done:
                bl_item.name = name
                db.session.add(bl_item)
                db.session.commit()
                return jsonify({'message': 'Item Name updated'})
            else:
                bl_item.name = name
                bl_item.done = done
                db.session.add(bl_item)
                db.session.commit()
                return jsonify({"message": "Item Updated"})


@bucket_view.route("/<id>/items/<item_id>", methods=["DELETE"])
@auth.login_required
def delete_item(id, item_id):
    bucket_list = db.session.query(Bucketlist).filter_by(
        id=id, created_by=g.user.id)
    if not bucket_list:
        return jsonify({'messsage': 'Please Enter Your Bucketlist id in url'})
    item = db.session.query(Item).filter_by(
        id=item_id, bucketlist_id=id).first()
    if not item:
        return jsonify({'message': 'Item does not exist'})

    db.session.delete(item)
    db.session.commit()

    return jsonify({'message': 'Item Deleted'}), 200
