from agno.agent import Agent
from agno.models.google import Gemini
from langfuse import observe, get_client


@observe()
def run_agent(user_prompt, instructions):
    langfuse = get_client()

    langfuse.update_current_trace(
        name="Story Generation",
        tags=["ext_eval_pipelines"]
    )
    agent = Agent(
        model=Gemini(id="gemini-2.0-flash"),
        description="Tu es un créateur de comptes pour enfant",
        instructions=[instructions],
        markdown=True,
        debug_mode=True
    )
    result = agent.run(user_prompt)

    return result

# run_agent("Une histoire sur un dragon gentil qui a peur des souris.", "Crée une histoire courte (entre 200 et 400 mots) basés sur le thème qui te va être communiqué par un enfant")