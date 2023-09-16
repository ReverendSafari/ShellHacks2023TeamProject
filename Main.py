#  SHELL HACKS 2023  #
#                    #
import openai
import os

# Load OpenAI API key from an environment variable or secret management service
api_key = os.getenv("OPENAI_API_KEY")

# Initialize the GPT-3 API client
openai.api_key = api_key

import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

response = openai.ChatCompletion.create(
  model="gpt-4",
  messages=[
    {
      "role": "system",
      "content": "You are an expert Spanish speaker, you are speaking with a user. The user is trying to learn "
                 "Spanish as it is not their first language. Your job is to assess the grammar of the sentences, "
                 "and grade it on a scale of 1 to 100. Go sentence by sentence making sure to grade each one "
                 "separately and explain your response. Then find the average of those scores."
    },
    {
      "role": "assistant",
      "content": "Your sentence is perfectly correct. I would grade it as 100 out of 100. Great job!"
    },
    {
      "role": "assistant",
      "content": "I'm sorry but the sentence \"Que Tu Bien Mucho Gusto\" is not grammatically correct. The words are "
                 "all Spanish but they are jumbled and not creating a coherent sentence. For instance, "
                 "\"Mucho Gusto\" is a phrase used to say \"Nice to meet you\", but the usage of \"Que Tu Bien\" is "
                 "incorrect in this context. Therefore, I would grade it as 20 out of 100. Keep practicing!"
    },
    {
      "role": "assistant",
      "content": "Tome el papel y la pluma para escribir la carta."
    },
    {
      "role": "assistant",
      "content": "\"Take the paper and pen to write the letter.\" This sentence is perfectly correct. The grammar is "
                 "precise and the word choice is accurate. I would rate it 100 out of 100. Excellent work!"
    },
    {
      "role": "assistant",
      "content": "Necesito compra zapatos nuevos para la fiesta."
    },
    {
      "role": "assistant",
      "content": "\"Necesito compra zapatos nuevos para la fiesta.\" This sentence is almost perfect, but there's a "
                 "small grammatical mistake. The correct form should be \"Necesito comprar zapatos nuevos para la "
                 "fiesta\", using \"comprar\" (to buy) instead of \"compra\". In this context, \"comprar\" is the "
                 "infinitive form of the verb which is needed after \"necesito\". Therefore, I would grade it as 90 "
                 "out of 100. Keep it up!"
    },
    {
      "role": "user",
      "content": "Por favor, puede usted ayudarme con formar una oracion en el idioma castellano?"
    },
    {
      "role": "assistant",
      "content": "\"Por favor, ¿puede usted ayudarme a formar una oración en el idioma castellano?\" This sentence is "
                 "almost perfect. There's a small oversight in forgetting to include the preposition \"a\" after "
                 "\"ayudarme\". The correct form is “ayudarme a formar” and not “ayudarme formar”. Therefore, "
                 "I would grade it as 95 out of 100. Good job!\n\nTo find the average of the scores, we add them all "
                 "up and divide by the number of sentences. Therefore, (20+100+90+95) / 4 = 76.25. So the average "
                 "score of these four sentences is approximately 76. Well done, keep practicing!"
    },
    {
      "role": "user",
      "content": "Perfecto, gracias por su directitud"
    },
    {
      "role": "assistant",
      "content": "\"Perfecto, gracias por su directitud.\" The correct form should be \"Perfecto, gracias por su "
                 "directividad\" or better yet \"Perfecto, gracias por su ayuda\". The word \"directitud\" does not "
                 "exist in Spanish. Therefore, I would grade it as 60 out of 100. Don't worry though, "
                 "this is a common mistake for learners. Keep it up!\n\nTo find the new average of the scores, "
                 "we add them all up and divide by the number of sentences. Therefore, (20+100+90+95+60) / 5 = 73. So "
                 "the average score of these sentences is approximately 73. Keep practicing!"
    },
    {
      "role": "user",
      "content": "Esto oracion es muy no correctones"
    },
    {
      "role": "assistant",
      "content": "\"Esto oracion es muy no correctones.\" This sentence has several mistakes. You should say \"Esta "
                 "oración no es muy correcta\". The terms \"esto oracion\" should be \"esta oración\", "
                 "because \"oración\" is a feminine noun so it needs a feminine determiner. Also, the negative form "
                 "\"muy no correctones\" is not correct, the right way to express that idea is \"no es muy "
                 "correcta\". Therefore, I would grade it as 40 out of 100. \n\nIncluding this sentence, the scores "
                 "are: 20, 100, 90, 95, 60, 40. The average score is 67.5 (405 / 6). Keep improving!"
    },
    {
      "role": "assistant",
      "content": "Espero que usted tener un gran día."
    },
    {
      "role": "user",
      "content": "Esto oracion tambien no es correcta en buen nivel"
    },
    {
      "role": "assistant",
      "content": "\"Espero que usted tener un gran día.\" This sentence is not grammatically correct. In Spanish, "
                 "after \"Espero que\" (I hope that) a subjunctive verb should be used. The correct form should be "
                 "\"Espero que usted tenga un gran día\". Therefore, I would grade it as 40 out of 100.\n\nWhen you "
                 "say, \"Esto oracion tambien no es correcta en buen nivel\", there are a few grammatical mistakes. "
                 "The correct form should be \"Esta oración también no está en buen nivel\". Therefore, I would grade "
                 "it as 60 out of 100.\n\nIncluding these sentences, the scores are: 20, 100, 90, 95, 60, 40, 40, "
                 "60. The average score is approximately 64.37. Keep going!"
    },
    {
      "role": "user",
      "content": "Esta tambien no esta correcta"
    },
    {
      "role": "assistant",
      "content": "\"Esta tambien no esta correcta.\" This sentence would be correctly written as \"Esta también está "
                 "incorrecta.\" The word \"no\" is not needed in this sentence when using the word \"incorrecta.\" "
                 "Therefore, I would grade it as 80 out of 100.\n\nAdding this to the previous scores: 20, 100, 90, "
                 "95, 60, 40, 40, 60, and now 80. We divide the total, 585, by 9 (the number of sentences) to get an "
                 "average score of around 65. Keep practicing!"
    },
    {
      "role": "user",
      "content": "Tampoco esta correcta"
    },
    {
      "role": "assistant",
      "content": "\"Tampoco esta correcta.\" This sentence is correctly formed. The word \"tampoco\" means "
                 "\"neither\" or \"not either\" and it is correctly used here. I'd just suggest adding a subject to "
                 "specify what is not correct for clearer understanding, such as \"Esta (oración) tampoco está "
                 "correcta\". Therefore, I would grade it as 90 out of 100.\n\nIncluding this, the scores are: 20, "
                 "100, 90, 95, 60, 40, 40, 60, 80, and now 90. The total sum would be 675. Therefore, when we divide "
                 "by the number of sentences (10), the average score is 67.5. Keep up the progress!"
    }
  ],
  temperature=1,
  max_tokens=256,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)
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
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=2000
    )
    return response.choices[0].text.strip()

def chat_in_language(language):
    user_input = ""
    while user_input.lower() != "quit":
        user_input = input(f"You ({language}): ")
        prompt = f"The following is a conversation in {language}.\nUser: {user_input}\nChatGPT:"
        response = ask_gpt3(prompt)
        print(f"ChatGPT: {response}")

if __name__ == "__main__":

    sentence = "Esto oracion no es escribo correctitud"
    language = "Spanish"
    result = assess_grammar(sentence, language)
    print(f"In {language}, the assessment is: {result}")