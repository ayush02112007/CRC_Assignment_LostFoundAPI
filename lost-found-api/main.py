from fastapi import FastAPI, HTTPException
from sqlmodel import Session, select

from database import engine, create_db_and_tables
from models import Item, ItemStatus


app = FastAPI(
    title="College Lost & Found API",
    description="API for managing lost and found items on campus",
    version="1.0.0"
)


# Create database tables when application starts
@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# 1. POST /items
@app.post("/items", response_model=Item, status_code=201)
def create_item(item: Item):
    with Session(engine) as session:
        session.add(item)
        session.commit()
        session.refresh(item)
        return item


# 2. GET /items
@app.get("/items", response_model=list[Item])
def get_items():
    with Session(engine) as session:
        items = session.exec(select(Item)).all()
        return items


# 3. GET /items/{item_id}
@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    with Session(engine) as session:
        item = session.get(Item, item_id)

        if item is None:
            raise HTTPException(
                status_code=404,
                detail="Item not found"
            )

        return item


# 4. PUT /items/{item_id}
@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, updated_item: Item):
    with Session(engine) as session:
        item = session.get(Item, item_id)

        if item is None:
            raise HTTPException(
                status_code=404,
                detail="Item not found"
            )

        item.title = updated_item.title
        item.description = updated_item.description
        item.category = updated_item.category
        item.location = updated_item.location
        item.reported_by = updated_item.reported_by
        item.status = updated_item.status

        session.add(item)
        session.commit()
        session.refresh(item)

        return item


# 5. DELETE /items/{item_id}
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    with Session(engine) as session:
        item = session.get(Item, item_id)

        if item is None:
            raise HTTPException(
                status_code=404,
                detail="Item not found"
            )

        session.delete(item)
        session.commit()

        return {
            "message": "Item deleted successfully"
        }


# 6. GET /items/status/{status}
@app.get("/items/status/{status}", response_model=list[Item])
def get_items_by_status(status: ItemStatus):
    with Session(engine) as session:
        statement = select(Item).where(Item.status == status)
        items = session.exec(statement).all()

        return items


# 7. GET /items/category/{category}
@app.get("/items/category/{category}", response_model=list[Item])
def get_items_by_category(category: str):
    with Session(engine) as session:
        statement = select(Item).where(Item.category == category)
        items = session.exec(statement).all()

        return items