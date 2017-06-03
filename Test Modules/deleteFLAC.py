import os

def delete_FLAC():
    #delete audio.flac from GCS
    os.remove("audio.flac")

if __name__ == '__main__':
    delete_FLAC()