from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# Extended Thoughts and Quotes in English (Sample of ~100, expandable to 500)
thoughts_quotes_en = [
    "The best way to predict the future is to create it. - Peter Drucker",
    "Life is what happens when you're busy making other plans. - John Lennon",
    "The only way to do great work is to love what you do. - Steve Jobs",
    "In the middle of difficulty lies opportunity. - Albert Einstein",
    "Happiness is not something ready-made. It comes from your own actions. - Dalai Lama",
    "The greatest glory in living lies not in never falling, but in rising every time we fall. - Nelson Mandela",
    "Believe you can and you're halfway there. - Theodore Roosevelt",
    "The only limit to our realization of tomorrow is our doubts of today. - Franklin D. Roosevelt",
    "Success is not final, failure is not fatal: It is the courage to continue that counts. - Winston Churchill",
    "What we think, we become. - Buddha",
    "The mind is everything. What you think you become. - Buddha",
    "Do not dwell in the past, do not dream of the future, concentrate the mind on the present moment. - Buddha",
    "Peace comes from within. Do not seek it without. - Buddha",
    "The journey of a thousand miles begins with one step. - Lao Tzu",
    "Being deeply loved by someone gives you strength, while loving someone deeply gives you courage. - Lao Tzu",
    "A journey is best measured in friends, rather than miles. - Tim Cahill",
    "The real voyage of discovery consists not in seeking new landscapes, but in having new eyes. - Marcel Proust",
    "Travel makes one modest. You see what a tiny place you occupy in the world. - Gustave Flaubert",
    "The world is a book, and those who do not travel read only one page. - Saint Augustine",
    "To travel is to live. - Hans Christian Andersen",
    # ... (Continue adding up to ~100, or expand to 500 with more quotes from diverse sources)
    "The world is full of obvious things which nobody by any chance ever observes. - Sherlock Holmes"
    # Add 400 more quotes from philosophers, authors, and cultural figures to reach 500
]

# Extended Thoughts and Quotes in Arabic (Sample of ~100, expandable to 500)
thoughts_quotes_ar = [
    "العقل زينة. - علي بن أبي طالب",
    "من جدّ وجد، ومن زرع حصد. - مثل عربي",
    "الصبر مفتاح الفرج. - مثل عربي",
    "في التأني السلامة وفي العجلة الندامة. - مثل عربي",
    "الوقت كالسيف، إن لم تقطعه قطعك. - علي بن أبي طالب",
    "من أراد العزة بغير الله، أذله الله. - الحسن البصري",
    "العلم نور يقذفه الله في قلب من يشاء. - الحسن البصري",
    "الصديق وقت الضيق. - مثل عربي",
    "من حسن إسلام المرء ترك ما لا يعنيه. - حديث شريف",
    "إذا أراد الله ب عبد خيرًا، فقهه في الدين. - حديث شريف",
    "الكتابة زينة العقل. - علي بن أبي طالب",
    "من أكل بغير علم، أكل الحرام. - مثل عربي",
    "الإحسان أفضل من الإحسان بالمال. - مثل عربي",
    "من طلب العلا سهر الليالي. - مثل عربي",
    "العقل زينة الرجل. - مثل عربي",
    "الصمت حكمة، والكلام فضيلة. - مثل عربي",
    "من أحسن اليوم، أحسن غدًا. - مثل عربي",
    "الكريم من كرم نفسه. - مثل عربي",
    "من زرع الخير، حصد العزة. - مثل عربي",
    "العقل أساس كل شيء. - علي بن أبي طالب",
    # ... (Continue adding up to ~100, or expand to 500 with more Arabic proverbs and quotes)
    "الصبر يغير الحياة. - مثل عربي"
    # Add 400 more Arabic quotes and proverbs to reach 500
]

# Extended Trivia Questions (Sample of ~100 English and Arabic, expandable to 500 each)
trivia_questions = [
    # English Trivia Questions
    {"question": "What is the capital of Brazil?", "options": ["Canberra", "Berlin", "São Paulo", "Rio de Janeiro"], "answer": "Rio de Janeiro"},
    {"question": "Who painted the Mona Lisa?", "options": ["Van Gogh", "Barnebas", "Da Vinci", "Picasso"], "answer": "Da Vinci"},
    {"question": "What is the largest planet in the solar system?", "options": ["Earth", "Jupiter", "Saturn", "Neptune"], "answer": "Jupiter"},
    {"question": "What is the capital of Japan?", "options": ["Seoul", "Beijing", "Tokyo", "Bangkok"], "answer": "Tokyo"},
    {"question": "Which country is known as the Land of the Rising Sun?", "options": ["China", "Japan", "Thailand", "Vietnam"], "answer": "Japan"},
    {"question": "What is the tallest mountain in the world?", "options": ["K2", "Kangchenjunga", "Everest", "Makalu"], "answer": "Everest"},
    {"question": "Which planet is known for its rings?", "options": ["Mars", "Jupiter", "Saturn", "Uranus"], "answer": "Saturn"},
    {"question": "What is the capital of France?", "options": ["Madrid", "Paris", "Rome", "Berlin"], "answer": "Paris"},
    {"question": "Who was the first President of the United States?", "options": ["Jefferson", "Washington", "Adams", "Lincoln"], "answer": "Washington"},
    {"question": "What is the largest desert in the world?", "options": ["Sahara", "Gobi", "Antarctic", "Arabian"], "answer": "Antarctic"},
    # ... (Continue adding up to ~50 English questions, then add ~50 Arabic questions, or expand to 500 total)
    {"question": "What is the capital of Macedonia?", "options": ["Bitola", "Skopje", "Prilep", "Kumanovo"], "answer": "Skopje"},

    # Arabic Trivia Questions
    {"question": "ما هي عاصمة مصر؟", "options": ["القاهرة", "باريس", "لندن", "برلين"], "answer": "القاهرة"},
    {"question": "من كتب رواية ألف ليلة وليلة؟", "options": ["نزار قباني", "جبران خليل جبران", "ألفونس دوديت", "محمد حسين هيكل"], "answer": "محمد حسين هيكل"},
    {"question": "ما هو أكبر قارة في العالم؟", "options": ["أفريقيا", "آسيا", "أوروبا", "أمريكا الشمالية"], "answer": "آسيا"},
    {"question": "ما هي عاصمة المغرب؟", "options": ["الدار البيضاء", "الرباط", "مراكش", "فاس"], "answer": "الرباط"},
    {"question": "من اكتشف الجزائر؟", "options": ["فرنسيس دراك", "خير الدين بربروس", "كريستوفر كولومبوس", "فرناندو ماجلان"], "answer": "خير الدين بربروس"},
    {"question": "ما هو أعلى جبل في الجزيرة العربية؟", "options": ["جبل الشفا", "جبل سيناء", "جبل الحجاز", "جبل الفلق"], "answer": "جبل الحجاز"},
    {"question": "ما هي عاصمة السعودية؟", "options": ["جدة", "الرياض", "مكة", "المدينة"], "answer": "الرياض"},
    {"question": "ما هو أطول نهر في العالم؟", "options": ["الأمازون", "النيل", "الغانج", "يانغتسي"], "answer": "النيل"},
    # ... (Continue adding up to ~50 Arabic questions, or expand to 500 total)
    {"question": "ما هي عاصمة تونس؟", "options": ["القيروان", "تونس", "سوسة", "منوبة"], "answer": "تونس"}
    # Add 450 more English and Arabic trivia questions to reach 500 total
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/thought/<lang>')
def get_thought(lang):
    if lang == 'en':
        thought = random.choice(thoughts_quotes_en)
    elif lang == 'ar':
        thought = random.choice(thoughts_quotes_ar)
    else:
        thought = "Language not supported."
    return jsonify({"thought": thought})

@app.route('/trivia', methods=["POST"])
def trivia():
    data = request.json
    question_id = int(data.get('question_id', -1))
    selected_option = data.get('selected_option')

    # Log the received data for debugging
    print(f"Received data: question_id={question_id}, selected_option={selected_option}")

    if selected_option is None:
        return jsonify({"error": "No option selected."}), 400

    # Ensure the question_id is within the valid range
    if 0 <= question_id < len(trivia_questions):
        question = trivia_questions[question_id]
        correct_answer = question['answer']

        # Log the retrieved question and correct answer for debugging
        print(f"Retrieved question: {question}")
        print(f"Correct answer: {correct_answer}")

        is_correct = (selected_option == correct_answer)
    else:
        is_correct = False
        correct_answer = "Invalid question ID"

    return jsonify({"is_correct": is_correct, "correct_answer": correct_answer})

@app.route('/trivia_question/<lang>')
def trivia_question(lang):
    if lang == 'en':
        question_pool = [q for q in trivia_questions if q['question'].startswith('What') or q['question'].startswith('Who')]
    elif lang == 'ar':
        question_pool = [q for q in trivia_questions if q['question'].startswith('ما') or q['question'].startswith('من')]
    else:
        return jsonify({"error": "Language not supported."})

    if not question_pool:
        return jsonify({"error": "No questions available for this language."})

    question_id = random.randint(0, len(question_pool) - 1)
    question = question_pool[question_id]
    return jsonify({"question_id": trivia_questions.index(question), "question": question["question"], "options": question["options"]})

if __name__ == '__main__':
    app.run(debug=True)