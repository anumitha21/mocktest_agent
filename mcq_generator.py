from typing import List, Dict
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import os
from dotenv import load_dotenv

load_dotenv()

class MCQGenerator:
    def __init__(self):
        self.groq = ChatGroq(
            api_key=os.getenv('GROQ_API_KEY'),
            model_name="llama-3.3-70b-versatile",
            temperature=0.5,  # Lower temperature for more consistent output
            max_tokens=4096,  # Increased for better context handling
        )
        self.output_parser = JsonOutputParser()
        self.previous_questions = []  # Store previous questions for context

    def generate_mcqs(self, context: str, num_questions: int = 10) -> List[Dict]:
        template = """You are an expert at creating practice questions similar to existing question patterns.
Given the following reference material, generate {num_questions} multiple choice questions that match the style and difficulty
of typical questions in this domain. The questions should test similar concepts but be newly formulated.

Reference Material:
{context}

Guidelines for Question Generation:
1. Analyze the context to understand:
   - The subject matter and key concepts
   - The typical complexity level
   - Common question patterns and styles
   - Types of concepts being tested

2. Create questions that:
   - Follow similar patterns to reference material
   - Test the same concepts but with different scenarios
   - Maintain consistent difficulty level
   - Use similar vocabulary and technical terms
   - Match the depth of knowledge required

Your response must be a valid JSON array with questions in this EXACT format:
[
    {{
        "question": "Question following similar pattern",
        "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
        "correct_answer": 0,
        "explanation": "Explanation with concept reference"
    }}
]

Requirements:
1. Generate exactly {num_questions} questions
2. Each question must:
   - Test concepts found in the reference material
   - Follow similar style and format
   - Have same difficulty level
3. Each question must have EXACTLY 4 options
4. Include clear explanations that reference the source material
5. Return only valid JSON array

Remember: Create questions that feel like they could have been part of the original material."""

        messages = [
            {
                "role": "system",
                "content": "You are a professional MCQ generator. You will generate questions in a specific JSON format."
            },
            {
                "role": "user",
                "content": template.format(num_questions=num_questions, context=context)
            }
        ]

        try:
            response = self.groq.invoke(messages)
            response_text = str(response.content)
            
            # Clean up the response
            response_text = response_text.strip()
            if response_text.startswith('```json'):
                response_text = response_text.split('```json')[1]
            if response_text.startswith('```'):
                response_text = response_text.split('```')[1]
            if response_text.endswith('```'):
                response_text = response_text.rsplit('```', 1)[0]
            response_text = response_text.strip()
            
            # Ensure the response starts with [ and ends with ]
            if not (response_text.startswith('[') and response_text.endswith(']')):
                raise ValueError("Response is not a valid JSON array")
            
            # Parse the JSON
            questions = self.output_parser.parse(response_text)
            
            # Validate the response
            if not isinstance(questions, list):
                raise ValueError("Response is not a list")
            
            # Ensure we have exactly the number of questions requested
            if len(questions) > num_questions:
                questions = questions[:num_questions]  # Take only the requested number
            elif len(questions) < num_questions:
                raise ValueError(f"Not enough questions generated. Expected {num_questions}, got {len(questions)}")
            
            return questions
            
        except Exception as e:
            print(f"Error generating questions: {str(e)}")
            # Return a default structure to help with debugging
            return [
                {
                    "question": "Error generating questions. Please try again.",
                    "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
                    "correct_answer": 0,
                    "explanation": str(e)
                }
            ]