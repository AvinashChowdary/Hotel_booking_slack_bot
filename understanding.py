import db
import nltk
from PyDictionary import PyDictionary
nltk.data.path.append("./nltk")

class understanding(object):

    def __init__(self):
        self.db = db.bot_db()
        self.dictionary = PyDictionary()
        self.lemmatizer = nltk.stem.WordNetLemmatizer()


    def understand(self, command):
        response = {}
        temp_command = command.lower()
        information = [word.lower() for word in nltk.tokenize.word_tokenize(temp_command)]
        lemmatized_command = [self.lemmatizer.lemmatize(word) for word in information]
        commands = self.db.read_commands()
        words = []

        for word in commands:
            if word.lower() in commands:
                words.append(word.lower())

        for word in lemmatized_command:
            if word.lower() in commands:
                words.append(word.lower())
                if self.dictionary.synonym(word) is not None:
                    for synonyms in self.dictionary.synonym(word):
                        words.append(synonyms.lower())

        response["words"] = list(set(words))
        return response