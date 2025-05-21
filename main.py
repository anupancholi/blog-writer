from flask import Flask, render_template, request
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate', methods=['GET', 'POST'])
def generate():
    if request.method == 'POST':
        user_input = request.json.get('prompt')  # Get input from frontend

        # ✅ Setup prompt
        prompt = PromptTemplate.from_template(
            "Generate a blog on title {title}?")

        # ✅ Get OpenAI API key from environment
        openai_key = os.getenv("OPENAI_API_KEY")
        if not openai_key:
            return "OPENAI_API_KEY is not set", 500

        # ✅ Create LLM with api_key
        llm = OpenAI(temperature=0.4, api_key=openai_key)

        # ✅ Setup the chain
        chain = LLMChain(llm=llm, prompt=prompt)

        # ✅ Run the chain with title argument
        output = chain.run({'title': user_input})

        return output


app.run(host='0.0.0.0', port=81)
