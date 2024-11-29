import streamlit as st
from chatGPThandler import chatGPTHandling


class QueryHandler:
    def __init__(self, api_key: str) -> None:
        self.chat_handler = chatGPTHandling(api_key)
        self.query_result: str = None

    def _process_query(self, query: str) -> str:
        return self.chat_handler.handle_query(query)


def run():
    # Initialize QueryHandler with API key
    api_key = open("./keys.txt", "r").read().strip()
    query_handler = QueryHandler(api_key)

    st.set_page_config(page_title="Energy Expert Agent", initial_sidebar_state="expanded")

    st.title("Energy Expert Agent")

    # Input fields
    query = st.text_input("Enter your energy-related question:")

    if st.button("Submit"):
        if query:
            response = query_handler._process_query(query)
            st.write("Response from Energy Expert Agent:")
            st.write(response)
        else:
            st.write("Please enter a query.")


if __name__ == "__main__":
    run()
