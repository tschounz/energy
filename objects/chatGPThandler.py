import openai


class RefinementPipeline:
    def __init__(self):
        pass

    def get_predefined_questions(self):
        return [
            "What is the estimated annual energy consumption \n"
            "for a house located in {location} "
            "with {occupants} occupants and an area of {area} m²?\n",
            "What size and type of heat pump would be most efficient\n"
            "for a house in {location} "
            "with {occupants} occupants and an area of {area} m²?\n",
            "How many solar panels would be required to meet \n"
            "the energy needs of a house in "
            "{location} with {occupants} occupants and \n"
            "an area of {area} m²?\n",
            "What are the potential cost savings and benefits \n"
            "of obtaining an energy certificate "
            "for a house in {location}?\n",
            "What are the most effective ways to improve \n"
            "the energy efficiency of a house in "
            "{location} with {occupants} occupants and an \n"
            "area of {area} m²?\n",
            "Is a hybrid heating system a better option for \n"
            "a house in {location} with {occupants} "
            "occupants and an area of {area} m², considering \n"
            "a budget of {budget}?\n",
            "What are the best practices for integrating \n"
            "electric car charging stations into the "
            "energy system of a house in {location}?\n",
            "What government incentives or rebates are available \n"
            "for installing renewable energy "
            "systems in a house located in {location}?\n",
            "How can smart home technologies be utilized to \n"
            "optimize energy consumption in a house "
            "in {location} with {occupants} occupants?\n",
            "What are the environmental benefits of switching \n"
            "to renewable energy sources for a "
            "house in {location} with {occupants} occupants and \n"
            "an area of {area} m²?\n",
        ]

    def get_predefined_summary(self):
        return [
            "Please summarize the following responses into one structured summary.\n",
            "The summary should be concise and informative.\n",
            "Include the key points from each response.\n",
            "Make sure to include the most important details and recommendations.\n",
            "The summary must be easy to read and understand.\n",
            "The summary must be very short and to the point.\n",
            "Avoid unnecessary details and repetition.\n",
            "The summary should be structured into the following sections:\n",
            "1. Energy demand household\n",
            "2. Heat pump\n",
            "3. Solar panels\n",
            "4. Improvement to the house\n",
            "5. Best practices for electric car charging\n",
            "6. Smart home technologies\n",
            "7. Environmental benefits\n\n",
        ]


class ChatGPTHandler(RefinementPipeline):
    def __init__(self):
        super().__init__()
        self.client = openai
        self.client.api_key = open("./data/key.txt", "r").read().strip()

    def handle_query(self, query):
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": query},
            ],
        )
        return response.choices[0].message.content

    def list_models(self):
        models = openai.models.list()
        return [model["id"] for model in models["data"]]

    def refine_response(self, response):
        query = (
            "Reduce the number of words \n"
            "and format the following response in bullet points:\n\n"
            f"{response}"
        )
        return self.handle_query(query)

    def summarize_responses(self, responses):
        combined_response = "\n\n".join(responses)
        query = f"{''.join(self.get_predefined_summary())} {combined_response}"
        return self.handle_query(query)


class HouseEnergyAdvisor(ChatGPTHandler):
    def __init__(self):
        """
        Initialize the HouseEnergyAdvisor
        with a ChatGPTHandler instance.

        :param chat_gpt_handler: Instance of ChatGPTHandler
        for processing queries.
        """
        super().__init__()

    def build_query(self, house_params):
        base_info = (
            f"House located in {house_params['location']}, \n"
            "with {house_params['occupants']} occupants. "
            f"It has an area of {house_params['area']} m². \n"
            "The house is {house_params['type']} and "
            f"the budget is {house_params['budget']}. "
        )
        additional_info = house_params.get("additional_info", "")
        queries = [
            f"{base_info} {q.format(**house_params)}"
            for q in self.get_predefined_questions()
        ]
        if additional_info:
            queries = [
                f"{q} Additional considerations: {additional_info}" for q in queries
            ]
        return queries

    def process_queries(self, queries):
        """
        Send refined queries to ChatGPT for processing.

        :param queries: List of refined queries.
        :return: List of responses from ChatGPT.
        """
        responses = []
        for query in queries:
            response = self.handle_query(query)
            responses.append(response)
        return responses

    def refine_responses(self, responses):
        refined_responses = []
        for response in responses:
            refined_response = self.refine_response(response)
            refined_responses.append(refined_response)
        return refined_responses
