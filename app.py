from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
from groq import Groq

app = Flask(__name__)

# Initialize your OpenAI client (replace with your actual API key)
client = Groq(
    api_key="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"
)

def answer_rater(user_message):
    system_content = """
                    You are an online IELTS writing test checker who will assess the candidate's answer and will give the overall band, strengths and areas of improvements, tips to score more.
                    """
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_message}
        ],
        model="llama3-8b-8192"
    )

    return chat_completion.choices[0].message.content

def ques_gen(user_message):
    system_content = """
                    You are an online IELTS writing test invigilator who will ask questions to the candidate. Respond in very short one or two sentences. And when asking the question, format in this way "Question: <question>", like that.
                    """
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_message}
        ],
        model="llama3-8b-8192"
    )
    return chat_completion.choices[0].message.content

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/general')
def general():
    return render_template('general.html')

@app.route('/academic')
def academic():
    return render_template('academic.html')

@app.route('/academic/reading')
def reading():
    return render_template('reading.html')

@app.route('/academic/writing')
def writing():
    return render_template('writing.html', firstquestion="If you are ready, ask me a question.")

@app.route('/academic/listening')
def listening():
    return render_template('listening.html')

@app.route('/academic/speaking')
def speaking():
    return render_template('speaking.html')

@app.route('/get_question', methods=['POST'])
def get_question():
    user_message = request.json['message']
    question = ques_gen(user_message)
    return jsonify({"question": question})


@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    user_answer = request.json['answer']
    # Get the rating from the answer_rater function
    rating = answer_rater(user_answer)
    # Pass the rating to the rating page directly
    return render_template('rating.html', rating=rating)

@app.route('/rating')
def rating():
    # Just render the rating page; no need to handle rating here
    return render_template('rating.html')

if __name__ == '__main__':
    app.run(debug=True)


# from flask import Flask, render_template, request, jsonify, redirect, url_for
# import json
# from groq import Groq

# app = Flask(__name__)

# # Initialize your OpenAI client (replace with your actual API key)
# client = Groq(
#     api_key="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"
# )

# def answer_rater(user_message):
#     system_content = """
#                     You are an online IELTS writing test checker who will assess the candidate's answer and will give the overall band, strengths and areas of improvements, tips to score more.
#                     """
#     chat_completion = client.chat.completions.create(
#         messages=[
#             {"role": "system", "content": system_content},
#             {"role": "user", "content": user_message}
#         ],
#         model="llama3-8b-8192"
#     )

#     return chat_completion.choices[0].message.content

# def ques_gen(user_message):
#     system_content = """
#                     You are an online IELTS writing test invigilator who will ask questions to the candidate. Respond in very short one or two sentences. And when asking the question, format in this way "Question: <question>", like that.
#                     """
#     chat_completion = client.chat.completions.create(
#         messages=[
#             {"role": "system", "content": system_content},
#             {"role": "user", "content": user_message}
#         ],
#         model="llama3-8b-8192"
#     )
#     return chat_completion.choices[0].message.content

# @app.route('/')
# def home():
#     return render_template('home.html')

# @app.route('/general')
# def general():
#     return render_template('general.html')

# @app.route('/academic')
# def academic():
#     return render_template('academic.html')

# @app.route('/academic/reading')
# def reading():
#     return render_template('reading.html')

# @app.route('/academic/writing')
# def writing():
#     return render_template('writing.html', firstquestion="If you are ready, ask me a question.")

# @app.route('/academic/listening')
# def listening():
#     return render_template('listening.html')

# @app.route('/academic/speaking')
# def speaking():
#     return render_template('speaking.html')

# @app.route('/get_question', methods=['POST'])
# def get_question():
#     user_message = request.json['message']
#     question = ques_gen(user_message)
#     return jsonify({"question": question})

# @app.route('/submit_answer', methods=['POST'])
# def submit_answer():
#     user_answer = request.json['answer']
#     # Get the rating from the answer_rater function
#     rating = answer_rater(user_answer)
#     # Return the rating as a JSON response
#     return jsonify({"rating": rating})

# @app.route('/rating')
# def rating():
#     # Just render the rating page; no need to handle rating here
#     return render_template('rating.html')

# if __name__ == '__main__':
#     app.run(debug=True)
