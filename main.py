from flask import Flask, render_template, request, redirect, url_for
import openai

app = Flask(__name__)

# Replace 'your-openai-api-key' with your actual OpenAI API key
openai.api_key = 'your-openai-api-key'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/text', methods=['GET', 'POST'])
def text_generator():
    if request.method == 'POST':
        prompt = request.form['prompt']
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150
        )
        return render_template('text.html', generated_text=response.choices[0].text, prompt=prompt)
    return render_template('text.html', generated_text=None)

@app.route('/image', methods=['GET', 'POST'])
def image_generator():
    if request.method == 'POST':
        prompt = request.form['prompt']
        response = openai.Image.create(
            model="dall-e-2",
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        image_url = response.data[0].url
        return render_template('image.html', image_url=image_url, prompt=prompt)
    return render_template('image.html', image_url=None)

if __name__ == '__main__':
    app.run(debug=True)
