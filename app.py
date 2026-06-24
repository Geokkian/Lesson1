import streamlit as st
import random
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Mario Fraction Adventure",
    page_icon="🍄",
    layout="wide"
)

# ---------------------------------------------------
# SESSION STATE
# ---------------------------------------------------

if "score" not in st.session_state:
    st.session_state.score = 0

if "level" not in st.session_state:
    st.session_state.level = 1


# ---------------------------------------------------
# CREATE NEW FRACTION QUESTION
# ---------------------------------------------------

def create_question():

    denominator = random.choice([2, 3, 4, 5, 6, 8])

    n1 = random.randint(1, denominator - 1)
    n2 = random.randint(1, denominator - 1)

    operation = random.choice(["+", "-"])

    if operation == "-" and n2 > n1:
        n1, n2 = n2, n1

    answer = n1 + n2 if operation == "+" else n1 - n2

    return {
        "n1": n1,
        "n2": n2,
        "denominator": denominator,
        "operation": operation,
        "answer": answer
    }


if "question" not in st.session_state:
    st.session_state.question = create_question()

q = st.session_state.question

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.title("🍄 Mario Fraction Adventure")
st.write(
    "Move the hero with the keyboard, collect coins, then solve the fraction challenge!"
)

col1, col2 = st.columns(2)

col1.metric("⭐ Score", st.session_state.score)
col2.metric("🏆 Level", st.session_state.level)

# ---------------------------------------------------
# GAME
# ---------------------------------------------------

game_html = """
<!DOCTYPE html>
<html>

<head>

<style>

body{
    margin:0;
}

#game{
    position:relative;
    width:100%;
    height:420px;
    overflow:hidden;
    border-radius:20px;
    background:linear-gradient(#7ec8ff 75%, #5dbb63 75%);
}

#ground{
    position:absolute;
    bottom:0;
    width:100%;
    height:100px;
    background:#3e8e41;
}

#player{
    position:absolute;
    left:50px;
    bottom:100px;
    width:60px;
    height:60px;
    font-size:45px;
}

.coin{
    position:absolute;
    font-size:35px;
}

.instructions{
    position:absolute;
    top:10px;
    left:10px;
    background:white;
    padding:10px;
    border-radius:10px;
    font-size:18px;
}

</style>

</head>

<body>

<div id="game">

<div class="instructions">
⬅️ ➡️ Move | SPACE Jump
</div>

<div id="player">🧒</div>

<div class="coin" style="left:250px;bottom:120px;">🪙</div>
<div class="coin" style="left:450px;bottom:160px;">🪙</div>
<div class="coin" style="left:650px;bottom:120px;">🪙</div>
<div class="coin" style="left:850px;bottom:180px;">🪙</div>
<div class="coin" style="left:1050px;bottom:120px;">🪙</div>

<div id="ground"></div>

</div>

<script>

let player = document.getElementById("player");

let x = 50;
let y = 100;

let velocity = 0;
let jumping = false;

document.addEventListener("keydown", function(e){

    if(e.key === "ArrowRight"){
        x += 20;
    }

    if(e.key === "ArrowLeft"){
        x -= 20;
    }

    if(e.code === "Space" && !jumping){
        velocity = 18;
        jumping = true;
    }

    if(x < 0) x = 0;

    player.style.left = x + "px";
});

function animate(){

    if(jumping){

        y += velocity;
        velocity -= 1;

        if(y <= 100){
            y = 100;
            velocity = 0;
            jumping = false;
        }

        player.style.bottom = y + "px";
    }

    requestAnimationFrame(animate);
}

animate();

</script>

</body>

</html>
"""

components.html(game_html, height=430)

# ---------------------------------------------------
# FRACTION CHALLENGE
# ---------------------------------------------------

st.divider()

st.subheader("🧮 Unlock the Castle")

st.markdown("Solve this fraction problem:")

st.latex(
    rf"\frac{{{q['n1']}}}{{{q['denominator']}}}"
    rf"{q['operation']}"
    rf"\frac{{{q['n2']}}}{{{q['denominator']}}}"
    rf"="
)

answer_num = st.number_input(
    "Numerator",
    min_value=0,
    max_value=20,
    step=1
)

answer_den = st.number_input(
    "Denominator",
    min_value=1,
    max_value=10,
    value=q["denominator"],
    step=1
)

# ---------------------------------------------------
# CHECK ANSWER
# ---------------------------------------------------

if st.button("🚪 Unlock Next Level"):

    if (
        answer_num == q["answer"]
        and answer_den == q["denominator"]
    ):

        st.success("🎉 Correct! Castle unlocked!")
        st.balloons()

        st.session_state.score += 10
        st.session_state.level += 1

        st.session_state.question = create_question()

    else:

        st.error("❌ Try again!")

        st.info(
            f"""
Correct Answer:

**{q['answer']}/{q['denominator']}**

Remember:

When adding or subtracting like fractions,
keep the denominator the same.
"""
        )

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

with st.sidebar:

    st.header("🎮 Controls")

    st.write("➡️ Arrow Right = Move")
    st.write("⬅️ Arrow Left = Move")
    st.write("␣ Space = Jump")

    st.header("📚 Fraction Rule")

    st.write(
        """
Keep the denominator the same.

Example:

3/8 + 2/8 = 5/8

6/10 - 2/10 = 4/10
"""
    )

    if st.button("🔄 Restart Game"):
        st.session_state.score = 0
        st.session_state.level = 1
        st.session_state.question = create_question()
        st.rerun()
