#https://nicschrading.com/project/Intro-to-NLP-with-spaCy/

from spacy.en import English
from subject_object_extraction import findSVOs
parser=English()
# can still work even without punctuation
#parse = parser("he and his brother shot me and my sister")
parse = parser("We are doing failback and having issues")
print(findSVOs(parse))
