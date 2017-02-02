from api.auth.auth import auth
from flask import request, jsonify, g, Blueprint, url_for
from api.models import Bucketlist, db, User, Item


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

    if not name and not description:
        return jsonify({"message": "Enter name or description"}), 400

    check_bucket = db.session.query(Bucketlist).filter_by(name=name).first()
    if check_bucket:
        return jsonify({'message': 'Bucketlist exists'}), 400

    if name and description:

        bucketlist = Bucketlist(
            name=name, description=description, created_by=g.user.id)
        db.session.add(bucketlist)
        db.session.commit()
    else:
        bucketlist = Bucketlist(
            name=name, created_by=g.user.id)
        db.session.add(bucketlist)
        db.session.commit()

    return jsonify({'message': 'Bucketlist created successfully'}), 201


@bucket_view.route("/", methods=["GET"])
@auth.login_required
def get_bucketlists():
    page = int(request.args.get('page', 1))
    limit = min(int(request.args.get('limit', 20)), 20)
    search = request.args.get('q', '')

    bucketlist = Bucketlist.query.filter_by(
        created_by=g.user.id).filter(
        Bucketlist.name.like('%{}%'.format(search))).paginate(
        page=page, per_page=limit)

    if not bucketlist.items:
        return jsonify({'message': 'Bucketlist does not exist'}), 404

    list_bucketlist = []
    for bucket in bucketlist.items:
        list_bucketlist.append(bucket.return_data())

    return jsonify({
        'Bucketlist': list_bucketlist,
        'next': url_for(
            request.endpoint, page=bucketlist.next_num, limit=limit,
            _external=True) if bucketlist.has_next else None,
        'prev': url_for(
            request.endpoint, page=bucketlist.prev_num, limit=limit,
            _external=True) if bucketlist.has_prev else None,
    }), 200


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
    bucket = db.session.query(Bucketlist).filter_by(
        id=id, created_by=g.user.id).first()

    if not bucket:
        return jsonify({"message": "Invalid bucketlist, might exist but doesn't belong to users"})
    if name or description:
        if bucket.name == name:
            if bucket.description == description:
                return jsonify({"message": "You have entered the same values, nothing to update"})
            else:
                bucket.description = description
                db.session.add(bucket)
                db.session.commit()
                return jsonify({'message': 'Decription updated!'}), 200
        else:
            if bucket.description == description:
                bucket.name = name
                db.session.add(bucket)
                db.session.commit()
                return jsonify({'message': 'Name updated'}), 200
            else:
                bucket.name = name
                bucket.decription = description
                db.session.add(bucket)
                db.session.commit()
                return jsonify({"message": "Updated"}), 200


@bucket_view.route("/<id>", methods=["DELETE"])
@auth.login_required
def delete_bucketlist(id):
    bucket = db.session.query(Bucketlist).filter_by(
        id=id, created_by=g.user.id).first()
    if bucket is None:
        return jsonify({'message': 'The bucketlist does not exist'})
    db.session.delete(bucket)
    db.session.commit()
    return jsonify({'message': 'Bucketlist deleted!'}), 200


@bucket_view.route("/<id>/items/", methods=["POST"])
@auth.login_required
def add_item(id):
    name = request.json.get('name')

    if name is None:
        return jsonify({'message': 'please provide item name'})
    bucket = db.session.query(Bucketlist).filter_by(
        id=id, created_by=g.user.id)
    if bucket is None:
        return jsonify({'message': 'Bucketlist does not exist'})
    item = db.session.query(Item).filter_by(bucketlist_id=id,
                                            name=name).first()
    if item:
        return jsonify({'message': 'Item exists'})

    item = Item(name=name, bucketlist_id=id)
    db.session.add(item)
    db.session.commit()

    return jsonify({'message': 'Item added successfully'}), 201


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

    bucket_item = db.session.query(Item).filter_by(
        id=id, bucketlist_id=id).first()

    if not bucket_item:
        return jsonify({"message": "Invalid Item Id"})
    if name or done:
        if bucket_item.name == name:
            if bucket_item.done == done:
                return jsonify({"message": "Same values entered"})
            else:
                db.session.add(bucket_item)
                db.session.commit()
                return jsonify({'message': 'Item Status updated!'}), 200
        else:
            if bucket_item.done == done:
                bucket_item.name = name
                db.session.add(bucket_item)
                db.session.commit()
                return jsonify({'message': 'Item Name updated'}), 200
            else:
                bucket_item.name = name
                bucket_item.done = done
                db.session.add(bucket_item)
                db.session.commit()
                return jsonify({"message": "Item Updated"}), 200


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
