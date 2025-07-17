from crewai import Crew, Task
from agents.web_researcher import get_web_researcher_agent
from agents.data_extractor import get_data_extractor_agent
from agents.report_editor import get_report_editor_agent

def build_crew(company, llm):
    # Initialize agents
    researcher = get_web_researcher_agent(llm)
    extractor = get_data_extractor_agent(llm)
    editor = get_report_editor_agent(llm)

    # Define tasks
    tasks = [
        Task(description=f"Search the web for latest news and insights about {company}",expected_output="A bullet‑list summary of recent news headlines with brief context.", agent=researcher),
        Task(description=f"Scrape and extract information from {company}'s official website or relevant pages", expected_output="Formatted textual content from company website and key data points.", agent=extractor),
        Task(description="Summarize and compile all findings into a report.", expected_output="A structured and formatted summary report including background, products, recent news, and market position.", agent=editor)
    ]

    # Build the Crew with memory off and no embedder (so no OpenAI key needed)
    return Crew(
        agents=[researcher, extractor, editor],
        tasks=tasks,
        verbose=True,
        memory=False,     # Turn off memory to avoid embedding defaults
        embedder=None     # Explicitly remove embedder config to prevent OPENAI key usage
    )
