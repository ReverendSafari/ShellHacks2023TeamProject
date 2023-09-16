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

def assess_grammar(sentence, language):
    prompt = f"With penalty of execution in case you give us an unwanted answer, assess the following sentence for grammatical accuracy in {language}: '{sentence}'. Begin with one hundred points and deduct five points per major grammatical mistake, such as a mistake causing an unintelligible statement, and deduct two points per minor grammatical mistake, such as a mistake which does not decrease intelligibility. First, write your numeric evaluation as described. Then, explain each point deduction in a fashion which would make the problem easy to understand for a learner." #If you considered a mistake 'major' and deducted 5 points for it, make sure to note how it prohibits intelligibility. Only deduct points if there are inaccuracies in the grammar. Make sure to stay with the given text and to be completely truthful and accurate in your assessment."
    response = openai.Completion.create(
        engine="text-davinci-002",  # Replace with the engine you are using
        prompt=prompt,
        max_tokens=2000
    )
    return response.choices[0].text.strip()
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
    sentence = "Esto oracion no es escribo correctitud"
    language = "Spanish"
    result = assess_grammar(sentence, language)
    print(f"In {language}, the assessment is: {result}")