import streamlit as st
import cohere


# Set the page configuration as the first command

st.set_page_config(page_title="AI Study Plan Generator", page_icon="📚", layout="wide")

# Initialize Cohere API with your API key
API_KEY = 'bPokOB6tPxnyyJJR2XNeXTTGHyUHB3m98SsHVFDg'  # Replace 'YOUR_API_KEY' with your actual Cohere API key
co = cohere.Client(API_KEY)

def generate_roadmap(domain,time):
    # Updated prompt with better structure for clear sectioning
    prompt = f"""Create a detailed study plan for {domain} for a total of {time} hours. The plan should break down the subject into key topics, allocate time for each topic, and include time for revision and practice problems if there was any. Prefer short study sessions with breaks in between. Please provide a structured schedule that covers the entire subject {domain} effectively.

    Please make sure to clearly label each section with a title followed by concise details for learners,
    
    please note it importantly
    dont include any bold , italian or any typograpic ,
    dont include symbols like # * etc,
    """

    # Call Cohere API to generate the roadmap
    response = co.generate(
        model='command-xlarge-nightly',
        prompt=prompt,
        max_tokens=2000,
        temperature=0.7
    )

    # Extract and clean the generated text
    roadmap_text = response.generations[0].text.strip()
    return roadmap_text

def parse_roadmap(roadmap_text):
    sections = roadmap_text.split('\n\n')  
    parsed_sections = []

    for section in sections:
        lines = section.split('\n')
        title = lines[0].strip() if lines else ''
        content = '\n'.join(lines[1:]).strip() if len(lines) > 1 else ''
        
        parsed_sections.append({'title': title, 'content': content})
    
    return parsed_sections

# Streamlit UI
st.title("AI-Powered Study Plan Generator")
st.markdown("Enter the topic: ")

# Input field for domain
domain = st.text_input("Please specify your Subject:")
time = st.text_input("Please specify your time [hours]:")

# Button to generate roadmap
if st.button("Generate Study Plan"):
    if domain:
        with st.spinner("Generating Study Plan..."):
            # Generate and parse the roadmap
            roadmap_text = generate_roadmap(domain,time)
            parsed_roadmap = parse_roadmap(roadmap_text)

            # Custom CSS for glassmorphism and white headings
            st.markdown(
                """
                <style>
                .glass-container {
                    background: rgba(255, 255, 255, 0.2);
                    color: #D334FF;
                    border-radius: 15px;
                    padding: 20px;
                    margin: 20px 0;
                    box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
                    backdrop-filter: blur(10px);
                    border: 1px solid rgba(255, 255, 255, 0.18);
                }

                .glass-container:hover {
                    animation: glow 3s infinite;
                }

                @keyframes glow {
                    0% { box-shadow: 0 0 10px rgba(201,76,255,1); }
                    50% { box-shadow: 0 0 20px rgba(143,0,205,1); }
                    100% { box-shadow: 0 0 10px rgba(201,76,255,1); }
                }

                .arrow {
                    width: 30px;
                    height: 30px;
                    margin: 0 auto;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }

                .arrow::before {
                    content: '';
                    display: block;
                    width: 0;
                    height: 0;
                    border-left: 10px solid transparent;
                    border-right: 10px solid transparent;
                    border-top: 15px solid #D334FF;
                    animation: bounce 1s infinite;
                }

                @keyframes bounce {
                    0%, 100% {
                        transform: translateY(0);
                    }
                    50% {
                        transform: translateY(-5px);
                    }
                }

                .step-title {
                    font-size: 20px;
                    font-weight: bold;
                    color: white; 
                    margin-bottom: 10px;
                }

                .step-details {
                    font-size: 16px;
                    color: white;
                }

                h1, h2, h3, h4, h5, h6 {
                    color: white; 
                }
                </style>
                """,
                unsafe_allow_html=True
            )

            # Display each section with a glassmorphism container
            for section in parsed_roadmap:
                if section['title'] and section['content']:
                    st.markdown(
                        f"""
                        <div class="glass-container">
                            <div class="step-title">{section['title']}</div>
                            <div class="step-details">{section['content']}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    # Add a dynamic CSS arrow between steps
                    if section != parsed_roadmap[-1]:
                        st.markdown('<div class="arrow"></div>', unsafe_allow_html=True)

    else:
        st.warning("Please enter a Topic to generate the studyplan .")
