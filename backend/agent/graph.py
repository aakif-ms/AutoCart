import os
from langgraph.graph import StateGraph
from langchain_openai import ChatOpenAI as LangChainChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from browser_use import Agent, Browser, ChatOpenAI as BrowserChatOpenAI
from agent.schema import AgentState
from dotenv import load_dotenv

from vault import VAULT

load_dotenv()

llm_graph = LangChainChatOpenAI(model="gpt-4.1-mini")
llm_browser = BrowserChatOpenAI(model="gpt-4o-mini")

def validate_input(state):
    if not state.user_input.products:
        raise ValueError("At least one product required")
    
    # Basic validation for product names
    for product in state.user_input.products:
        if not product.name.strip():
            raise ValueError("Product name cannot be empty")
        if product.quantity <= 0:
            raise ValueError("Product quantity must be greater than 0")
    
    return state

def normalize_website(state):
    site = state.user_input.website.lower()
    
    if "amazon" in site:
        state.normalized_site = "https://www.amazon.in"
        state.requires_login = True
    elif "flipkart" in site:
        state.normalized_site = "https://www.flipkart.com"
        state.requires_login = True
    else:
        # For other websites, just add https if missing
        if not site.startswith('http'):
            state.normalized_site = f"https://{site}"
        else:
            state.normalized_site = site
        state.requires_login = False
    
    return state

def product_reasoning(state):
    for product in state.user_input.products:
        product.name = product.name.strip()
        product.name = ' '.join(product.name.split())
    
    return state

# def credential_check(state):
#     if not state.requires_login:
#         return state
        
#     key = state.normalized_site.replace("https://", "").replace("www.", "")
#     if key in VAULT:
#         state.credentials = VAULT[key]
    
#     return state

def build_prompt(state):
    
    SYSTEM_PROMPT = """
    You generate ONE executable natural-language task for a browser automation agent.

    Hard rules:
    - Output ONLY a single string
    - No markdown
    - No bullet points
    - No explanations
    - No step numbers
    - Imperative tone
    - Assume a real browser
    - The agent must stop safely
    - Avoid clicking on any login or sign in buttons
    """

    USER_PROMPT = """
    Use the following behavioral instructions and constraints to generate the final task.

    Agent identity and startup:
    "You are an autonomous browser agent. Visit {website} using a real browser."+
    Close any pop-us if available.
    Login behavior:
    If asked for pincode, use 226016
    {login_instructions}

    Product actions:
    {product_instructions}

    Safety constraints:
    "Do NOT proceed to checkout or payment under any circumstances."
    "If a payment page, OTP request, CAPTCHA, or unexpected verification appears, immediately stop and abort the task."
    "Stop execution once all products are added to the cart."

    Generate the final browser-executable task instruction as a single clear paragraph.
    """

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("user", USER_PROMPT),
    ])
    
    if state.credentials:
        login_instructions = (
            "Close the login box if possible, but if forced to login, "
            "sign in using the existing browser profile. "
            "If login fails or a CAPTCHA appears, immediately stop and abort the task."
        )
    else:
        login_instructions = "Do not attempt to log in."

    # ---- product rules ----
    product_lines = []
    for p in state.user_input.products:
        line = f"Search for '{p.name}'."

        if p.max_price:
            line += f" Filter results under ₹{p.max_price}."

        # if p.min_rating:
        #     line += f" Only consider products with rating above {p.min_rating} stars."

        line += " Select the best available matching product and add exactly one unit to the cart."
        product_lines.append(line)

    product_instructions = " ".join(product_lines)

    messages = prompt.format_messages(
        website=state.normalized_site,
        login_instructions=login_instructions,
        product_instructions=product_instructions
    )

    response = llm_graph.invoke(messages)

    state.final_prompt = response.content
    state.status = "planned"
    return state


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("validate", validate_input)
    graph.add_node("normalize", normalize_website)
    graph.add_node("reason", product_reasoning)
    # graph.add_node("creds", credential_check)
    graph.add_node("prompt", build_prompt)

    graph.set_entry_point("validate")
    graph.add_edge("validate", "normalize")
    graph.add_edge("normalize", "reason")
    # graph.add_edge("reason", "creds")
    graph.add_edge("reason", "prompt")
    graph.set_finish_point("prompt")
    
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

    try:
        await agent.run()
        print("Finished running")
        return {"status": "completed"}
    finally:
        await browser.kill() 
