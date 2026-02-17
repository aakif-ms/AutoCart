# 🛒 AutoCart - AI-Powered Shopping Assistant

AutoCart is an intelligent automation system that navigates e-commerce websites and automatically adds products to your shopping cart based on your specifications. Using advanced AI reasoning and browser automation, AutoCart can understand shopping intent, plan execution strategies, and safely interact with various e-commerce platforms.

## ✨ Features

- **🤖 Intelligent Shopping Agent**: Multi-stage AI reasoning pipeline for optimal shopping strategies
- **🌐 Universal Site Support**: Works with any e-commerce website without hardcoded site-specific logic
- **🎯 Smart Product Search**: Automatically finds products based on name, price, quantity, and rating constraints
- **🛡️ Safety-First Design**: Built-in safeguards prevent unintended checkout or payment actions
- **📱 Modern Web Interface**: Clean, responsive UI built with Next.js and Tailwind CSS
- **⚡ Real-time Execution**: Live status updates and task monitoring
- **🔐 Secure Credentials**: Vault system for storing login credentials when needed

## Demo Video
https://github.com/user-attachments/assets/6342e91f-7bc5-46c8-9bf3-8939c1f0cbed

## 🏗️ Architecture

### Frontend (Next.js + TypeScript)
- Modern React application with TypeScript
- Tailwind CSS for responsive styling
- Real-time task execution monitoring
- Intuitive product specification interface

### Backend (FastAPI + Python)
- RESTful API with asyncio support
- LangGraph for AI workflow orchestration
- Browser automation using Playwright
- Multi-model LLM support (GPT-4, custom models)

### AI Agent System
The core AI agent operates through a sophisticated pipeline:

1. **Intent Analysis** - Understands shopping goals and constraints
2. **Strategy Building** - Plans navigation approach for the target website
3. **Product Planning** - Creates specific action plans for each product
4. **Safety Evaluation** - Identifies potential risks and failure modes
5. **Task Synthesis** - Generates executable browser automation instructions

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Google Chrome browser
- OpenAI API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AutoCart
   ```

2. **Backend Setup**
   ```bash
   cd backend
   pip install -e .
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   ```

4. **Environment Configuration**
   
   Create a `.env` file in the backend directory:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

5. **Install Playwright Browsers**
   ```bash
   playwright install chromium
   ```

### Running the Application

1. **Start the Backend**
   ```bash
   cd backend
   uvicorn main:app --reload
   ```
   Backend will be available at `http://localhost:8000`

2. **Start the Frontend**
   ```bash
   cd frontend
   npm run dev
   ```
   Frontend will be available at `http://localhost:3000`

## 🎮 Usage

1. **Open the application** in your browser at `http://localhost:3000`

2. **Enter your shopping request**:
   - **Website**: The e-commerce site you want to shop on (e.g., `amazon.com`)
   - **Products**: Add products with specifications:
     - Product name (required)
     - Maximum price (optional)
     - Quantity (default: 1)
     - Minimum rating (optional)

3. **Execute the task** and monitor real-time progress

4. **Review results** - The AI agent will add qualifying products to your cart and stop before checkout

### Example Shopping Request

```json
{
  "website": "amazon.com",
  "products": [
    {
      "name": "Wireless Bluetooth Headphones",
      "max_price": 100,
      "quantity": 1,
      "rating": "4+"
    },
    {
      "name": "USB-C Cable",
      "max_price": 15,
      "quantity": 2
    }
  ]
}
```

## 🔧 Configuration

### Model Configuration

The system supports multiple LLM providers:

```python
# LangChain models for planning
llm_graph = LangChainChatOpenAI(model="gpt-4o-mini", temperature=0)

# Browser automation models
llm_browser = ChatBrowserUse(model="bu-2-0")  # Custom browser-optimized model
# llm_browser = BrowserChatOpenAI(model="gpt-4o-mini")  # Alternative
```

### Credential Management

Update [vault.py](backend/vault.py) to add site-specific credentials:

```python
VAULT = {
    "amazon.com": {
        "username": "your_username",
        "password": "your_password"
    },
    "target.com": {
        "username": "another_username", 
        "password": "another_password"
    }
}
```

### Browser Settings

Customize browser behavior in [graph.py](backend/agent/graph.py):

```python
browser = Browser(
    executable_path="/path/to/chrome",  # Chrome executable path
    user_data_dir="./chrome-profile",   # Profile directory
    headless=False,                      # Set to True for headless mode
    keep_alive=True                      # Keep browser open after tasks
)
```

## 🛡️ Safety Features

AutoCart includes several built-in safety mechanisms:

- **Checkout Prevention**: Never proceeds to checkout or payment pages
- **Price Verification**: Double-checks prices before adding items
- **Quantity Limits**: Respects specified quantity constraints
- **CAPTCHA Detection**: Gracefully handles anti-bot measures
- **Session Management**: Maintains secure browsing sessions
- **Error Recovery**: Robust error handling and recovery mechanisms

## 📁 Project Structure

```
AutoCart/
├── backend/
│   ├── main.py              # FastAPI application entry point
│   ├── vault.py             # Credential storage
│   ├── pyproject.toml       # Python dependencies
│   └── agent/
│       ├── graph.py         # AI agent workflow and browser automation
│       └── schema.py        # Pydantic models and data structures
├── frontend/
│   ├── app/
│   │   ├── page.tsx         # Main shopping interface
│   │   ├── layout.tsx       # App layout and styling
│   │   └── globals.css      # Global styles
│   ├── services/
│   │   └── api.ts           # API client and types
│   ├── package.json         # Node.js dependencies
│   └── next.config.ts       # Next.js configuration
└── README.md
```

## 🔄 API Reference

### POST /execute

Execute a shopping task with the AI agent.

**Request Body:**
```json
{
  "website": "string",
  "products": [
    {
      "name": "string",
      "max_price": "number (optional)",
      "quantity": "number",
      "rating": "string (optional)"
    }
  ]
}
```

**Response:**
```json
{
  "task_prompt": "string",
  "execution_status": "started"
}
```

## 🧪 Development

### Running Tests

```bash
# Backend tests
cd backend
python -m pytest

# Frontend tests  
cd frontend
npm test
```

### Code Quality

```bash
# Python linting
cd backend
black . && isort . && flake8

# TypeScript/React linting
cd frontend
npm run lint
```

## ⚠️ Disclaimer

AutoCart is designed for educational and personal use. Please:
- Use responsibly and respect website terms of service
- Do not use for unauthorized or malicious activities  
- Test thoroughly before relying on automated purchases
- Keep credentials secure and use at your own risk

## 🙏 Acknowledgments

- [LangChain](https://github.com/langchain-ai/langchain) for AI workflow orchestration
- [Browser-Use](https://github.com/browser-use/browser-use) for intelligent browser automation
- [FastAPI](https://fastapi.tiangolo.com/) for the robust backend framework
- [Next.js](https://nextjs.org/) for the modern frontend framework
- [Playwright](https://playwright.dev/) for reliable browser automation
