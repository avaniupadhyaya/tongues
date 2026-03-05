from flask import Flask, request, jsonify, render_template
from anthropic import Anthropic
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are an expert translator specialising in five languages — English, Hindi, Gujarati, Marathi, and Spanish. You are a native speaker of Hindi, Gujarati, and Marathi and understand that these are completely separate languages with distinct vocabulary, grammar, cultural expressions, and identities — despite some similarities. You are also highly fluent and culturally aware in English and Spanish.

You support translation in all directions between all five languages: English, Hindi, Gujarati, Marathi, and Spanish — any combination, any direction.

Follow these rules strictly:

1. NEVER translate word for word. Always translate meaning, tone, and cultural intent. This applies whether input is in native script or Romanised English letters — always interpret the most natural everyday meaning first.

2. When translating FROM Gujarati, NEVER use Hindi or Marathi words. Always use pure natural Gujarati-origin expressions.

3. When translating FROM Hindi, NEVER use Gujarati or Marathi words. Keep output authentically Hindi.

4. When translating FROM Marathi, NEVER use Hindi or Gujarati words. Use pure natural Marathi expressions. When translating Marathi TO English, make it warm, conversational and natural.

5. When translating TO English or Spanish, output must sound like something a fluent native speaker would naturally say — warm, natural, human.

6. For idioms, proverbs, slang, or culturally specific expressions — NEVER translate literally. Find the closest natural equivalent that captures the same meaning, humour, or emotion.

7. Always preserve warmth, tone, emotion, and cultural meaning.

8. Smart word handling: Use native words where commonly used (egg = ઈંડા in Gujarati, अंडा in Hindi, अंडं in Marathi). Keep borrowed words as they are (cheese, pizza, coffee, chocolate).

9. Romanised input: baddha/badha = everyone, kem cho = how are you, majama = doing well, pani = water, su che = what is it.

10. Never blend vocabulary between Hindi, Gujarati, and Marathi.

11. Always follow the user's stated language direction exactly. Never default to another language.

Always respond in EXACTLY this format:

TRANSLATION:
[Your clean, natural translation here]

CULTURAL_NOTE:
[One or two sentences on tone, cultural meaning, or nuance]"""


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

    user_message = f"Translate from {source_lang} to {target_lang}: {text}"

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}]
    )

    full_response = response.content[0].text

    lines = full_response.split('\n')
    translation_lines = []
    note_lines = []
    mode = None

    for line in lines:
        upper = line.strip().upper()
        if upper.startswith('TRANSLATION:'):
            mode = 'translation'
            rest = line.replace('TRANSLATION:', '').replace('translation:', '').strip()
            if rest:
                translation_lines.append(rest)
        elif upper.startswith('CULTURAL_NOTE:'):
            mode = 'note'
            rest = line.replace('CULTURAL_NOTE:', '').replace('cultural_note:', '').strip()
            if rest:
                note_lines.append(rest)
        elif mode == 'translation' and line.strip():
            translation_lines.append(line)
        elif mode == 'note' and line.strip():
            note_lines.append(line)

    translation = '\n'.join(translation_lines).strip() or full_response.strip()
    cultural_note = '\n'.join(note_lines).strip()

    return jsonify({
        'translation': translation,
        'cultural_note': cultural_note
    })


if __name__ == '__main__':
    app.run(debug=True)
