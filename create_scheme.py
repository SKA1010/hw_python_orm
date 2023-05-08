import sqlalchemy
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
Base = declarative_base()

class Publisher(Base):
    __tablename__ = "publisher"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=60), unique=True)

    book_publ = relationship("Book", back_populates="publ_book")

    def __str__(self):
        return f'{self.id}: {self.name}'


class Book(Base):
    __tablename__ = "book"
    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=60), unique=True)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable=False)
    
    publ_book = relationship(Publisher, back_populates="book_publ")
    stock_book = relationship("Stock", back_populates="book_stock")

class Stock(Base):
    __tablename__ = "stock"
    id = sq.Column(sq.Integer, primary_key=True)
    count = sq.Column(sq.Integer, nullable=False)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable=False)

    book_stock = relationship("Book", back_populates="stock_book")
    shop_stock = relationship("Shop", back_populates="stock_shop")
    sale_stock = relationship("Sale", back_populates="stock_sale")

class Shop(Base):
    __tablename__ = "shop"
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=60), unique=True)

    stock_shop = relationship("Stock", back_populates="shop_stock")

    def __str__(self):
        return f'{self.id}: {self.name}'

class Sale(Base):
    __tablename__ = "sale"
    id = sq.Column(sq.Integer, primary_key=True)
    count = sq.Column(sq.Integer, nullable=False)
    price = sq.Column(sq.Float, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id"), nullable=False)

    stock_sale = relationship("Stock", back_populates="sale_stock")


def create_tables(engine):
#    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

DSN = "postgresql://postgres:123@localhost:5432/book_shop"
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

publ = input("Введите имя или id писателя: ")
if publ.isnumeric():
    for i in session.query(Shop.name).join(Stock.shop_stock).join(Stock.book_stock).join(Book.publ_book).filter(Publisher.id == int(publ)).all():
            print(i)
else:
    for i in session.query(Shop.name).join(Stock.shop_stock).join(Stock.book_stock).join(Book.publ_book).filter(Publisher.name == str(publ)).all():
        print(i)

session.close()