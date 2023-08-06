########
# Info #
########
# This is now the Python Library CoderElijah. To install, type "pip install coderelijah" into shell.

#################
# Basic Imports #
#################
from time import sleep # Several of my functions require a delay

####################
# ANSI Color Codes #
####################
class ansi:
  '''Color choices are:
  `cyan`
  `red`
  `yellow`
  `green`
  `blue`
  `purple`
  `white`
  There is also `burntYellow`, but there is no difference on Replit.'''
  cyan = '\033[36m'
  red = "\033[31m"
  burntYellow = "\033[33m"
  yellow = "\033[93m"
  green = "\033[32m"
  blue = "\033[34m"
  purple = "\033[35m"
  white = "\033[37m"


###########################
# Create a clear function #
###########################
# Thanks to @bigminiboss on Replit.com for this clear command.
# To use, type "clear()"
clear = lambda: print("\033c", end="", flush=True)


###################
# Timeout Command #
###################
def timeout(timeDuration: int, function):
  """Usage:
  `timeDuration`: Enter the time in seconds for this command to run
  `function`: Enter the name of the function you wish to use (no quotes!)
  This function displays a countdown timer. The function you use should print something and nothing more."""
  x = int(timeDuration)
  while x >= 0:
    clear()
    function()
    print("\nThis message will display for " + str(x) + " seconds.")
    x = x - 1
    sleep(1)


############
# Rickroll #
############
# This can display a text file line by line. Or, it can display lorem ipsum text. It can display either the full version of "Never Gonna Give You Up", or just the chorus. To use the full version, set the filename to "full". For the chorus (short version), use "short". Or, for lerem ipsum, use "lorem".
# timePerLine is how long each line is displayed, and infinity is whether or not the function loops (thus making it infinite).
def rick_roll(fileName: str='short', timePerLine: int=2, infinity: bool=True):
  '''This function can do way more than Rick Roll people
  `fileName`: The name of the text file to read. You may leave blank to get the chorus of "Never Gonna Give You Up", "full" for the full version, or "lorem" for lorem ipsum text.
  `timePerLine`: Delay (in seconds) after each line appears before the next line appears (default: 2)
  `infinity`:This determines whether or not the function loops forever and ever (default: `True`)'''
  if fileName not in ('short', 'full', 'lorem'):
    rick = open(fileName)
    contents = rick.readlines()
  elif fileName == 'short':
    from .rickPy import rickRoll_short
    contents = rickRoll_short
  elif fileName == 'full':
    from .rickPy import rickRoll_full
    contents = rickRoll_full
  elif fileName == 'lorem':
    from .rickPy import lorem
    contents = lorem

  def main():
    clear()
    for fun in contents:
      print(fun.strip("\n")) # When reading text files in Python, it adds a new line to every line, the stip() command allows me to make it single-spaced rather than double-spaced
      if fun not in ('\n', ''): # Only delay the next line if the line is not blank
        sleep(timePerLine)


  main()
  while infinity == True:
    main()


##############################
# Timed Display of Text File #
##############################
# This is a modified rickRoll()
def timed_show(contents: list='help', timeToShow: int=10):
  '''Parameters:
  `contents`: The string you wish to display (leave blank for "HELP ME" in ASCII)
  `timeToShow`: How long to display the message in seconds (default: 10)
  This function displays a text file with a countdown timer'''
  if contents == 'help':
    from .rickPy import helpMe
    contents = helpMe
  def main():
    for fun in contents:
        print(fun.strip("\n"))
  timeout(timeToShow, main)


###########################################
# Display Text File (for titles and such) #
###########################################
# This is a modified rickRoll()
def read_lines(fileName: str, startLine: int="", endLine: int=""):
  '''Returns lines x-y of a text file (advanced `readlines` function)
  `fileName`: The name of the file
  `startLine`: The starting line number of your text
  `endLine`: The ending line number of your text
  Note that if `startLine` and `endLine` are left blank, it shows the whole text file. Also note that you may put in the real line numbers as this function automatically accounts for Python's count starting at 0, e.g., to access line 1, type 1 not 0.'''
  rick = open(fileName)
  contents = rick.readlines()
  if startLine == "":
    startLine = 0
  else:
    startLine = int(startLine) - 1
  if endLine == "":
    endLine = len(contents)
  else:
    endLine = int(endLine)
  if startLine == 0 and endLine == 0:
    all_lines = 1
  else:
    all_lines = endLine - startLine
  file_contents = ""
  x = startLine
  for fun in range(all_lines):
    file_contents += contents[x]
    #print(contents[x].strip("\n"))
    x = x + 1
  return file_contents

############################
# User Input Error Catcher #
############################
def get_input(prompt: str, options: list, inputLine: str = '=> ', error: str = 'Invalid Input', clearScreen: bool = True):
  """`prompt`: The question the user is asked.
  `options`: The options available to the user (must be in the form of a list)
  `inputLine`: The text displayed on the line that the user types in their input. If you want it to be blank, set it to '' or "".
  `error`: The message displayed when the user's input is invalid.
  `clearScreen`: Whether the screen is cleared upon invalid input being entered or not.
  Adapted from @InvisibleOne's post here:
  https://ask.replit.com/t/how-to-validate-user-input-properly/9586/2?
  Thanks also to @QwertyQwerty54 for the help with the docstrings.
  """
  while True: # This runs until it is ended
    print(prompt) # Display the prompt
    for option in options: # Goes through the whole list of options
      print(f"{options.index(option)+1} {option}") # Displays the option number and text
      
    userInput = input(inputLine) # Gets user input, dipslaying the text from "inputLine"
    
    try: # This stops the code from crashing when it gets errors
      userInput = int(userInput) # Convert user's input into a number
      
      if options[userInput-1]: # This returns the value of the number the user inputted as their answer. The text is not actually used and Python just uses the numbers
        return userInput-1
    except: # If anything went awry (such as the user putting in text)
      if clearScreen == True: # User must set it to clear manually from the function options
        clear() # Clear screen
    else:
      print() # Displays blank line
      pass # Keep going
    
    print(error) # Display error message
##################################
# Using Text Files for Variables #
##################################
def add_storage(fileName: str, store, append: bool=True):
  '''Store variable in text file
  `fileName`: Name of file to write to
  `store`: Data to store in file
  `append`: Whether it erases the file or appends it (default: `True`). It is not generally recommended to change this default.'''
  if append in ('append', 'a', 'add'):
    file = open(str(fileName), 'a')
  else:
    file = open(str(fileName), 'w')
  file.write(f"{store}\n")
  file.close()
def access_storage(fileName: str, lineNum: int=1):
  '''Access data from text file as variable
  `fileName`: Name of the text file containing the data
  `lineNum`: The line number the data is on (default: 1)
  This function returns the data as a string. You can assign it to a variable like so:
  `myVar = accessStorage("file.txt", 2)`'''
  lineNum = int(lineNum) - 1
  file = open(str(fileName))
  contents = file.readlines()
  return contents[lineNum].strip('\n')
  contents.close()
######################
# Auto Docs Creation #
######################
def auto_docs(py_file, output_file:str='CoderElijah'):
  '''This function creates an MD file with documentation on a Python Library from the docstrings. DO NOT INCLUDE THE FILE NAME EXTENSIONS!
  `py_file`: The name of the Py file you wish to create documentation for. Use `CoderElijah` to get docs on the CoderElijah library.
  `output_file`: The name of your file. If left blank, it will create `CoderElijah.md`.'''
  md = ""
  for i in dir(py_file):
      if (not i.startswith("__") and not i.endswith("__")):
          doc_string = getattr(py_file, i).__doc__
          try:
            doc_string = doc_string.split('\n')
            docs = ""
            for line in doc_string:
              docs += line + "\n\n"
            md += f'''<details><summary> The <code>{i}</code> function</summary>
  
  {docs}</details>'''
          except:
            pass
  with open(f'{output_file}.md', 'w') as file:
    file.write(md)
###############
# ASCII Movie #
###############
# I now know that this can be simplfied. However, due to lack of demand and its complexity and the fact that I don't want to break it, it will not be updated at this time.
# This was created in order to display the Star Wars ASCII movie using Python.
# However, it can be used with any ASCII movie that meets the following parameters:
# (1) The ASCII movie must be in a text file
# (2) The first line of the text file must contain a number indicating the number of times each frame should be shown
# (3) After that, there must be a "frame" consisting of 13 lines of text, or you can specify the number of lines of text in the function
# (4) Repeat steps 2 and 3 indefinitely; the program will work just fine no matter how many frames there are. There must be at least 3 and the last frame must have 0 as the number of frames for the program to work properly.
# Syntax: from E import movie
# Syntax: movie("text file", "font color", #)
# Syntax: # represents any number you wish; it is the number of lines per frame. Default is 13. Default text color is white. There is not default text file, so you must specify that.
def movie(textFile, fontColor="white", lines=13):
  '''I now know that this can be simplfied. However, due to lack of demand and its complexity and the fact that I don't want to break it, it will not be updated at this time.
This was created in order to display the Star Wars ASCII movie using Python.
However, it can be used with any ASCII movie that meets the following parameters:
(1) The ASCII movie must be in a text file
(2) The first line of the text file must contain a number indicating the number of times each frame should be shown
(3) After that, there must be a "frame" consisting of 13 lines of text, or you can specify the number of lines of text in the function
(4) Repeat steps 2 and 3 indefinitely; the program will work just fine no matter how many frames there are. There must be at least 3 and the last frame must have 0 as the number of frames for the program to work properly.
Syntax: from E import movie
Syntax: movie("text file", "font color", #)
Syntax: # represents any number you wish; it is the number of lines per frame. Default is 13. Default text color is white. There is not default text file, so you must specify that.'''
  ##############
  # Font Color #
  ##############
  if fontColor == "red":
    color = ansi.red
  elif fontColor == "burntYellow":  # No orange, but true ANSI yellow is really weird
    color = ansi.burntYellow
    # In Replit the two yellows are the same, but not when running this from a computer
  elif fontColor == "yellow":  # Technically bright yellow, I like it better
    color = ansi.yellow
  elif fontColor == "green":
    color = ansi.green
  elif fontColor == "blue":
    color = ansi.blue
  elif fontColor == "purple":  # Technically magenta
    color = ansi.purple
  else:  # If parameters are not met, font is white
    color = ansi.white
  #####################
  # Movie Source File #
  #####################
  file = open(textFile)
  #############
  # Read File #
  #############
  content = file.readlines()
  #######################
  # Configure Variables #
  #######################
  lineWithInt = lines + 1  # This is the number of lines per frame, INCLUDING the data line (how many times to show each line)
  x = 1  # "x" is the line that the program is displaying
  delayNum = 0  # The first line of the text file is line 0 (it's a Python thing), and we need that line number
  delayFrame = int(
    content[delayNum].strip()
  )  # Get the contents of the above line number and remove the weird double-spacing that Python does when reading text files
  ##############
  # Show Movie #
  ##############
  for fun in range(len(content)):  # This "for" loop plays the movie
    for movie in range(
        delayFrame
    ):  # This "for" loop plays each frame as many times as the text file indicates
      clear()  # Always start each frame with a blank canvas
      y = x  # "y" is the first line of each frame
      for frame in range(lines):  # This "for" loop creates each frame
        print(color + str(content[y]).strip("\n"))  # Print first line of frame
        y = y + 1  # This causes the loop to move on to the next line of the frame
      print(
      )  # Optional blank line at the bottom of each frame so the blinking cursor doesn't detract from the experience. Comment this line to remove it.
      sleep(
        0.067
      )  # After each complete frame is displayed, there is a 0.067 second pause. Otherwise, Python would show the movie as fast as it can, which is unbearably fast. I had it at 0.1 seconds, but discovered on the website that first made the animation that it should be 15 frames per second. 1/15 seconds is 0.067. So, I updated it.
    x = x + 14  # There are a total of 14 lines per frame: 1 of data (delayFrame) and 13 lines of image
    if delayNum < len(
        content
    ) - lineWithInt:  # This "if" statement stops the program from printing lines that come after the end of the text file (which don't exist), and end the program when it is supposed to end instead
      delayNum = delayNum + lineWithInt
      delayFrame = int(content[delayNum].strip())

