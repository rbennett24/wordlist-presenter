from tkinter import * # Python GUI
from easygui import * # For input
import pandas as pd # For dataframes and the like
import random # For random shuffling
import os # For file management

# Initiate GUI
root = Tk()


# Get input from user (easygui)
spk = integerbox(msg="Speaker code: ",title="",root=root)
blocks = integerbox(msg="Number of blocks: ",title="",default="5",root=root)
lng = enterbox(msg="Language: ",title="",default="Kaq",root=root)


# Read in .csv file as Panda dataframe
df = pd.read_csv(('%s.csv') % (lng),index_col=0, squeeze=True, header=None)
dfDict = df.to_dict() # convert dataframe to dictionary
keys = list(dfDict.keys()) # Get list of (Spanish) key words in dictionary
numit = len(keys) # Total # of items in list

# Set textfile for keeping track of presentations
txtFile = ("EGG_%s_spk_%s.txt") % (lng,spk)

# Ask for permission to delete file if it exists using easygui
if os.path.exists(txtFile):
    delfile = ccbox(msg="Warning: file already exists! Do you want to continue, and delete the existing file? ",title="WARNING")
    if delfile == True:
        os.remove(txtFile) # Delete the preexisting file
    else:
        root.destroy() # Close GUI
        sys.exit() # Kill the script


spkFile = open(txtFile,"a") #append mode 
spkFile.write(lng+"\tSpanish\tBlock\n")

# Start counter for iterating through items in the list.
counter = 0

# Set counter for blocks
currentBlock = 1



################
# Functions for cycling through words in the list.

# Create a function controlling how words are presented
# (here, both Spanish and Mayan presented simultaneously on different parts of the screen)
def displayWord():
    global spantext,mayatext
    span = keys[counter]
    maya = dfDict[span]
    spantext = Label(root, text=span)
    mayatext = Label(root, text=maya)

    # Control fontstyles
    # http://www.java2s.com/Tutorial/Python/0360__Tkinker/ConfigLabelforitsbackgroundfontandsize.htm
    spantext.config(font=('times', 64, 'bold'))
    spantext.config(height=6, width=20)
    mayatext.config(font=('times', 48, 'italic'))
    mayatext.config(height=0, width=20)

    spantext.pack(expand=YES, fill=BOTH)
    mayatext.pack(expand=YES, fill=BOTH)

    # Write down which item was being presented.
    spkFile.write(maya+"\t"+span+"\t"+str(currentBlock)+"\n")


# Set function for moving foward in the list
def moveBack(event):
    global counter,spantext,mayatext

    # Can't go past first item in the list
    if counter == 0:
        pass # Do nothing

    else:
        # Destroy frame/text contents
        mayatext.destroy()
        spantext.destroy()
        
        # Display previous word
        counter -= 1
        displayWord()

        #print("Going back!")
        #print(counter)


# Set function for moving backward in the list
def moveUp(event):
    global counter,spantext,mayatextm,currentBlock

    # Destroy frame/text contents
    spantext.destroy()
    mayatext.destroy()

    # Can't go past last item in the list
    if counter == numit-1:
        # Increment block counter
        currentBlock +=1

        # End item presentation if last block finished
        if currentBlock > blocks:

            # Display text indicating that we've finished
            spantext = Label(root, text='Xk\'is, matyox chawe\'.')
            spantext.config(font=('times', 84, 'bold'))
            spantext.pack(expand=YES, fill=BOTH)


            # Close file keeping track of order of presentation of items.
            spkFile.close()

            
            # Rebind keyboard keys so that only escape works, and it quits program
            # https://www.tcl.tk/man/tcl8.4/TkCmd/keysyms.htm
            root.bind('<Left>',dummyfnc)
            root.bind('<Right>',dummyfnc)
            root.bind('<space>',dummyfnc)
            root.bind('<Escape>',exitEvent)


        else:
            # Display text indicating that it's time for a break
            spantext = Label(root, text='Uxlanem!')
            spantext.config(font=('times', 84, 'bold'))
            spantext.pack(expand=YES, fill=BOTH)

            # Reset counter
            counter = -1

            # Re-randomize stimulus list
            random.shuffle(keys)

    else:
        # Display next word
        counter += 1
        displayWord()

        #print("Advancing!")
        #print(counter)

def dummyfnc(event):
    pass # Do nothing

def exitEvent(event):
    root.destroy()

    
# Assign keys for moving forward/backward in the wordlist
# (i.e. bind keys to functions)
root.bind('<Left>', moveBack)
root.bind('<Right>', moveUp)
root.bind('<space>', moveUp)

# Randomize the order of presentation of items in the first block.
random.shuffle(keys)

# Start up the GUI with the first item
root.state('zoomed') # https://stackoverflow.com/questions/7966119/display-fullscreen-mode-on-tkinter
displayWord()
root.mainloop()
