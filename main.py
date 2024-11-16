import streamlit as st
import cohere

# Set up Cohere API
COHERE_API_KEY = '1uwUIUdriN3uDnjB2zais6SEfwmsAXKNnTirGM4H'  # Replace with your actual API key
co = cohere.Client(COHERE_API_KEY)

# Define variables to store session state
if 'answers' not in st.session_state:
    st.session_state.answers = []
if 'current_step' not in st.session_state:
    st.session_state.current_step = 0

# Define a list of questions for the flow
questions = [
    "What are your top skills or areas of expertise?",
    "What industries or types of work are you most interested in?",
    "Do you have any specific tools or technologies you specialize in?",
    "What is your preferred working style (e.g., short-term, long-term projects)?"
]

# Define function to generate AI-enhanced job suggestions
def generate_job_suggestions(answers):
    """
    Generate job suggestions using the Cohere API based on session answers.
    """
    try:
        combined_answers = " | ".join(answers)
        response = co.generate(
            model='command-xlarge-nightly',
            prompt=(
                f"Based on the following inputs, suggest freelancing job opportunities:\n"
                f"{combined_answers}\n"
                f"Provide clear and specific job titles, matching the user's skills and preferences. if the answers were inapproprate or just garbage values , ask the ser to input correct values"
            ),
            max_tokens=100,
            temperature=0.8,
            k=0,
            p=0.75,
            stop_sequences=["--"],
            return_likelihoods='NONE'
        )
        return response.generations[0].text.strip()
    except Exception as e:
        return f"Error generating suggestions: {e}"

# Display the current question
st.title("AI Powered Skill Assessment Test:")
question_label = st.text(questions[st.session_state.current_step])

# Input box for user answer
user_input = st.text_input("Your Answer:", "")

# Button to submit the answer and move to the next question
if st.button("Next"):
    answer = user_input.strip()
    if not answer:
        st.warning("Please provide an answer before proceeding.")
    else:
        # Store the answer and move to the next question
        st.session_state.answers.append(answer)
        st.session_state.current_step += 1
        
        if st.session_state.current_step < len(questions):
            # Display the next question
            st.rerun()  # Use st.rerun() to refresh the app
        else:
            # Generate suggestions based on all answers
            st.write("Generating job suggestions based on your inputs...")
            suggestions = generate_job_suggestions(st.session_state.answers)
            st.write("Job Suggestions:\n")
            st.write(suggestions)
            
            # Do not reset the state and leave the result on the screen
            st.session_state.answers = []  # Optionally reset answers here if needed
            st.session_state.current_step = 0  # Optionally reset current_step here if needed
