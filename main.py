import base64
from fpdf import FPDF
import streamlit as st

from objects.chatGPThandler import HouseEnergyAdvisor

# Initialize ChatGPTHandler and Advisor
energy_advisor = HouseEnergyAdvisor()


class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "House Energy Advisor Responses", 0, 1, "C")

    def chapter_title(self, num, label):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, f"Query {num}: {label}", 0, 1, "L")
        self.ln(10)

    def chapter_body(self, body):
        self.set_font("Arial", "", 12)
        self.multi_cell(0, 10, body)
        self.ln()


def generate_pdf(response_data):
    pdf = PDF()
    pdf.add_page()

    for i, (query, response) in enumerate(
        zip(response_data["Query"], response_data["Response"]), 1
    ):
        pdf.chapter_title(i, query)
        pdf.chapter_body(response)

    pdf_output = "responses.pdf"
    pdf.output(pdf_output, "F")
    return pdf_output


# Function to download PDF
def download_pdf(pdf_file):
    with open(pdf_file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode("utf-8")
        href = (
            f'<a href="data:application/octet-stream;base64,{base64_pdf}" '
            f'download="{pdf_file}">'
            "Download PDF</a>"
        )
    return href


# Streamlit App Configuration
st.set_page_config(page_title="House Energy Advisor", initial_sidebar_state="expanded")
st.title("House Energy Advisor")

# Sidebar Inputs for House Parameters
st.sidebar.title("House Details")
location = st.sidebar.text_input("Where is the house located?", "Switzerland")
occupants = st.sidebar.text_input("How many people live in the house?", "1")
area = st.sidebar.text_input("What is the area of the house in square meters (m²)?", "95")
house_type = st.sidebar.selectbox(
    "What type of house is it?", ["Detached", "Semi-detached", "Apartment"]
)
budget = st.sidebar.text_input(
    "What is your budget for energy solutions?", "10000 Swiss Franks"
)
additional_info = st.sidebar.text_input(
    "Anything else to consider?", "Potentially adding electric car charging."
)

# Store Parameters
house_params = {
    "location": location,
    "occupants": occupants,
    "area": area,
    "type": house_type,
    "budget": budget,
    "additional_info": additional_info,
}

# Submit Button
if st.sidebar.button("Submit"):
    if location and occupants and area and budget:
        # Build and Process Queries
        refined_queries = energy_advisor.build_query(house_params)
        st.write("Processing your queries... This may take a moment.")

        # Use a spinner for user experience
        with st.spinner("Refining answers with ChatGPT..."):
            responses = energy_advisor.process_queries(refined_queries)

        # # Display Responses
        # st.write("Responses from Energy Advisor:")
        # for i, (query, response) in enumerate(zip(refined_queries, responses), 1):
        #     st.subheader(f"Query {i}")
        #     st.write(f"**Query:** {query}")
        #     st.write(f"**Response:** {response}")

        with st.spinner("Refining responses..."):
            refined_responses = energy_advisor.refine_responses(responses)

        with st.spinner("Summarizing responses..."):
            summarized_response = energy_advisor.summarize_responses(refined_responses)

        # response_data = {
        #     "Query": refined_queries,
        #     "Response": responses
        # }
        # Display Responses
        st.write("Responses from Energy Advisor:")
        st.write(summarized_response)
        # for i, (query, response) in enumerate(zip(summarized_response, responses), 1):
        #     st.subheader(f"Query {i}")
        #     st.write(f"**Query:** {query}")
        #     st.write(f"**Response:** {response}")

        # st.table(response_data)

        # # Generate and download PDF
        # pdf_file = generate_pdf(response_data)
        # st.markdown(download_pdf(pdf_file), unsafe_allow_html=True)

    else:
        st.sidebar.error("Please fill in all required fields.")
