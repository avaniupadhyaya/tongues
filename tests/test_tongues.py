"""
Tongues App — Pytest Test Suite
Tests cover:
  1. Database — proverb seeding, lookup, cross-language equivalents
  2. API endpoints — translate, feedback, dashboard
  3. Translation quality — proverb cultural notes, register matching
"""

import pytest
import json
import sys
import os

# Add parent directory to path so we can import app and database
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app as flask_app
from database import init_db, find_proverb, get_db


# ─────────────────────────────────────────
# FIXTURES
# ─────────────────────────────────────────

@pytest.fixture
def client():
    """Flask test client with test config."""
    flask_app.config['TESTING'] = True
    flask_app.config['DATABASE'] = 'tongues_test.db'
    with flask_app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def setup_db():
    """Ensure DB is initialised before each test."""
    init_db()
    yield


# ─────────────────────────────────────────
# 1. DATABASE TESTS
# ─────────────────────────────────────────

class TestDatabaseSeeding:

    def test_gujarati_proverbs_count(self):
        """Should have exactly 100 Gujarati proverbs."""
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT COUNT(*) as total FROM proverbs WHERE language = 'Gujarati'")
        count = c.fetchone()['total']
        conn.close()
        assert count == 100, f"Expected 100 Gujarati proverbs, got {count}"

    def test_hindi_proverbs_count(self):
        """Should have exactly 100 Hindi proverbs."""
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT COUNT(*) as total FROM proverbs WHERE language = 'Hindi'")
        count = c.fetchone()['total']
        conn.close()
        assert count == 100, f"Expected 100 Hindi proverbs, got {count}"

    def test_marathi_proverbs_count(self):
        """Should have exactly 100 Marathi proverbs."""
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT COUNT(*) as total FROM proverbs WHERE language = 'Marathi'")
        count = c.fetchone()['total']
        conn.close()
        assert count == 100, f"Expected 100 Marathi proverbs, got {count}"

    def test_total_proverbs_count(self):
        """Should have exactly 300 proverbs total."""
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT COUNT(*) as total FROM proverbs")
        count = c.fetchone()['total']
        conn.close()
        assert count == 300, f"Expected 300 total proverbs, got {count}"

    def test_all_proverbs_have_real_meaning(self):
        """Every proverb must have a real_meaning field."""
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT COUNT(*) as total FROM proverbs WHERE real_meaning IS NULL OR real_meaning = ''")
        count = c.fetchone()['total']
        conn.close()
        assert count == 0, f"{count} proverbs are missing real_meaning"

    def test_all_proverbs_have_romanised(self):
        """Every proverb must have a romanised field."""
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT COUNT(*) as total FROM proverbs WHERE romanised IS NULL OR romanised = ''")
        count = c.fetchone()['total']
        conn.close()
        assert count == 0, f"{count} proverbs are missing romanised text"

    def test_equivalents_table_populated(self):
        """proverb_equivalents table should have entries."""
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT COUNT(*) as total FROM proverb_equivalents")
        count = c.fetchone()['total']
        conn.close()
        assert count > 0, "proverb_equivalents table is empty"


class TestProverbLookup:

    def test_gujarati_proverb_lookup_by_script(self):
        """find_proverb should find a Gujarati proverb by exact script."""
        result = find_proverb('મૂળ કરતા વ્યાજ વહાલું', 'Gujarati')
        assert result is not None, "Gujarati proverb not found"
        assert result['language'] == 'Gujarati'

    def test_gujarati_proverb_real_meaning(self):
        """મૂળ કરતા વ્યાજ વહાલું must return grandparents meaning, not finance."""
        result = find_proverb('મૂળ કરતા વ્યાજ વહાલું', 'Gujarati')
        assert result is not None
        meaning = result['real_meaning'].lower()
        assert 'grandp' in meaning or 'grandchildren' in meaning, \
            f"Wrong meaning returned: {result['real_meaning']}"
        assert 'finance' not in meaning and 'interest' not in meaning.lower()[:20], \
            "Proverb is being interpreted as a finance proverb"

    def test_hindi_proverb_lookup(self):
        """find_proverb should find a Hindi proverb by script."""
        result = find_proverb('जहाँ चाह वहाँ राह', 'Hindi')
        assert result is not None, "Hindi proverb not found"
        assert result['language'] == 'Hindi'

    def test_marathi_proverb_lookup(self):
        """find_proverb should find a Marathi proverb by script."""
        result = find_proverb('दुरून डोंगर साजरे', 'Marathi')
        assert result is not None, "Marathi proverb not found"
        assert result['language'] == 'Marathi'

    def test_nonexistent_proverb_returns_none(self):
        """find_proverb should return None for unknown text."""
        result = find_proverb('this is not a proverb', 'Gujarati')
        assert result is None


class TestCrossLanguageEquivalents:

    def test_marathi_to_gujarati_equivalent(self):
        """दुरून डोंगर साजरे should return Gujarati equivalent દૂરથી ડુંગર રળિયામણા."""
        result = find_proverb('दुरून डोंगर साजरे', 'Marathi', 'Gujarati')
        assert result is not None
        assert result['target_equivalent'] is not None, "No Gujarati equivalent found"
        assert 'દૂરથી ડુંગર રળિયામણા' in result['target_equivalent']['equivalent_script'], \
            f"Wrong equivalent: {result['target_equivalent']['equivalent_script']}"

    def test_marathi_to_hindi_equivalent(self):
        """दुरून डोंगर साजरे should return Hindi equivalent दूर के ढोल सुहावने."""
        result = find_proverb('दुरून डोंगर साजरे', 'Marathi', 'Hindi')
        assert result is not None
        assert result['target_equivalent'] is not None
        assert 'दूर के ढोल सुहावने' in result['target_equivalent']['equivalent_script']

    def test_gujarati_to_hindi_equivalent(self):
        """ટીપે ટીપે સરોવર ભરાય should return Hindi equivalent बूंद बूंद से सागर भरता है."""
        result = find_proverb('ટીપે ટીપે સરોવર ભરાય', 'Gujarati', 'Hindi')
        assert result is not None
        assert result['target_equivalent'] is not None
        assert 'बूंद बूंद से सागर भरता है' in result['target_equivalent']['equivalent_script']

    def test_gujarati_to_marathi_equivalent(self):
        """ટીપે ટીપે સરોવર ભરાય should return Marathi equivalent थेंबे थेंबे तळे साचे."""
        result = find_proverb('ટીપે ટીપે સરોવર ભરાય', 'Gujarati', 'Marathi')
        assert result is not None
        assert result['target_equivalent'] is not None
        assert 'थेंबे थेंबे तळे साचे' in result['target_equivalent']['equivalent_script']

    def test_hindi_to_gujarati_equivalent(self):
        """एक हाथ से ताली नहीं बजती should return Gujarati equivalent."""
        result = find_proverb('एक हाथ से ताली नहीं बजती', 'Hindi', 'Gujarati')
        assert result is not None
        assert result['target_equivalent'] is not None
        assert 'એક હાથે તાળી ન પડે' in result['target_equivalent']['equivalent_script']

    def test_no_equivalent_returns_none_target(self):
        """Proverb without a cross-language mapping should return None for target_equivalent."""
        result = find_proverb('ધૈર્ય ફળ આપે છે', 'Gujarati', 'Hindi')
        assert result is not None
        assert result.get('target_equivalent') is None


# ─────────────────────────────────────────
# 2. API ENDPOINT TESTS
# ─────────────────────────────────────────

class TestHomeRoute:

    def test_home_returns_200(self, client):
        """Home page should return 200."""
        response = client.get('/')
        assert response.status_code == 200

    def test_home_returns_html(self, client):
        """Home page should return HTML content."""
        response = client.get('/')
        assert b'html' in response.data.lower() or response.content_type == 'text/html; charset=utf-8'


class TestTranslateEndpoint:

    def test_translate_returns_200(self, client):
        """Translate endpoint should return 200 for valid input."""
        response = client.post('/translate',
            data=json.dumps({
                'text': 'Hello',
                'source_lang': 'English',
                'target_lang': 'Hindi'
            }),
            content_type='application/json'
        )
        assert response.status_code == 200

    def test_translate_returns_translation_field(self, client):
        """Response should contain a translation field."""
        response = client.post('/translate',
            data=json.dumps({
                'text': 'Good morning',
                'source_lang': 'English',
                'target_lang': 'Gujarati'
            }),
            content_type='application/json'
        )
        data = json.loads(response.data)
        assert 'translation' in data
        assert len(data['translation']) > 0

    def test_translate_returns_romanised_field(self, client):
        """Response should contain a romanised field for Indian languages."""
        response = client.post('/translate',
            data=json.dumps({
                'text': 'Thank you',
                'source_lang': 'English',
                'target_lang': 'Marathi'
            }),
            content_type='application/json'
        )
        data = json.loads(response.data)
        assert 'romanised' in data

    def test_translate_returns_cultural_note(self, client):
        """Response should contain a cultural_note field."""
        response = client.post('/translate',
            data=json.dumps({
                'text': 'How are you',
                'source_lang': 'English',
                'target_lang': 'Hindi'
            }),
            content_type='application/json'
        )
        data = json.loads(response.data)
        assert 'cultural_note' in data

    def test_empty_text_returns_400(self, client):
        """Empty input should return 400 error."""
        response = client.post('/translate',
            data=json.dumps({
                'text': '',
                'source_lang': 'English',
                'target_lang': 'Hindi'
            }),
            content_type='application/json'
        )
        assert response.status_code == 400

    def test_same_language_returns_400(self, client):
        """Same source and target language should return 400."""
        response = client.post('/translate',
            data=json.dumps({
                'text': 'Hello',
                'source_lang': 'Hindi',
                'target_lang': 'Hindi'
            }),
            content_type='application/json'
        )
        assert response.status_code == 400

    def test_all_nine_languages_accepted(self, client):
        """All nine supported languages should be accepted without error."""
        languages = ['English', 'Hindi', 'Gujarati', 'Marathi', 'Tamil', 'Telugu', 'Spanish', 'German', 'Japanese']
        for lang in languages:
            if lang != 'English':
                response = client.post('/translate',
                    data=json.dumps({
                        'text': 'Hello',
                        'source_lang': 'English',
                        'target_lang': lang
                    }),
                    content_type='application/json'
                )
                assert response.status_code == 200, f"Failed for language: {lang}"


class TestFeedbackEndpoint:

    def test_feedback_returns_success(self, client):
        """Feedback endpoint should return success for valid input."""
        response = client.post('/feedback',
            data=json.dumps({
                'source_lang': 'English',
                'target_lang': 'Hindi',
                'input_text': 'Hello',
                'translation': 'नमस्ते',
                'rating': 'good',
                'comment': 'Great translation!'
            }),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data.get('success') is True

    def test_feedback_bad_rating_stored(self, client):
        """Negative feedback should also be stored successfully."""
        response = client.post('/feedback',
            data=json.dumps({
                'source_lang': 'English',
                'target_lang': 'Marathi',
                'input_text': 'My name is Amit',
                'translation': 'माझे नाव अमित आहे',
                'rating': 'bad',
                'comment': 'Should be माझं not माझे'
            }),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data.get('success') is True


class TestDashboardRoute:

    def test_dashboard_returns_200(self, client):
        """Dashboard should return 200."""
        response = client.get('/dashboard')
        assert response.status_code == 200

    def test_dashboard_returns_html(self, client):
        """Dashboard should return HTML."""
        response = client.get('/dashboard')
        assert response.content_type == 'text/html; charset=utf-8'


# ─────────────────────────────────────────
# 3. TRANSLATION QUALITY TESTS
# ─────────────────────────────────────────

class TestTranslationQuality:

    def test_gujarati_proverb_not_literal(self, client):
        """મૂળ કરતા વ્યાજ વહાલું should not be translated as a finance proverb."""
        response = client.post('/translate',
            data=json.dumps({
                'text': 'મૂળ કરતા વ્યાજ વહાલું',
                'source_lang': 'Gujarati',
                'target_lang': 'English'
            }),
            content_type='application/json'
        )
        data = json.loads(response.data)
        translation = data.get('translation', '').lower()
        note = data.get('cultural_note', '').lower()
        combined = translation + ' ' + note
        assert 'interest' not in combined[:50] or 'grandp' in combined or 'grandchildren' in combined, \
            "Proverb is being translated as a finance term"

    def test_marathi_cross_language_proverb(self, client):
        """दुरून डोंगर साजरे translated to Gujarati should return the Gujarati equivalent."""
        response = client.post('/translate',
            data=json.dumps({
                'text': 'दुरून डोंगर साजरे',
                'source_lang': 'Marathi',
                'target_lang': 'Gujarati'
            }),
            content_type='application/json'
        )
        data = json.loads(response.data)
        translation = data.get('translation', '')
        assert 'દૂરથી ડુંગર રળિયામણા' in translation, \
            f"Expected Gujarati equivalent proverb, got: {translation}"

    def test_english_to_hindi_not_empty(self, client):
        """English to Hindi translation should not be empty."""
        response = client.post('/translate',
            data=json.dumps({
                'text': 'My name is Amit',
                'source_lang': 'English',
                'target_lang': 'Hindi'
            }),
            content_type='application/json'
        )
        data = json.loads(response.data)
        assert len(data.get('translation', '')) > 0

    def test_english_to_marathi_uses_mazha(self, client):
        """'My name is Amit' in Marathi should use माझं (casual) not माझे (formal)."""
        response = client.post('/translate',
            data=json.dumps({
                'text': 'My name is Amit',
                'source_lang': 'English',
                'target_lang': 'Marathi'
            }),
            content_type='application/json'
        )
        data = json.loads(response.data)
        translation = data.get('translation', '')
        assert 'माझं' in translation, \
            f"Expected casual माझं, got: {translation}"

    def test_romanised_output_not_empty_for_indian_languages(self, client):
        """Romanised field should not be empty for Indian language translations."""
        for lang in ['Hindi', 'Gujarati', 'Marathi']:
            response = client.post('/translate',
                data=json.dumps({
                    'text': 'Good morning',
                    'source_lang': 'English',
                    'target_lang': lang
                }),
                content_type='application/json'
            )
            data = json.loads(response.data)
            assert len(data.get('romanised', '')) > 0, \
                f"Romanised output empty for {lang}"

    def test_english_output_has_no_romanised(self, client):
        """Translating TO English should return empty romanised field."""
        response = client.post('/translate',
            data=json.dumps({
                'text': 'नमस्ते',
                'source_lang': 'Hindi',
                'target_lang': 'English'
            }),
            content_type='application/json'
        )
        data = json.loads(response.data)
        romanised = data.get('romanised', '')
        assert romanised == '' or romanised.upper() == 'NONE', \
            f"Expected empty romanised for English output, got: {romanised}"
