from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "sqlite:///./base_datos.db"

engine = create_engine(DATABASE_URL, echo=True)


def crear_tablas():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
