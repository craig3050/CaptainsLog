import datetime



def append_text_to_file(output_text, mood):
    #with open automatically closes file after you leave the code block
    with open(r"C:\Users\craig\Google Drive\CaptainsLog\Captains_log.txt", 'a') as Captains_Log:
        the_date = datetime.datetime.now()
        the_date = the_date.strftime("%d %b %Y")
        Captains_Log.write("\n\n\n")
        Captains_Log.write("Date: {},   Mood: {} \n".format(the_date, mood))
        Captains_Log.write(output_text)


if __name__ == '__main__':
    mood = "Positive"
    output_text = """
    This is a big long text document.
    It is a really nice document
    Possibly the best ever
    Fake News
    """
    append_text_to_file(output_text,mood)