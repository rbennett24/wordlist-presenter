# wordlist-presenter
A simple Python script which presents experimental stimuli on a screen using EasyGUI

This script assumes that there's an input CSV file with two columns. I use it to present bilingual stimuli, so one column is the target language (e.g. Kaqchikel) and the other a translation (e.g. Spanish).

Item presentation is self-paced: participants use the spacebar (or right arrow) to advance. To go back, use the left arrow.

The script will present the same word list some fixed number of times (the "blocks"). Each block presents the items in randomized order. For each participant, the script will save a .txt file recording the order of items in each block. This will include all and any items that have been repeated within a block by pressing the left arrow.

Participants are given a break at the end of each block, and a message when all blocks are complete. Use ESC to exit once all blocks are complete.
