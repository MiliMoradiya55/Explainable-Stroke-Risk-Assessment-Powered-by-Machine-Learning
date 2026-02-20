# import sqlite3

# def get_user_db():
#     conn = sqlite3.connect('users.db', check_same_thread=False)
#     conn.row_factory = sqlite3.Row
#     return conn

# def init_users_db():
#     with get_user_db() as conn:
#         conn.execute('''
#             CREATE TABLE IF NOT EXISTS users (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 username TEXT UNIQUE NOT NULL,
#                 password TEXT NOT NULL,
#                 mobile TEXT
#             )
#         ''')
#         conn.commit()
#     print("✅ Users table ready (username + mobile).")

# def create_user(username, password, mobile):
#     try:
#         with get_user_db() as conn:
#             conn.execute(
#                 'INSERT INTO users (username, password, mobile) VALUES (?, ?, ?)',
#                 (username, password, mobile)
#             )
#             conn.commit()
#             return True
#     except sqlite3.IntegrityError:
#         # Username already exists
#         return False
#     except Exception as e:
#         print("❌ Database error in create_user:", e)
#         return False

# def get_user_by_username(username):
#     with get_user_db() as conn:
#         return conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()

# def get_user_by_id(user_id):
#     with get_user_db() as conn:
#         return conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()

# # ---------- Stroke predictions database (unchanged) ----------
# def get_stroke_db():
#     conn = sqlite3.connect('stroke_users.db', check_same_thread=False)
#     conn.row_factory = sqlite3.Row
#     return conn

# def init_stroke_db():
#     with get_stroke_db() as conn:
#         conn.execute('''
#             CREATE TABLE IF NOT EXISTS predictions (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 user_id INTEGER NOT NULL,
#                 gender TEXT,
#                 age REAL,
#                 hypertension INTEGER,
#                 heart_disease INTEGER,
#                 ever_married TEXT,
#                 work_type TEXT,
#                 residence_type TEXT,
#                 avg_glucose_level REAL,
#                 bmi REAL,
#                 smoking_status TEXT,
#                 prediction INTEGER,
#                 probability REAL,
#                 timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
#             )
#         ''')
#         conn.commit()
#     print("✅ Predictions table ready.")

# def save_prediction(user_id, data, pred, proba):
#     with get_stroke_db() as conn:
#         conn.execute('''
#             INSERT INTO predictions (
#                 user_id, gender, age, hypertension, heart_disease, ever_married,
#                 work_type, residence_type, avg_glucose_level, bmi, smoking_status,
#                 prediction, probability
#             ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#         ''', (
#             user_id,
#             data['gender'],
#             data['age'],
#             data['hypertension'],
#             data['heart_disease'],
#             data['ever_married'],
#             data['work_type'],
#             data['residence_type'],
#             data['avg_glucose_level'],
#             data['bmi'],
#             data['smoking_status'],
#             pred,
#             proba
#         ))
#         conn.commit()

# def get_user_predictions(user_id):
#     with get_stroke_db() as conn:
#         rows = conn.execute(
#             'SELECT * FROM predictions WHERE user_id = ? ORDER BY timestamp DESC',
#             (user_id,)
#         ).fetchall()
#         return [dict(row) for row in rows]

# def get_prediction(pred_id, user_id):
#     with get_stroke_db() as conn:
#         row = conn.execute(
#             'SELECT * FROM predictions WHERE id = ? AND user_id = ?',
#             (pred_id, user_id)
#         ).fetchone()
#         return dict(row) if row else None

import sqlite3

def get_user_db():
    conn = sqlite3.connect('users.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_users_db():
    with get_user_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                mobile TEXT
            )
        ''')
        conn.commit()
    print("✅ Users table ready (username + mobile).")

def create_user(username, password, mobile):
    try:
        with get_user_db() as conn:
            conn.execute(
                'INSERT INTO users (username, password, mobile) VALUES (?, ?, ?)',
                (username, password, mobile)
            )
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        return False
    except Exception as e:
        print("❌ Database error in create_user:", e)
        return False

def get_user_by_username(username):
    with get_user_db() as conn:
        return conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()

def get_user_by_id(user_id):
    with get_user_db() as conn:
        return conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()

def get_stroke_db():
    conn = sqlite3.connect('stroke_users.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_stroke_db():
    with get_stroke_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                gender TEXT,
                age REAL,
                hypertension INTEGER,
                heart_disease INTEGER,
                ever_married TEXT,
                work_type TEXT,
                residence_type TEXT,
                avg_glucose_level REAL,
                bmi REAL,
                smoking_status TEXT,
                prediction INTEGER,
                probability REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
    print("✅ Predictions table ready.")

def save_prediction(user_id, data, pred, proba):
    with get_stroke_db() as conn:
        conn.execute('''
            INSERT INTO predictions (
                user_id, gender, age, hypertension, heart_disease, ever_married,
                work_type, residence_type, avg_glucose_level, bmi, smoking_status,
                prediction, probability
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_id,
            data['gender'],
            data['age'],
            data['hypertension'],
            data['heart_disease'],
            data['ever_married'],
            data['work_type'],
            data['residence_type'],
            data['avg_glucose_level'],
            data['bmi'],
            data['smoking_status'],
            pred,
            proba
        ))
        conn.commit()

def get_user_predictions(user_id):
    with get_stroke_db() as conn:
        rows = conn.execute(
            'SELECT * FROM predictions WHERE user_id = ? ORDER BY timestamp DESC',
            (user_id,)
        ).fetchall()
        return [dict(row) for row in rows]

def get_prediction(pred_id, user_id):
    with get_stroke_db() as conn:
        row = conn.execute(
            'SELECT * FROM predictions WHERE id = ? AND user_id = ?',
            (pred_id, user_id)
        ).fetchone()
        return dict(row) if row else None
