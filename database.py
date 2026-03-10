import sqlite3
from datetime import datetime, timedelta

DATABASE = 'tongues.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS proverbs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            language TEXT NOT NULL,
            script TEXT NOT NULL,
            romanised TEXT,
            literal_translation TEXT,
            real_meaning TEXT NOT NULL,
            english_equivalent TEXT,
            notes TEXT,
            verified BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_lang TEXT NOT NULL,
            target_lang TEXT NOT NULL,
            input_text TEXT NOT NULL,
            translation TEXT NOT NULL,
            rating TEXT NOT NULL,
            comment TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usage_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_lang TEXT NOT NULL,
            target_lang TEXT NOT NULL,
            input_length INTEGER,
            success BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()


def find_proverb(text, source_lang):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM proverbs
        WHERE language = ?
        AND (script = ? OR LOWER(romanised) = LOWER(?) OR LOWER(script) = LOWER(?))
    ''', (source_lang, text.strip(), text.strip(), text.strip()))
    result = cursor.fetchone()
    conn.close()
    return dict(result) if result else None


def log_feedback(source_lang, target_lang, input_text, translation, rating, comment=''):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO feedback (source_lang, target_lang, input_text, translation, rating, comment)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (source_lang, target_lang, input_text or '', translation or '', rating, comment or ''))
    conn.commit()
    conn.close()


def log_usage(source_lang, target_lang, input_length, success=True):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO usage_stats (source_lang, target_lang, input_length, success)
        VALUES (?, ?, ?, ?)
    ''', (source_lang, target_lang, input_length, success))
    conn.commit()
    conn.close()


def get_stats():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) as total FROM usage_stats WHERE success = 1')
    total = cursor.fetchone()['total']

    today = datetime.now().strftime('%Y-%m-%d')
    cursor.execute("SELECT COUNT(*) as total FROM usage_stats WHERE DATE(created_at) = ? AND success = 1", (today,))
    today_count = cursor.fetchone()['total']

    week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    cursor.execute("SELECT COUNT(*) as total FROM usage_stats WHERE DATE(created_at) >= ? AND success = 1", (week_ago,))
    week_count = cursor.fetchone()['total']

    cursor.execute('''
        SELECT source_lang || ' → ' || target_lang as pair, COUNT(*) as count
        FROM usage_stats WHERE success = 1
        GROUP BY source_lang, target_lang
        ORDER BY count DESC LIMIT 8
    ''')
    top_pairs = [dict(r) for r in cursor.fetchall()]

    cursor.execute("SELECT COUNT(*) as total FROM feedback WHERE rating = 'good'")
    good = cursor.fetchone()['total']

    cursor.execute("SELECT COUNT(*) as total FROM feedback WHERE rating = 'bad'")
    bad = cursor.fetchone()['total']

    cursor.execute('SELECT COUNT(*) as total FROM proverbs')
    proverb_count = cursor.fetchone()['total']

    conn.close()
    return {
        'total': total,
        'today': today_count,
        'this_week': week_count,
        'top_pairs': top_pairs,
        'thumbs_up': good,
        'thumbs_down': bad,
        'proverb_count': proverb_count
    }


def get_recent_feedback():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM feedback
        ORDER BY created_at DESC LIMIT 15
    ''')
    results = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return results


def get_recent_translations():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM usage_stats
        ORDER BY created_at DESC LIMIT 15
    ''')
    results = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return results

