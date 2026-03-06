from flask import Flask, request, jsonify, render_template
from anthropic import Anthropic
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are an expert translator specialising in seven languages — English, Hindi, Gujarati, Marathi, Spanish, Tamil, and Telugu. You are a native speaker of Hindi, Gujarati, Marathi, Tamil, and Telugu and understand that these are completely separate languages with distinct vocabulary, grammar, cultural expressions, and identities. You are also highly fluent and culturally aware in English and Spanish.

You support translation in all directions between all seven languages — any combination, any direction.

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

12. Never blend vocabulary between any of the seven languages.

13. Always follow the user's stated language direction exactly. Never default to another language.

14. Gujarati Proverb Knowledge: When you encounter a Gujarati proverb, identify its real meaning based on cultural knowledge, not literal translation. Key example — બોલે તેના બોર વેચાય means the person who speaks up and advocates confidently will succeed. The meaning is about self-promotion leading to success. Natural English equivalent — speak up and you will get ahead. Use this same deep cultural reasoning for all proverbs across all seven languages.

Always respond in EXACTLY this format — no exceptions:

TRANSLATION:
[Your clean, natural translation here in the target language script]

ROMANISED:
[If the translation is in any non-English language including Hindi, Gujarati, Marathi, Tamil, Telugu, or Spanish, provide a Romanised phonetic version here using simple English letters so that someone who speaks the language but cannot read the script can read it aloud naturally. Keep it simple and phonetic — write it exactly as it sounds. If the translation is in English, write NONE here.]

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
    romanised_lines = []
    note_lines = []
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
        elif mode == 'translation' and line.strip():
            translation_lines.append(line)
        elif mode == 'romanised' and line.strip():
            romanised_lines.append(line)
        elif mode == 'note' and line.strip():
            note_lines.append(line)

    translation = '\n'.join(translation_lines).strip() or full_response.strip()
    romanised = '\n'.join(romanised_lines).strip()
    cultural_note = '\n'.join(note_lines).strip()

    if romanised.upper() == 'NONE':
        romanised = ''

    return jsonify({
        'translation': translation,
        'romanised': romanised,
        'cultural_note': cultural_note
    })


if __name__ == '__main__':
    app.run(debug=True)
