import re;
from flask import Flask, request, render_template, redirect;
from write import GetCharacters, FinishQuote;
from shakespeare_splitter import LoadTitle, LoadText, LoadTitles;

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
@app.route('/<url>/', methods=['GET', 'POST'])
@app.route('/<url>/<chr>/', methods=['GET', 'POST'])
def website(url="tempest", chr="NONE"):

    # Load the titles from the main website
    urls = LoadTitles();
    titles_from_url = [LoadTitle(urls[i]) for i in range(0, len(urls))];  

    if request.method == 'GET':
        return render_template('shakespeare.html', val="INPUT STARTING TEXT", character_list=GetCharacters(), tit=LoadTitle(url), chr=chr.upper(), urls=titles_from_url);

    # Load the text from the url
    LoadText(url);  
    text = request.form.get('text_inp');

    # Load the information from the form
    try:
        word_length = int(request.form.get('length_inp'));
    except ValueError:
        word_length = 10;
    new_play = request.form.get('play');
    new_url = urls[titles_from_url.index(new_play)];
    new_chr = request.form.get('character');

    # Check if the extension has changed
    if(not url.lower() == new_url.lower() or not chr.lower() == new_chr.lower()):
        return redirect("/" + new_url.lower() + "/" + new_chr.lower() + "/", code=307);

    # Finish the quote
    inp_arr = [re.sub(r'[^\w\s]', '', word).upper() for word in text.split()];
    if(chr == "NONE"):
        finished_arr = FinishQuote(inp_arr, word_length, None);
    else:
        finished_arr = FinishQuote(inp_arr, word_length, chr.upper());
    to_text = "";
    for word in finished_arr:
        to_text += word + " ";

    return render_template('shakespeare.html', val=to_text, character_list=GetCharacters(), tit=LoadTitle(url), chr=chr.upper(), urls=titles_from_url);