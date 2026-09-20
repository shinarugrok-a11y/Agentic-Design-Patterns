"""Chapter 6 — Plan then write (CrewAI sequential)."""
from crewai import Agent, Task, Crew, Process

def plan_and_write(llm, topic: str) -> str:
    planner = Agent(role="Article Planner and Writer",
                    goal="Plan and write a concise summary.", llm=llm)
    task = Task(
        description=(
            f"1. Create a bullet-point plan for a summary on: '{topic}'.\n"
            "2. Write the summary based on your plan (~200 words)."
        ),
        expected_output="### Plan\n...\n### Summary\n...",
        agent=planner,
    )
    return str(Crew(agents=[planner], tasks=[task], process=Process.sequential).kickoff())
