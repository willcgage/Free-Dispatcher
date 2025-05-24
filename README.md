This project is to create an app that can be used during modular railroad gatherings for tracking trains by dispatchers.

To initialize Alembic (run only once):
sh
alembic init alembic
To create a new migration after modifying your models:
sh
alembic revision --autogenerate -m "Your migration message"
To apply migrations:
sh
alembic upgrade head

