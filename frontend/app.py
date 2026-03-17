import streamlit as st
import requests

st.set_page_config(page_title="AI Roadmap Generator", layout="centered")

st.title("AI Roadmap Recommendation System")
st.write("Generate personalized learning roadmaps based on your profile.")

# API URL - configurable in a real app
API_URL = "http://localhost:8000/api/generate-roadmap"

# Input Form
with st.form("profile_form"):
    experience_level = st.selectbox("Experience Level", ["Beginner", "Intermediate", "Advanced"])
    
    current_skills = st.text_input("Current Skills (comma separated)", "Python, HTML")
    career_goal = st.text_input("Career Goal", "Fullstack Developer")
    preferred_stack = st.text_input("Preferred Stack (comma separated)", "React, FastAPI")
    
    st.write("Availability & Timeline")
    col1, col2 = st.columns(2)
    with col1:
        daily_study_hours = st.number_input("Daily Study Hours", min_value=1, max_value=24, value=3)
    with col2:
        target_months = st.number_input("Timeline (months)", min_value=1, max_value=60, value=6)
        
    submitted = st.form_submit_button("Generate Roadmap")

if submitted:
    # Process inputs
    skills_list = [s.strip() for s in current_skills.split(",") if s.strip()]
    stack_list = [s.strip() for s in preferred_stack.split(",") if s.strip()]
    
    payload = {
        "experience_level": experience_level.lower(),
        "current_skills": skills_list,
        "career_goal": career_goal,
        "preferred_stack": stack_list,
        "daily_study_hours": daily_study_hours,
        "target_months": target_months
    }
    
    with st.spinner("Generating your personalized roadmap..."):
        try:
            response = requests.post(API_URL, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                roadmap_data = data.get("roadmap_data", {})
                phases = roadmap_data.get("phases", [])
                
                st.success("Roadmap generated successfully!")
                
                # Display roadmap phases
                if phases:
                    for phase in phases:
                        with st.expander(phase.get("phase", "Phase"), expanded=True):
                            st.write(f"**Topics to cover:**")
                            st.write(", ".join(phase.get("topics", [])))
                            st.write(f"**Project:** {phase.get('project', 'None')}")
                else:
                    st.warning("No phases returned in the roadmap.")
                    st.json(roadmap_data) # fallback display
            else:
                st.error(f"Error generating roadmap: {response.status_code}")
                st.write(response.text)
                
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the backend server. Make sure it is running on http://localhost:8000.")
