from sqlmodel import Session, SQLModel, create_engine


def create_db_sessionmaker(url: str):
    """
    Creates connection to db.

    url: postgres://<username>:<password>@<host>/<db_name>
    """
    url = url.replace("postgres", "postgresql", 1)
    engine = create_engine(url)
    create_db_and_tables(engine)

    def get_database_api():
        with Session(engine) as session:
            yield session

    return get_database_api


def create_db_and_tables(engine):
    SQLModel.metadata.create_all(engine)
