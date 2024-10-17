import os
from openai import OpenAI
import streamlit as st

openai_key = os.environ['OpenAI_API_Key']
client = OpenAI(api_key=openai_key)

questions = [
    {
        "text": """Find the sum: 38,075 + 991,002 + 75,600 =""",
        "answer": "1096677",
        "type": "sum"
    },
    {
        "text": """Find the difference: 6,732,189 - 5,401,207 =""",
        "answer": "1330982",
        "type": "difference"
    },
    {
        "text": """Find the product: 6 × 230,000 =""",
        "answer": "1380000",
        "type": "product"
    },
    {
        "text": """Divide: 3,051,000 ÷ 5 =""",
        "answer": "610200",
        "type": "division"
    },
]

current_question_index = 0
user_score = 0

def question(question_index):
    """Fetches the question content and calls OpenAI for step-by-step solution."""
    system_prompt = """
    You are a helpful assistant that can answer questions about grade 6 mathematics questions,
    show the solving step by step. And show the symbol instead of word like x instead of
    /times. Dont show \boxed.
    """
    prompt = questions[question_index]["text"] + "\n" + system_prompt
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt},
        ],
        temperature=0.1,
        max_tokens=2000
    )
   
    return response.choices[0].message.content

def check_answer(user_input):
    """Checks the user's answer and updates score."""
    correct_answer = questions[current_question_index]["answer"]
    if user_input == correct_answer:
        global user_score
        user_score += 1
        return "Correct! You earned 1 mark. Your score is now " + str(user_score)
    else:
        correct_answer_text = "Incorrect. The correct answer is " + str(correct_answer)
        return correct_answer_text

if __name__ == "__main__":
    # Display the question
    if current_question_index < len(questions):
        question_text = questions[current_question_index]["text"]
        st.write(question_text)

        # User input and answer check
        user_answer = st.text_input("Answer")
        if st.button("Submit Answer"):
            feedback = check_answer(user_answer)
            st.write(feedback)

            # Move to the next question if there are more
            if current_question_index < len(questions) - 1:
                current_question_index += 1

    # Button to display next question (if available)
    if current_question_index < len(questions) and user_score > 0:
        if st.button("Next Question"):
            # Clear the previous question and display the next one
            st.write("")  # Clear previous content
            st.write(questions[current_question_index]["text"])
            current_question_index += 1