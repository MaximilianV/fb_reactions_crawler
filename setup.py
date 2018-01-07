import pip


def install_dependencies():
    pip.main(['install', '-r', 'requirements.txt'])


if __name__ == '__main__':
    install_dependencies()
    import nltk
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('perluniprops')