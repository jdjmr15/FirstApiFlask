import uuid
from typing import Dict, Any
from db import stores, items

from flask_smorest import abort
from flask import Flask, request


app = Flask(__name__)


@app.get("/store")
def get_stores():
    return {"stores": list(stores.values())}, 200


@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(404, message="Store not found.!!")


@app.get("/item")
def get_all_items():
    return {"stores": list(items.values())}, 200


@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(404, message="Item not found.!!")


@app.delete("/item/<string:item_id>")
def delete_item(item_id):
    try:
        del items[item_id]
        return {"message": "Item deleted"}
    except KeyError:
        abort(404, message="Item not found.!!")


@app.post("/store")
def create_store():
    store_data: Dict[str, Any] = request.get_json()
    store_id = uuid.uuid4().hex
    store = {**store_data, "id": store_id}
    stores[store_id] = store
    return store, 201


@app.post("/item")
def create_item():
    item_data: Dict[str, Any] = request.get_json()
    if item_data["store_id"] not in stores:
        abort(404, message="Store not found.!!")

    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    items[item_id] = item

    return item, 201
