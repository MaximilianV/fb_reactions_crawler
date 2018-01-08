import pip
import pathlib


def install_dependencies():
    pip.main(['install', '-r', 'requirements.txt'])


def initialize_folderstructure():
    print("Initializing required folder structure...", end="")
    pathlib.Path('data/datasets').mkdir(parents=True, exist_ok=True)
    pathlib.Path('data/models').mkdir(parents=True, exist_ok=True)
    pathlib.Path('logs').mkdir(parents=True, exist_ok=True)
    print(" Finished.")


if __name__ == '__main__':
    install_dependencies()
    import nltk
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('perluniprops')
    initialize_folderstructure()
