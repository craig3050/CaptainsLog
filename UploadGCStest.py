import os

def Upload_to_GCS():
    # upload resultant file to GCS
    file_path = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(file_path, "audio.flac")
    filename = "\"" + filename + "\""
    os.system("start /wait cmd /c gsutil cp {} gs://audioprocess/".format(filename))

if __name__ == '__main__':
    Upload_to_GCS()