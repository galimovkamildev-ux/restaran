from pydantic import BaseModel, Field
from typing import List

# Skhemy dlya kategoriy
class CategoryBase(BaseModel):
    name: str = Field(max_length=100)

class CategoryCreate(CategoryBase):
    pass

class CategoryOut(CategoryBase):
    id: int

# Skhemy dlya elementov menyu
class MenuItemBase(BaseModel):
    name: str = Field(max_length=100)
    price: float = Field(ge=0)
    description: str = Field(max_length=500)
    category_id: int

class MenuItemCreate(MenuItemBase):
    pass

class MenuItemOut(MenuItemBase):
    id: int

class MenuItemDetailOut(MenuItemOut):
    category: CategoryOut

# Skhemy dlya zakazov
class OrderBase(BaseModel):
    address: str = Field(max_length=200)
    phone_number: str = Field(max_length=20)
    status: str = Field(max_length=50)

class OrderCreate(OrderBase):
    pass

class OrderOut(OrderBase):
    id: int
    total: float

class OrderDetailOut(OrderOut):
    order_items: List['OrderItemOut'] = []

# Skhemy dlya elementov zakaza
class OrderItemBase(BaseModel):
    menu_item_id: int
    quantity: int = Field(ge=1)
    total: float = Field(ge=0)
    order_id: int

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemOut(OrderItemBase):
    id: int
    menu_item: MenuItemOut

class OrderItemUpdate(BaseModel):
    quantity: int = Field(ge=1)
    total: float = Field(ge=0)
