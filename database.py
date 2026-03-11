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

    # Seed proverbs only if table is empty
    cursor.execute('SELECT COUNT(*) as total FROM proverbs')
    count = cursor.fetchone()['total']

    if count == 0:
        proverbs = [
            # Gujarati
            ('Gujarati', 'દૂધનો દાઝેલો છાશ પણ ફૂંકી ફૂંકીને પીએ', 'Dudh no daazelo chaash pan funki funkine piye', 'One burned by milk blows even on buttermilk', 'Once hurt, a person becomes overly cautious even in safe situations', 'Once bitten, twice shy', 'Very commonly used in Gujarati households'),
            ('Gujarati', 'જેવી દ્રષ્ટિ તેવી સૃષ્ટિ', 'Jevi drashti tevi srushti', 'As the vision, so the world', 'The world appears as you perceive it — your mindset shapes your reality', 'Beauty is in the eye of the beholder', None),
            ('Gujarati', 'નાચ ન જાણે આંગણ વાંકુ', 'Naach na jaane aangan vaanku', 'Cannot dance, blames the courtyard', 'A bad workman blames their tools or circumstances', 'A bad workman blames his tools', 'Used humorously to call out excuse-making'),
            ('Gujarati', 'ઘરનો વૈદ્ય ગધેડો', 'Gharna vaidya gadhedo', 'The doctor at home is a donkey', 'Expertise is not valued when it comes from someone close to you', 'A prophet is not recognised in his own land', None),
            ('Gujarati', 'બાર ગાઉએ બોલી બદલાય', 'Baar gaue boli badle', 'Speech changes every twelve miles', 'Language and dialect shift constantly across regions', None, 'Reflects Gujarati linguistic diversity'),
            ('Gujarati', 'સો સોનાર ની એક લુહાર ની', 'So sonar ni ek luhar ni', 'A hundred blows of a goldsmith equal one of a blacksmith', 'One decisive action is worth more than many weak attempts', 'One stroke of a real blow beats a hundred light ones', None),
            ('Gujarati', 'આંધળામાં કાણો રાજા', 'Aandhla ma kaano raja', 'Among the blind, the one-eyed is king', 'Even partial ability makes you stand out among those with none', 'In the land of the blind, the one-eyed man is king', None),
            ('Gujarati', 'અતિ સર્વત્ર વર્જયેત', 'Ati sarvatra varjayet', 'Excess should be avoided everywhere', 'Too much of anything is harmful', 'Everything in moderation', 'Sanskrit origin, widely used in Gujarati'),
            ('Gujarati', 'મૂળ કરતા વ્યાજ વહાલું', 'Mool karta vyaaj vahalu', 'The interest is dearer than the principal', 'Grandparents love their grandchildren even more than their own children — affection deepens across generations', 'Grandparents always cherish their grandchildren more than their own children', 'This is about family love skipping a generation, NOT a finance proverb. Never translate as a money/banking expression.'),

            # Hindi
            ('Hindi', 'अब पछताए होत क्या जब चिड़िया चुग गई खेत', 'Ab pachtaye hot kya jab chidiya chug gayi khet', 'What use is regret when the birds have eaten the field', 'It is too late to regret after the damage is done', 'No use crying over spilled milk', None),
            ('Hindi', 'अंधों में काना राजा', 'Andhon mein kaana raja', 'Among the blind, the one-eyed is king', 'Even partial ability makes you stand out among those with none', 'In the land of the blind, the one-eyed man is king', None),
            ('Hindi', 'जैसी करनी वैसी भरनी', 'Jaisi karni waisi bharni', 'As you sow, so shall you reap', 'Your actions determine your outcomes', 'You reap what you sow', None),
            ('Hindi', 'दूध का जला छाछ भी फूंक फूंक कर पीता है', 'Dudh ka jala chaach bhi funky funk kar peeta hai', 'One burned by milk blows even on buttermilk', 'Once hurt, a person becomes overly cautious', 'Once bitten, twice shy', None),
            ('Hindi', 'नाच न जाने आंगन टेढ़ा', 'Naach na jaane aangan tedha', 'Cannot dance, blames the crooked courtyard', 'A bad workman blames their tools', 'A bad workman blames his tools', None),
            ('Hindi', 'घर का भेदी लंका ढाए', 'Ghar ka bhedi lanka dhaye', 'The insider who betrays can destroy Lanka itself', 'An insider leak or betrayal causes the greatest damage', 'It takes a thief to catch a thief / Beware the enemy within', None),

            # Marathi
            ('Marathi', 'नाचता येईना अंगण वाकडे', 'Nachata yeina angan vakade', 'Cannot dance, blames the crooked courtyard', 'A bad workman blames their tools', 'A bad workman blames his tools', None),
            ('Marathi', 'शहाण्याला शब्द एक मूर्खाला लाख', 'Shahanyala shabda ek murkhala lakh', 'A wise person needs one word, a fool needs a hundred thousand', 'Intelligent people understand quickly; fools need endless explanation', 'A word to the wise is sufficient', None),
            ('Marathi', 'जसे बीज पेराल तसे उगवेल', 'Jase beej peral tase ugavel', 'As you sow, so shall it grow', 'Your actions determine your outcomes', 'You reap what you sow', None),
        ]

        cursor.executemany('''
            INSERT INTO proverbs (language, script, romanised, literal_translation, real_meaning, english_equivalent, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', proverbs)

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

