from fastapi import FastAPI 
from pydantic import BaseModel


app=FastAPI()

#temporary in-memory storage for items
items_db={}

#Models
class Item(BaseModel):
    item_id:str
    name:str
    price:float
    quantity:int
    
class Order(BaseModel):
    item_id:str
    quantity:int
    
#CRUD Routes for item manipulation
@app.post("/items")
def create_item(item:Item):
    item_id=item.item_id
    if item_id in items_db:
        return {"error":"Item ID already exists"}
    items_db[item_id]=item
    return item

@app.get("/items/{item_id}")
def read_item(item_id:str):
    if item_id in items_db:
        return items_db[item_id]
    return {"error":"Item not found!"}

@app.put("/items/{item_id}")
def update_item(item_id:str,item:Item):
    if item_id in items_db:
        items_db[item_id]=item
        return item
    return {"error":"Item not found!"}

@app.delete("/items/{item_id}")
def delete_item(item_id:str):
    if item_id in items_db:
        del items_db[item_id]
        return {"message":"Item Deleted!"}
    return {"error":"Item not found!"}

#Managing inventory
@app.post("/manage_inventory")
def manage_inventory(orders:list[Order]):
    for order in orders:
        item_id=order.item_id
        quantity=order.quantity
        
        if item_id in items_db:
            item=items_db[item_id]
            if item.quantity>=quantity:
                item.quantity-=quantity
            else:
                return {"error":"Insufficient quantity for item: {item_id}"}
        else:
            return {"error":f"No such item with id:{item_id}!"}
    return {"message":"Inventory managed successfully"}

if __name__=="__main__":
    import uvicorn
    
    uvicorn.run(app,host="0.0.0.0",port=8000)