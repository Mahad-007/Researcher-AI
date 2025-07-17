import streamlit as st
import os
from dotenv import load_dotenv
from crewai import LLM
from crew.research_crew import build_crew

load_dotenv()

st.title("🔎 Multi‑Agent Research App")
company = st.text_input("Enter Company/Product Name")

if st.button("Run Research") and company:
    st.write("⏳ Running multi‑agent research...")

    llm = LLM(
        model="gemini/gemini-2.5-pro",
        api_key=os.getenv("GEMINI_API_KEY"),
        temperature=0.0,
        max_retries=2
    )

    crew = build_crew(company, llm)
    report = crew.kickoff()

    st.subheader("📝 Research Report")
    st.write(report)
