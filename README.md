# 🎯 Placement AI - Your Personal Interview and Aptitude Trainer

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An AI-powered interactive quiz application that helps you prepare for placement interviews and aptitude tests. Generate personalized multiple-choice questions from curated content and track your progress over time with detailed analytics and weak area identification.

## ✨ Features

-  **Dual Categories**: Practice aptitude and interview questions from real placement papers
-  **AI-Generated Questions**: Powered by Groq's LLaMA model for diverse, relevant questions
-  **Progress Tracking**: Monitor your scores and improvement over time with visual charts
-  **Weak Area Analysis**: Automatically identify and highlight topics that need more practice
-  **Score History**: View your performance trends across multiple attempts
-  **Interactive UI**: Clean, user-friendly Streamlit interface with real-time feedback
-  **Detailed Explanations**: Get comprehensive explanations for each question
-  **Adaptive Learning**: Questions are generated based on your previous performance

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Groq API Key (get from [Groq Console](https://console.groq.com/))

### Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd mcq
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   Create a `.env` file in the root directory:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

4. **Run the application:**
   ```bash
   streamlit run main.py
   ```

5. **Open your browser** and navigate to the local Streamlit URL (usually `http://localhost:8501`)

## 📖 Usage

### Getting Started
1. **Select Category**: Choose between "Aptitude Questions" or "Interview Questions" from the sidebar
2. **Configure Quiz**: Select the number of questions (10-30) you want to attempt
3. **Generate Questions**: Click the "Generate Questions" button to create your personalized quiz

### Taking the Quiz
1. **Answer Questions**: Read each question carefully and select your answer from the 4 options
2. **Submit Answers**: Click "Submit All Answers" when you've completed all questions
3. **Review Results**: Check your score, see correct answers, and read detailed explanations

### Tracking Progress
- **Current Score**: View your performance on the current quiz with a progress bar
- **Score History**: Click "📊 View Past Scores" to see your improvement over time
- **Weak Areas**: Click "📈 View Improvements" to identify topics that need more practice

### Tips for Best Results
- Start with shorter quizzes (10 questions) to get familiar
- Review explanations carefully to understand concepts
- Focus on weak areas identified by the app
- Take quizzes regularly to track improvement

## 🏗️ Project Structure

```
mcq/
├── main.py                 # Main Streamlit application
├── mcq_generator.py        # AI-powered question generation
├── document_processor.py   # PDF processing and text chunking
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore rules
├── README.md              # Project documentation
├── cache/                 # Cached embeddings (auto-generated)
├── INFOSYS -APTITUDE-MODEL paper.pdf    # Aptitude questions source , you can add any resource 
└── Sample Interview Questions.pdf       # Interview questions source , you can add any resource 
```

## 🛠️ Technical Details

### Dependencies
- **Streamlit**: Web app framework
- **LangChain + Groq**: AI question generation
- **PyPDF2**: PDF text extraction
- **python-dotenv**: Environment variable management

### AI Model
- Uses Groq's `llama-3.3-70b-versatile` model
- Configured for consistent, educational question generation
- Processes document chunks to create contextually relevant questions

### Document Processing
- Automatically loads and processes PDF documents
- Splits content into manageable chunks for AI processing
- Intelligent keyword matching for relevant content retrieval

## 🤝 Contributing

We welcome contributions! 
