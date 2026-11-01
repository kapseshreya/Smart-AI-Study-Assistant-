import streamlit as st
import random
import pandas as pd
import json
import os

# ----------------- Page Config -----------------
st.set_page_config(page_title="Smart AI Study Assistant", layout="wide")

# ----------------- Data -----------------
study_data = {
    "Physics": {
        "laser": "LASER stands for Light Amplification by Stimulated Emission of Radiation.",
        "spontaneous emission": "Spontaneous emission is the process in which an excited atom emits a photon without external influence.",
        "stimulated emission": "Stimulated emission occurs when an incoming photon causes an excited atom to emit another photon.",
        "Active System": "A system in which the population inversion takes place is called as active system.",
        "Properties of laser": "Coherence, Directionality, Polarization, Intensity, Monochromaticity.",
        "Numerical Aperture": "Numerical aperture is the light gathering capacity or ability of an optical fiber.",
        "Types of Attenuation": "Intrinsic attenuation, Extrinsic attenuation",
    },
    "Chemistry": {
        "What is corrosion": "Corrosion is the gradual destruction of metals by chemical reactions with the environment.",
        "what is hard water": "Hard water is water that contains dissolved calcium and magnesium salts.",
        "What is Polymer": "A polymer is a large molecule made of repeating monomer units.",
        "What is electrolysis": "Electrolysis is the chemical decomposition of a substance using electric current.",
        "What is nanotechnology": "Nanotechnology is the study and application of materials and the nanometer scale.",
        "What is adsorption": "Adsorption is the accumulation of molecules on the surface of the substance.",
    },
    "Mathematics": {
        "integration": "Integration of 1/(1+x^2) is tan⁻¹(x) + C.",
        "derivative": "Derivative of x^n is n*x^(n-1).",
        "What is a matrix": "A rectangular array of numbers",
        "dy/dx of sinx": "cosx",
        "dy/dx of cosecx": "-cosecx.cotx",
        "dy/dx of tanx": "sec^2x",
        "dy/dx of logx": "1/x",
    },
    "Programming": {
        "python": "Python is a high-level programming language used for AI, web development and data science.",
        "loop": "A loop is used to repeat a block of code multiple times.",
        "Tuple": "In Python, Tuple is an immutable, ordered collection of elements enclosed within parentheses.",
        "Tuple Operations": "Concatenation, repetition, membership test, length",
        "List": "Lists in Python are data structures used to store multiple items in a single variable.",
    },
    "BXE": { 
        "What is a semiconductor": "A semiconductor is a material whose conductivity is between a conductor and an insulator.",
        "Types of semiconductors": "Intrinsic semiconductor and Extrinsic semiconductor.",
        "What is a diode": "A diode is a two terminal electronic device that allows current to flow in only one direction.",
        "Function of a diode": "The main function of a diode is to allow current to pass in one direction and block it in the opposite direction.",
        "What is a PN junction": "A PN junction is formed when P-type and N-type semiconductors are joined together.",
        "What is forward biasing": "Forward biasing is when the P-side is connected to the positive terminal and the N-side to the negative terminal of a battery."
    }
}

quiz_data = {
    "Physics": [
        {"question": "What is the SI unit of force?", "answer": "newton"},
        {"question": "What is the speed of light?", "answer": "3x10^8"},
        {"question": "Who invented laser?", "answer": "theodore maiman"},
        {"question": "Unit of electric current?", "answer": "ampere"},
        {"question": "Device used to measure voltage?", "answer": "voltmeter"}
    ],
    "Chemistry": [
        {"question": "Chemical formula of water?", "answer": "h2o"},
        {"question": "Atomic number of oxygen?", "answer": "8"},
        {"question": "Gas used in photosynthesis?", "answer": "carbon dioxide"},
        {"question": "pH of pure water?", "answer": "7"},
        {"question": "Acid present in lemon?", "answer": "citric acid"}
    ],
    "Mathematics": [
        {"question": "Value of pi approximately?", "answer": "3.14"},
        {"question": "Square root of 64?", "answer": "8"},
        {"question": "2 + 2 = ?", "answer": "4"},
        {"question": "Derivative of x^2?", "answer": "2x"},
        {"question": "10 divided by 2?", "answer": "5"}
    ],
    "Programming": [
        {"question": "Who developed Python?", "answer": "guido van rossum"},
        {"question": "What symbol is used for comments in Python?", "answer": "#"},
        {"question": "Which keyword is used to define a function?", "answer": "def"},
        {"question": "Which data type stores text?", "answer": "string"},
        {"question": "Which loop repeats until condition becomes false?", "answer": "while"}
    ],
    "BXE": [
        {"question": "What does BXE stand for?", "answer": "basic electrical engineering"},
        {"question": "Unit of resistance?", "answer": "ohm"},
        {"question": "Device used to measure current?", "answer": "ammeter"},
        {"question": "Ohm's law formula?", "answer": "v=ir"},
        {"question": "Unit of power?", "answer": "watt"}
    ]
}

synonyms = {
    "laser": ["laser", "light amplification", "stimulated emission"],
    "acid": ["acid", "h+ donor"]
}

daily_tips = [
    "Revise one topic every day for 30 minutes.",
    "Practice previous year questions to improve faster.",
    "Take short breaks to boost memory.",
    "Explain concepts to yourself like teaching someone else.",
    "Start your day with your weakest topic."
]

# ----------------- Persistent Storage -----------------

def load_json(filename, default):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f)

def load_csv(file):
  try:
      return pd.read_csv(file)
  except (pd.errors.EmptyDataError,FileNotFoundError):
      return pd.DataFrame(columns=["Date", "Topic", "Time"])


# ----------------- Session State -----------------
if "quiz_scores" not in st.session_state:
    st.session_state.quiz_scores = load_json("quiz_scores.json",
                                              {s: [] for s in study_data.keys()})
if "weak_topics" not in st.session_state:
    st.session_state.weak_topics = load_json("weak_topics.json",
                                              {s: {} for s in study_data.keys()})
if "daily_tracker" not in st.session_state:
    st.session_state.daily_tracker = load_csv("daily_tracker.csv")
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "daily_tip" not in st.session_state:
    st.session_state.daily_tip = random.choice(daily_tips)

# ----------------- Sidebar -----------------
st.sidebar.markdown("## 📚 Menu")
page = st.sidebar.radio("Navigate:", ["Study", "Quiz", "Chatbot", "Progress"])

# Daily Tip Card
st.sidebar.markdown(f"""
<div style="background-color:#FFF3E0; padding:10px; border-radius:10px; margin-bottom:10px;">
💡 <b>Daily Tip:</b> {st.session_state.daily_tip}
</div>
""", unsafe_allow_html=True)

# Clear Chat Button
if st.sidebar.button("Clear Chat"):
    st.session_state.chat_history = []

# ----------------- Helper -----------------
def find_answer(question):
    question = question.lower()
    for subject, topics in study_data.items():
        for topic, answer in topics.items():
            keys = [topic.lower()]
            if topic.lower() in synonyms:
                keys.extend([syn.lower() for syn in synonyms[topic.lower()]])
            if any(k in question for k in keys):
                return answer
    return "Sorry, I don't know. Check Study Notes or try a different question."

# ----------------- Study Tab -----------------
if page == "Study":
    st.markdown("<h1 style='text-align:center; color:#4B0082;'>📖 Study Notes</h1>", unsafe_allow_html=True)
    subject = st.selectbox("Select Subject:", list(study_data.keys()))
    topics = list(study_data[subject].keys())
    cols = st.columns(3)
    for idx, topic in enumerate(topics):
        with cols[idx % 3]:
            st.markdown(f"""
            <div style='background-color:#E0F7FA; padding:20px; border-radius:15px; margin-bottom:10px; box-shadow: 2px 2px 5px #B0B0B0;'>
            <h4>📌 {topic}</h4>
            <p>{study_data[subject][topic]}</p>
            </div>
            """, unsafe_allow_html=True)

# ----------------- Quiz Tab -----------------
elif page == "Quiz":
    st.markdown("<h1 style='text-align:center; color:#4B0082;'>📝 Quiz Time</h1>", unsafe_allow_html=True)
    subject = st.selectbox("Select Subject:", list(quiz_data.keys()))
    questions = quiz_data[subject]

    score = 0
    weak_topics_today = []

    for q in questions:
        user_answer = st.text_input(f"❓ {q['question']}", key=f"{subject}_{q['question']}")
        if user_answer:
            if q["answer"].lower() in user_answer.lower():
                st.success("✅ Correct!")
                score += 1
            else:
                st.error(f"❌ Wrong! Answer: {q['answer']}")
                weak_topics_today.append(q["question"])
                if subject not in st.session_state.weak_topics:
                    st.session_state.weak_topics[subject] = {}
                st.session_state.weak_topics[subject][q["question"]] = st.session_state.weak_topics[subject].get(q["question"], 0) + 1

    if st.button("Submit Quiz"):
        st.session_state.quiz_scores[subject].append(score)
        st.success(f"Your score: {score}/{len(questions)}")
        if weak_topics_today:
            st.warning(f"Topics to revise: {', '.join(weak_topics_today)}")
        else:
            st.success("No weak topics today!")
        today = pd.Timestamp.now().date()
        st.session_state.daily_tracker = pd.concat(
            [st.session_state.daily_tracker, pd.DataFrame([{"Date": today, "Subject": subject, "Quiz Taken": 1}])],
            ignore_index=True
        )
        save_json("quiz_scores.json", st.session_state.quiz_scores)
        save_json("weak_topics.json", st.session_state.weak_topics)
        st.session_state.daily_tracker.to_csv("daily_tracker.csv", index=False)

# ----------------- Chatbot Tab -----------------
elif page == "Chatbot":
    st.markdown("<h1 style='text-align:center; color:#4B0082;'>💬 AI Study Chatbot</h1>", unsafe_allow_html=True)
    user_input = st.text_input("Ask a question:")

    if user_input:
        answer = find_answer(user_input)
        st.session_state.chat_history.append({"user": user_input, "bot": answer})

    for chat in st.session_state.chat_history:
        st.markdown(f"""
        <div style='background-color:#E6E6FA; padding:10px; border-radius:15px; margin-bottom:5px;'>
        <b>You:</b> {chat['user']}</div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
        <div style='background-color:#D8F6CE; padding:10px; border-radius:15px; margin-bottom:10px;'>
        <b>Bot:</b> {chat['bot']}</div>
        """, unsafe_allow_html=True)

# ----------------- Progress Tab -----------------
elif page == "Progress":
    st.markdown("<h1 style='text-align:center; color:#4B0082;'>📊 Learning Progress</h1>", unsafe_allow_html=True)
    cols = st.columns(2)
    for idx, (subject, scores) in enumerate(st.session_state.quiz_scores.items()):
        with cols[idx % 2]:
            avg = round(sum(scores)/len(scores),2) if scores else 0
            st.markdown(f"""
            <div style='background-color:#FFF3E0; padding:15px; border-radius:15px; margin-bottom:10px; box-shadow: 2px 2px 5px #B0B0B0;'>
            <h4>{subject}</h4>
            <p>Scores: {scores if scores else 'No quizzes yet'}</p>
            <p>Average: {avg}</p>
            </div>
            """, unsafe_allow_html=True)