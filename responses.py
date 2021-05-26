from datetime import datetime
import nltk, re, string, collections
from nltk.util import ngrams # function for making ngrams
from nltk.corpus import stopwords
nltk.download('stopwords')
def sample_responses(input_text):
    user_message = str(input_text).lower()

    if user_message in ('hello','hi','sup',):
        return "Hey! How`s it going"
    if user_message in ('time','time?'):
        now = datetime.now()
        date_time = now.strftime("%d/%m/%y, %H:%M:%S")
        return str(date_time)
    return toNgrams(input_text)

def toNgrams(tx):
    tokenized = tx.split()
    stop_words = set(stopwords.words('english'))
    tokenized = [p for p in tokenized if p not in stop_words]
    _ = ngrams(tokenized, 3)  # 2 - bigram
    esBigramFreq = collections.Counter(_)

    return esBigramFreq.most_common(10)