from copy import deepcopy
from typing import Dict, TypedDict, Optional
from langgraph.graph import StateGraph, START, END
import time
import PyPDF2
from groq import Groq
import streamlit as st
from ats import *
from interview import *
from ui import *
from dotenv import load_dotenv
import os
from pathlib import Path


env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

from prompts import (
    prompt_clean,
    subagent_desc,
    agent_desc,
    prompt_subagent,
    prompt_agent,
    prompt_superagent
)

st.set_page_config(
    page_title="Resume Analyzer",
    layout="wide"
)

load_css()
show_header()
show_sidebar()

agent_subagent_pairs = {}
for main_key, nested_dict in subagent_desc.items():
        pairs = {main_key:list(nested_dict.keys())}
        agent_subagent_pairs.update(pairs)

history = deepcopy(subagent_desc)

agent = list(agent_subagent_pairs.keys())[0]
subagent = agent_subagent_pairs[agent][0]

for key, value in history.items():
    if isinstance(value, dict):
        value["Overall"] = ""
        for nested_key, nested_value in value.items():
            value[nested_key] = ""
			

if not GROQ_API_KEY:
    st.error(
        "Groq API key not found in .env file."
    )
    st.stop()

client = Groq(
    api_key=GROQ_API_KEY
)

model_name = "llama-3.3-70b-versatile"

def llm(x):
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {
                    "role": "user",
                    "content": x
                }
            ],
            temperature=0.3
        )

        return response.choices[0].message.content

    except Exception as exc:
        raise RuntimeError(
            f"Groq request failed ({type(exc).__name__}): {exc}"
        ) from exc
	

def extract_skills(text):

    prompt = f"""
    You are an ATS Skill Extraction Engine.

    Extract ONLY technical skills.

    Rules:
    - Include programming languages
    - Include frameworks
    - Include databases
    - Include cloud platforms
    - Include AI/ML technologies
    - Include developer tools
    - Remove duplicates
    - Ignore soft skills
    - Ignore job titles
    - Ignore education

    Return ONLY comma separated skills.

    Resume Text:
    {text}
    """

    return llm(prompt)


def extract_pdf_text(pdf):

    lines = []

    pdf_reader = PyPDF2.PdfReader(pdf)

    for page in pdf_reader.pages:

        page_text = page.extract_text()

        if page_text:

            lines.extend(
                page_text.split("\n")
            )

    return "\n".join(lines)

    
class GraphState(TypedDict):
    subagent_feedback: Optional[list] = []
    agent_feedback: Optional[list] = []
    history: Optional[dict] = {}
    resume: Optional[str] = None
    final_verdict: Optional[str] = None
    all_pairs: Optional[list]=[]
    subagent: Optional[str] = None
    agent: Optional[str] = None

workflow = StateGraph(GraphState)

def handle_clean(state):
    resume = state.get('resume')
    
    st.success("Cleaning loaded text..")
    resume = llm(prompt_clean.format(resume))
    return {'resume':resume}

def handle_subagent(state):
    print("In sub-agent")
    time.sleep(1)
    history = state.get('history')
    subagent_feedback = state.get('subagent_feedback')
    resume = state.get("resume")
    all_pairs = state.get('all_pairs')
    agent = state.get('agent')

    agent=list(all_pairs.keys())[0]
    subagent=all_pairs[agent][0]
    
    current_feedback = llm(prompt_subagent.format(subagent,subagent_desc[agent][subagent],resume))
    subagent_feedback.extend(["{} : {}".format(subagent,current_feedback)])
    history[agent][subagent]=current_feedback

    all_pairs[agent].remove(subagent)
    
    return {'subagent_feedback':subagent_feedback,'history':history,"all_pairs":all_pairs,'agent':agent}

def handle_agent(state):
    print("In agent")
    time.sleep(1)
    feedback = state.get('subagent_feedback')
    agent_feedback = state.get('agent_feedback')
    all_pairs = state.get('all_pairs')
    history = state.get("history")
    
    agent=list(all_pairs.keys())[0]

    st.info("Reviewing {} ...".format(agent))

    summary = llm(prompt_agent.format(agent,agent_desc[agent],feedback))
    agent_feedback.extend(["{} : {}".format(agent,summary)])
    history[agent]["Overall"]=summary
    
    del all_pairs[agent]

    try:
        agent = list(all_pairs.keys())[0]
    except:
        pass

    return {'agent_feedback':agent_feedback,'history':history,"all_pairs":all_pairs,"agent":agent}

def handle_superagent(state):
    print("In superagent")
    time.sleep(1)
    st.success("Final verdict getting updated...")
    history = state.get("history")
    feedback = state.get('agent_feedback')
    result = llm(prompt_superagent.format(feedback))
    history.update({"Final Verdict":result})

    return {'final_verdict':result,'history':history}
	
workflow.add_node("handle_clean",handle_clean)
workflow.add_node("handle_subagent",handle_subagent)
workflow.add_node("handle_agent",handle_agent)
workflow.add_node("handle_superagent",handle_superagent)

def subagent_check(state):
    agent = state.get('agent')
    all_pairs = state.get('all_pairs')
    
    if len(all_pairs[agent]):
        return "handle_subagent"
    else:
        return "handle_agent"

def agent_check(state):
    all_pairs = state.get('all_pairs')

    if len(all_pairs.keys()):
        return "handle_subagent"
    else:
        return "handle_superagent"

workflow.add_conditional_edges(
    "handle_subagent",
    subagent_check,
    {
        "handle_subagent": "handle_subagent",
        "handle_agent": "handle_agent"
    }
)

workflow.add_conditional_edges(
    "handle_agent",
    agent_check,
    {
        "handle_subagent": "handle_subagent",
        "handle_superagent": "handle_superagent"
    }
)

workflow.set_entry_point("handle_clean")
workflow.add_edge('handle_clean', "handle_subagent")
workflow.add_edge('handle_superagent',END)

app = workflow.compile()

lines = []
pdf_file = st.file_uploader(
    "Upload Resume PDF",
    type=["pdf"]
)

jd_file = st.file_uploader(
    "Upload Job Description PDF",
    type=["pdf"],
    key="jd"
)

if GROQ_API_KEY and pdf_file and jd_file:
    analysis_tab, review_tab, interview_tab = st.tabs([
        "📊 Analysis",
        "📋 Resume Review",
        "🎤 Interview Prep"
    ])
    try:
        resume_text = extract_pdf_text(
            pdf_file
        )

        jd_text = extract_pdf_text(
            jd_file
        )

        lines = resume_text

        if jd_file:

            resume_skills = extract_skills(lines)

            jd_skills = extract_skills(
                jd_text
            )

            match_score, matched, missing = compare_skills(
                resume_skills,
                jd_skills
            )

            resume_score = calculate_ats_score(
                lines
            )

            final_ats_score = round(
                (resume_score * 0.7)
                +
            (match_score * 0.3)
            )

            with analysis_tab:

                st.metric(
                    "ATS Score",
                    final_ats_score
                )

                st.metric(
                    "JD Match %",
                    round(match_score)
                )

                col1, col2 = st.columns(2)

                with col1:

                    st.subheader("✅ Matched Skills")

                    show_skill_tags(matched)

                with col2:

                    st.subheader("❌ Missing Skills")

                    show_skill_tags(missing)

        st.subheader("Resume Review")

        conversation = app.invoke(
            {
                "subagent_feedback": [],
                "agent_feedback": [],
                "history": history,
                "resume": lines,
                "all_pairs": deepcopy(agent_subagent_pairs),
                "agent": agent,
                "subagent": subagent
            },
            {
                "recursion_limit": 100
            }
        )

        questions = generate_questions(
            lines,
            llm
        )

        with review_tab:

            st.subheader("Resume Review")

            for key, value in conversation['history'].items():

                if key != "Final Verdict":
                    with st.expander(key):
                        st.write(value)

            st.subheader("📋 Final Assessment")

            final_verdict = conversation['history'].get(
                "Final Verdict",
                ""
            )

            st.markdown(
                f"""
            <div style="
            padding:20px;
            border-radius:12px;
            background-color:#1E293B;
            border:1px solid #334155;
            ">
            {final_verdict}
            </div>
            """,
                unsafe_allow_html=True
            )         

        with interview_tab:

            st.subheader("Interview Questions")

            st.write(questions)            

        

    except Exception as exc:
        st.error(f"Resume analysis failed: {type(exc).__name__}: {exc}")
        st.stop()
