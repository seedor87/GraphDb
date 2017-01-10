from textblob.classifiers import NaiveBayesClassifier
from textblob import TextBlob

train = [
    ('00:00:00', 'time'),
    ('1/2/69', 'date'),
    ('00:00', 'time'),
    ('00-00-00.', 'date'),
    ('11:59', 'time'),
    ('03:45', 'time'),
    ('12/25/2016', 'date'),
    ("07.08.94", 'date'),
    ('02-03-01', 'date'),
    ('08:34:27', 'time')
]
test = [
    ('1/1/11', 'date'),
    ('05:34', 'time'),
    ("05-10-2007", 'date'),
    ("11:59:59", 'time'),
    ('10:19:01', 'time'),
    ("09.12.1994", 'date')
]

cl = NaiveBayesClassifier(train)

# Classify some text
print(cl.classify("12/28/2016"))  # "date"
print(cl.classify("I don't like their pizza."))   # "text"

# Classify a TextBlob
blob = TextBlob("02/03/1992", classifier=cl)
print(blob)
print(blob.classify())

for sentence in blob.sentences:
    print(sentence)
    print(sentence.classify())

# Compute accuracy
print("Accuracy: {0}".format(cl.accuracy(test)))

# Show 5 most informative features
cl.show_informative_features(5)
