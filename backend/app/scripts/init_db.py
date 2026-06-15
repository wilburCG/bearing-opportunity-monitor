from app.db.session import Base, engine
import app.models  # noqa: F401 - register models


def main():
    Base.metadata.create_all(bind=engine)
    print("database tables created")


if __name__ == "__main__":
    main()
