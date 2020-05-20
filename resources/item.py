from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel


class Item(Resource):
    # 
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help='This field cannot be left blank!'
    )
    parser.add_argument(
        'store_id',
        type=int,
        required=True,
        help='Every item needs a store id.'
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            return item.json()
        return {'message': f'item {name} not found'}, 404

    def post(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            print(item)
            return {'message': f'item {name} already exists'}, 400

        request_data = self.parser.parse_args()
        new_item = ItemModel(name, **request_data)

        try:
            new_item.save_to_db()
        except:
            return {"message": "An error occurred inserting an item"}, 500

        return {
                   'message': 'item created successfully',
                   'item': ItemModel.find_by_name(name).json()
               }, 201

    def put(self, name):
        request_data = self.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **request_data)
        else:
            item.price = request_data['price']
            item.store_id = request_data['store_id']

        item.save_to_db()
        return ItemModel.find_by_name(name).json()

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
