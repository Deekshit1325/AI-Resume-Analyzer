import streamlit as st
from utils import (
    extract_text_from_pdf,
    clean_text,
    get_role_rankings,
    analyze_target_role)

# PAGE CONFIG
st.set_page_config(
    page_title="AI Resume Analyzer V4",
    page_icon="📄",
    layout="wide"
)

# HEADER
st.title("📄 AI Resume Analyzer + ATS Career Copilot V4")
st.write("Premium Resume Intelligence Platform")
st.markdown("---")

# INPUTS
col1, col2 = st.columns(2)
with col1:
    uploaded_file = st.file_uploader(
        "Upload Resume (PDF)",
        type=["pdf"])
with col2:
    jd_text = st.text_area(
        "Paste Job Description (Optional)",
        height=220)

# ANALYZE
if st.button(" Analyze Resume"):
    if uploaded_file is None:
        st.warning("Upload resume first.")
    else:
        text = extract_text_from_pdf(uploaded_file)
        text = clean_text(text)
        rankings = get_role_rankings(text)
        # TOP CARDS
        st.markdown("---")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("ATS Score", f"{rankings[0][1]}%")
        c2.metric("Best Role", rankings[0][0])
        c3.metric("Eligible Roles", len(rankings))
        c4.metric("Placement Ready", "Yes")

        # TABS
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "Overview",
            "Eligible Roles",
            "Gap Analysis",
            "Projects",
            "Roadmap"])

        # TAB 1
        with tab1:
            st.subheader("📊 Top Match Roles")
            for role, score in rankings:
                st.write(role)
                st.progress(score / 100)

        # TAB 2
        with tab2:
            st.subheader("🎯 Select Target Role")
            roles = [x[0] for x in rankings]
            selected_role = st.selectbox(
                "Choose Role",
                roles)

            result = analyze_target_role(
                text,
                selected_role)

            st.metric(
                "Role Match",
                f"{result['score']}%")

        # TAB 3
        with tab3:
            st.subheader("✅ Skills You Have")
            for i in result["matched"]:
                st.write("•", i.title())
            st.subheader("❌ Skills To Learn")
            for i in result["missing"]:
                st.write("•", i.title())

        # TAB 4
        with tab4:
            st.subheader("💼 Recommended Projects")
            for i in result["projects"]:
                st.write("•", i)

        # TAB 5
        with tab5:
            st.subheader("📚 Learning Roadmap")
            for i in result["roadmap"]:
                st.write("•", i)

# FOOTER
st.markdown("---")
st.caption("Built with Python + Streamlit + Semantic AI")