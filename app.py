import streamlit as st
from agent_traced import ask

st.set_page_config(page_title="Campaign Analyst Agent", page_icon="🤖")
st.title("🤖 Multi-Step Campaign Analyst Agent")

# --- Password gate: blocks strangers from spending your OpenAI credit ---
try:
    correct_password = st.secrets["APP_PASSWORD"]
except Exception:
    correct_password = None  # no password set (e.g. running locally)

if correct_password:
    entered = st.text_input("Password", type="password")
    if entered != correct_password:
        if entered:
            st.error("Wrong password.")
        st.stop()
# -----------------------------------------------------------------------

st.write("Ask a question that needs campaign context and/or benchmark comparison.")
question = st.text_input("Your question:")

if question:
    with st.spinner("Agent reasoning..."):
        answer, used = ask(question)
    st.write("### Answer")
    st.write(answer)
    st.caption("Tools called: " + (" → ".join(used) if used else "none"))