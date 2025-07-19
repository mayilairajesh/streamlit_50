import streamlit as st

# Set the title of the app
st.title("Hello World Streamlit App")

# Display a simple text message
st.write("This is a simple 'Hello World' application using Streamlit.")

# Display text using Markdown
st.markdown("""
## Markdown Example

This section demonstrates **bold** text, *italic* text, and `code` snippets.

- Item 1
- Item 2
    - Sub-item A
    - Sub-item B

Here's a link to [Streamlit's official website](https://streamlit.io/).

---

### Basic Formatting

You can also use HTML-like formatting within `st.markdown()`:

<p style="font-size:20px; color:blue;">This text is blue and larger.</p>
<p>This is a <b>bold</b> paragraph.</p>
""")

# Display a header
st.header("Another Section")
st.write("You can organize your app with different headers and sections.")

# Display a success message
st.success("App loaded successfully!")

# Display a warning message
st.warning("This is a warning message.")

# Display an error message
st.error("This is an error message (just for demonstration).")

# Display a simple data frame (demonstrates basic data display)
import pandas as pd
data = {'Column A': [1, 2, 3], 'Column B': ['X', 'Y', 'Z']}
df = pd.DataFrame(data)
st.subheader("Data Display Example")
st.dataframe(df)

# You can also add interactive widgets, but for "hello world" we keep it simple.
# For example:
# name = st.text_input("Enter your name:")
# if name:
#     st.write(f"Hello, {name}!")

