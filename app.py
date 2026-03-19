from flask import Flask, request, jsonify, render_template
from anthropic import Anthropic
from dotenv import load_dotenv
from database import init_db, find_proverb, log_feedback, log_usage, get_stats, get_recent_feedback, get_recent_translations
import os
import requests
import base64

load_dotenv()

app = Flask(__name__)
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

init_db()

SYSTEM_PROMPT = """You are an expert translator specialising in nine languages — English, Hindi, Gujarati, Marathi, Tamil, Telugu, Spanish, German, and Japanese. You are a native speaker of Hindi, Gujarati, Marathi, Tamil, and Telugu and understand that these are completely separate languages with distinct vocabulary, grammar, cultural expressions, and identities. You are also highly fluent and culturally aware in English, Spanish, German, and Japanese.

You support translation in all directions between all nine languages — any combination, any direction.

Follow these rules strictly:

1. NEVER translate word for word. Always translate meaning, tone, and cultural intent. This applies whether input is in native script or Romanised English letters — always interpret the most natural everyday meaning first. Always prioritise natural conversational output over accurate literal output. A slightly loose but natural translation is always better than a precise but robotic one.

2. When translating FROM Gujarati, NEVER use Hindi, Marathi, Tamil or Telugu words. Always use pure natural Gujarati-origin expressions.

3. When translating FROM Hindi, NEVER use Gujarati, Marathi, Tamil or Telugu words. Keep output authentically Hindi.

4. When translating FROM Marathi, NEVER use Hindi, Gujarati, Tamil or Telugu words. Use pure natural Marathi expressions. When translating Marathi TO English, make it warm, conversational and natural.

5. When translating FROM Tamil, NEVER use Hindi, Gujarati, Marathi or Telugu words. Use pure natural Tamil expressions that a native Tamil speaker would actually say in conversation.

6. When translating FROM Telugu, NEVER use Hindi, Gujarati, Marathi or Tamil words. Use pure natural Telugu expressions that a native Telugu speaker would actually say in conversation.

7. When translating TO English or Spanish, your output must sound exactly like something a fluent native speaker would naturally say out loud in casual conversation — warm, natural, human, and colloquial. Never write an explanation of what the original means. Never write something that sounds like a dictionary or a textbook. Ask yourself — would a real person actually say this in conversation? If not, rewrite it until they would. For proverbs and idioms specifically, give a single punchy natural equivalent — not a description of the meaning.

8. For idioms, proverbs, slang, or culturally specific expressions in ANY language — NEVER translate literally under any circumstances. Always identify if the input is a proverb or idiom first, then find the closest natural equivalent in the target language that captures the same life lesson, humour, or emotion.

9. Always preserve warmth, tone, emotion, and cultural meaning.

10. Smart word handling: Use native words where commonly used. Keep globally borrowed words as they naturally appear in everyday speech (cheese, pizza, coffee, chocolate etc).

11. Romanised input: Interpret Romanised input by most common everyday meaning. Common examples — baddha/badha = everyone in Gujarati, kem cho = how are you in Gujarati, majama = doing well, pani = water, naan = bread, amma = mother in Tamil/Telugu.

12. Never blend vocabulary between any of the nine languages.

13. Always follow the user's stated language direction exactly. Never default to another language.

14. Gujarati Proverb Knowledge: When you encounter a Gujarati proverb, identify its real meaning based on cultural knowledge, not literal translation. Key example — બોલે તેના બોર વેચાય means the person who speaks up and advocates confidently will succeed. The meaning is about self-promotion leading to success. Natural English equivalent — speak up and you will get ahead. Use this same deep cultural reasoning for all proverbs across all nine languages.

15. Pronoun Preservation: Always preserve explicit gender pronouns from the source text exactly. If the source text uses "she" or "her", use the feminine form in the target language. If the source text uses "he" or "him", use the masculine form. Never neutralise or change an explicit gendered pronoun to a gender-neutral form. Only use gender-neutral pronouns if the source text itself uses them.

16. Register Matching: Always match the register and tone of the source text. Use natural spoken forms — but always preserve the full sentence structure of the original. Do not strip sentences down to bare fragments. The goal is natural-sounding language, not minimal language.

Key examples by language:
- Marathi: Use contracted possessives — माझं (not माझे), तुझं (not तुझे), आमचं (not आमचे), तुमचं (not तुमचे). So "My name is Amit" = माझं नाव अमित आहे — full sentence, soft possessive. Never reduce to मी अमित which sounds abrupt and incomplete.
- Hindi: Use the natural full sentence form — "My name is Amit" = मेरा नाम अमित है. This is already the natural everyday Hindi. Do not reduce to मैं अमित हूँ which strips the sentence unnecessarily.
- Gujarati: Prefer spoken contractions and natural everyday forms over written/formal ones, while keeping the full sentence structure intact.
- Tamil and Telugu: Use the informal spoken register for casual input, not the formal written register, while preserving full sentence structure.

Before outputting, always ask: does this sound like how a real native speaker would naturally say this in conversation — with the full meaning intact? If it sounds robotic or overly formal, use softer spoken forms. If it sounds too clipped or incomplete, restore the full sentence.

17. Content Guardrails: Tongues is a cultural translation app for everyone. If the input contains any of the following, do NOT translate it. Instead respond with exactly this and nothing else: "This content cannot be translated. Tongues is a cultural translation app — please keep it respectful."

Block the following:
- Hate speech, casteist slurs, communal slurs, racial slurs, or language targeting any religion, caste, ethnicity, or community
- Sexual or explicit content of any kind
- Threats, violent language, or content inciting harm against any person or group
- Deeply offensive slurs in any of the nine supported languages

Do NOT block:
- Mild everyday language or casual expressions
- Proverbs or idioms that may sound edgy but are culturally valid
- Words that are only offensive in some contexts but are being used neutrally
- Common crude idioms and colloquial expressions that describe emotions or situations (e.g. "shitting in my pants" meaning terrified, "balls" meaning courage, "ass" in everyday use, "damn", "hell", "crap", "bloody") — these are valid everyday language and must be translated naturally
- Any expression where the intent is clearly emotional, humorous, or descriptive rather than hateful or sexual

Always respond in EXACTLY this format — no exceptions:

TRANSLATION:
[Your clean, natural translation here in the target language script]

ROMANISED:
[If the translation is in any non-English language including Hindi, Gujarati, Marathi, Tamil, Telugu, Spanish, German, or Japanese, provide a Romanised phonetic version here using simple English letters so that someone who speaks the language but cannot read the script can read it aloud naturally. Keep it simple and phonetic — write it exactly as it sounds. If the translation is in English, write NONE here.]

CULTURAL_NOTE:
[One or two sentences on tone, cultural meaning, or nuance]

ALTERNATIVES:
[Provide 2-3 alternative translations only when there are meaningfully different options — for example a more formal version, a more casual version, a regional variant, or an idiomatic alternative. Format each alternative on its own line as: LABEL | translation text. Example: Formal | वह बहुत साहसी है. Labels should be short and descriptive — Formal, Casual, Idiomatic, Regional, Literal, More expressive, Softer tone, Stronger emphasis etc. If there are no meaningful alternatives, write NONE here.]"""


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()

    text = data.get('text', '').strip()
    source_lang = data.get('source_lang', 'English')
    target_lang = data.get('target_lang', 'Hindi')

    if not text:
        return jsonify({'error': 'Please enter some text to translate'}), 400

    if source_lang == target_lang:
        return jsonify({'error': 'Please select two different languages'}), 400

    try:
        proverb_match = find_proverb(text, source_lang, target_lang)

        user_message = f"Translate from {source_lang} to {target_lang}: {text}"

        if proverb_match:
            if proverb_match.get('target_equivalent'):
                equiv = proverb_match['target_equivalent']
                user_message += f"\n\nNote: This is a known {source_lang} proverb. Its real meaning is: {proverb_match['real_meaning']}. There is a natural {target_lang} equivalent proverb: {equiv['equivalent_script']} ({equiv['equivalent_romanised']}). Use this equivalent proverb as your translation — do not translate literally."
            else:
                user_message += f"\n\nNote: This is a known {source_lang} proverb. Its real meaning is: {proverb_match['real_meaning']}. Natural English equivalent: {proverb_match['english_equivalent']}. Use this cultural knowledge in your translation."

        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_message}]
        )

        full_response = response.content[0].text

        # Guardrail check — if Claude returned the content warning, surface it as 400
        if 'This content cannot be translated' in full_response:
            return jsonify({'error': 'This content cannot be translated. Tongues is a cultural translation app — please keep it respectful.'}), 400

        lines = full_response.split('\n')
        translation_lines = []
        romanised_lines = []
        note_lines = []
        alternatives_lines = []
        mode = None

        for line in lines:
            upper = line.strip().upper()
            if upper.startswith('TRANSLATION:'):
                mode = 'translation'
                rest = line.replace('TRANSLATION:', '').replace('translation:', '').strip()
                if rest:
                    translation_lines.append(rest)
            elif upper.startswith('ROMANISED:'):
                mode = 'romanised'
                rest = line.replace('ROMANISED:', '').replace('romanised:', '').strip()
                if rest:
                    romanised_lines.append(rest)
            elif upper.startswith('CULTURAL_NOTE:'):
                mode = 'note'
                rest = line.replace('CULTURAL_NOTE:', '').replace('cultural_note:', '').strip()
                if rest:
                    note_lines.append(rest)
            elif upper.startswith('ALTERNATIVES:'):
                mode = 'alternatives'
                rest = line.replace('ALTERNATIVES:', '').replace('alternatives:', '').strip()
                if rest:
                    alternatives_lines.append(rest)
            elif mode == 'translation' and line.strip():
                translation_lines.append(line)
            elif mode == 'romanised' and line.strip():
                romanised_lines.append(line)
            elif mode == 'note' and line.strip():
                note_lines.append(line)
            elif mode == 'alternatives' and line.strip():
                alternatives_lines.append(line)

        translation = '\n'.join(translation_lines).strip() or full_response.strip()
        romanised = '\n'.join(romanised_lines).strip()
        cultural_note = '\n'.join(note_lines).strip()

        if romanised.upper() == 'NONE':
            romanised = ''

        # Parse alternatives into structured list
        alternatives = []
        raw_alts = '\n'.join(alternatives_lines).strip()
        if raw_alts and raw_alts.upper() != 'NONE':
            for alt_line in raw_alts.split('\n'):
                alt_line = alt_line.strip()
                if '|' in alt_line:
                    parts = alt_line.split('|', 1)
                    label = parts[0].strip().lstrip('-').strip()
                    text_alt = parts[1].strip()
                    if label and text_alt:
                        alternatives.append({'label': label, 'text': text_alt})

        log_usage(source_lang, target_lang, len(text), True)

        return jsonify({
            'translation': translation,
            'romanised': romanised,
            'cultural_note': cultural_note,
            'input_text': text,
            'alternatives': alternatives
        })

    except Exception as e:
        log_usage(source_lang, target_lang, len(text), False)
        return jsonify({'error': str(e)}), 500


@app.route('/tts', methods=['POST'])
def tts():
    data = request.get_json()
    text = data.get('text', '').strip()
    language = data.get('language', 'English')

    if not text:
        return jsonify({'error': 'No text provided'}), 400

    # Map Tongues language names to Google Cloud TTS language codes and voices
    voice_map = {
        'English':  {'languageCode': 'en-US', 'name': 'en-US-Neural2-F'},
        'Hindi':    {'languageCode': 'hi-IN', 'name': 'hi-IN-Neural2-A'},
        'Gujarati': {'languageCode': 'gu-IN', 'name': 'gu-IN-Standard-A'},
        'Marathi':  {'languageCode': 'mr-IN', 'name': 'mr-IN-Standard-A'},
        'Tamil':    {'languageCode': 'ta-IN', 'name': 'ta-IN-Neural2-A'},
        'Telugu':   {'languageCode': 'te-IN', 'name': 'te-IN-Standard-A'},
        'Spanish':  {'languageCode': 'es-ES', 'name': 'es-ES-Neural2-A'},
        'German':   {'languageCode': 'de-DE', 'name': 'de-DE-Neural2-A'},
        'Japanese': {'languageCode': 'ja-JP', 'name': 'ja-JP-Neural2-B'},
    }

    voice = voice_map.get(language, voice_map['English'])
    api_key = os.getenv('GOOGLE_TTS_API_KEY')

    if not api_key:
        return jsonify({'error': 'TTS not configured'}), 500

    try:
        response = requests.post(
            f'https://texttospeech.googleapis.com/v1/text:synthesize?key={api_key}',
            json={
                'input': {'text': text},
                'voice': voice,
                'audioConfig': {'audioEncoding': 'MP3', 'speakingRate': 0.9}
            }
        )
        response.raise_for_status()
        audio_content = response.json().get('audioContent', '')
        return jsonify({'audio': audio_content})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/feedback', methods=['POST'])
def feedback():
    data = request.get_json()
    log_feedback(
        data.get('source_lang'),
        data.get('target_lang'),
        data.get('input_text'),
        data.get('translation'),
        data.get('rating'),
        data.get('comment', '')
    )
    return jsonify({'success': True})


@app.route('/proverb-of-the-day')
def proverb_of_the_day():
    from database import get_db
    from datetime import date
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) as total FROM proverbs')
    total = cursor.fetchone()['total']
    if total == 0:
        conn.close()
        return jsonify({'error': 'No proverbs found'}), 404
    # Use today's date as seed so same proverb shows all day
    day_index = date.today().toordinal() % total
    cursor.execute('SELECT * FROM proverbs LIMIT 1 OFFSET ?', (day_index,))
    row = cursor.fetchone()
    conn.close()
    return jsonify(dict(row))


@app.route('/dashboard')
def dashboard():
    stats = get_stats()
    recent_feedback = get_recent_feedback()
    recent_translations = get_recent_translations()
    return render_template('dashboard.html',
                           stats=stats,
                           recent_feedback=recent_feedback,
                           recent_translations=recent_translations)


if __name__ == '__main__':
    app.run(debug=True)
