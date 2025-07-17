import os
import asyncio
import streamlit as st
from dotenv import load_dotenv
from crewai import LLM
from crew.research_crew import build_crew
from crewai.agents.parser import AgentAction, AgentFinish
from crewai.agents.crew_agent_executor import ToolResult
from crewai.tasks.task_output import TaskOutput

load_dotenv()
st.set_page_config(page_title="🔎 Multi‑Agent Research App", layout="wide")

st.title("🔎 Multi‑Agent Research App")
company = st.text_input("Enter Company/Product Name", key="company_input")

if st.button("Run Research"):
    if not company:
        st.warning("Please enter a company or product name.")
    else:
        llm = LLM(
            model="gemini/gemini-2.5-pro",
            api_key=os.getenv("GEMINI_API_KEY"),
            temperature=0.0,
            max_retries=2,
        )

        # Collect logs during Crew execution (callbacks must not call st.*)
        log_lines = []

        def step_cb(evt):
            if isinstance(evt, AgentAction):
                log_lines.append(f"🛠️ AgentAction: {evt.text}")
            elif isinstance(evt, ToolResult):
                log_lines.append(f"🔧 ToolResult: {evt.result}")
            elif isinstance(evt, AgentFinish):
                log_lines.append(f"✅ AgentFinish: {evt.text}")

        def task_cb(task_out: TaskOutput):
            log_lines.append(f"🎯 Task completed: {task_out.description}")

        # Build and configure Crew
        crew = build_crew(company, llm)
        crew.step_callback = step_cb
        crew.task_callback = task_cb
        crew.verbose = True

        # Run Crew asynchronously
        report = asyncio.run(crew.kickoff_async(inputs={"company": company}))

        # ✅ Safe UI updates after Crew finishes
        st.subheader("📋 Execution Log")
        st.markdown("\n\n".join(log_lines) or "_No intermediate steps captured_")

        st.subheader("📝 Final Research Report")
        final = getattr(report, "output", report)
        if getattr(final, "json_dict", None):
            st.json(final.json_dict)
        else:
            for t in getattr(final, "tasks_output", []):
                st.markdown(f"### {t.description}")
                st.markdown(t.summary or f"`{t.raw}`")
