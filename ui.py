import streamlit as st

def load_css():
    st.markdown("""
    <style>
    .main {
        background-color: #0E1117;
    }

    .block-container {
        padding-top: 1rem;
        max-width: 1200px;
    }

    .hero {
        background: linear-gradient(
            90deg,
            #667eea,
            #764ba2
        );
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 25px;
    }

    .hero h1 {
        color: white;
    }

    .hero p {
        color: white;
    }

    .skill-pill {
        display: inline-block;
        background: #1f2937;
        color: white;
        padding: 8px 14px;
        margin: 5px;
        border-radius: 20px;
        font-size: 14px;
        font-weight: 500;
    }
    </style>
    """, unsafe_allow_html=True)

def show_header():
    st.markdown("""
    <div class="hero">
        <h1>🎯 SkillSync AI</h1>
        <p>AI Powered Recruitment Intelligence</p>
    </div>
    """, unsafe_allow_html=True)

def show_sidebar():

    with st.sidebar:

        st.markdown(
            """
            <h2 style='
                text-align:center;
                margin-bottom:20px;
            '>
                About
            </h2>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div style="
                background-color:#243B5A;
                padding:20px;
                border-radius:15px;
                margin-bottom:20px;
            ">

            <h4 style="
                color:#5EA8FF;
                margin-bottom:15px;
            ">
                SkillSync AI uses AI Agents to:
            </h4>

            <p>✅ Analyze Resume Content</p>

            <p>✅ Match Resume with Job Description</p>

            <p>✅ Identify Missing Skills</p>

            <p>✅ Generate Interview Questions</p>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("---")

        st.subheader("Criteria Weights")

        st.write("ATS Resume Score : 70%")
        st.write("JD Skill Match   : 30%")



def show_skill_tags(skills):

    html = ""

    for skill in skills:

        html += f"""
        <span class="skill-pill">
            {skill}
        </span>
        """

    st.markdown(
        html,
        unsafe_allow_html=True
    )