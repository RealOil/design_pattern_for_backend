# user_service.py

import sqlite3
import requests

class UserService:
    def create_user(self, user_id: int, name: str):
        # DB 연결
        conn = sqlite3.connect("app.db")
        cursor = conn.cursor()

        try:
            # DB 저장
            cursor.execute(
                "INSERT INTO users (id, name) VALUES (?, ?)",
                (user_id, name)
            )

            # 외부 API 호출
            response = requests.post(
                "https://external.api/send",
                json={"user_id": user_id}
            )
            response.raise_for_status()

            # 커밋
            conn.commit()

        except Exception as e:
            conn.rollback()
            raise e

        finally:
            conn.close()