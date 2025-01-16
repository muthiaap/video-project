import os
from groq import Groq

class TextGenerated:
    def __init__(self, api_key):
        """
        Initialize the Groq client with the provided API key.

        :param api_key: API key for authenticating with Groq
        """
        self.client = Groq(api_key=api_key)
        self.prompt_template = (
            """
            Anda adalah pakar pemasaran yang membantu klien di industri keuangan. 
            Berdasarkan pola transaksi yang diberikan, buatlah ringkasan yang ramah dan menarik tentang apa transaksi yang sering dia lakukan yang ditujukan langsung kepada pelanggan.
            Mulailah respons dengan \"Haloo,\" dan jelaskan kebiasaan transaksi mereka dengan nada percakapan yang relevan pakai sapaan 'kamu'.
            Tulis hingga 2 kalimat pendek agar menarik dan mudah dipahami.

            Data input: {user_query}
            """
        )

    def get_response(self, user_input):
        """
        Generate a response from the Groq model based on the user input.

        :param user_input: The user's query to process
        :return: Generated response as a string
        """
        final_prompt = self.prompt_template.format(user_query=user_input)

        response = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": final_prompt},
            ],
            model="llama-3.3-70b-versatile",
        )

        return response.choices[0].message.content