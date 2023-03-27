from langchain.chains import LLMChain
from langchain.chains.base import Chain
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from typing import Dict, List

# Import things that are needed generically
from langchain.agents import initialize_agent, Tool
from langchain.tools import BaseTool
from langchain.llms import OpenAI
from langchain import LLMMathChain, SerpAPIWrapper


from langchain.llms.base import LLM
from typing import Optional, List, Mapping, Any

import chatGPT


class CustomLLM(LLM):
    n: int

    @property
    def _llm_type(self) -> str:
        return "custom"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        #if stop is not None:
        #    raise ValueError("stop kwargs are not permitted.")

        ret = chatGPT.chat(prompt, stop)

        return ret

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {"n": self.n}


llm = CustomLLM(n=10)
# print(llm)

# r = llm("This is a foobar thing")
# print(r)

# Load the tool configs that are needed.
# search = SerpAPIWrapper()


def key_run(self, *args: str, **kwargs: str) -> str:
    return 'YES'


def flow_run(self, *args: str, **kwargs: str) -> str:
    return 'YES'


llm_math_chain = LLMMathChain(llm=llm, verbose=True)
tools = [
    Tool(
        name="key",
        func=key_run,
        description="useful for when you need to answer questions about searching keyword in log, input: 'key1'"
    ),
    Tool(
        name="flow",
        func=flow_run,
        description="useful for when you need to answer questions about check flow in log, input: ['key1', [key2]"
    )
]

PREFIX = '''Answer the following questions as best you can. You have access to the following tools:'''

FORMAT_INSTRUCTIONS ='''Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action'''

SUFFIX = '''Begin!

Question: {input}
Thought: {agent_scratchpad}'''


# Construct the agent. We will use the default agent type here.
# See documentation for a full list of options.
agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True,
    # agent_kwargs={'prefix': PREFIX, 'format_instructions': FORMAT_INSTRUCTIONS, 'suffix': SUFFIX},
    )

ret = agent.run("check 'Exception', if yes, check flow ('A', 'B', 'C')")

print(ret)
