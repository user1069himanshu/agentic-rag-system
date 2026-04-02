from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI


def create_agent(tools, memory):
    """
    Create agent with tools
    """

    llm = ChatOpenAI(model="gpt-4o-mini")

    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        memory=memory,
        verbose=True
    )

    return agent