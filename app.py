# fraction_quest_game.py
# Run with:
# streamlit run fraction_quest_game.py

import streamlit as st
import random

st.set_page_config(
    page_title="Fraction Quest!",
    page_icon="🏰",
    layout="centered"
)

# --------------------------------------------------
# GAME DATA
# --------------------------------------------------

SCENARIOS = [
    ("🍕 Pizza Party", "pizza slices"),
    ("🍰 Cake Shop", "cake pieces"),
    ("🍎 Apple Basket", "apple baskets"),
    ("🍫 Chocolate Factory", "chocolate bars"),
    ("🍪 Cookie Jar", "cookies"),
    ("🎨 Art Studio", "paint sections"),
]

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "score" not in st.session_state:
    st.session_state.score = 0

if "lives" not in st.session_state:
    st.session_state.lives = 3

if "level" not in st.session_state:
    st.session_state.level = 1

if "streak" not in st.session_state:
    st.session_state.streak = 0

if "answered" not in st.session_state:
    st.session_state.answered = False

if "game_over" not in st.session_state:
    st.session_state.game_over = False

if "question" not in st.session_state:
    st.session_state.question = None


# --------------------------------------------------
# FUNCTIONS
# --------------------------------------------------

def make_question():

    denominator = random.choice([2, 3, 4, 5, 6, 8])

    # Increase difficulty with level
    max_num = min(denominator - 1, 1 + st.session_state.level)

    n1 = random.randint(1, max_num)
    n2 = random.randint(1, max_num)

    operation = random.choice(["+", "-"])

    # Prevent negative answers
    if operation == "-" and n2 > n1:
        n1, n2 = n2, n1

    answer = n1 + n2 if operation == "+" else n1 - n2

    theme, item = random.choice(SCENARIOS)

    if operation == "+":
        story = (
            f"Hero Max collected **{n1}/{denominator}** {item}. "
            f"Later, he found another **{n2}/{denominator}**.\n\n"
            f"How many {item} does Max have now?"
        )
    else:
        story = (
            f"Hero Max had **{n1}/{denominator}** {item}. "
            f"He used **{n2}/{denominator}**.\n\n"
            f"How many {item} are left?"
        )

    explanation = (
        f"Keep the denominator **{denominator}** the same.\n\n"
        f"{n1} {operation} {n2} = {answer}\n\n"
        f"So the answer is **{answer}/{denominator}**."
    )

    return {
        "theme": theme,
        "story": story,
        "n1": n1,
        "n2": n2,
        "denominator": denominator,
        "operation": operation,
        "answer": answer,
        "explanation": explanation,
    }


def new_question():
    st.session_state.question = make_question()
    st.session_state.answered = False


def restart_game():
    st.session_state.score = 0
    st.session_state.lives = 3
    st.session_state.level = 1
    st.session_state.streak = 0
    st.session_state.game_over = False
    new_question()


if st.session_state.question is None:
    new_question()

q = st.session_state.question

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🏰 Fraction Quest")
st.subheader("Become the Fraction Champion!")

# --------------------------------------------------
# SCOREBOARD
# --------------------------------------------------

c1, c2, c3, c4 = st.columns(4)

c1.metric("⭐ Score", st.session_state.score)
c2.metric("❤️ Lives", st.session_state.lives)
c3.metric("🏆 Level", st.session_state.level)
c4.metric("🔥 Streak", st.session_state.streak)

st.divider()

# --------------------------------------------------
# GAME OVER SCREEN
# --------------------------------------------------

if st.session_state.game_over:

    st.error("Game Over!")

    st.markdown(
        f"""
        ## Final Score: **{st.session_state.score}**

        Great effort, Math Hero! 🎉
        """
    )

    if st.button("🔄 Play Again"):
        restart_game()
        st.rerun()

    st.stop()

# --------------------------------------------------
# MISSION
# --------------------------------------------------

st.markdown(f"## {q['theme']}")
st.info(q["story"])

st.markdown("### Solve this challenge")

st.latex(
    rf"\frac{{{q['n1']}}}{{{q['denominator']}}}"
    rf"{q['operation']}"
    rf"\frac{{{q['n2']}}}{{{q['denominator']}}}"
    rf"=?"
)

# --------------------------------------------------
# ANSWER INPUT
# --------------------------------------------------

answer_num = st.number_input(
    "Enter the numerator",
    min_value=0,
    max_value=30,
    step=1
)

answer_den = st.number_input(
    "Enter the denominator",
    min_value=1,
    max_value=12,
    value=q["denominator"],
    step=1
)

# --------------------------------------------------
# CHECK ANSWER
# --------------------------------------------------

if not st.session_state.answered:

    if st.button("⚔️ Submit Answer"):

        st.session_state.answered = True

        correct = (
            answer_num == q["answer"]
            and answer_den == q["denominator"]
        )

        if correct:

            st.success("🎉 Correct! You defeated the challenge!")
            st.balloons()

            st.session_state.score += 10
            st.session_state.streak += 1

            # Level up every 5 correct answers
            if st.session_state.streak % 5 == 0:
                st.session_state.level += 1
                st.success("🏆 LEVEL UP!")

        else:

            st.error("Oops! The challenge defeated you.")

            st.session_state.lives -= 1
            st.session_state.streak = 0

            if st.session_state.lives <= 0:
                st.session_state.game_over = True

# --------------------------------------------------
# FEEDBACK
# --------------------------------------------------

if st.session_state.answered:

    correct = (
        answer_num == q["answer"]
        and answer_den == q["denominator"]
    )

    if not correct:
        st.warning(
            f"The correct answer was "
            f"**{q['answer']}/{q['denominator']}**"
        )

    st.markdown("### 💡 Hint")
    st.info(q["explanation"])

    if st.button("➡️ Next Mission"):

        if st.session_state.lives <= 0:
            st.session_state.game_over = True

        new_question()
        st.rerun()

# --------------------------------------------------
# BADGES
# --------------------------------------------------

st.divider()
st.markdown("## 🏅 Badges")

badges = []

if st.session_state.score >= 20:
    badges.append("🥉 Bronze Fraction Hero")

if st.session_state.score >= 50:
    badges.append("🥈 Silver Fraction Hero")

if st.session_state.score >= 100:
    badges.append("🥇 Gold Fraction Champion")

if not badges:
    st.write("Earn points to unlock badges!")

for badge in badges:
    st.success(badge)

# --------------------------------------------------
# SIDEBAR RULES
# --------------------------------------------------

with st.sidebar:
    st.header("🎮 How to Play")

    st.markdown("""
    1. Read the story.
    2. Solve the fraction problem.
    3. Enter the numerator and denominator.
    4. Earn **10 points** for every correct answer.
    5. You have **3 lives**.
    6. Every 5 correct answers increases your level.
    """)

    st.header("📚 Remember")

    st.markdown("""
    **Like Fractions**

    Keep the denominator the same.

    Example:

    3/8 + 2/8 = 5/8

    6/10 - 2/10 = 4/10
    """)

    if st.button("🔄 Restart Game"):
        restart_game()
        st.rerun()
