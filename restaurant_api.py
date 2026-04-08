from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from schemas import (
    CategoryCreate, CategoryOut,
    MenuItemCreate, MenuItemOut, MenuItemDetailOut,
    OrderCreate, OrderOut, OrderDetailOut,
    OrderItemCreate, OrderItemOut, OrderItemUpdate
)
from database import get_db, engine
from models import Category, MenuItem, Order, OrderItem, Base

Base.metadata.create_all(bind=engine)
api_router = APIRouter(prefix='/api/restaurant')

# Endpunkty dlya kategoriy
@api_router.get('/categories', response_model=List[CategoryOut])
def get_categories(db: Session = Depends(get_db)):
    stmt = select(Category)
    categories = db.scalars(stmt).all()
    return categories

@api_router.post('/categories', response_model=CategoryOut)
def create_category(category_in: CategoryCreate, db: Session = Depends(get_db)):
    category = Category(**category_in.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

# Endpunkty dlya elementov menyu
@api_router.get('/menu-items', response_model=List[MenuItemOut])
def get_menu_items(db: Session = Depends(get_db)):
    stmt = select(MenuItem)
    menu_items = db.scalars(stmt).all()
    return menu_items

@api_router.post('/menu-items', response_model=MenuItemOut)
def create_menu_item(menu_item_in: MenuItemCreate, db: Session = Depends(get_db)):
    # Proverka sushchestvovaniya kategorii
    stmt = select(Category).where(Category.id == menu_item_in.category_id)
    category = db.scalar(stmt)
    if not category:
        raise HTTPException(status_code=400, detail="Kategoriya ne naydena")
    
    menu_item = MenuItem(**menu_item_in.model_dump())
    db.add(menu_item)
    db.commit()
    db.refresh(menu_item)
    return menu_item

@api_router.get('/menu-items/{item_id}', response_model=MenuItemDetailOut)
def get_menu_item_detail(item_id: int, db: Session = Depends(get_db)):
    from sqlalchemy.orm import selectinload
    stmt = select(MenuItem).options(selectinload(MenuItem.category)).where(MenuItem.id == item_id)
    menu_item = db.scalar(stmt)
    if not menu_item:
        raise HTTPException(status_code=404, detail="Element menyu ne nayden")
    return menu_item

# Endpunkty dlya elementov zakaza
@api_router.get('/order-items', response_model=List[OrderItemOut])
def get_order_items(db: Session = Depends(get_db)):
    from sqlalchemy.orm import selectinload
    stmt = select(OrderItem).options(selectinload(OrderItem.menu_item))
    order_items = db.scalars(stmt).all()
    return order_items

@api_router.post('/order-items', response_model=OrderItemOut)
def create_order_item(order_item_in: OrderItemCreate, db: Session = Depends(get_db)):
    # Proverka sushchestvovaniya elementa menyu
    stmt = select(MenuItem).where(MenuItem.id == order_item_in.menu_item_id)
    menu_item = db.scalar(stmt)
    if not menu_item:
        raise HTTPException(status_code=400, detail="Element menyu ne nayden")
    
    # Proverka sushchestvovaniya zakaza
    stmt = select(Order).where(Order.id == order_item_in.order_id)
    order = db.scalar(stmt)
    if not order:
        raise HTTPException(status_code=400, detail="Zakaz ne nayden")
    
    order_item = OrderItem(**order_item_in.model_dump())
    db.add(order_item)
    db.commit()
    db.refresh(order_item)
    return order_item

@api_router.put('/order-items/{item_id}', response_model=OrderItemOut)
def update_order_item(item_id: int, order_item_in: OrderItemUpdate, db: Session = Depends(get_db)):
    stmt = select(OrderItem).where(OrderItem.id == item_id)
    order_item = db.scalar(stmt)
    if not order_item:
        raise HTTPException(status_code=404, detail="Element zakaza ne nayden")
    
    order_item.quantity = order_item_in.quantity
    order_item.total = order_item_in.total
    db.add(order_item)
    db.commit()
    db.refresh(order_item)
    return order_item

@api_router.delete('/order-items/{item_id}')
def delete_order_item(item_id: int, db: Session = Depends(get_db)):
    stmt = select(OrderItem).where(OrderItem.id == item_id)
    order_item = db.scalar(stmt)
    if not order_item:
        raise HTTPException(status_code=404, detail="Element zakaza ne nayden")
    
    db.delete(order_item)
    db.commit()
    return {"status": "udalen"}

# Endpunkty dlya zakazov
@api_router.get('/orders', response_model=List[OrderOut])
def get_orders(db: Session = Depends(get_db)):
    stmt = select(Order)
    orders = db.scalars(stmt).all()
    return orders

@api_router.post('/orders', response_model=OrderOut)
def create_order(order_in: OrderCreate, db: Session = Depends(get_db)):
    order = Order(**order_in.model_dump(), total=0.0)
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

@api_router.get('/orders/{order_id}', response_model=OrderDetailOut)
def get_order_detail(order_id: int, db: Session = Depends(get_db)):
    from sqlalchemy.orm import selectinload
    stmt = select(Order).options(selectinload(Order.order_items).selectinload(OrderItem.menu_item)).where(Order.id == order_id)
    order = db.scalar(stmt)
    if not order:
        raise HTTPException(status_code=404, detail="Zakaz ne nayden")
    return order

@api_router.delete('/orders/{order_id}')
def delete_order(order_id: int, db: Session = Depends(get_db)):
    """Udalit' zakaz"""
    stmt = select(Order).where(Order.id == order_id)
    order = db.scalar(stmt)
    if not order:
        raise HTTPException(status_code=404, detail="Zakaz ne nayden")
    
    db.delete(order)
    db.commit()
    return {"status": "udalen"}
