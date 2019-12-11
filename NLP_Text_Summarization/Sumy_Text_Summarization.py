#Import library essentials
from sumy.parsers.plaintext import PlaintextParser #We're choosing a plaintext parser here, other parsers available for HTML etc.
from sumy.nlp.tokenizers import Tokenizer 
from sumy.summarizers.lex_rank import LexRankSummarizer #We're choosing Lexrank, other algorithms are also built in
file="C:\\Users\\kach\\Desktop\\Temp\\CPE_H2ManagedQ3.txt"
parser = PlaintextParser.from_file(file, Tokenizer("english"))
summarizer = LexRankSummarizer()

summary = summarizer(parser.document, 5) #Summarize the document with 5 sentences

#print(summary)

for sentence in summary:
    print(sentence)


#Q2)How can Microsoft better show you that they 'care about your needs'? 
