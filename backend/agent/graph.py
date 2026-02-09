import os
from langgraph.graph import StateGraph
from langchain_openai import ChatOpenAI
from agent.schema import AgentState
from browser_use import Agent, Browser, ChatOpenAI
from dotenv import load_dotenv

from vault import VAULT

load_dotenv()

llm = ChatOpenAI(model="gpt-4.1-mini")

def validate_input(state):
    if not state.user_input.products:
        raise ValueError("At least one product required")
    return state

def normalize_website(state):
    site = state.user_input.website.lower()
    if "amazon" in site:
        state.normalize_site = "https://www.amazon.in"
        state.requires_login = True
    return state

def product_reasoning(state):
    return state

def credential_check(state):
    key = state.normalize_site.replace("https://", "")
    if state.requires_login and key in VAULT:
        state.credentials = VAULT[key]
    return state

def build_prompt(state):
    lines = []
    lines.append(f"Visit {state.normalized_site}.")

    if state.credentials:
        lines.append(
            "If not logged in, sign in using the provided email and password."
        )

    for p in state.user_input.products:
        line = f"Search for '{p.name}'."
        if p.max_price:
            line += f" Filter results under ₹{p.max_price}."
        if p.min_rating:
            line += f" Choose products with rating above {p.min_rating} stars."
        line += " Add the best matching product to the cart."
        lines.append(line)

    lines.append("Stop after confirming all items are added to the cart.")
    lines.append("Abort if CAPTCHA or payment page is detected.")

    state.final_prompt = " ".join(lines)
    return state

def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("validate", validate_input)
    graph.add_node("normalize", normalize_website)
    graph.add_node("reason", product_reasoning)
    graph.add_node("creds", credential_check)
    graph.add_node("prompt", build_prompt)

    graph.set_entry_point("validate")
    graph.add_edge("validate", "normalize")
    graph.add_edge("normalize", "reason")
    graph.add_edge("reason", "creds")
    graph.add_edge("creds", "prompt")
    graph.set_finish_point("prompt")
    
    return graph.compile()

async def run_browser_task():
    print("--------Reached browser node---------")
    browser = Browser(
    use_cloud=True,  
    )

    agent = Agent(
        task="Visit https://www.instacart.com/. Search for 'wireless mouse'. Add a mouse that is under $30. Add the best matching product to the cart. Stop after confirming all items are added to the cart. Abort if CAPTCHA or payment page or login page is detected. If asked for login use this email id: od_ams@yahoo.com",
        browser_session=browser,
        llm=llm,
    )

    try:
        await agent.run()
        print("Finished running")
        return {"status": "completed"}
    finally:
        await browser.kill() 
