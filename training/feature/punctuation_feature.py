from sklearn.feature_extraction.text import CountVectorizer

# As from https://sirinnes.wordpress.com/2015/01/22/custom-vectorizer-for-scikit-learn/


class PunctuationVectorizer(CountVectorizer):
    def __init__(self):
        super(PunctuationVectorizer, self).__init__()

    def prepare_doc(self, doc):
        punc_list = ['!', '"', '#', '$', '%', '&', '\'' ,'(' ,')', '*', '+', ',', '-', '.' ,'/' ,':' ,';' ,'' ,'?' ,'@' ,'[' ,'\\' ,']' ,'^' ,'_' ,'`' ,'{' ,'|' ,'}' ,'~']
        doc = doc.replace("\\r\\n"," ")
        for character in doc:
            if character not in punc_list:
                doc = doc.replace(character, "")
        return doc

    def build_analyzer(self):
        preprocess = self.build_preprocessor()
        return lambda doc : preprocess(self.decode(self.prepare_doc(doc)))
