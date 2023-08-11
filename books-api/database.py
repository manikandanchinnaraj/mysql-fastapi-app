import os

from sqlalchemy.orm import registry, relationship, Session

from sqlalchemy import Column, String, Integer, create_engine, ForeignKey, select

engine = create_engine(
    url=f"mysql+mysqlconnector://root:test123@{os.getenv('DB_HOST')}:3306/books",
    echo=True
)

mapper_registry = registry()

Base = mapper_registry.generate_base()


class Author(Base):
    __tablename__ = 'authors'
    author_id = Column(Integer, primary_key=True)
    first_name = Column(String(length=50))
    last_name = Column(String(length=50))

    def __repr__(self):
        return f"<Author(author_id={self.author_id}, first_name={self.first_name}, last_name={self.last_name})>"


class Book(Base):
    __tablename__ = 'books'

    book_id = Column(Integer, primary_key=True)
    title = Column(String(length=255))
    number_of_pages = Column(Integer)

    def __repr__(self):
        return f"<Book(book_id={self.book_id},title={self.title}, number_of_pages={self.number_of_pages})>"


class BookAuthor(Base):
    __tablename__ = "bookauthors"

    bookauthor_id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('authors.author_id'))
    book_id = Column(Integer, ForeignKey('books.book_id'))

    author = relationship(Author)
    book = relationship(Book)

    def __repr__(self):
        return f"<BookAuthor(bookauthor_id={self.bookauthor_id}, author_id={self.author_id}, book_id={self.book_id})>"


Base.metadata.create_all(engine)


def add_book(book: Book, author: Author):
    with Session(engine) as session:

        existing_book = session.execute(
            select(Book).filter(Book.title == book.title,
                                Book.number_of_pages == book.number_of_pages)).scalar()
        if existing_book is not None:
            print("Book has already been added.")
            return
        print("Book does not exist. Adding book")
        session.add(book)

        existing_author = session.execute(
            select(Author).filter(Author.first_name == author.first_name,
                                  Author.last_name == author.last_name)).scalar()
        if existing_author is not None:
            print("Author exists! Adding book")
            session.flush()
            pairing = BookAuthor(author_id=existing_author.author_id, book_id=book.book_id)
        else:
            print("Author does not exist! Adding author")
            session.add(author)
            session.flush()
            pairing = BookAuthor(author_id=author.author_id, book_id=book.book_id)

        session.add(pairing)
        session.commit()
        print("New pairing added " + str(pairing))
