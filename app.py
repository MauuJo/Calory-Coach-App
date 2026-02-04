import os
import re
import google.generativeai as genai
from PIL import Image
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = "secret_nutrition_key" # Required for flash messages

# --- STEP 2: Initialize Gemini Model ---
# Ensure you have GEMINI_API_KEY in your .env file
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Using Gemini 1.5 Flash for multimodal capabilities (image + text)
model = genai.GenerativeModel('gemini-2.5-flash')

# --- STEP 3: Image Handling Helper ---
def input_image_setup(uploaded_file):
    """
    Prepares the uploaded image for Gemini.
    Unlike WatsonX, Gemini accepts PIL Image objects directly.
    """
    if uploaded_file is not None:
        # Open the image using PIL
        image = Image.open(uploaded_file)
        return image
    else:
        raise FileNotFoundError("No file uploaded")

# --- STEP 4: Response Formatting Helper ---
def format_response(response_text):
    """
    Converts Gemini's Markdown output into clean HTML for the Flask frontend.
    """
    # 1. Convert Markdown bold (**text**) to HTML strong
    response_text = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", response_text)

    # 2. Convert Bullet points (*) to HTML list items (<li>)
    response_text = re.sub(r"(?m)^\s*[\*\-]\s+(.*)", r"<li>\1</li>", response_text)

    # 3. Wrap groups of <li> in <ul> tags
    response_text = re.sub(r"(<li>.*?</li>)+", lambda match: f"<ul>{match.group(0)}</ul>", response_text, flags=re.DOTALL)

    # 4. Handle line breaks and paragraphs
    response_text = response_text.replace('\n\n', '</p><p>').replace('\n', '<br>')
    
    return f"<div class='analysis-result'>{response_text}</div>"

# --- STEP 5: Generate Model Response ---
def generate_model_response(image_object, user_query, assistant_prompt):
    """
    Sends the image and prompt to Gemini and retrieves the formatted analysis.
    """
    try:
        # Combine the persona prompt with the user's specific request
        full_prompt = f"{assistant_prompt}\n\nAdditional User Request: {user_query}"
        
        # Gemini takes a list of [prompt_text, image_data]
        response = model.generate_content([full_prompt, image_object])
        
        # Format the raw markdown text into HTML
        formatted_response = format_response(response.text)
        return formatted_response
    except Exception as e:
        print(f"Error in generating response: {e}")
        return "<p>An error occurred while the AI Coach was analyzing your meal.</p>"

# --- MAIN ROUTE ---
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_query = request.form.get("user_query")
        uploaded_file = request.files.get("file")

        if uploaded_file and uploaded_file.filename != '':
            try:
                # Process the image (Step 3)
                image_data = input_image_setup(uploaded_file)

                # The Prompt (from Step 6 of your lab)
                assistant_prompt = """
                You are an expert nutritionist. Your task is to analyze the food items displayed in the image and provide a detailed nutritional assessment using the following format:

                1. **Identification**: List each identified food item clearly, one per line.
                2. **Portion Size & Calorie Estimation**: For each identified food item, specify the portion size and provide an estimated number of calories. Use bullet points with the following structure:
                - **[Food Item]**: [Portion Size], [Number of Calories] calories

                3. **Total Calories**: Provide the total number of calories for all food items.
                Format: Total Calories: [Number of Calories]

                4. **Nutrient Breakdown**: Include a breakdown of Protein, Carbohydrates, Fats, Vitamins, and Minerals. Use bullet points.

                5. **Health Evaluation**: Evaluate the healthiness of the meal in one paragraph.

                6. **Disclaimer**: 
                The nutritional information and calorie estimates provided are approximate and are based on general food data. 
                Actual values may vary. For precise dietary advice, consult a qualified nutritionist.
                """

                # Generate and format response (Step 5)
                response = generate_model_response(image_data, user_query, assistant_prompt)

                return render_template("index.html", user_query=user_query, response=response)

            except Exception as e:
                flash(f"Error processing image: {str(e)}", "danger")
                return redirect(url_for("index"))
        else:
            flash("Please upload an image file.", "danger")
            return redirect(url_for("index"))

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)