from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from agent.graph import build_graph, run_browser_task
from agent.schema import UserInput, AgentState

app = FastAPI()
graph = build_graph()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/execute")
async def execute_task(
    input: UserInput,
    background_tasks: BackgroundTasks):

    state = AgentState(user_input=input)
    result = graph.invoke(state)
    task_prompt = result["final_prompt"]

    print(f"Queued browser task: {task_prompt}")

    background_tasks.add_task(run_browser_task, task_prompt)

    return {
        "task_prompt": task_prompt,
        "execution_status": "started"
    }
