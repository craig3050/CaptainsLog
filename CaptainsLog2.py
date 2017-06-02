import argparse
import io
import time
import os
import sys


def transcribe_file(speech_file):
    #convert to flac and rename file to audio.flac
    done

    #upload file to GCS for processing
    done

    #send GCS link of file to google speech for processing
    text_returned = transcribe_gcs("gs://audioprocess/audio.flac")
    print ("This is the output from ##date##\n\n")
    print ("Confidence = {[1]}\n".format(text_returned))
    print ("Transcription = {[0]}\n\n\n".format(text_returned))

    # send text result for sentiment analysis
    done

    #open main diary text file
    #append text to file
    #append date and time to file, and the sentiment of the text
    #close file
    done



    #delete audio from gcs


    #delete .flac file from local


    #move processed file to 'processed' directory


    #print a message saying it's all done successfully

    #
    # """Transcribe the given audio file asynchronously."""
    # from google.cloud import speech
    # speech_client = speech.Client()
    #
    # with io.open(speech_file, 'rb') as audio_file:
    #     content = audio_file.read()
    #     audio_sample = speech_client.sample(
    #         content,
    #         source_uri=None,
    #         encoding='FLAC')
    #
    # operation = audio_sample.long_running_recognize('en-GB')
    #
    # retry_count = 100
    # while retry_count > 0 and not operation.complete:
    #     retry_count -= 1
    #     time.sleep(2)
    #     operation.poll()
    #
    # if not operation.complete:
    #     print('Operation not complete and retry limit reached.')
    #     return
    #
    # alternatives = operation.results
    # text_output = ""
    # for alternative in alternatives:
    #     print('Transcript: {}'.format(alternative.transcript))
    #     text_output += alternative.transcript
    #     print('Confidence: {}'.format(alternative.confidence))
    #
    # return (text_output)
    # [END send_request]


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



if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'path', help='File or GCS path for audio file to be recognized')
    args = parser.parse_args()
    if args.path.startswith('gs://'):
        transcribe_gcs(args.path)
    else:
        transcribe_file(args.path)