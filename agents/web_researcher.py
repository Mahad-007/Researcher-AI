from crewai import Agent
# from crewai_tools import WebsiteSearchTool
from crewai_tools import SerperDevTool

def get_web_researcher_agent(llm):
    # tool = WebsiteSearchTool(
    #     config={
    #         "llm": {"provider": "groq", "config": {"model": "mixtral-8x7b-32768"}},
    #         # "embedder": {"provider": "huggingface", "config": {"model": "sentence-transformers/all-MiniLM-L6-v2"}}
    #     }
    # )
    tool = SerperDevTool() 
    return Agent(
        role="Web Researcher",
        goal="Find the latest and most relevant online data about the target company/product.",
        backstory=(
            "An investigative analyst who once worked for an elite financial intelligence agency, "
            "you specialize in discovering accurate, real-time data across the web. You thrive in digital chaos, "
            "cutting through noise to extract the most reliable insights. You are efficient, skeptical of vague sources, "
            "and always hungry for breaking news."
        ),
        tools=[tool],
        llm=llm,
        verbose=True
    )
