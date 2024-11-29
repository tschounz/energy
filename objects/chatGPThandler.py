from openai import OpenAI


class chatGPTHandling:
    def __init__(self) -> None:
        self.client = OpenAI(api_key=open("./keys.txt", "r").read().strip())

    def handle_query(self, query: str) -> str:
        response = self.client.Completion.create(
            model="gpt-4o", prompt=query, max_tokens=150
        )
        return response.choices[0].text.strip()
