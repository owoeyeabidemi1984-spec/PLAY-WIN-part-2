import streamlit as st
from PIL import Image
import os

st.set_page_config(page_title="Maths Made Easy With Oly", page_icon="🎮", layout="centered")

# LOGO
if os.path.exists("logo.jpg"):
    st.image("logo.jpg", use_container_width=True)
st.markdown("<h1 style='text-align:center;color:#FF9A00;'>MATHS MADE EASY WITH OLY 🎮</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;font-weight:800;'>BASIC 1 • JSS 2 • MATHEMATICS GAME</p>", unsafe_allow_html=True)

basic1 = [
 ("1. What is 5 + 7 ?", ["10","11","12","13"], "12"),
 ("2. What is 15 - 8 ?", ["6","7","8","9"], "7"),
 ("3. What is 4 × 6 ?", ["20","22","24","26"], "24"),
 ("4. What is 20 ÷ 4 ?", ["4","5","6","20"], "5"),
 ("5. Which is greater? 45 or 54 ?", ["45","54","Equal","None"], "54"),
 ("6. Place value of 5 in 356 ?", ["5","50","500","5,000"], "50"),
 ("7. What is 100 + 250 ?", ["300","350","400","250"], "350"),
 ("8. How many sides does a triangle have?", ["2","3","4","5"], "3"),
 ("9. What is 1/2 of 10 ?", ["2","5","10","20"], "5"),
 ("10. Next: 10, 20, 30, ___", ["35","40","45","50"], "40"),
 ("11. What is 9 × 3 ?", ["21","24","27","30"], "27"),
 ("12. ₦50 - ₦20 = ?", ["₦20","₦30","₦40","₦70"], "₦30"),
 ("13. Minutes in 1 hour?", ["30","45","60","90"], "60"),
 ("14. What is 7 + 8 + 5 ?", ["18","19","20","21"], "20"),
 ("15. Which shape is round?", ["Square","Triangle","Circle","Rectangle"], "Circle"),
 ("16. What is 48 - 19 ?", ["29","30","31","39"], "29"),
 ("17. What is 6 × 7 ?", ["36","40","42","48"], "42"),
 ("18. What is 1/4 of 20 ?", ["4","5","10","20"], "5"),
 ("19. Days in a week?", ["5","6","7","8"], "7"),
 ("20. What is 99 + 1 ?", ["90","99","100","110"], "100"),
]
jss2 = [
 ("1. Evaluate: 2x + 3 = 11", ["x = 3","x = 4","x = 5","x = 8"], "x = 3"),
 ("2. Which is prime?", ["1","2","4","9"], "2"),
 ("3. Simplify: 3(x + 2) = 15", ["x = 1","x = 2","x = 3","x = 5"], "x = 3"),
 ("4. Find x: 2x + 7 = 19", ["x = 4","x = 6","x = 8","x = 10"], "x = 6"),
 ("5. What is 3² ?", ["3","6","9","27"], "9"),
 ("6. Simplify: (a²)³", ["a³","a⁵","a⁶","a⁹"], "a⁶"),
 ("7. Expand: (x + 3)²", ["x² + 3x + 9","x² + 6x + 9","x² - 3x + 9","x² + 9x + 6"], "x² + 6x + 9"),
 ("8. Factorize: x² - 9", ["(x + 3)(x - 3)","(x + 9)(x - 1)","(x + 3)²","(x - 3)²"], "(x + 3)(x - 3)"),
 ("9. Next: 2, 5, 8, 11, ...", ["13","14","15","16"], "14"),
 ("10. What is 3/4 + 1/4 ?", ["1/3","1/2","3/4","1"], "1"),
 ("11. Simplify: 5/6 + 1/3", ["1/2","2/3","5/6","7/6"], "7/6"),
 ("12. Perimeter: length 7cm, breadth 3cm", ["10 cm","14 cm","18 cm","20 cm"], "20 cm"),
 ("13. Which = 50%?", ["1/4","1/2","3/4","100%"], "1/2"),
 ("14. Solve: 3x = 24", ["x = 4","x = 6","x = 8","x = 12"], "x = 8"),
 ("15. 48 pencils, 8 per pack. How many packs?", ["4","5","6","8"], "6"),
 ("16. Value of 5⁰ ?", ["0","1","5","10"], "1"),
 ("17. Complementary, one is 62°. Find x.", ["28°","32°","38°","62°"], "28°"),
 ("18. Convert 60cm to metres.", ["0.06 m","0.6 m","6 m","60 m"], "0.6 m"),
 ("19. Which is divisible by 3?", ["17","21","25","29"], "21"),
 ("20. Value of 7x - 3 when x = 2 ?", ["11","10","7","1"], "11"),
]

all_q = [("STEP 1: BASIC 1", q, o, a) for q,o,a in basic1] + [("STEP 2: JSS 2", q, o, a) for q,o,a in jss2]

if "idx" not in st.session_state:
    st.session_state.idx = 0
    st.session_state.score = 0
    st.session_state.answered = False

idx = st.session_state.idx
step, q, opts, ans = all_q[idx]

st.markdown(f"### {step}  |  ⭐ Score: {st.session_state.score}  |  Q {idx+1}/40")
st.progress((idx)/40)
st.markdown(f"## {q}")

choice = st.radio("Choose one:", opts, key=f"q{idx}", index=None)

if choice:
    if not st.session_state.answered:
        if choice == ans:
            st.session_state.score += 1
            st.success("✅ Correct! +1 point")
        else:
            st.error(f"❌ Wrong. Correct answer is {ans}")
        st.session_state.answered = True
    else:
        if choice == ans:
            st.success("✅ Correct!")
        else:
            st.error(f"❌ Wrong. Correct answer is {ans}")

col1, col2 = st.columns([1,1])
with col1:
    if idx > 0:
        if st.button("← Back"):
            st.session_state.idx -= 1
            st.session_state.answered = False
            st.rerun()
with col2:
    # BLACK ARROW NEXT
    label = "Finish 🏁" if idx == 39 else "Next ➔"
    if st.button(label, disabled=(choice is None)):
        if idx < 39:
            st.session_state.idx += 1
            st.session_state.answered = False
            st.rerun()
        else:
            st.session_state.finished = True
            st.rerun()

if st.session_state.get("finished"):
    st.balloons()
    st.markdown(f"# 🏆 You scored {st.session_state.score} / 40")
    if st.button("🔁 Play Again"):
        st.session_state.idx = 0
        st.session_state.score = 0
        st.session_state.answered = False
        st.session_state.finished = False
        st.rerun()
