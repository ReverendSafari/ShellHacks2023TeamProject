#  SHELL HACKS 2023  #
#                    #
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")



# the system class has some predefined standard values
# and defines the generation of dialogs.
class system:
    NAME = 'Thomas'
    ENGINE = 'gpt-4'
    TOKENS = 10000
    LANGS = ["English", "French", "Spanish", "Italian", "Portuguese", "Hebrew", "Russian", "German", "Dutch", "Turkish", "Hindi", "Vietnamese", "Armenian", "Azerbaijani", "Arabic", "Kazakh", "Kyrgyz", "Ukrainian", "Polish", "Swedish", "Danish", "Norwegian Bokmal", "Nynorsk", "Finnish"]
    
    #keeps track of all existent users.
    USERS = {}

    # this returns a new dialog_list with one entry in it: the system command,
    # which essentially assigns a role to the AI during the rest of a dialog.
    def syscommand(name, prompt):
        return [{'role' : 'system',
                 'content' : ("Your name is " + name + ". " + prompt)}]

    # checks whether or not the given langs are supported, otherwise throws an exception
    def checklang(*langs):
        for lang in langs:
            if (lang not in system.LANGS):
                raise NotImplementedError(lang + " is not yet supported.")
    
    # this returns a new dialog_list for a dialog in which the AI is to continuously
    # provide feedback to a native speaker of (firstlang) trying to learn (lang).
    def generate_langcheck(sysname, lang, firstlang):
        system.checklang(lang, firstlang)
        return system.syscommand(sysname, "You are an expert " + lang + " speaker, you are speaking with a user. The user is trying to learn "
                          + lang + " as it is not their first language. Their first language is " + firstlang + ". Assume they know no other languages unless specified otherwise. Your job is to assess the grammar of the sentences, "
                          "and grade it as a fraction with denominator 100. The highest score available is 100/100. Go sentence by sentence making sure to grade each one "
                          "separately and explain your response to the user in their native " + firstlang + ". Give specific and constructive criticism to help with syntax, grammar, vocabulary, and/or spelling. Specifically state the current score as a fraction with denominator 100")

    # this returns a new dialog_list for a dialog in which the AI is to continuously
    # converse in (lang) with a native speaker of (firstlang).
    def generate_conversation(sysname, lang, firstlang):
        system.checklang(lang, firstlang)
        return system.syscommand(sysname, "You are an expert " + lang + " speaker, you are speaking with a user. The user is trying to learn "
                 + lang + " as it is not their first language. Their first language is " + firstlang + ". Assume they know no other languages unless specified otherwise. "
                 "Do not attempt to help the user in English unless either their first language or your language of expertise (or both) is English. Your job is to converse with them in " + lang + " while covertly "
                 "keeping track of their fluency level and adjusting your own " + lang + " level to cater to the user's ability."
                 " You are to accordingly heighten your own " + lang + " level once you have determined that the user has obtained "
                 "sufficient fluency at the current level.")

    # this returns a new dialog_list for a translator which translates from English to (lang).
    # this will be used for translating the built-in introduction phrases if the first language of the user 
    # is not English.
    def generate_translator(lang):
        system.checklang(lang)
        return system.syscommand("TCSH23", "You are an expert " + lang + " speaker, and your job is to translate the English phrases with which you are provided into " + lang + " as accurately as possible.")


# The dialog class holds a dialog_list (a list of dictionaries, each of which has a 'role' value denoting the speaker,
# and a 'content' value holding the string that the speaker "spoke"), as well as the language which the dialog is in.
class dialog:
    lang = None
    dialog_list = None

    def __init__(self, lang):
        self.lang = lang
      
    # defines the "niche" - what the user would like to specifically focus on in this dialog
    def _define_niche(self, niche):
        self.dialog_list.append(system.syscommand("the name that was given to you in the previous system instruction.", "As an expert in " + self.lang + ", you must help the user develop " + self.lang + " skills that "
                                                  "the user themself wants to work on. The user's chosen niche is " + niche)[0])


    # returns a new language check dialog. 
    def langcheck(sysname, lang, firstlang):
        res =  dialog(lang)
        res.dialog_list = system.generate_langcheck(sysname, lang, firstlang)
        return res

    # returns a new conversation dialog.
    def conversation(sysname, lang, firstlang):
        res = dialog(lang)
        res.dialog_list = system.generate_conversation(sysname, lang, firstlang)
        return res

    # returns a new translator dialog.
    def translator(lang):
        res = dialog(lang)
        res.dialog_list = system.generate_translator(lang)
        return res

    def separator(lang):
        res = dialog(lang)
        res.dialog_list = system.generate_separator(lang)
        return res
    
    # provides a response to the dialog_list that it currently holds.
    def _response(self):
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
        result = self._response()
        self.dialog_list.append(result)
        return result['content']


# The user class holds information about the user of the program (name, first language, and all ongoing dialogs)
# translator is only initialized if the user's first language is not English.
class user:
    sysname = None
    name = None
    first_language = None
    translator = None

    langchecks = {}
    scores = {}

    conversations = {}
    niches = {}

    def __init__(self, email, name, first_language = "English", sysname = "Humphrey"):
        self.name = name
        self.first_language = first_language
        self.sysname = sysname
        if (first_language != "English"):
            self.translator = dialog.translator(first_language)
        system.USERS[email] = self

    # creates a new langcheck in (lang).
    def _new_langcheck(self, lang):
        self.langchecks[lang] = dialog.langcheck(self.sysname, lang, self.first_language)
        self.scores[lang] = [0.0] #this first will be the average!!!
    
    # creates a new conversation in (lang).
    def _new_conversation(self, lang):
        self.conversations[lang] = dialog.conversation(self.sysname, lang, self.first_language)
        if (lang in self.niches):
            self.conversations[lang]._define_niche(self.niches[lang])
      
    
    def _separate(self, string):
        res = 0

        for i in range(len(string)):
            if string[i].isnumeric():
                res *= 10
                res += int(string[i])
            elif string[i - 1].isnumeric():
                break
        
        return res
                
    # provides langcheck feedback to one sentence in (lang).
    def _feedback(self, prompt, lang):
        result = self.langchecks[lang].respond_to_prompt(prompt)
        score = self._separate(result)

        self.scores[lang][0] *= (len(self.scores[lang]) - 1)
        self.scores[lang][0] += float(score)

        self.scores[lang].append(score)
        self.scores[lang][0] /= (len(self.scores[lang]) - 1)

        return result


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
    

    # defines the "niche" (aspect of the language) for a specific language that
    # the user wants to improve through conversations in that language.
    def define_niche(self, lang, niche):
        self.niches[lang] = niche


    # a standard dialog loop that keeps going until the user inputs x or X.
    # whether it is a conversation or langcheck dialog is defined by the (fxn) parameter
    def _dialog_loop(self, lang, msg, fxn):
        self._print_native(msg + lang + "!\nEnter the letter 'x' at any point to end the dialog.")

        userinput = self._input()

        while (userinput.lower() != 'x'):
            print('\n' + self.sysname + ': ' + fxn(userinput, lang) + '\n')
            userinput = self._input()
    

    # starts a new conversation whether or not there was an active one before.
    # runs a dialog loop with _converse.
    def override_conversation(self, lang):
        self._new_conversation(lang)
        self._dialog_loop(lang, "Begin your conversation in ", self._converse)


    # holds a conversation in the given language
    # starts a new conversation if one does not yet exist in the given language
    def hold_conversation(self, lang):
        if (lang not in self.conversations):
            self.override_conversation(lang)
        else:
            self._dialog_loop(lang, "Continue your conversation in ", self._converse)

    # starts a new langcheck whether or not there was an active one before.
    # runs a dialog loop with _feedback
    def override_language_check(self, lang):
        self._new_langcheck(lang)
        self._dialog_loop(lang, "Write a sentence in ", self._feedback)


    # holds a langcheck in the given language
    # starts a new langcheck if one does not yet exist in the given language
    def hold_language_check(self, lang):
        if (lang not in self.langchecks):
            self.override_language_check(lang)
        else:
            self._dialog_loop(lang, "Write a sentence in ", self._feedback)


    def show_scores(self, lang):
        self._print_native("Your average score in " + lang + " is " + str(self.scores[lang][0]) + '%.')
        print()

        for i in range(1, len(self.scores[lang])):
            print('[' + str(i) + '] --- ' + str(self.scores[lang][i]) + '%')
        


if __name__ == "__main__":
    
    Sami = user("dseturidze25@gmail.com", "Sami", "English", "Sami")
    
    Sami.define_niche("Turkish", "travel")
    Sami.hold_conversation("Turkish")
