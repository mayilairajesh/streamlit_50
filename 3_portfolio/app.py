import streamlit as st
from pathlib import Path
import base64

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="My Portfolio", page_icon=":briefcase:", layout="centered")

# ------------------ HEADER ------------------
st.title("👋 Hello, I'm Rajesh")
st.subheader(" Data Enthusiast | ...")

# ------------------ PROFILE IMAGE ------------------
profile_pic = Path("assets/profile.jpeg")
if profile_pic.exists():
    with open(profile_pic, "rb") as f:
        img_data = f.read()
    profile_pic_base64 = base64.b64encode(img_data).decode()
    st.markdown(f"""
    <style>
        .circle-img {{
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 150px;
            height: 150px;
            border-radius: 50%;
            object-fit: cover;
        }}
    </style>
    <img src="data:image/png;base64,{profile_pic_base64}" class="circle-img">
    """, unsafe_allow_html=True)
else:
    st.warning("Profile image not found. Place it in assets/profile.jpg")

# ------------------ ABOUT ME ------------------
st.markdown("## 🧠 About Me")
st.markdown("""
I'm a passionate software engineer with a knack for building scalable applications and solving real-world problems using data and modern technologies. With experience in full-stack development, machine learning, and cloud platforms, I thrive in collaborative environments where innovation is key.
""")

# ------------------ SKILLS ------------------
st.markdown("## 🔧 Skills")
skills = ["Python", "Streamlit", "Pandas", "Git","Loading....."]
cols = st.columns(len(skills))
for col, skill in zip(cols, skills):
    col.markdown(f"`{skill}`")

# ------------------ SOCIAL LINKS ------------------
st.markdown("## 🌐 Connect With Me")

socials = {
    "GitHub": "https://github.com/mayilairajesh ",
    "Email":   "mailto:mayilairajesh@gmail.com"
}

for name, link in socials.items():
    st.markdown(f"[{name}]({link})")

# ------------------ RESUME DOWNLOAD ------------------
resume_path = Path("assets/resume.pdf")
if resume_path.exists():
    with open(resume_path, "rb") as f:
        resume_bytes = f.read()
    st.download_button(
        label="📄 Download Resume",
        data=resume_bytes,
        file_name="resume.pdf",
        mime="application/pdf"
    )
else:
    st.warning("Resume file not found. Place it in assets/resume.pdf")

# ------------------ FOOTER ------------------
st.markdown("<hr><center>Made with ❤️ using Streamlit</center>", unsafe_allow_html=True)