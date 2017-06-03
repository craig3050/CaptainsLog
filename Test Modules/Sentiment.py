
from google.cloud import language
#if error run pip install --upgrade google-cloud-language
import time

def sentiment_analysis(output_text):
    """Run a sentiment analysis request on text within a passed filename."""
    language_client = language.Client()
    document = language_client.document_from_html(output_text)
    # Detects sentiment in the document.
    annotations = document.annotate_text(include_sentiment=True, include_syntax=False, include_entities=False)
    score = annotations.sentiment.score
    magnitude = annotations.sentiment.magnitude

    for index, sentence in enumerate(annotations.sentences):
        sentence_sentiment = sentence.sentiment.score
        print('Sentence {} has a sentiment score of {}'.format(
            index, sentence_sentiment))

    print('Overall Sentiment: score of {} with magnitude of {}'.format(
        score, magnitude))

    print('Sentiment: score of {} with magnitude of {}'.format(
        score, magnitude))

    if score >= 0.2:
        return "Positive"
    elif score == 0.1:
        return "Neutral"
    elif score == 0.0:
        return "Mixed"
    elif score <0.0:
        return "Negative"

if __name__ == '__main__':
    sample_text = """
Some weeks ago through medical doubt
I met someone I'd heard lots about
I never thought our paths would cross
Our meeting left me at a loss.
I'd had no contact with this guy
He picked me out...... I wonder why?
He's very sneaky, changes disguise
I've made small payments towards his demise,
But he moves about with sadistic glee
And now he takes revenge on me.
He's never redundant nor on the dole
He violates your inner soul.
He's sometimes slow and sometimes swift
But the net result is Satans' gift.
What can I do now he's moved in?
He's hurting now my next of kin.
He's no compassion no fear no shame
It's no surprise cancer's his name.
World-wide great efforts attack this thing,
And wondrous improvements this will bring
They'll drain his strength give him the sack
Once beaten he'll have no way back
It may be too late for you or me
But we'll fight our corner as best can be.
With help from family and friends
With medical treatment and new trends
We'll do our best through smooth and rough
To stay real positive ....... hang in tough.
And maybe before our final breath
We may rejoice at cancers death."""

    General_mood = sentiment_analysis(sample_text)
    print (General_mood)
    time.sleep(20)