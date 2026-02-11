import os
from langgraph.graph import StateGraph
from langchain_openai import ChatOpenAI as LangChainChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from browser_use import Agent, Browser, ChatOpenAI as BrowserChatOpenAI
from agent.schema import AgentState
from dotenv import load_dotenv

from vault import VAULT

load_dotenv()

llm_graph = LangChainChatOpenAI(model="gpt-4o-mini", temperature=0)
llm_browser = BrowserChatOpenAI(model="gpt-4o-mini")

def understand_intent(state):
    print("-------Reached understand node------------")

    prompt = f"""
    You are an intelligent shopping task analyst.

    Analyze this shopping request and extract:
    - Core user goal
    - Shopping intent type (bulk, comparison, urgent, budget, premium, etc.)
    - Constraints (price limits, quantity, brand sensitivity)
    - Risk factors (login, captcha, delivery restriction, pincode issues)

    Website: {state.user_input.website}
    Products: {[(p.name, p.quantity, p.max_price) for p in state.user_input.products]}

    Return a structured reasoning paragraph.
    """
    
    response = llm_graph.invoke(prompt)
    state.intent_analysis = response.content
    return state


def build_strategy(state):
    print("-------Reached startegy node------------")
    prompt = f"""
    You are an e-commerce navigation strategist.

    Given this website and intent analysis, decide:

    - Whether login should be avoided or bypassed
    - How to safely handle popups and delivery pincode prompts
    - Optimal search strategy (search bar vs categories)
    - Price filtering logic
    - Safe stopping condition

    Website: {state.user_input.website}
    Intent analysis:
    {state.intent_analysis}

    Return a concise execution strategy paragraph.
    """
    
    response = llm_graph.invoke(prompt)
    state.execution_strategy = response.content
    return state
   
def plan_products(state):
    print("-------Reached plan product node------------")
    prompt = f"""
    You are a shopping automation planner.

    For each product below, generate a high-level action plan:
    - How to search
    - How to filter
    - How to choose the best item
    - How many units to add

    Products:
    {[(p.name, p.quantity, p.max_price) for p in state.user_input.products]}

    Return a clear product-by-product action reasoning paragraph.
    """
    response = llm_graph.invoke(prompt)
    state.product_plan = response.content
    return state

def safety_evaluator(state):
    print("-------Reached evaluator node------------")
    prompt = f"""
    You are a browser automation risk assessor.

    Analyze the following strategy and product plan.
    Identify potential failure triggers:
    - CAPTCHA
    - Login wall
    - OTP
    - Payment redirect
    - Infinite scroll traps
    - Sponsored manipulation

    Provide safeguards and strict stop conditions.

    Strategy:
    {state.execution_strategy}

    Product Plan:
    {state.product_plan}
    """

    response = llm_graph.invoke(prompt)
    state.safety_plan = response.content
    return state

def synthesize_task(state):
    print("-------Reached synthesize node------------")
    SYSTEM = """
    You generate ONE executable natural-language task for a browser automation agent.

    Hard Rules:
    - Output ONLY one paragraph
    - No markdown
    - No bullet points
    - No explanations
    - Imperative tone
    - Real browser assumption
    - After visiting the website always close the pop ups first, close all the pop ups then proceed to next step.
    - If asked for pincode use 226016 and then hit apply.
    - First search then dont explicitly apply the filter just check the price and then add it to the cart, dont go to the filter column.
    - Must stop safely
    - Never proceed to checkout
    """

    USER = f"""
    Website: {state.user_input.website}

    Intent Analysis:
    {state.intent_analysis}

    Execution Strategy:
    {state.execution_strategy}

    Product Plan:
    {state.product_plan}

    Safety Plan:
    {state.safety_plan}

    Generate the final browser-executable instruction.
    """
    
    messages = [
        ("system", SYSTEM),
        ("user", USER)
    ]
    
    response = llm_graph.invoke(messages)
    state.final_prompt = response.content
    return state
   
def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("intent", understand_intent)
    graph.add_node("strategy", build_strategy)
    graph.add_node("product_plan", plan_products)
    graph.add_node("safety", safety_evaluator)
    graph.add_node("synthesize", synthesize_task)

    graph.set_entry_point("intent")

    graph.add_edge("intent", "strategy")
    graph.add_edge("strategy", "product_plan")
    graph.add_edge("product_plan", "safety")
    graph.add_edge("safety", "synthesize")

    graph.set_finish_point("synthesize")

    return graph.compile()
   

    

async def run_browser_task(task_prompt: str ):
    print("--------Reached browser node---------")
    browser = Browser(
    executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    user_data_dir=os.path.join(os.getcwd(), ".chrome-profile"),
    headless=False)


    agent = Agent(
        task=task_prompt,
        browser=browser,
        llm=llm_browser,
    )

    await agent.run()
    print("Finished running")
    return {"status": "completed"}