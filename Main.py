#  SHELL HACKS 2023  #
#                    #
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")



# the system class has some predefined standard values
# and defines the generation of dialogs.
class system:
    ENGINE = 'gpt-4'
    TOKENS = 2000
    LANGS = ["English", "French", "Spanish", "Italian", "Portuguese", "Hebrew", "Russian", "German", "Dutch", "Turkish"]

    # this returns a new dialog_list with one entry in it: the system command,
    # which essentially assigns a role to the AI during the rest of a dialog.
    def syscommand(prompt):
        return [{'role' : 'system',
                 'content' : prompt}]

    # checks whether or not the given langs are supported, otherwise throws an exception
    def checklang(*langs):
        for lang in langs:
            if (lang not in system.LANGS):
                raise NotImplementedError(lang + " is not yet supported.")
    
    # this returns a new dialog_list for a dialog in which the AI is to continuously
    # provide feedback to a native speaker of (firstlang) trying to learn (lang).
    def generate_langcheck(lang, firstlang):
        system.checklang(lang, firstlang)
        return system.syscommand("You are an expert " + lang + " speaker, you are speaking with a user. The user is trying to learn "
                          + lang + " as it is not their first language. Their first language is " + firstlang + ". Assume they know no other languages unless specified otherwise. Your job is to assess the grammar of the sentences, "
                          "and grade it on a scale of 1 to 100. Go sentence by sentence making sure to grade each one "
                          "separately and explain your response to the user in their native " + firstlang + ". Then find the average of those scores.")

    # this returns a new dialog_list for a dialog in which the AI is to continuously
    # converse in (lang) with a native speaker of (firstlang).
    def generate_conversation(lang, firstlang):
        system.checklang(lang, firstlang)
        return system.syscommand("You are an expert " + lang + " speaker, you are speaking with a user. The user is trying to learn "
                 + lang + " as it is not their first language. Their first language is " + firstlang + ". Assume they know no other languages unless specified otherwise. Your job is to converse with them in " + lang + " while covertly "
                 "keeping track of their fluency level and adjusting your own " + lang + " level to cater to the user's ability."
                 " You are to accordingly heighten your own " + lang + " level once you have determined that the user has obtained "
                 "sufficient fluency at the current level.")

    # this returns a new dialog_list for a translator which translates from English to (lang).
    # this will be used for translating the built-in introduction phrases if the first language of the user 
    # is not English.
    def generate_translator(lang):
        system.checklang(lang)
        return system.syscommand("You are an expert " + lang + " speaker, and your job is to translate the English phrases with which you are provided into " + lang + " as accurately as possible.")


# The dialog class holds a dialog_list (a list of dictionaries, each of which has a 'role' value denoting the speaker,
# and a 'content' value holding the string that the speaker "spoke"), as well as the language which the dialog is in.
class dialog:
    lang = None
    dialog_list = None

    def __init__(self, lang):
        self.lang = lang
      

    # returns a new language check dialog. 
    def langcheck(lang, firstlang):
        res =  dialog(lang)
        res.dialog_list = system.generate_langcheck(lang, firstlang)
        return res

    # returns a new conversation dialog.
    def conversation(lang, firstlang):
        res = dialog(lang)
        res.dialog_list = system.generate_conversation(lang, firstlang)
        return res

    # returns a new translator dialog.
    def translator(lang):
        res = dialog(lang)
        res.dialog_list = system.generate_translator(lang)
        return res
    
    # provides a response to the dialog_list that it currently holds.
    def response(self):
        return openai.ChatCompletion.create(
          model = system.ENGINE,
          messages = self.dialog_list,
          temperature = 1,
          max_tokens = system.TOKENS,
          top_p = 1,
          frequency_penalty = 0,
          presence_penalty = 0
      ).choices[0].message

    # appends (prompt) to dialog_list and responds to its dialog_list, also 
    # appending its response. this keeps the dialog up to date for as long as the program runs.
    def respond_to_prompt(self, prompt):
        self.dialog_list.append({'role' : 'user', 'content' : prompt})
        result = self.response()
        self.dialog_list.append(result)
        return result['content']


# The user class holds information about the user of the program (name, first language, and all ongoing dialogs)
# translator is only initialized if the user's first language is not English.
class user:
    name = None
    first_language = None
    translator = None

    langchecks = {}
    conversations = {}

    def __init__(self, name, first_language = "English"):
        self.name = name
        self.first_language = first_language
        if (first_language != "English"):
            self.translator = dialog.translator(first_language)

    # creates a new langcheck in (lang).
    def _new_langcheck(self, lang):
        self.langchecks[lang] = dialog.langcheck(lang, self.first_language)
    
    # creates a new conversation in (lang).
    def _new_conversation(self, lang):
        self.conversations[lang] = dialog.conversation(lang, self.first_language)
      
    # provides langcheck feedback to one sentence in (lang).
    def _feedback(self, prompt, lang):
        return self.langchecks[lang].respond_to_prompt(prompt)

    # responds to the given conversation entry in (lang)
    def _converse(self, prompt, lang):
        return self.conversations[lang].respond_to_prompt(prompt)
    
    # takes an input string from the user, but formatted like so:
    # <username>: "LOREM IPSUM..."
    def _input(self):
        return str(input(self.name + ': '))

    # prints the given (val) string in the first language of the user.
    def _print_native(self, val):
        # translator is only null when first language is English.
        if (self.translator == None):
            print(val)
        else:
            print(self.translator.respond_to_prompt(val))
    

    # holds a conversation in the given language
    # starts a new conversation if one does not yet exist in the given language
    def hold_conversation(self, lang):
        if (lang not in self.conversations):
            self._new_conversation(lang)
            verb = "Begin"
        else:
            verb = "Continue"
        
        self._print_native(verb + " your conversation in " + lang + "!\nEnter the letter X at any point to end the dialog.")

        userinput = self._input()

        while (userinput != 'X'):
            print('\nHumphrey: ' + self._converse(userinput, lang) + '\n')
            userinput = self._input()
    
    # holds a langcheck in the given language
    # starts a new langcheck if one does not yet exist in the given language
    def hold_language_check(self, lang):
        if (lang not in self.langchecks):
            self._new_langcheck(lang)
          
        self._print_native("Write a sentence in " + lang + "!\nEnter the letter X at any point to end the dialog.")

        userinput = self._input()

        while (userinput != 'X'):
            print('\nHumphrey: ' + self._feedback(userinput, lang) + '\n')
            userinput = self._input()



if __name__ == "__main__":
    
    Deme = user("Deme")

    Deme.hold_conversation("Spanish")