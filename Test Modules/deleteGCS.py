import os

def delete_GCS():
    #delete audio.flac from GCS
    os.system("start /wait cmd /c gsutil rm gs://audioprocess/audio.flac")

if __name__ == '__main__':
    delete_GCS()