from pydantic import BaseModel
from typing import List, Optional, Dict, Literal

class ProductInput(BaseModel):
    name: str
    max_price: Optional[int] = None
    rating: Optional[str] = None
    quantity: int = 1
    
class UserInput(BaseModel):
    website: str
    products: List[ProductInput]

class AgentState(BaseModel):
    user_input: UserInput
    normalized_site: Optional[str] = None
    requires_login: bool = False
    credentials: Optional[Dict[str, str]] = None

    intent_analysis: Optional[str] = None
    execution_strategy: Optional[str] = None
    product_plan: Optional[str] = None
    safety_plan: Optional[str] = None
    
    final_prompt: Optional[str] = None