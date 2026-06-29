prompt_clean = """
You are an ATS Resume Preprocessing System.

Your task:
1. Clean OCR noise, duplicated words, and broken formatting.
2. Preserve all resume content.
3. Preserve section names.
4. Preserve achievements, skills, projects, education and experience.
5. Remove only meaningless symbols, extra spaces and formatting artifacts.
6. Do NOT summarize.
7. Do NOT rewrite content.
8. Return only the cleaned resume text.

Resume:
{}
"""

subagent_desc = {
    
"Impact": {
"Quantify impact": "Use specific numbers, percentages, or metrics to demonstrate the scale and significance of your achievements.",
"Repetition": "Maintain consistent language and terminology, but avoid repeating the same phrases or descriptions across multiple sections.",
"Weak verbs": "Use strong, action-oriented verbs to effectively convey your contributions and responsibilities.",
"Verb tenses": "Use present tense for current roles and past tense for previous roles, maintaining consistency throughout.",
"Responsibilities": "Focus on key duties and tasks tailored to the job you're applying for, rather than generic job descriptions.",
"Spelling & consistency": "Ensure your resume is free of errors and maintains consistent formatting, capitalization, and punctuation."
},
    
"Brevity":{
"Length": "Keep your resume concise, typically one page, up to two pages for extensive experience.",
"Bullet Lengths": "Maintain concise bullet points, typically 1-2 lines, to highlight the most important information.",
"Filler Words": "Minimize the use of filler words to maximize the impact and conciseness of your resume."
},
    
"Style": {
    "Buzzwords": "Ensure your resume includes relevant industry-specific keywords and buzzwords that match the job description.",
    "Dates": "Format your employment dates consistently (e.g. MM/YYYY) and ensure there are no unexplained gaps in your work history.",
    "Contact and Personal Details": "Make sure your name, contact information, and other personal details are clearly displayed and up-to-date.",
    "Readability": "Use a clean, simple layout and font that is easy for the ATS to parse. Avoid complex formatting, tables, and graphics.",
    "Personal Pronouns": "Minimize the use of personal pronouns like 'I', 'me', and 'my' to keep the focus on your achievements and skills.",
    "Active Voice": "Use active voice to describe your responsibilities and accomplishments, making your resume more impactful.",
    "Consistency": "Maintain consistent formatting, language, and style throughout your resume to present a professional and polished document."
},
    
"Sections": {
    "Summary": "A concise overview of your key qualifications, experience, and career goals.",
    "Education": "Details about your academic background, including degrees, schools, and relevant coursework or achievements.",
    "Unnecessary Sections": "Sections that may not be relevant or add value to your resume, such as hobbies, interests, or irrelevant work experience.",
    "Skills": "A list of your relevant technical, soft, and transferable skills that demonstrate your capabilities."
}
    
}

agent_desc = {
    "Impact": "Ensuring your resume content showcases your achievements, contributions, and the value you can bring to an employer.",
    "Brevity": "Keeping your resume concise, focused, and easy to scan, typically one page for entry-level and two pages for experienced candidates.",
    "Style": "The overall formatting, layout, and visual appeal of your resume, which should be clean, consistent, and professional.",
    "Sections": "The key components of a resume, such as Summary, Education, Work Experience, Skills, and any other relevant sections."
}

prompt_subagent = """
You are a Senior Resume Reviewer working for a top technology company.

Evaluation Category:
{}

Evaluation Criteria:
{}

Review the resume only from this perspective.

Scoring Rubric:
0-2 = Poor
3-4 = Below Average
5-6 = Average
7-8 = Strong
9-10 = Excellent

Return EXACTLY in this format:

Score: X/10

Strength:
One concise sentence.

Weakness:
One concise sentence.

Recommendation:
One concise actionable improvement.

Resume:
{}
"""

prompt_agent = """
You are a Lead Hiring Manager.

Category:
{}

Description:
{}

You are given multiple reviewer reports.

Combine the reports and produce a single professional assessment.

Scoring Rubric:
0-2 = Poor
3-4 = Below Average
5-6 = Average
7-8 = Strong
9-10 = Excellent

Return EXACTLY in this format:

Score: X/10

Summary:
One concise sentence.

Key Issue:
Most important weakness.

Recommendation:
Most impactful improvement.

Reports:
{}
"""

prompt_superagent = """
You are a Senior Technical Recruiter and ATS Evaluation Specialist.

Analyze all reviewer feedback and provide a final hiring assessment.

Scoring Guide:

0-3  = Reject
4-5  = Needs Major Improvement
6-7  = Average
8-9  = Strong Candidate
10   = Outstanding Candidate

Return EXACTLY in this format:

Overall Score: X/10

Hiring Recommendation:
Reject / Consider / Interview Recommended / Strongly Recommended

Top Strengths:
- Point 1
- Point 2
- Point 3

Critical Improvements:
- Point 1
- Point 2
- Point 3

Final Verdict:
Maximum 3 sentences.

Reviewer Feedback:
{}
"""
