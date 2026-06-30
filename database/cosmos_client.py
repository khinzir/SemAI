"""
Azure Cosmos DB client for data persistence with SQLite fallback
"""
import os
import json
import sqlite3
import uuid
import re
from datetime import datetime

try:
    from azure.cosmos import CosmosClient, PartitionKey, exceptions
    HAS_AZURE = True
except ImportError:
    HAS_AZURE = False


class CosmosClientManager:
    def __init__(self):
        self.use_cosmos = False
        self.db_path = "semai_local.db"

        connection_string = os.getenv("COSMOS_DB_CONNECTION_STRING")

        if connection_string and HAS_AZURE:
            try:
                self.client = CosmosClient.from_connection_string(connection_string)
                self.database_name = os.getenv("COSMOS_DB_NAME", "csit-guru")
                self.container_name = os.getenv("COSMOS_DB_CONTAINER", "user-data")

                database = self.client.create_database_if_not_exists(id=self.database_name)
                self.container = database.create_container_if_not_exists(
                    id=self.container_name,
                    partition_key=PartitionKey(path="/user_id"),
                )
                self.use_cosmos = True
                print("✅ Connected to Azure Cosmos DB")
            except Exception as e:
                print(f"⚠️ Cosmos DB connection failed: {e}. Using SQLite fallback.")
                self._init_sqlite()
        else:
            print("📁 Using SQLite local database")
            self._init_sqlite()

    def _init_sqlite(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                email TEXT UNIQUE,
                password TEXT,
                name TEXT,
                semester INTEGER,
                created_at TEXT
            )
        """)
        c.execute("""
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
        c.execute("""
            CREATE TABLE IF NOT EXISTS progress (
                user_id TEXT,
                semester INTEGER,
                subject_code TEXT,
                minutes_studied INTEGER,
                PRIMARY KEY (user_id, semester, subject_code)
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS preferences (
                user_id TEXT,
                key TEXT,
                value TEXT,
                PRIMARY KEY (user_id, key)
            )
        """)
        conn.commit()
        conn.close()

    def validate_signup_inputs(self, email: str, password: str) -> tuple[bool, str]:
        """Validates standard institutional email formats and security password criteria."""
        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_regex, email):
            return False, "Please enter a valid email address structure (e.g., student@domain.com)."

        if len(password) < 6:
            return False, "Security passcode must be at least 6 characters long."

        return True, ""

    def save_user(self, email, password, name, semester=1):
        user_id = email.replace("@", "_").replace(".", "_")

        if self.use_cosmos:
            user_doc = {
                "id": f"user_{user_id}",
                "user_id": user_id,
                "email": email,
                "password": password,
                "name": name,
                "semester": semester,
                "type": "user",
                "created_at": datetime.utcnow().isoformat()
            }
            self.container.upsert_item(user_doc)
        else:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("""
                INSERT OR REPLACE INTO users (user_id, email, password, name, semester, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (user_id, email, password, name, semester, datetime.utcnow().isoformat()))
            conn.commit()
            conn.close()
        return user_id

    def get_user(self, email):
        user_id = email.replace("@", "_").replace(".", "_")
        if self.use_cosmos:
            try:
                # Point read optimization prevents cross-partition query failures
                item = self.container.read_item(item=f"user_{user_id}", partition_key=user_id)
                return item
            except Exception:
                return None
        else:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE email = ?", (email,))
            row = c.fetchone()
            conn.close()
            if row:
                return {
                    "user_id": row[0],
                    "email": row[1],
                    "password": row[2],
                    "name": row[3],
                    "semester": row[4]
                }
            return None

    def save_message(self, user_id, subject, role, content, citations=None):
        msg_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()

        if self.use_cosmos:
            self.container.upsert_item({
                "id": msg_id,
                "user_id": user_id,
                "subject": subject,
                "role": role,
                "content": content,
                "citations": citations or [],
                "timestamp": timestamp,
                "type": "message"
            })
        else:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("""
                INSERT INTO messages (id, user_id, subject, role, content, citations, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (msg_id, user_id, subject, role, content, json.dumps(citations or []), timestamp))
            conn.commit()
            conn.close()

    def load_chat_history(self, user_id, subject):
        if self.use_cosmos:
            try:
                query = f"SELECT * FROM c WHERE c.user_id = '{user_id}' AND c.subject = '{subject}' AND c.type = 'message' ORDER BY c.timestamp ASC"
                items = list(self.container.query_items(query, partition_key=user_id))
                return [{"role": i["role"], "content": i["content"], "citations": i.get("citations", [])} for i in items]
            except Exception:
                return []
        else:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("""
                SELECT role, content, citations FROM messages
                WHERE user_id = ? AND subject = ?
                ORDER BY timestamp ASC
            """, (user_id, subject))
            rows = c.fetchall()
            conn.close()
            return [{"role": r[0], "content": r[1], "citations": json.loads(r[2]) if r[2] else []} for r in rows]

    def save_progress(self, user_id, semester, subject_code, minutes):
        if self.use_cosmos:
            self.container.upsert_item({
                "id": f"prog_{user_id}_{semester}_{subject_code}",
                "user_id": user_id,
                "semester": semester,
                "subject_code": subject_code,
                "minutes_studied": minutes,
                "type": "progress",
                "last_updated": datetime.utcnow().isoformat()
            })
        else:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("""
                INSERT OR REPLACE INTO progress (user_id, semester, subject_code, minutes_studied)
                VALUES (?, ?, ?, ?)
            """, (user_id, semester, subject_code, minutes))
            conn.commit()
            conn.close()

    def get_progress(self, user_id, semester, subject_code):
        if self.use_cosmos:
            try:
                item = self.container.read_item(
                    item=f"prog_{user_id}_{semester}_{subject_code}",
                    partition_key=user_id
                )
                return item.get("minutes_studied", 0)
            except Exception:
                return 0
        else:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("""
                SELECT minutes_studied FROM progress
                WHERE user_id = ? AND semester = ? AND subject_code = ?
            """, (user_id, semester, subject_code))
            row = c.fetchone()
            conn.close()
            return row[0] if row else 0

    def save_preference(self, user_id, key, value):
        if self.use_cosmos:
            self.container.upsert_item({
                "id": f"pref_{user_id}_{key}",
                "user_id": user_id,
                "key": key,
                "value": value,
                "type": "preference",
                "timestamp": datetime.utcnow().isoformat()
            })
        else:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("""
                INSERT OR REPLACE INTO preferences (user_id, key, value)
                VALUES (?, ?, ?)
            """, (user_id, key, value))
            conn.commit()
            conn.close()

    def get_user_preference(self, user_id, key):
        if self.use_cosmos:
            try:
                item = self.container.read_item(
                    item=f"pref_{user_id}_{key}",
                    partition_key=user_id
                )
                return item.get("value", "")
            except Exception:
                return ""
        else:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("SELECT value FROM preferences WHERE user_id = ? AND key = ?", (user_id, key))
            row = c.fetchone()
            conn.close()
            return row[0] if row else ""