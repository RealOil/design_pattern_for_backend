import sqlite3
from app.repositories.user_repository import User, UserRepository

class SQLiteUserRepository(UserRepository):
        def __init__(self, db_path: str = "app.db") -> None:
                self.db_path = db_path

        def save(self, user: User) -> None:
                conn = sqlite3.connect(self.db_path)
                try:
                        cursor = conn.cursor()
                        cursor.execute(
                                "INSERT INTO users (id, name) VALUES (?, ?)",
                                (user.id, user.name),
                        )
                        conn.commit()
                finally:
                        conn.close()