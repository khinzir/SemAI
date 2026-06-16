"""
Azure Cosmos DB client for data persistence
"""
import os
from azure.cosmos import CosmosClient, PartitionKey, exceptions
from datetime import datetime
import uuid


class CosmosClientManager:
    def __init__(self):
        connection_string = os.getenv("COSMOS_DB_CONNECTION_STRING")
        database_name = os.getenv("COSMOS_DB_NAME", "csit-guru")
        container_name = os.getenv("COSMOS_DB_CONTAINER", "user-data")

        if connection_string:
            try:
                self.client = CosmosClient.from_connection_string(connection_string)
                self.database_name = database_name
                self.container_name = container_name

                # Automatically connect or safely build if missing
                database = self.client.create_database_if_not_exists(id=self.database_name)
                self.container = database.create_container_if_not_exists(
                    id=self.container_name,
                    partition_key=PartitionKey(path="/user_id"),
                    offer_throughput=400
                )
                self.use_cosmos = True
            except Exception as e:
                print(f"Cosmos Connection Failed, falling back to SQLite: {e}")
                self.use_cosmos = False
                self._init_sqlite()
        else:
            self.use_cosmos = False
            self._init_sqlite()

    def _init_sqlite(self):
        """Fallback to SQLite"""
        import sqlite3
        self.db_path = "local_csit_guru.db"
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                password TEXT,
                created_at TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id TEXT PRIMARY KEY,
                user_id TEXT,
                subject TEXT,
                role TEXT,
                content TEXT,
                citations TEXT,
                timestamp TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS progress (
                user_id TEXT,
                semester INTEGER,
                subject_code TEXT,
                minutes_studied INTEGER,
                PRIMARY KEY (user_id, semester, subject_code)
            )
        """)
        conn.commit()
        conn.close()

    def verify_or_create_user(self, email: str, password: str) -> dict:
        """Verifies or registers a user document and tracks session persistence"""
        user_id = email.replace("@", "_").replace(".", "_")

        if self.use_cosmos:
            try:
                # Try to read existing profile
                user_doc = self.container.read_item(item=user_id, partition_key=user_id)
                return user_doc
            except exceptions.CosmosResourceNotFoundError:
                # Create a fresh profile if new registration
                new_profile = {
                    "id": user_id,
                    "user_id": user_id,
                    "email": email,
                    "password": password,  # In production, use hashing
                    "created_at": datetime.utcnow().isoformat()
                }
                self.container.upsert_item(new_profile)
                return new_profile
        else:
            import sqlite3
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
            row = cursor.fetchone()

            if not row:
                cursor.execute("INSERT INTO users (user_id, password, created_at) VALUES (?, ?, ?)",
                               (user_id, password, datetime.utcnow().isoformat()))
                conn.commit()
            conn.close()
            return {"user_id": user_id, "email": email}

    def save_message(self, user_id: str, subject: str, role: str, content: str, citations: list = None):
        """Save chat message"""
        message_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()

        if self.use_cosmos:
            self.container.upsert_item({
                "id": message_id,
                "user_id": user_id,
                "subject": subject,
                "role": role,
                "content": content,
                "citations": citations or [],
                "timestamp": timestamp
            })
        else:
            import sqlite3
            import json
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO messages (id, user_id, subject, role, content, citations, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (message_id, user_id, subject, role, content, json.dumps(citations or []), timestamp))
            conn.commit()
            conn.close()

    def save_progress(self, user_id: str, semester: int, subject_code: str, minutes: int):
        """Save study progress"""
        if self.use_cosmos:
            progress_id = f"prog_{user_id}_{semester}_{subject_code}"
            self.container.upsert_item({
                "id": progress_id,
                "user_id": user_id,
                "semester": semester,
                "subject_code": subject_code,
                "minutes_studied": minutes,
                "last_updated": datetime.utcnow().isoformat()
            })
        else:
            import sqlite3
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO progress (user_id, semester, subject_code, minutes_studied)
                VALUES (?, ?, ?, ?)
            """, (user_id, semester, subject_code, minutes))
            conn.commit()
            conn.close()

    def get_progress(self, user_id: str, semester: int, subject_code: str) -> int:
        """Get study progress"""
        if self.use_cosmos:
            try:
                progress_id = f"prog_{user_id}_{semester}_{subject_code}"
                item = self.container.read_item(
                    item=progress_id,
                    partition_key=user_id
                )
                return item.get("minutes_studied", 0)
            except Exception:
                return 0
        else:
            import sqlite3
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT minutes_studied FROM progress
                WHERE user_id = ? AND semester = ? AND subject_code = ?
            """, (user_id, semester, subject_code))
            result = cursor.fetchone()
            conn.close()
            return result[0] if result else 0