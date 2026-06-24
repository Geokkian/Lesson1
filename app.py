# fractions_game.py
# Streamlit Fraction Adventure Game
# Ready to run with: streamlit run fractions_game.py

import streamlit as st
import random

st.set_page_config(
    page_title="Fraction Adventure!",
    page_icon="🍕",
    layout="centered"
)

# ---------- Initialize Session State ----------
if "score" not in st.session_state:
    st.session_state.score = 0

if "question_number" not in st.session_state:
    st.session_state.question_number = 1

if "current_question" not in st.session_state:
    st.session_state.current_question = None

if "answered" not in st.session_state:
    st.session_state.answered = False

if "feedback" not in st.session_state:
    st.session_state.feedback = ""

if "show_answer" not in st.session_state:
    st.session_state.show_answer = False


# ---------- Question Generator ----------
def generate_question():
    denominator = random.choice([2, 3, 4, 5, 6, 8, 10])

    # Ensure sensible numerators
    num1 = random.randint(1, denominator - 1)
    num2 = random.randint(1, denominator - 1)

    operation = random.choice(["+", "-"])

    if operation == "-":
        # Make sure answer is not negative
        if num2 > num1:
            num1, num2 = num2, num1

        answer = num1 - num2
        explanation = (
            f"To subtract like fractions, keep the denominator ({denominator}) "
            f"the same and subtract the numerators: "
            f"{num1} - {num2} = {answer}."
        )

    else:
        answer = num1 + num2
        explanation = (
            f"To add like fractions, keep the denominator ({denominator}) "
            f"the same and add the numerators: "
            f"{num1} + {num2} = {answer}."
        )

    scenarios = [
        (
            f"🍕 Sam ate {num1}/{denominator} of a pizza and "
            f"Tom ate {num2}/{denominator}. "
            f"How much pizza did they eat altogether?"
            if operation == "+"
            else
            f"🍰 Mia had {num1}/{denominator} of a cake and ate "
            f"{num2}/{denominator}. How much cake is left?"
        ),
        (
            f"🍎 Lily collected {num1}/{denominator} basket of apples "
            f"and later {'found' if operation == '+' else 'gave away'} "
            f"{num2}/{denominator} basket."
        ),
        (
            f"🎨 A painting was coloured {num1}/{denominator}. Then "
            f"{num2}/{denominator} was "
            f"{'coloured more' if operation == '+' else 'erased'}."
        )
    ]

    story = random.choice(scenarios)

    return {
        "num1": num1,
        "num2": num2,
        "denominator": denominator,
        "operation": operation,
        "answer": answer,
        "story": story,
        "explanation": explanation
    }


if st.session_state.current_question is None:
    st.session_state.current_question = generate_question()

q = st.session_state.current_question

# ---------- Header ----------
st.title("🎮 Fraction Adventure!")
st.subheader("Learn to Add and Subtract Like Fractions")

st.markdown(
    """
    Welcome, Math Explorer! 🚀

    Solve the fraction challenge and earn points!
    """
)

# ---------- Scoreboard ----------
col1, col2 = st.columns(2)

with col1:
    st.metric("⭐ Score", st.session_state.score)

with col2:
    st.metric("📝 Question", st.session_state.question_number)

st.divider()

# ---------- Question ----------
st.markdown("### Story Problem")
st.info(q["story"])

st.markdown("### Fraction Challenge")

st.latex(
    rf"\frac{{{q['num1']}}}{{{q['denominator']}}}"
    rf"{q['operation']}"
    rf"\frac{{{q['num2']}}}{{{q['denominator']}}}"
    rf"=?"
)

st.write("Enter your answer:")

answer_num = st.number_input(
    "Numerator",
    min_value=0,
    max_value=50,
    step=1,
    key="num_input"
)

answer_den = st.number_input(
    "Denominator",
    min_value=1,
    max_value=20,
    step=1,
    value=q["denominator"],
    key="den_input"
)

# ---------- Check Answer ----------
if not st.session_state.answered:
    if st.button("✅ Check My Answer"):
        st.session_state.answered = True

        if (
            answer_num == q["answer"]
            and answer_den == q["denominator"]
        ):
            st.session_state.score += 10
            st.session_state.feedback = (
                "🎉 Correct! Great job, Fraction Hero!"
            )
        else:
            st.session_state.feedback = (
                "❌ Not quite. Keep trying!"
            )

# ---------- Feedback ----------
if st.session_state.answered:
    if (
        answer_num == q["answer"]
        and answer_den == q["denominator"]
    ):
        st.success(st.session_state.feedback)
        st.balloons()
    else:
        st.error(st.session_state.feedback)

        st.warning(
            f"The correct answer is "
            f"{q['answer']}/{q['denominator']}"
        )

    st.markdown("### 💡 Explanation")
    st.info(q["explanation"])

    if st.button("➡️ Next Question"):
        st.session_state.question_number += 1
        st.session_state.current_question = generate_question()
        st.session_state.answered = False
        st.session_state.feedback = ""
        st.rerun()

st.divider()

st.markdown(
    """
    ### 🌟 How to Add or Subtract Like Fractions

    * Keep the denominator the same.
    * Add or subtract only the numerators.
    * Write the answer with the same denominator.

    Example:

    **3/8 + 2/8 = 5/8**

    Happy learning! 🎓
    """
)
