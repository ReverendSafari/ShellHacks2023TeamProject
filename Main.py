#Test this Repo
import openai
import os

# Load OpenAI API key from an environment variable or secret management service
api_key = os.getenv("OPENAI_API_KEY")

# Initialize the GPT-3 API client
openai.api_key = api_key

# Function to ask a question to the ChatGPT model
def ask_gpt3(prompt, model="text-davinci-002", tokens=150):
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=tokens
    )
    message = response.choices[0].text.strip()
    return message

# Main function to simulate a chat
def chat_in_language(language):
    user_input = ""
    while user_input.lower() != "quit":
        user_input = input(f"You ({language}): ")
        prompt = f"The following is a conversation in {language}.\nUser: {user_input}\nChatGPT:"
        response = ask_gpt3(prompt)
        print(f"ChatGPT: {response}")

if __name__ == "__main__":
    # Substitute 'French' with the language you want to have a conversation in
    chat_in_language("Spanish")