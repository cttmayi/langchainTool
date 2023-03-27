from langchain.llms.fake import FakeListLLM
from langchain.agents import load_tools
from langchain.agents import initialize_agent

tools = load_tools(["python_repl"])

responses = [
    "Action: Python REPL\n"
    "Action Input: print(2 + 6)",
    "Final Answer: 4"
]
llm = FakeListLLM(responses=responses)

agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

agent.run("whats 2 + 3")