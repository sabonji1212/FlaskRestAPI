from flask import Flask ,request 
from flask_smorest import abort
import uuid
from db import stores,items
app = Flask(__name__)


@app.get('/store')
def get_stores():
    return {'stores': list(stores.values())}

@app.post('/store')
def create_store():
    store_data = request.get_json()
    if "name" not in store_data:
        abort(400, message="Bad request. Ensure 'name' is included in the request body.")
    for store in stores.values():
        if store["name"] == store_data["name"]:
            abort(400, message=f"A store with name '{store_data['name']}' already exists.")
            
    store_id = uuid.uuid4().hex
    store = { **store_data, 'id': store_id }
    stores[store_id] = store
    return store , 201
#price , name , store_id
@app.post('/item')
def create_item_in_store(name):
    item_data = request.get_json() 

    if ("price " not in item_data or "name" not in item_data or "store_id" not in item_data):
        abort(400, message="Bad request. Ensure 'price', 'name' and 'store_id' are included in the request body.")
    for itemt in items.values():
        if (itemt["name"] == item_data["name"] or itemt["store_id"] == item_data["store_id"]):
            abort(400, message=f"An item with name '{item_data['name']}' already exists.")

    if item_data["store_id"] not in stores:
        abort(404, message="store not found")
    
    item_id = uuid.uuid4().hex
    item = { **item_data, 'id': item_id }
    items[item_id] = item
    
    return item , 201


@app.get('/item')
def get_all_items():
    return {'items': list(items.values())} 

@app.get('/store/<string:store_id>')
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
            abort(404, message="store not found")


@app.get('/item/<string:item_id>')
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:    
            abort(404, message="item not found")
    