import streamlit as st
import random
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Fraction Mario Adventure",
    page_icon="🍄",
    layout="wide"
)

st.title("🍄 Fraction Mario Adventure")
st.write(
    "Collect all the coins, then answer the fraction question to unlock the next level!"
)

# ------------------------------------------
# Generate Question
# ------------------------------------------

if "score" not in st.session_state:
    st.session_state.score = 0

if "level" not in st.session_state:
    st.session_state.level = 1

if "question" not in st.session_state:
    denom = random.choice([2, 3, 4, 5, 6, 8])
    n1 = random.randint(1, denom - 1)
    n2 = random.randint(1, denom - 1)
    operation = random.choice(["+", "-"])

    if operation == "-" and n2 > n1:
        n1, n2 = n2, n1

    answer = n1 + n2 if operation == "+" else n1 - n2

    st.session_state.question = {
        "n1": n1,
        "n2": n2,
        "denom": denom,
        "op": operation,
        "answer": answer
    }

q = st.session_state.question

col1, col2 = st.columns(2)
col1.metric("⭐ Score", st.session_state.score)
col2.metric("🏆 Level", st.session_state.level)

# ------------------------------------------
# GAME AREA
# ------------------------------------------

game_html = """
<!DOCTYPE html>
<html>
<head>
<style>

body{
    margin:0;
    overflow:hidden;
}

#game{
    position:relative;
    width:100%;
    height:400px;
    background:linear-gradient(#87CEEB 70%, #8B4513 70%);
    overflow:hidden;
    border-radius:15px;
}

#ground{
    position:absolute;
    bottom:0;
    width:100%;
    height:100px;
    background:#3CB371;
}

#player{
    position:absolute;
    bottom:100px;
    left:50px;
    width:50px;
    height:50px;
    background:red;
    border-radius:10px;
    font-size:35px;
    text-align:center;
}

.coin{
    position:absolute;
    width:35px;
    height:35px;
    font-size:30px;
}

#message{
    position:absolute;
    top:10px;
    left:10px;
    font-size:24px;
    background:white;
    padding:10px;
    border-radius:10px;
}

</style>
</head>

<body>

<div id="game">

<div id="message">
Coins: <span id="score">0</span>/5
</div>

<div id="player">🧒</div>

<div class="coin" style="left:250px;bottom:120px;">🪙</div>
<div class="coin" style="left:450px;bottom:120px;">🪙</div>
<div class="coin" style="left:650px;bottom:180px;">🪙</div>
<div class="coin" style="left:850px;bottom:120px;">🪙</div>
<div class="coin" style="left:1050px;bottom:150px;">🪙</div>

<div id="ground"></div>

</div>

<script>

const player = document.getElementById("player");
const coins = document.querySelectorAll(".coin");

let x = 50;
let y = 100;
let velocity = 0;
let jumping = false;
let collected = 0;

document.addEventListener("keydown", e=>{

    if(e.key==="ArrowRight"){
        x += 20;
    }

    if(e.key==="ArrowLeft"){
        x -= 20;
    }

    if(e.code==="Space" && !jumping){
        velocity = 18;
        jumping = true;
    }

    player.style.left = x + "px";
});

function gameLoop(){

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

    coins.forEach(c=>{

        if(c.style.display !== "none"){

            let coinX = parseInt(c.style.left);

            if(Math.abs(x - coinX) < 40 && Math.abs(y - 120) < 80){
                c.style.display = "none";
                collected++;

                document.getElementById("score").innerText = collected;

                if(collected === 5){
                    document.getElementById("message").innerHTML =
                    "🎉 Great! Scroll down and solve the fraction!";
                }
            }
        }
    });

    requestAnimationFrame(gameLoop);
}

gameLoop();

</script>

</body>
</html>
"""

components.html(game_html, height=430)

st.divider()

st.subheader("🧮 Fraction Gate Challenge")

st.latex(
    rf"\frac{{{q['n1']}}}{{{q['denom']}}}"
    rf"{q['op']}"
    rf"\frac{{{q['n2']}}}{{{q['denom']}}}=?"
)

num = st.number_input(
    "Numerator",
    min_value=0,
    max_value=20,
    step=1
)

den = st.number_input(
    "Denominator",
    min_value=1,
    max_value=10,
    value=q["denom"],
    step=1
)

if st.button("Unlock Next Level 🚪"):

    if num == q["answer"] and den == q["denom"]:

        st.success("🎉 Correct! Level unlocked!")
        st.balloons()

        st.session_state.score += 10
        st.session_state.level += 1

        denom = random.choice([2,3,4,5,6,8])
        n1 = random.randint(1, denom-1)
        n2 = random.randint(1, denom-1)

        op = random.choice(["+","-"])

        if op == "-" and n2 > n1:
            n1, n2 = n2, n1

        answer = n1 + n2 if op == "+" else n1 - n2

        st.session_state.question = {
            "n1": n1,
            "n2": n2,
            "denom": denom,
            "op": op,
            "answer": answer
        }

    else:
        st.error("❌ Not quite.")

        st.info(
            f"""
            Remember:

            Keep the denominator the same.

            Correct answer:

            {q['answer']}/{q['denom']}
            """
        )

st.sidebar.header("🎮 Controls")
st.sidebar.write("➡️ Arrow Right = Move Right")
st.sidebar.write("⬅️ Arrow Left = Move Left")
st.sidebar.write("␣ Spacebar = Jump")

st.sidebar.header("🏆 Goal")
st.sidebar.write(
    """
    1. Collect coins.
    2. Solve the fraction challenge.
    3. Unlock the next level.
    4. Earn points.
    """
)
