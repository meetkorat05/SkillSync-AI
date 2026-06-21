def generate_questions(
        resume,
        llm):

    prompt = f"""
You are a senior AI Engineer interviewer.

Analyze the resume carefully.

Generate ONLY 5 interview questions.

Rules:

1. Questions must be based on projects mentioned in the resume.
2. Questions must test practical understanding.
3. Avoid generic questions like:
    - What is Machine Learning?
    - What is NLP?
    - What is AI?
4. Ask questions about:
    - Design decisions
    - Architecture
    - Model selection
    - Challenges faced
    - Deployment
    - Scalability
5. Make the questions suitable for an AI Engineer internship interview.

Resume:
{resume}
"""

    return llm(prompt)