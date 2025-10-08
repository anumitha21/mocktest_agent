
import streamlit as st
from document_processor import DocumentProcessor
from mcq_generator import MCQGenerator
import os
from dotenv import load_dotenv

load_dotenv()

def main():
    st.title("Placement AI - Your Personal Interview and Aptitude Trainer")
    
    # Initialize processors
    doc_processor = DocumentProcessor()
    mcq_generator = MCQGenerator()
    
    # Session state for storing questions, answers, and history
    if 'questions' not in st.session_state:
        st.session_state.questions = []
    if 'answers' not in st.session_state:
        st.session_state.answers = {}
    if 'submitted' not in st.session_state:
        st.session_state.submitted = False
    if 'score_history' not in st.session_state:
        st.session_state.score_history = []
    if 'category_history' not in st.session_state:
        st.session_state.category_history = []
    if 'current_weak_areas' not in st.session_state:
        st.session_state.current_weak_areas = []
    
    # Sidebar for configuration and score
    with st.sidebar:
        st.header("Configuration")
        
        # Document category selection
        category = st.selectbox(
            "Select Question Category",
            doc_processor.get_available_categories(),
            format_func=lambda x: "Aptitude Questions" if x == "aptitude" else "Interview Questions"
        )
        
        # Current test score
        if st.session_state.submitted:
            # Calculate current score
            correct_answers = sum(1 for q_idx, ans in st.session_state.answers.items() 
                                if ans == st.session_state.questions[q_idx]['correct_answer'])
            total_questions = len(st.session_state.questions)
            percentage = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
            
            # Display current score
            st.metric("Current Score", f"{correct_answers}/{total_questions}")
            st.progress(percentage / 100)
            st.write(f"Current Percentage: {percentage:.1f}%")

            # Add current score to history
            if len(st.session_state.score_history) == 0 or st.session_state.score_history[-1] != percentage:
                st.session_state.score_history.append(percentage)
                st.session_state.category_history.append(category)
                
                # Analyze weak areas
                weak_areas = []
                for idx, question in enumerate(st.session_state.questions):
                    if st.session_state.answers.get(idx) != question['correct_answer']:
                        concept = question['explanation'].split('.')[0]
                        weak_areas.append(concept)
                st.session_state.current_weak_areas = weak_areas

        # Separate buttons for past scores and improvements
        st.write("---")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📊 View Past Scores"):
                st.session_state.show_history = True
                st.session_state.show_improvements = False
                
        with col2:
            if st.button("📈 View Improvements"):
                st.session_state.show_improvements = True
                st.session_state.show_history = False

        # Initialize state variables if they don't exist
        if 'show_history' not in st.session_state:
            st.session_state.show_history = False
        if 'show_improvements' not in st.session_state:
            st.session_state.show_improvements = False

        # Display Past Scores
        if st.session_state.show_history and len(st.session_state.score_history) > 0:
            st.subheader("📊 Score History")
            
            # Create score history chart
            history_data = {
                'Attempt': list(range(1, len(st.session_state.score_history) + 1)),
                'Score (%)': st.session_state.score_history,
                'Category': st.session_state.category_history
            }
            st.line_chart(history_data, x='Attempt', y='Score (%)')
            
            # Show detailed history
            st.write("Detailed History:")
            for i, (score, cat) in enumerate(zip(st.session_state.score_history, st.session_state.category_history)):
                st.write(f"Attempt {i+1}: {score:.1f}% - {cat}")

        # Display Improvements Analysis
        if st.session_state.show_improvements and len(st.session_state.score_history) > 0:
            st.subheader("📌 Topics to Review")
            
            # Extract topics from current test
            if st.session_state.submitted and st.session_state.questions:
                topics_to_review = set()  # Using set to avoid duplicates
                for idx, question in enumerate(st.session_state.questions):
                    if st.session_state.answers.get(idx) != question['correct_answer']:
                        # Extract topic from the first sentence of explanation
                        topic = question['explanation'].split('.')[0].strip()
                        topics_to_review.add(topic)
                
                if topics_to_review:
                    st.warning("These topics need more practice:")
                    for topic in topics_to_review:
                        st.write(f"📌 {topic}")
                    
                    # Simple recommendation
                    st.write("")  # Add some spacing
                    st.info("💡 Focus on reviewing these topics before moving forward.")
                else:
                    st.success("🎉 Great job! You have a good understanding of all topics in this test.")
        
        num_questions = st.select_slider(
            "Number of Questions",
            options=[10, 15, 20, 25, 30],
            value=10
        )
        
        if st.button("Generate Questions"):
            with st.spinner("Generating questions..."):
                # Get relevant document chunks based on previous questions or default context
                query = "Generate questions about core concepts and important topics"
                if st.session_state.questions:
                    # Use previous questions to guide next question generation
                    recent_questions = [q["question"] for q in st.session_state.questions[-3:]]
                    query = "Generate questions similar to: " + " ".join(recent_questions)
                
                # Get relevant chunks directly (no async needed)
                relevant_chunks = doc_processor.get_relevant_chunks(query, category, top_k=3)
                
                if relevant_chunks:
                    # Join chunks with proper spacing and add context
                    document_text = " ".join(relevant_chunks)
                    questions = mcq_generator.generate_mcqs(document_text, num_questions)
                    
                    # Reset session state
                    st.session_state.questions = questions
                    st.session_state.answers = {}
                    st.session_state.submitted = False
                    
                    if len(questions) > 0 and not isinstance(questions[0], dict):
                        st.error("Error generating questions. Please try again.")
                else:
                    st.error(f"No content found for category: {category}")
    
    # Main content area
    if st.session_state.questions:
        st.header("Multiple Choice Questions")
        
        # Create a form for all questions
        with st.form("quiz_form"):
            for idx, question in enumerate(st.session_state.questions):
                st.subheader(f"Question {idx + 1}")
                st.write(question["question"])
                
                # Display options as radio buttons
                answer = st.radio(
                    "Select your answer:",
                    options=question["options"],
                    key=f"q_{idx}",
                    index=None  # No default selection
                )
                
                # Store answer in session state
                if answer is not None:
                    st.session_state.answers[idx] = question["options"].index(answer)
                
                st.write("---")  # Divider between questions
            
            # Submit button for all questions
            submit_button = st.form_submit_button("Submit All Answers")
            if submit_button and len(st.session_state.answers) == len(st.session_state.questions):
                st.session_state.submitted = True
        
        # Display results after submission
        if st.session_state.submitted:
            st.header("Results")
            for idx, question in enumerate(st.session_state.questions):
                user_answer_idx = st.session_state.answers.get(idx)
                correct_answer_idx = question["correct_answer"]
                
                with st.expander(f"Question {idx + 1} - {'Correct ✅' if user_answer_idx == correct_answer_idx else 'Incorrect ❌'}"):
                    st.write(question["question"])
                    st.write("Your answer:", question["options"][user_answer_idx])
                    if user_answer_idx != correct_answer_idx:
                        st.write("Correct answer:", question["options"][correct_answer_idx])
                    st.write("Explanation:", question["explanation"])
            
            if st.button("Try Again"):
                st.session_state.questions = []
                st.session_state.answers = {}
                st.session_state.submitted = False
                st.rerun()

if __name__ == "__main__":
    main()