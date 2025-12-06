import streamlit as st
import math
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import base64
import requests

# ============================
# PAGE CONFIG
# ============================
st.set_page_config(
    page_title="Math Web App",
    page_icon="🧮",
    layout="wide"
)

# ============================
# FUNCTION: CONVERT IMAGE → BASE64 WITH PLACEHOLDER
# ============================
def img_to_base64(filepath):
    try:
        with open(filepath, "rb") as img_file:
            data = img_file.read()
        return base64.b64encode(data).decode()
    except:
        # Placeholder online jika file tidak ditemukan
        placeholder_url = "https://via.placeholder.com/120x120.png?text=No+Image"
        data = requests.get(placeholder_url).content
        return base64.b64encode(data).decode()

# ============================
# CSS PRESUNIV
# ============================
st.markdown("""
<style>
[data-testid="stAppViewContainer"], [data-testid="stVerticalBlock"], [data-testid="stBlock"] {
    background: transparent !important;
}
html, body {
    background: linear-gradient(140deg, #002060, #C00000);
}
.title {
    text-align: center;
    font-size: 40px;
    font-weight: bold;
    color: black;
    margin-bottom: 30px;
    text-shadow: 2px 2px 6px rgba(255,255,255,0.4);
}
.member-card {
    background: linear-gradient(135deg, #002060, #C00000);
    border-radius: 20px;
    padding: 20px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.25);
    text-align: center;
    border: 3px solid white;
    width: 260px;
    height: 350px;
    margin-left: auto;
    margin-right: auto;
    color: white;
    margin-bottom: 20px;
}
.member-photo {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    object-fit: cover;
    border: 3px solid white;
    margin-bottom: 15px;
    display: block;
    margin-left: auto;
    margin-right: auto;
}
.member-name {
    font-size: 20px;
    font-weight: bold;
    color: #FFD700;
}
.member-role {
    font-size: 14px;
    color: white;
    padding-top: 5px;
}
</style>
""", unsafe_allow_html=True)

# ============================
# SIDEBAR NAVIGATION
# ============================
page = st.sidebar.radio("Navigate", ["Group Members", "Function Tools", "Optimization Solver"])

# ============================
# PAGE 1: GROUP MEMBERS
# ============================
if page == "Group Members":
    st.markdown("<div class='title'>Group Members</div>", unsafe_allow_html=True)

    members = [
        {"name": "Pardi Ihsan", "role": "Leader / Brainstorming and Project Execution", "photo": "Pardi.jpeg"},
        {"name": "Fikri Ariansyah", "role": "Member / Brainstorming and Project Execution", "photo": "Fikri.jpeg"},
        {"name": "M. Adam Asyrofi", "role": "Member / Brainstorming and Project Execution", "photo": "Adam.jpeg"},
        {"name": "Riska Dwi Ambarwati", "role": "Member / Brainstorming and Project Execution", "photo": "Riska.jpeg"}
    ]

    cols_per_row = 2
    total_rows = math.ceil(len(members) / cols_per_row)

    for row in range(total_rows):
        cols = st.columns(cols_per_row)
        for i, col in enumerate(cols):
            idx = row * cols_per_row + i
            if idx < len(members):
                m = members[idx]
                with col:
                    img_base64 = img_to_base64(m["photo"])
                    st.markdown(f"""
                    <div class='member-card'>
                        <img src="data:image/jpeg;base64,{img_base64}" class="member-photo">
                        <div class='member-name'>{m["name"]}</div>
                        <div class='member-role'>{m["role"]}</div>
                    </div>
                    """, unsafe_allow_html=True)

# ============================
# PAGE 2: FUNCTION VISUALIZATION & DIFFERENTIATION
# ============================
elif page == "Function Tools":
    st.markdown("<div class='title'>Function Visualization & Differentiation</div>", unsafe_allow_html=True)
    st.info("Input a function of x (e.g., x**2 + 3*x + 2). The app will plot the function and show its derivative.")

    func_input = st.text_input("Enter function of x:", "x**2")
    x = sp.symbols('x')

    # Plot
    try:
        f_lambd = sp.lambdify(x, sp.sympify(func_input), 'numpy')
        x_vals = np.linspace(-10, 10, 400)
        y_vals = f_lambd(x_vals)

        fig, ax = plt.subplots()
        ax.plot(x_vals, y_vals)
        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")
        ax.set_title("Function Plot")
        ax.grid(True)
        st.pyplot(fig)
    except:
        st.error("Invalid function input for plotting!")

    # Derivative
    try:
        derivative = sp.diff(sp.sympify(func_input), x)
        st.write(f"Derivative: {derivative}")
    except:
        st.error("Cannot compute derivative.")

# ============================
# PAGE 3: OPTIMIZATION WORD-PROBLEM SOLVER
# ============================
elif page == "Optimization Solver":
    st.markdown("<div class='title'>Optimization Word-Problem Solver</div>", unsafe_allow_html=True)
    st.info("Enter a function representing a word problem (e.g., profit, distance). Input variable(s) and choose whether to maximize or minimize.")

    var_input = st.text_input("Variable(s):", "x")
    func_input = st.text_input("Function:", "-x**2 + 4*x")
    optimize_type = st.radio("Type of Optimization:", ["Maximize", "Minimize"])

    try:
        vars_list = [sp.symbols(v.strip()) for v in var_input.split(",")]
        func = sp.sympify(func_input)

        st.subheader("Derivatives")
        derivs = [sp.diff(func, v) for v in vars_list]
        for v, d in zip(vars_list, derivs):
            st.write(f"∂f/∂{v} = {d}")

        st.subheader("Critical Points")
        crit_points = sp.solve(derivs, vars_list, dict=True)

        if crit_points:
            for pt in crit_points:
                st.write(pt)

            if optimize_type == "Maximize":
                best_point = max(crit_points, key=lambda p: func.subs(p))
            else:
                best_point = min(crit_points, key=lambda p: func.subs(p))

            best_value = func.subs(best_point)
            st.success(f"{optimize_type} occurs at {best_point} with f = {best_value}")
        else:
            st.warning("No critical points found.")

    except Exception as e:
        st.error(f"Error: {e}")
