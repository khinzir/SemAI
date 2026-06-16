"""
Azure Cosmos DB client for data persistence
"""
import os
from azure.cosmos import CosmosClient, PartitionKey, exceptions
from datetime import datetime
import uuid
import json


class CosmosClientManager:
    def __init__(self):
        # Gracefully pull strings from secrets or fall back to production defaults
        connection_string = os.getenv("COSMOS_DB_CONNECTION_STRING")
        database_name = os.getenv("COSMOS_DB_NAME", "csit-guru")
        container_name = os.getenv("COSMOS_DB_CONTAINER", "chat-history")

        self.client = CosmosClient.from_connection_string(connection_string)

        # Ensures the script automatically builds the structures if Azure can't find them
        self.database = self.client.create_database_if_not_exists(id=database_name)
        self.container = self.database.create_container_if_not_exists(
            id=container_name,
            partition_key=PartitionKey(path="/id"),
            offer_throughput=400
        )

    def _init_cosmos(self):
        """Initialize Cosmos DB containers"""
        try:
            database = self.client.create_database_if_not_exists(id=self.database_name)
            self.container = database.create_container_if_not_exists(
                id=self.container_name,
                partition_key=PartitionKey(path="/user_id"),
                offer_throughput=400
            )
        except Exception:
            database = self.client.get_database_client(self.database_name)
            self.container = database.get_container_client(self.container_name)

    def _init_sqlite(self):
        """Fallback to SQLite"""
        import sqlite3
        self.db_path = "local_csit_semai.db"
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create message logs
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

        # Create progress tracking metrics
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS progress (
                user_id TEXT,
                semester INTEGER,
                subject_code TEXT,
                minutes_studied INTEGER,
                PRIMARY KEY (user_id, semester, subject_code)
            )
        """)

        # NEW: Robust student profile table schema configuration
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                password TEXT,
                selected_semester INTEGER DEFAULT 1
            )
        """)

        conn.commit()
        conn.close()

    # ==================== NEW AUTHENTICATION MECHANISMS ====================

    def verify_or_create_user(self, email: str, passcode: str) -> dict:
        """Securely verifies profile records or creates a new row if email is unseen."""
        user_id = email.strip().lower().replace("@", "_").replace(".", "_")
        passcode = passcode.strip()

        if self.use_cosmos:
            try:
                # Primary partition key lookup
                item_id = f"user_{user_id}"
                user_profile = self.container.read_item(item=item_id, partition_key=user_id)

                if user_profile.get("password") == passcode:
                    return {"user_id": user_id, "selected_semester": user_profile.get("selected_semester", 1)}
                return {}  # Incorrect password
            except exceptions.CosmosResourceNotFoundError:
                # Auto-registration on first successful input
                profile_doc = {
                    "id": f"user_{user_id}",
                    "user_id": user_id,
                    "type": "profile",
                    "password": passcode,
                    "selected_semester": 1,
                    "created_at": datetime.utcnow().isoformat()
                }
                self.container.upsert_item(profile_doc)
                return {"user_id": user_id, "selected_semester": 1}
            except Exception:
                return {"user_id": user_id, "selected_semester": 1}  # Resilient fallback pass
        else:
            import sqlite3
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT password, selected_semester FROM users WHERE user_id = ?", (user_id,))
            row = cursor.fetchone()

            if row:
                if row[0] == passcode:
                    conn.close()
                    return {"user_id": user_id, "selected_semester": row[1]}
                conn.close()
                return {}  # Wrong password fallback
            else:
                # Store new credentials cleanly
                cursor.execute("INSERT INTO users (user_id, password, selected_semester) VALUES (?, ?, ?)",
                               (user_id, passcode, 1))
                conn.commit()
                conn.close()
                return {"user_id": user_id, "selected_semester": 1}

    def save_semester_preference(self, user_id: str, semester: int):
        """Persists the user's selected semester preference."""
        if self.use_cosmos:
            try:
                item_id = f"user_{user_id}"
                profile = self.container.read_item(item=item_id, partition_key=user_id)
                profile["selected_semester"] = int(semester)
                self.container.upsert_item(profile)
            except Exception:
                pass
        else:
            import sqlite3
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET selected_semester = ? WHERE user_id = ?", (int(semester), user_id))
            conn.commit()
            conn.close()

    # ==================== DATA REHYDRATION ACCESSORS ====================

    def load_all_user_progress(self, user_id: str) -> dict:
        """Loads historical progress to reconstruct progress maps on login or reload."""
        progress_map = {}
        if self.use_cosmos:
            try:
                query = "SELECT c.semester, c.subject_code, c.minutes_studied FROM c WHERE c.user_id = @uid AND IS_DEFINED(c.minutes_studied)"
                items = self.container.query_items(
                    query=query,
                    parameters=[{"name": "@uid", "value": user_id}],
                    enable_cross_partition_query=True
                )
                for item in items:
                    key = f"{user_id}_{item['semester']}_{item['subject_code']}"
                    progress_map[key] = item['minutes_studied']
            except Exception:
                pass
        else:
            import sqlite3
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT semester, subject_code, minutes_studied FROM progress WHERE user_id = ?",
                               (user_id,))
                for row in cursor.fetchall():
                    key = f"{user_id}_{row[0]}_{row[1]}"
                    progress_map[key] = row[2]
                conn.close()
            except Exception:
                pass
        return progress_map

    def load_chat_history(self, user_id: str, subject: str) -> list:
        """Retrieves past dialogue streams to restore history memory grids."""
        history = []
        if self.use_cosmos:
            try:
                query = "SELECT c.role, c.content FROM c WHERE c.user_id = @uid AND c.subject = @sub ORDER BY c.timestamp ASC"
                items = self.container.query_items(
                    query=query,
                    parameters=[{"name": "@uid", "value": user_id}, {"name": "@sub", "value": subject}],
                    enable_cross_partition_query=True
                )
                for item in items:
                    history.append({"role": item["role"], "content": item["content"]})
            except Exception:
                pass
        else:
            import sqlite3
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT role, content FROM messages WHERE user_id = ? AND subject = ? ORDER BY timestamp ASC",
                    (user_id, subject))
                for row in cursor.fetchall():
                    history.append({"role": row[0], "content": row[1]})
                conn.close()
            except Exception:
                pass
        return history

    # ==================== LEGACY METHOD STUBS ====================

    def save_message(self, user_id: str, subject: str, role: str, content: str, citations: list = None):
        message_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()
        if self.use_cosmos:
            try:
                self.container.upsert_item({
                    "id": message_id,
                    "user_id": user_id,
                    "subject": subject,
                    "role": role,
                    "content": content,
                    "citations": citations or [],
                    "timestamp": timestamp
                })
            except Exception:
                pass
        else:
            import sqlite3
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO messages (id, user_id, subject, role, content, citations, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (message_id, user_id, subject, role, content, json.dumps(citations or []), timestamp))
            conn.commit()
            conn.close()

    def save_progress(self, user_id: str, semester: int, subject_code: str, minutes: int):
        if self.use_cosmos:
            try:
                progress_id = f"{user_id}_{semester}_{subject_code}"
                self.container.upsert_item({
                    "id": progress_id,
                    "user_id": user_id,
                    "semester": semester,
                    "subject_code": subject_code,
                    "minutes_studied": minutes,
                    "last_updated": datetime.utcnow().isoformat()
                })
            except Exception:
                pass
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
        if self.use_cosmos:
            try:
                item = self.container.read_item(item=f"{user_id}_{semester}_{subject_code}", partition_key=user_id)
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