from agno.agent import Agent
from agno.models.anthropic import Claude

agent = Agent(
    model=Claude(id="claude-sonnet-4-20250514"),
    description="Tu es un créateur de comptes pour enfant",
    instructions=["Crée une histoire courte (entre 200 et 400 mots) basés sur le thème qui te va être communiqué par un enfant"],
    markdown=True,
    debug_mode=True
)

agent.print_response("Raconte moi une histoire de princesse.", stream=True)