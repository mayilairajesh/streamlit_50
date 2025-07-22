import streamlit as st
import pandas as pd
import datetime
import os

# -------------------------------
# Configuration
# -------------------------------

st.set_page_config(
    page_title="User Feedback Survey",
    page_icon="📝",
    layout="centered"
)

# Persistent storage (simple CSV)
DATA_FILE = "feedback_data.csv"

# Initialize session state for form reset
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

# -------------------------------
# Helper Functions
# -------------------------------

def save_feedback(data):
    """Append feedback to CSV file."""
    df = pd.DataFrame([data])
    if os.path.exists(DATA_FILE):
        df.to_csv(DATA_FILE, mode='a', header=False, index=False)
    else:
        df.to_csv(DATA_FILE, mode='w', header=True, index=False)

def validate_email(email):
    """Simple email validation."""
    return '@' in email and '.' in email

# -------------------------------
# UI: Title & Description
# -------------------------------

st.title("📝 User Feedback Survey")
st.markdown("""
Thank you for taking the time to provide feedback!  
Your input helps us improve our services.
""")

# Only show form if not submitted
if not st.session_state.submitted:
    with st.form("feedback_form"):
        st.header("📋 Your Information")

        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First Name*", placeholder="John", max_chars=50)
        with col2:
            last_name = st.text_input("Last Name*", placeholder="Doe", max_chars=50)

        email = st.text_input("Email Address*", placeholder="john.doe@example.com")

        st.header("📊 Feedback")

        rating = st.slider(
            "How would you rate your overall experience?",
            min_value=1,
            max_value=5,
            value=3,
            format="%d ⭐"
        )

        satisfaction = st.selectbox(
            "How satisfied are you with our product/service?",
            ["Very Satisfied", "Satisfied", "Neutral", "Dissatisfied", "Very Dissatisfied"]
        )

        features = st.multiselect(
            "Which features do you use regularly?",
            [
                "Dashboard",
                "Reports",
                "Notifications",
                "API Access",
                "Mobile App",
                "Customer Support",
                "Other"
            ]
        )

        usage = st.radio(
            "How often do you use our product?",
            ["Daily", "Weekly", "Monthly", "Rarely", "First Time"]
        )

        feedback = st.text_area(
            "Do you have any suggestions or comments?",
            placeholder="We'd love to hear your thoughts...",
            height=120
        )

        recommend = st.checkbox(
            "Would you recommend us to a friend or colleague?"
        )

        # Required field indicator
        st.markdown("**Please fill all required fields marked with \\***")

        submit_button = st.form_submit_button("✅ Submit Feedback")

        # Validation and submission
        if submit_button:
            if not first_name or not last_name:
                st.error("Please enter both first and last name.")
            elif not email or not validate_email(email):
                st.error("Please enter a valid email address.")
            else:
                # Collect data
                data = {
                    "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "FirstName": first_name,
                    "LastName": last_name,
                    "Email": email,
                    "Rating": rating,
                    "Satisfaction": satisfaction,
                    "Features": ", ".join(features) if features else "None",
                    "UsageFrequency": usage,
                    "Feedback": feedback.strip() or "No comments",
                    "WouldRecommend": "Yes" if recommend else "No"
                }

                # Save to file
                save_feedback(data)

                # Set submitted state
                st.session_state.submitted = True
                st.rerun()

else:
    # Success screen
    st.success("🎉 Thank you for your feedback!")
    st.balloons()

    st.markdown("### Summary of your submission:")
    saved_df = pd.read_csv(DATA_FILE)
    latest = saved_df.iloc[-1]

    with st.expander("View Your Submission"):
        for key, value in latest.items():
            st.markdown(f"**{key.replace('_', ' ').title()}**: {value}")

    if st.button("📋 Submit Another Response"):
        st.session_state.submitted = False
        st.rerun()

# -------------------------------
# Admin: View Data (Optional)
# -------------------------------

with st.sidebar:
    st.subheader("Admin Panel")
    if st.checkbox("Show collected data"):
        if os.path.exists(DATA_FILE):
            df = pd.read_csv(DATA_FILE)
            st.dataframe(df, use_container_width=True)
            st.download_button(
                label="💾 Download Data (CSV)",
                data=open(DATA_FILE, 'rb').read(),
                file_name="feedback_export.csv",
                mime="text/csv"
            )
        else:
            st.info("No feedback collected yet.")