from typing import List, Dict
import os
from PyPDF2 import PdfReader
import textwrap
from dotenv import load_dotenv

load_dotenv()

class DocumentProcessor:
    def __init__(self):
        self.chunk_size = 1000
        self.chunk_overlap = 200
        self.documents = {}
        # Load PDFs on initialization
        self.load_default_pdfs()

    def get_relevant_chunks(self, query: str, category: str, top_k: int = 3) -> List[str]:
        """Get document chunks using keyword matching with intelligent scoring"""
        if category not in self.documents:
            return []

        chunks = self.documents[category]
        
        # Extract meaningful keywords from the query
        query_lower = query.lower()
        # Remove common words that might not be relevant for matching
        stop_words = {'a', 'an', 'the', 'to', 'in', 'on', 'at', 'for', 'of', 'with', 'by', 'similar', 'questions', 'about', 'and', 'or', 'but', 'generate', 'create'}
        keywords = [word for word in query_lower.split() if word not in stop_words]
        
        # If no meaningful keywords found, return evenly spaced chunks
        if not keywords:
            if len(chunks) <= top_k:
                return chunks
            step = len(chunks) // top_k
            return [chunks[i] for i in range(0, len(chunks), step)][:top_k]
        
        # Score chunks based on keyword matches
        chunk_scores = []
        for i, chunk in enumerate(chunks):
            chunk_lower = chunk.lower()
            
            # Calculate base score from keyword matches
            score = 0
            matched_keywords = set()
            
            for keyword in keywords:
                # Count occurrences
                occurrences = chunk_lower.count(keyword)
                if occurrences > 0:
                    matched_keywords.add(keyword)
                    # Points for each occurrence
                    score += occurrences * 2
                    
                    # Bonus for keyword at the start
                    if chunk_lower.startswith(keyword):
                        score += 3
                        
                    # Bonus for keywords appearing in the first sentence
                    first_sentence = chunk_lower.split('.')[0]
                    if keyword in first_sentence:
                        score += 2
            
            # Bonus points for matching multiple different keywords
            coverage = len(matched_keywords) / len(keywords)
            score *= (1 + coverage)
            
            # Bonus for shorter chunks with matches (more focused content)
            if score > 0:
                chunk_scores.append((score, i))
        
        # Sort by score and return top_k chunks
        if chunk_scores:
            chunk_scores.sort(reverse=True)
            return [chunks[idx] for _, idx in chunk_scores[:top_k]]
        
        # If no matches found, fall back to evenly spaced chunks
        if len(chunks) <= top_k:
            return chunks
        step = len(chunks) // top_k
        return [chunks[i] for i in range(0, len(chunks), step)][:top_k]

    def process_pdf(self, pdf_path) -> str:
        """Process PDF file and return extracted text"""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    try:
                        # Clean and normalize text to handle encoding issues
                        page_text = page.extract_text()
                        # Replace problematic characters and normalize whitespace
                        page_text = page_text.encode('ascii', 'ignore').decode('ascii')
                        page_text = ' '.join(page_text.split())
                        text += page_text + "\n"
                    except Exception as e:
                        print(f"Error processing page: {e}")
                        continue
                return text
        except Exception as e:
            print(f"Error reading PDF {pdf_path}: {e}")
            return ""

    def get_document_chunks(self, text: str) -> List[str]:
        """Split document into chunks for processing"""
        # Remove extra whitespace and split into paragraphs
        text = " ".join(text.split())
        paragraphs = text.split('\n\n')
        
        # Split long paragraphs into smaller chunks
        chunks = []
        for para in paragraphs:
            if len(para) > self.chunk_size:
                # Use textwrap to split long paragraphs
                para_chunks = textwrap.wrap(para, self.chunk_size - self.chunk_overlap)
                chunks.extend(para_chunks)
            else:
                chunks.append(para)
        
        return [chunk.strip() for chunk in chunks if chunk.strip()]

    def process_document(self, pdf_file) -> List[str]:
        """Process PDF and return chunks of text"""
        text = self.process_pdf(pdf_file)
        chunks = self.get_document_chunks(text)
        self.documents['current'] = chunks
        return chunks

    def load_default_pdfs(self):
        """Load the default PDFs included in the project"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Define the PDFs and their categories
        pdfs = {
            'aptitude': 'INFOSYS -APTITUDE-MODEL paper.pdf',
            'interview': 'Sample Interview Questions.pdf'
        }
        
        for category, pdf_name in pdfs.items():
            pdf_path = os.path.join(current_dir, pdf_name)
            if os.path.exists(pdf_path):
                text = self.process_pdf(pdf_path)
                chunks = self.get_document_chunks(text)
                self.documents[category] = chunks
                print(f"Loaded {len(chunks)} chunks for {category}")

    def get_document_by_category(self, category: str) -> List[str]:
        """Get document chunks by category"""
        return self.documents.get(category, [])
    
    def get_available_categories(self) -> List[str]:
        """Get list of available document categories"""
        return list(self.documents.keys())