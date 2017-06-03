import argparse
import time
import os
import shutil
import datetime


def transcribe_file(speech_file):
    #convert to flac and rename file to audio.flac
    print ("Converting to FLAC - I will now open a separate window to complete this")
    convert_to_flac(speech_file)

    #upload file to GCS for processing
    print ("Uploading to Google Cloud Storage - I will now open a separate window to complete this")
    Upload_to_GCS()

    #send GCS link of file to google speech for processing
    print ("Sending to Google Speech for processing...")
    text_returned = transcribe_gcs("gs://audioprocess/audio.flac")
    print ("This is the output from ##date##\n\n")
    print ("Confidence = {[1]}\n".format(text_returned))
    print ("Transcription = {[0]}\n\n\n".format(text_returned))
    text_for_sentiment_analysis = "{[0]}".format(text_returned)

    # send text result for sentiment analysis
    print ("Now sending off the text for sentiment analysis...")
    sentiment_returned = sentiment_analysis(text_for_sentiment_analysis)

    #open main diary text file
    #append text to file
    #append date and time to file, and the sentiment of the text
    #close file
    print ("Writing to Captain's Log file in your Google Drive")
    append_text_to_file(text_for_sentiment_analysis,sentiment_returned)



    #delete audio from gcs
    print ("Deleting Audio from Google Cloud Storage...")
    delete_GCS()

    #delete .flac file from local
    print ("Deleting the temporary .FLAC file used for upload...")
    delete_FLAC()

    #move processed file to 'processed' directory
    print ("Moving the file to the processed directory in your Google Drive")
    move_to_processed(speech_file)

    #print a message saying it's all done successfully
    print ("That's all done, go grab a beer!")
    input("press enter to quit")

def convert_to_flac(filename):
    #adding quotes around the filename so it is sent to the command line with quotes around it
    filename = "\"" + filename + "\""
    os.system("start /wait cmd /c ffmpeg -i {} audio.flac".format(filename))

def Upload_to_GCS():
    # upload resultant file to GCS
    file_path = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(file_path, "audio.flac")
    filename = "\"" + filename + "\""
    os.system("start /wait cmd /c gsutil cp {} gs://audioprocess/".format(filename))

def transcribe_gcs(gcs_uri):
    """Asynchronously transcribes the audio file specified by the gcs_uri."""
    from google.cloud import speech
    speech_client = speech.Client()

    audio_sample = speech_client.sample(
        content=None,
        source_uri=gcs_uri,
        encoding='FLAC')

    operation = audio_sample.long_running_recognize('en-GB')

    retry_count = 100
    while retry_count > 0 and not operation.complete:
        retry_count -= 1
        time.sleep(2)
        operation.poll()

    if not operation.complete:
        print('Operation not complete and retry limit reached.')
        return

    alternatives = operation.results
    text_output = ""
    confidence_total = 0
    confidence_counter = 0
    for alternative in alternatives:
        print('Transcript: {}'.format(alternative.transcript))
        text_output += alternative.transcript
        print('Confidence: {}'.format(alternative.confidence))
        confidence_total += alternative.confidence
        confidence_counter += 1
    confidence_total = confidence_total / confidence_counter
    return text_output,confidence_total;
    # [END send_request_gcs]


def sentiment_analysis(output_text):
    """Run a sentiment analysis request on text within a passed filename."""
    from google.cloud import language
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

def append_text_to_file(output_text, mood):
    #with open automatically closes file after you leave the code block
    with open(r"C:\Users\craig\Google Drive\CaptainsLog\Captains_log.txt", 'a') as Captains_Log:
        the_date = datetime.datetime.now()
        the_date = the_date.strftime("%d %b %Y")
        Captains_Log.write("\n\n\n")
        Captains_Log.write("Date: {},   Mood: {} \n".format(the_date, mood))
        Captains_Log.write(output_text)

def delete_GCS():
    #delete audio.flac from GCS
    os.system("start /wait cmd /c gsutil rm gs://audioprocess/audio.flac")

def delete_FLAC():
    #delete audio.flac from GCS
    os.remove("audio.flac")

def move_to_processed(file_path):
    destination = "C:/Users/craig/Google Drive/CaptainsLog/Processed"
    shutil.move(file_path, destination)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'path', help='File or GCS path for audio file to be recognized')
    args = parser.parse_args()
    transcribe_file(args.path)
