import re;
import urllib.request;

def LoadTitles():
    urls = [];

    file = open("main_site.html", 'r');
    lines = file.readlines();
    file.close();

    for line in lines:
        if("<br><a href=" in line):
            line_split = line.split('"');
            urls.append(line_split[1][:-11]);
    
    return urls;

def LoadTitle(ext):
    file = urllib.request.urlopen("http://shakespeare.mit.edu/" + ext + "/index.html")
    lines = file.read().decode("utf8").split("\n");
    file.close();

    for line in lines:
        if "<title>" in line:
            return line[8:-16];
    
    return "";

def LoadText(ext):
    file = urllib.request.urlopen("http://shakespeare.mit.edu/" + ext + "/full.html")
    lines = file.read().decode("utf8").split("\n");
    file.close();

    lines_processed = [];

    for line in lines:
        line_split = re.split("<A NAME=|<title>|</title>|<tr>|</tr>|<h3>|</h3>|<H3>|</H3>|<p>|</p>|<i>|</i>|<b>|</b>|<a>|</a>|<A>|</A>|<br>|</br>|<blockquote>|</blockquote>|\n|>|''", line);
        while('' in line_split):
            line_split.remove('');
        while(' ' in line_split):
            line_split.remove(' ');
        if(len(line_split) == 2):
            lines_processed.append(line_split);

    while(lines_processed[0][0] != "speech1"):
        lines_processed.pop(0);

    lines_out = open("lines.txt", "w");
    characters_out = open("characters.txt", "w");

    current_char = "";
    for line in lines_processed:
        if("speech" in line[0]):
            current_char = line[1];
        else:
            lines_out.write(line[1] + "\n");
            characters_out.write(current_char + "\n");

    lines_out.close();
    characters_out.close();

