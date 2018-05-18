NOTE: this is a work in progress and is by no means perfect (yet, at least).

This is a project I started that uses a small corpus of text to generate some commonly occurring two-word phrases in the English language.

Considering that the corpus of text I'm using is currently quite small, it is definitely not a complete list of commonly occurring phrases, but if you examine the output, some interesting results are seen such as ['goodness', 'oh'], ['carrying', 'guns'], etc.

The output is in the form of a list of lists, and each sublist contains the words of the two-word phrase. The output is ordered such that the words that are more likely to be common phrases appear first.

For now I am only using the "spoken" data, I'll try including the "written" data later and the results will probably be a lot more interesting.

To run the program, run the common_phrases.py file. Note that it may take a few seconds for the output to show up.

The code is really messy right now but I'll clean it sometime.



