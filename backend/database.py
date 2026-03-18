import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

DATABASE_URL = "mysql+pymysql://root:jaya%40123@db:3306/student_db"

# Retry connection logic
for i in range(10):
    try:
        engine = create_engine(DATABASE_URL, echo=True)
        connection = engine.connect()
        print("Connected to MySQL successfully!")
        connection.close()
        break
    except OperationalError:
        print("MySQL not ready... retrying in 5 seconds")
        time.sleep(5)
else:
    print("Could not connect to MySQL after retries")
    raise

SessionLocal = sessionmaker(bind=engine)
