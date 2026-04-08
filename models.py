from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Boolean, ForeignKey, SmallInteger, Numeric

# Modeli dlya bazy dannikh restorana
from database import Base

class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(length=100))
    # Svyaz s elementami menyu
    menu_items: Mapped[list['MenuItem']] = relationship(back_populates='category')


class MenuItem(Base):
    __tablename__ = 'menu_items'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(length=100))
    # Cena blyuda
    price: Mapped[float] = mapped_column(Numeric(10, 2))
    # Opisanie blyuda
    description: Mapped[str] = mapped_column(String(length=500))
    # Vneshniy klyuch na kategoriyu
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))

    # Svyaz s kategoriej i elementami zakaza
    category: Mapped[Category] = relationship(back_populates='menu_items')
    order_items: Mapped['OrderItem'] = relationship(back_populates='menu_item')

class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # Adres dostavki
    address: Mapped[str] = mapped_column(String(length=200))
    # Obshhaya summa zakaza
    total: Mapped[float] = mapped_column(Numeric(10, 2))
    # Nomer telefona klienta
    phone_number: Mapped[str] = mapped_column(String(length=20))
    # Status zakaza
    status: Mapped[str] = mapped_column(String(length=50))

    # Svyaz s elementami zakaza
    order_items: Mapped[list['OrderItem']] = relationship(back_populates='order')

class OrderItem(Base):
    __tablename__ = 'order_items'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # Vneshniy klyuch na blyudo v menyu
    menu_item_id: Mapped[int] = mapped_column(ForeignKey('menu_items.id'))
    # Kolichestvo blyud v zakaze
    quantity: Mapped[int] = mapped_column(SmallInteger)
    # Stoimost vseh blyud etogo tipa
    total: Mapped[float] = mapped_column(Numeric(10, 2))
    # Vneshniy klyuch na zakaz
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'))

    # Svyaz s blyudom i zakazom
    menu_item: Mapped[MenuItem] = relationship(back_populates='order_items')
    order: Mapped[Order] = relationship(back_populates='order_items')
    
