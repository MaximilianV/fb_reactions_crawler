import pip

def installDependencies():
    pip.main(['install', '-r', 'requirements.txt'])

# Example
if __name__ == '__main__':
    installDependencies()
    import nltk
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('perluniprops')