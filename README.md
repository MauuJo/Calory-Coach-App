# 🥗 Calorie Coach AI

An intelligent, conversational nutrition assistant designed to help users track macros, understand their eating habits, and receive personalized health coaching in real-time.

## 🚀 Features

- **Natural Language Logging:** No more searching through databases. Just type "I had a bowl of oatmeal with blueberries" and let the AI do the math.
- **Personalized Coaching:** Receive proactive advice based on your daily goals (e.g., "You're a bit low on protein today; try adding Greek yogurt to your snack").
- **Macro Breakdown:** Automatic calculation of Calories, Proteins, Carbs, and Fats.
- **Progress Tracking:** Weekly summaries and insights into your nutritional trends.

## 🛠️ Tech Stack

- **Backend:** Python 3.10+, FastAPI
- **AI Engine:** Google Gemini API (or OpenAI GPT-4)
- **Data Handling:** Pandas & Pydantic
- **Environment:** Dotenv for secure API key management

## 📦 Installation

1.  **Clone the repository:**

    ```bash
    git clone [https://github.com/yourusername/calorie-coach.git](https://github.com/yourusername/calorie-coach.git)
    cd calorie-coach
    ```

2.  **Create a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your environment variables:**
    Create a `.env` file in the root directory and add your API keys:
    ```env
    AI_API_KEY=your_api_key_here
    PORT=8000
    ```

## 🚦 Quick Start

Run the application locally:

```bash
uvicorn main:app --reload
```
