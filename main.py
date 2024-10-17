import os
import streamlit as st
from openai import OpenAI

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

  question_text = response.choices[0].message.content.split("\n")
  answer_text = response.choices[0].message.content.split("\n")
  return question_text, answer_text

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

# Function to give feedback to the user
#def feedback_solution()

# Function to check the answer
def check_answer(question_text, answer_text):
  if question_text == answer_text:
    return "Correct! You earned 1 mark."
  else:
    return "Incorrect. The correct answer is " + str(answer_text)

#Verify Answer
def verify_answer(user_answer, question_text):
  system_prompt = f"This is the solution for the question: {question_text}"
  response = client.chat.completions.create(
      model="gpt-4o-mini",
      messages=[
          {"role": "system", "content": system_prompt},
          {"role": "user", "content": user_answer}
      ],
      temperature=1.3,
      max_tokens=2000
  )
  answer_text = response.choices[0].message.content.strip()
  return answer_text == user_answer

# Function to display the question and get user input
def display_question(question_text, answer_text):
  user_answer = st.text_input("Answer")
  if st.button("Submit Answer"):
    if verify_answer(user_answer, question_text):
      feedback = "Correct! You earned 1 mark."
    else:
      feedback = "Incorrect. The correct answer is " + str(answer_text)  
      # Replace with actual logic to get correct answer
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
    st.write("""
    Welcome to Academy Fighter, a tool for solving Grade 6 mathematics questions. Please Click 
    'Generate Question' to start answering the question.""")

    # Track score and question number
    current_score = 0
    question_number = 0
    question_limit = 10  # Maximum number of questions

    # Display the question
    if st.button("Generate Question"):
        st.divider()
        question_text, answer_text = question("Generate a question")
        st.write(question_text)
        if question_number < question_limit:  # Only allow up to 10 questions
            question_number += 1
            display_question(question_text, answer_text)
            current_score = track_score(current_score, question_number - 1)  
            # Update score after answering

    if question_number == question_limit:
        display_score(current_score)  # Show score after answering all questions

if __name__ == "__main__":
    main()

