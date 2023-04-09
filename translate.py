
import codecs
import openai


# The locations of the files to be translated. Dont forget use double \
filesToAddTranslationLocation = 'Location'

# Dont forget change here. You need to replace it with the file containing the text to be translated
fileNameToBeTranslated = 'willTranslate.json'

# Names of the files to be translated
filesToAddTranslation = [
    'en_US.json',
    'tr_TR.json',
    'ru_RU.json',
    'nl_NL.json',
    'ar_AE.json'
]

# Read the text to be translated
textToBeTranslated = codecs.open(
    filesToAddTranslationLocation+fileNameToBeTranslated, 'r', encoding='utf-8').read()


def askGPT(text):
    # Enter your openai api key here
    openai.api_key = "Openai_api_key"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": text}]
    )
    return response.choices[0].message.content


def controlForSyntaxProblem(TranslatedText):
    # Make translated text addable to main text
    result = ''
    for char in range(TranslatedText.find("{")+1, TranslatedText.find("}")+1):
        result += TranslatedText[char]
    return result


def getLanguage(fileName):
    fileLanguage = "English"
    # Detect translate language
    # Don't forget to add languages!
    match fileName.split('_')[0]:
        case 'en':
            fileLanguage = 'English'
        case 'tr':
            fileLanguage = 'Turkish'
        case 'ru':
            fileLanguage = 'Russian'
        case 'nl':
            fileLanguage = 'Dutch'
        case 'ar':
            fileLanguage = 'Arabic'
    return fileLanguage


for fileName in filesToAddTranslation:
    fileLanguage = getLanguage(fileName)

    # Translate text
    TranslatedText = askGPT(
        'Translate this json to {0} for app"{1}"'.format(fileLanguage, textToBeTranslated))

    TranslatedText = controlForSyntaxProblem(TranslatedText)
    TranslatedText = controlForSyntaxProblem(TranslatedText)

    # Read file for main text and make the main text suitable for adding the translated text
    file = codecs.open(filesToAddTranslationLocation +
                       fileName, 'r', encoding='utf-8')
    mainText = file.read()[:-3]+','
    file.close()
    # Add translated text
    file = codecs.open(filesToAddTranslationLocation +
                       fileName, 'w+', encoding='utf-8')

    newText = mainText+TranslatedText
    file.write(newText)
    file.close()
