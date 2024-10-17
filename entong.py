import os
import streamlit as st
from openai import OpenAI

#client = OpenAI(api_key=os.environ["OpenAI_API_Key"])
client = OpenAI(api_key=st.secrets["OpenAI_API_Key"])

# Function to generate a question
def question(prompt):
  system_prompt = """
  You are a helpful assistant that can create questions about grade 6 mathematics question. Generate mathematics question randomly. Besides, let the questions be numbers and the users just need to answer in number format.
  """
  response =   client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
     {"role": "system", "content": system_prompt},
      {"role": "user", "content": prompt}
    ],
    temperature=1.3, #>1 to be more random
    max_tokens=2000
  )
  return response.choices[0].message.content

# Function to generate an answer
def answer(prompt):
  system_prompt = """
  This is the answer for question that given just now.
  """
  response =   client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
     {"role": "system", "content": system_prompt},
      {"role": "user", "content": prompt}
    ],
    temperature=1.3, #>1 to be more random
    max_tokens=2000
  )
  return response.choices[0].message.content

# Function to check the answer
def check_answer(user_input, correct_answer):
  if user_input == correct_answer:
    return "Correct! You earned 1 mark."
  else:
    return f"Incorrect. The correct answer is {correct_answer}"

# Function to display the question and get user input
def display_question(question_text):
  user_answer = st.text_input("Answer")
  if st.button("Submit Answer"):
    feedback = check_answer(user_answer, correct_answer)
    st.write(feedback)

# Function to track user score and questions answered
def track_score(current_score, question_number):
    if question_number > 0:
        current_score += 1
    return current_score

def display_score(current_score):
    st.write(f"Your score: {current_score} out of {question_limit}")

# Main function
def main():
    st.title("Academy Fighter")
    st.write("Welcome to Academy Fighter, a tool for solving mathematics questions.")

    # Track score and question number
    current_score = 0
    question_number = 0
    question_limit = 10  # Maximum number of questions

    # Display the question
    if st.button("Generate Question"):
        st.divider()
        question_text = question("Generate a question")
        st.write(question_text)
        if question_number < question_limit:  # Only allow up to 10 questions
            question_number += 1
            display_question(question_text)
            current_score = track_score(current_score, question_number - 1)  # Update score after answering

    if question_number == question_limit:
        display_score(current_score)  # Show score after answering all questions

if __name__ == "__main__":
    main()

