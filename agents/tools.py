from langchain.tools import Tool


def create_tools(rag_chain, llm):
    """
    Create tools for agent
    """

    # 🔹 RAG TOOL
    def rag_tool_func(query: str):
        response = rag_chain.invoke({"input": query})
        return response["answer"]

    rag_tool = Tool(
        name="Document QA Tool",
        func=rag_tool_func,
        description="Use this tool to answer questions from the document"
    )

    # 🔹 SUMMARIZATION TOOL
    def summarize_tool_func(query: str):
        response = rag_chain.invoke({"input": query})
        text = response["answer"]

        # then summarize
        summary = llm.invoke(f"Summarize this in 20 words:\n{text}")
        return summary.content

    summarize_tool = Tool(
        name="Summarization Tool",
        func=summarize_tool_func,
        description="Use this tool to summarize text or documents"
    )

     # 🔹 CALCULATOR TOOL
    def calculator_tool_func(expression: str):
        try:
            return str(eval(expression))
        except Exception:
            return "Invalid mathematical expression"

    calculator_tool = Tool(
        name="Calculator Tool",
        func=calculator_tool_func,
        description="Use this tool to solve math problems"
    )

    return [rag_tool, summarize_tool, calculator_tool]