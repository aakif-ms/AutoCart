from fastapi import FastAPI
from agent.graph import build_graph, run_browser_task
from agent.schema import UserInput, AgentState

app = FastAPI()
graph = build_graph()

@app.post("/plan")
def plan(input: UserInput):
    state = AgentState(user_input=input)
    result = graph.invoke(state)
    return {"task_prompt": result.final_prompt}

@app.post("/run-browser-task")
async def run_task():
    print("Running from main")
    await run_browser_task()
    return {"status": "completed"}