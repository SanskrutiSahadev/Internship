from flask import Flask, request, jsonify, render_template
from IPython.display import display, Markdown

app = Flask(__name__)

# This function processes the data and generates the "real-time" output text
def generate_output(name, age, hobby):
    # Sanitize and format the input
    name = name.strip()
    
    # Logic to format the output content dynamically
    if name:
        name_output = f"<b>{name}</b>"
        greeting = f"Fantastic to Meet You, {name}! 🎉"
        output_name_tag = f'<h2 class="output-name">{name}! <span class="emoji">🎉</span></h2>'
    else:
        name_output = "a new friend"
        greeting = "Welcome! Say Hello"
        output_name_tag = '<h2 class="output-name">New Friend! <span class="emoji">🎉</span></h2>'


    hobbies_list = [h.strip() for h in hobby.split(',') if h.strip()]

    # Assemble the dynamic content for Stage 2
    output_html = f"""
        <p class="greeting">
            <span class="emoji">🎶</span> <b>{greeting}</b>
        </p>
        <b>{output_name_tag}</b>
        <p class="snapshot-header">Here's a snapshot of who you are</p>
        <ul class="output-list">
            <li>You are <b>{name_output}</b>! That's plenty of awesome to start!</li>
    """
    
    if hobbies_list:
        # Just taking the first two hobbies for a concise display
        favorite_pastime = ", ".join(hobbies_list[:2]) + ("..." if len(hobbies_list) > 2 else "")
        output_html += f"""
            <li>And we love that your favorite pastime is <b>{favorite_pastime}</b>. 
            This seems like a wonderful way to spend your time.</li>
        """
    
    output_html += """
        </ul>
        <p class="adventure-text">
            ## Let's start the adventure!
            We're so happy to have you here. See just what we can do together.
        </p>
        <button class="btn-secondary">
            Explore the Program
        </button>
    """
    
    return output_html

@app.route('/')
def index():
    # Render the initial HTML template (which includes the internal CSS)
    return render_template('task1.html')


@app.route('/result', methods=['POST'])
def result():
    name = request.form.get('name', '')
    age = request.form.get('age', '')
    hobby = request.form.get('hobby', '')
    
    output_html = generate_output(name, age, hobby)

    return render_template('result.html', output_html=output_html)


if __name__ == '__main__':
    # Flask will look for templates in a 'templates' folder
    app.run(debug=True)