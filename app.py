from flask import Flask, render_template, request, redirect, url_for, flash
import openai
from flask import session
 # Add a secret key for session management


app = Flask(__name__)
app.config['SECRET_KEY'] = 'key' 
# Replace 'your-openai-api-key' with your actual OpenAI API key
openai.api_key = 'your-openai-api-key'

# Dummy user database
users = {'admin': 'password'}

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')

@app.route('/logout')
def logout():
    # Remove 'username' from session
    session.pop('username', None)
    # Optionally, you can use flash to confirm the user has logged out
    flash('You have been logged out.')
    # Redirect to the login page
    return redirect(url_for('login'))


#@app.route('/')
#def home():
#    return render_template('home.html')

@app.route('/text', methods=['GET', 'POST'])
def text_generator():
    if request.method == 'POST':
        prompt = request.form['prompt']
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150
        )
        generated_text = response.choices[0].text
        
        # Update chat history in session
        if not session.get('chat_history'):
            session['chat_history'] = []
        session['chat_history'].append({'sender': 'user', 'text': prompt})
        session['chat_history'].append({'sender': 'ai', 'text': generated_text})
        session.modified = True

        return redirect(url_for('text_generator'))
    return render_template('text.html')


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

        # Update image history in session
        if 'image_history' not in session:
            session['image_history'] = []
        session['image_history'].append({'prompt': prompt, 'url': image_url})
        session.modified = True

        return redirect(url_for('image_generator'))
    return render_template('image.html')

if __name__ == '__main__':
    app.run(debug=True)
