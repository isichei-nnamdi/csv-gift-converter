import streamlit as st
import csv
import io

# Function to convert CSV to GIFT format
def convert_csv_to_gift(csv_file):
    """Converts an uploaded CSV file to GIFT format."""
    gift_output = io.StringIO()
    reader = csv.DictReader(io.StringIO(csv_file.getvalue().decode("utf-8")), delimiter=",")

    for row in reader:
        question_text = row["question"].strip()
        options = [row["option1"], row["option2"], row["option3"], row["option4"]]
        correct_option = row["correct_option"].strip()

        # Write GIFT format
        gift_output.write(f":: {question_text} :: {question_text} {{\n")
        for option in options:
            option = option.strip()
            if option == row[correct_option]:  # Match with correct option
                gift_output.write(f"   ={option}\n")  # Correct answer
            else:
                gift_output.write(f"   ~{option}\n")  # Incorrect answers
        gift_output.write("}\n\n")

    return gift_output.getvalue()

# Initialize session state variables
if "gift_content" not in st.session_state:
    st.session_state["gift_content"] = ""
if "file_uploaded" not in st.session_state:
    st.session_state["file_uploaded"] = False

# Streamlit UI
st.title("CSV to GIFT Converter for Moodle 📚")
st.write("Upload a CSV file and download the GIFT formatted file for Moodle LMS.")

# User input for filename
question_name = st.text_input("Enter a name for the question file (without extension)")

# File uploader
uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file:
    st.session_state["file_uploaded"] = True
    st.session_state["gift_content"] = convert_csv_to_gift(uploaded_file)

if st.session_state["gift_content"]:
    st.subheader("Preview of GIFT File:")
    st.text_area("Generated GIFT Format:", st.session_state["gift_content"], height=300)

    # Arrange buttons in columns
    col1, col2 = st.columns([2, 1])

    with col1:
        # If download button is clicked, trigger a JS refresh
        if st.download_button(
            label="Download GIFT File",
            data=st.session_state["gift_content"],
            file_name=f"{question_name}.gift",
            mime="text/plain"
        ):
            st.markdown(
                """<script>window.location.reload();</script>""",
                unsafe_allow_html=True
            )

    with col2:
        if st.button("Clear & Restart"):
            st.markdown(
                """<script>window.location.reload();</script>""",
                unsafe_allow_html=True
            )

    # Footer
st.markdown(
    """
    <style>
        .footer {
            position: fixed;
            bottom: 0;
            width: 60%;
            background-color: #ffffff;
            text-align: center;
            padding: 10px;
            font-size: 14px;
            color: #A72D2D;
        }
    </style>
    <div class="footer">
        Design and developed by Nnamdi for Miva Open University &copy; 2025
    </div>
    """,
    unsafe_allow_html=True
)


