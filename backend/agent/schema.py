from pydantic import BaseModel
from typing import List, Optional, Dict, Literal

class ProductInput(BaseModel):
    name: str
    max_price: Optional[int] = None
    max_rating: Optional[float] = None
    quantity: int = 1
    
class UserInput(BaseModel):
    website: str
    products: List[ProductInput]

class AgentState(BaseModel):
    user_input: UserInput
    normalized_site: Optional[str] = None
    requires_login: bool = False
    credentials: Optional[Dict[str, str]] = None
    final_prompt: Optional[str] = None

    status: Literal[
        "idle",
        "planned",
        "running",
        "aborted",
        "completed",
    ] = "idle"