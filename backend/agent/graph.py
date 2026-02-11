import os
from langgraph.graph import StateGraph
from langchain_openai import ChatOpenAI as LangChainChatOpenAI
from browser_use import Agent, Browser, ChatOpenAI as BrowserChatOpenAI, ChatBrowserUse
from agent.schema import AgentState
from dotenv import load_dotenv

from vault import VAULT

load_dotenv()

llm_graph = LangChainChatOpenAI(model="gpt-4o-mini", temperature=0)
# llm_browser = BrowserChatOpenAI(model="gpt-4o-mini")
llm_browser = ChatBrowserUse(model="bu-latest")

def understand_intent(state):
    print("--------Reached understand node-------------")
    prompt = f"""
    You are an intelligent shopping task analyst.

    Analyze the following shopping request and extract:

    - Core objective
    - Shopping intent classification (bulk purchase, price-sensitive, comparison-based, urgent, premium preference, etc.)
    - Explicit and implicit constraints (budget ceilings, quantities, brand restrictions, delivery sensitivity)
    - Automation risk factors (login walls, captchas, regional restrictions, popups, dynamic pricing)

    Website:
    {state.user_input.website}

    Products:
    {[(p.name, p.quantity, p.max_price) for p in state.user_input.products]}

    Return a structured reasoning paragraph.
    """

    response = llm_graph.invoke(prompt)
    state.intent_analysis = response.content
    return state


def build_strategy(state):
    print("--------Reached strategy node-------------")
    prompt = f"""
    You are an e-commerce navigation strategist.

    Based on the website and intent analysis, determine:

    - Whether login should be avoided unless strictly necessary
    - How to handle popups, banners, and location prompts generically
    - Optimal product discovery approach (search bar, navigation menu, or smart suggestions)
    - How to evaluate price without relying on site-specific filter assumptions
    - A universal stopping rule once all required items are added to cart

    Website:
    {state.user_input.website}

    Intent Analysis:
    {state.intent_analysis}

    Return a concise execution strategy paragraph.
    """

    response = llm_graph.invoke(prompt)
    state.execution_strategy = response.content
    return state


def plan_products(state):
    print("--------Reached planning node-------------")
    prompt = f"""
    You are a shopping automation planner.

    For each product below, generate a high-level action plan:

    - Search query strategy
    - How to compare options safely
    - How to verify price constraint compliance
    - How to select quantity
    - Clear condition for considering the product successfully added

    Products:
    {[(p.name, p.quantity, p.max_price) for p in state.user_input.products]}

    Return a product-by-product reasoning paragraph.
    """

    response = llm_graph.invoke(prompt)
    state.product_plan = response.content
    return state


def safety_evaluator(state):
    print("--------Reached safety node-------------")
    prompt = f"""
    You are a browser automation risk assessor.

    Review the strategy and product plan. Identify potential failure triggers such as:

    - CAPTCHA challenges
    - Login requirements
    - OTP verification
    - Forced redirects
    - Infinite scrolling traps
    - Sponsored or misleading listings
    - Out-of-stock loops

    Provide safeguards and strict stop conditions.
    The automation must terminate immediately after all required products are successfully added to the cart.
    It must never proceed to checkout or payment.

    Strategy:
    {state.execution_strategy}

    Product Plan:
    {state.product_plan}
    """

    response = llm_graph.invoke(prompt)
    state.safety_plan = response.content
    return state


def synthesize_task(state):
    print("--------Reached synthesize node-------------")
    SYSTEM = """
    You generate ONE executable natural-language task for a browser automation agent.

    Hard Rules:
    - Output ONLY one paragraph
    - No markdown
    - No bullet points
    - No explanations
    - Imperative tone
    - Assume a real browser environment
    - After loading the website, close any visible popups or overlays before proceeding
    - Avoid logging in unless absolutely required to add items to cart
    - Use the search function when available to locate products
    - Evaluate product price directly from the listing or product page
    - Add only items that satisfy quantity and price constraints
    - Remember the price that user entered is price of individual items not collective.
    - Do not search for reviews if not entered by the user.
    - After all required products are successfully added to the cart, STOP immediately
    - Do NOT navigate to checkout
    - Do NOT initiate payment
    - Do NOT continue browsing after cart completion
    """

    USER = f"""
    Website:
    {state.user_input.website}

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


async def run_browser_task(task_prompt: str):
    browser = Browser(
        executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        user_data_dir=os.path.join(os.getcwd(), ".chrome-profile"),
        headless=False
    )

    agent = Agent(
        task=task_prompt,
        browser=browser,
        llm=llm_browser,
    )

    await agent.run()
    return {"status": "completed"}
