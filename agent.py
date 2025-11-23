import requests
import json

class InterviewAgent:
    def __init__(self, model="llama3"):
        self.model = model
        self.role = None
        self.answers = []
        self.question_count = 0

    def ollama_generate(self, prompt):
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": self.model,
            "prompt": prompt,
            "stream": False
        })
        return response.json()["response"].strip()

    def start_interview(self, role):
        self.role = role
        self.answers = []
        self.question_count = 1
        
        return f"Great, let's begin. Tell me about yourself for the {role} role."

    def process_answer(self, answer):
        self.answers.append(answer)
        self.question_count += 1

        if self.question_count > 6:
            return "Thank you. You've completed the interview. Click 'End Interview & Get Feedback'."

        prompt = f"""
        You are interviewing a candidate for a {self.role} role.

        Candidate answer: {answer}

        Ask the next follow-up question. Keep it short, relevant, and natural.
        Do NOT compliment the answer. Just ask the next question.
        """

        return self.ollama_generate(prompt)

    def get_feedback(self):
        prompt = f"""
        Evaluate this candidate for a {self.role} position.

        Answers: {json.dumps(self.answers)}

        Provide:
        - Strengths
        - Weaknesses
        - Suggested improvements
        - Scores (Communication, Knowledge, Confidence) out of 10
        - Final recommendation (Hire/Maybe/No)
        """

        return self.ollama_generate(prompt)
