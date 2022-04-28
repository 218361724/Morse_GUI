# Morse GUI

# Implements an interface to output any text in Morse code. Integrates with RPi to
# faciliate signalling by switching an LED on/off.

# Reference used for translation: https://morsecode.world/international/morse2.html

from operator import sub
import RPi.GPIO as GPIO
import tkinter as tk

rootWindow = tk.Tk()

# Setup led pin
ledPin = 7
GPIO.setmode(GPIO.BOARD)
GPIO.setup(ledPin, GPIO.OUT)

# -- Morse signalling helpers
dotLengthMs = 500
dashLengthMs = dotLengthMs * 3
wordGapLengthMs = dotLengthMs * 7
letterGapLengthMs = dotLengthMs * 3
subLetterGapLengthMs = dotLengthMs
letterToMorse = {
    "a": ("dot", "dash"),
    "b": ("dash", "dot", "dot", "dot"),
    "c": ("dash", "dot", "dash", "dot"),
    "d": ("dash", "dot", "dot"),
    "e": ("dot",),
    "f": ("dot", "dot", "dash", "dot"),
    "g": ("dash", "dash", "dot"),
    "h": ("dot", "dot", "dot", "dot"),
    "i": ("dot", "dot"),
    "j": ("dot", "dash", "dash", "dash"),
    "k": ("dash", "dot", "dash"),
    "l": ("dot", "dash", "dot", "dot"),
    "m": ("dash", "dash"),
    "n": ("dash", "dot"),
    "o": ("dash", "dash", "dash"),
    "p": ("dot", "dash", "dash", "dot"),
    "q": ("dash", "dash", "dot", "dash"),
    "r": ("dot", "dash", "dot"),
    "s": ("dot", "dot", "dot"),
    "t": ("dash",),
    "u": ("dot", "dot", "dash"),
    "v": ("dot", "dot", "dot", "dash"),
    "w": ("dot", "dash", "dash"),
    "x": ("dash", "dot", "dot", "dash"),
    "y": ("dash", "dot", "dash", "dash"),
    "z": ("dash", "dash", "dot", "dot"),
}
# Sub letter
def signalSubLetter(type, isFinal = False):
    # Switch LED on for dot / dash length
    GPIO.output(ledPin, GPIO.HIGH)
    rootWindow.after(
        dotLengthMs if type == "dot" else dashLengthMs
    )
    # Switch LED off for letter / sub-letter gap length
    GPIO.output(ledPin, GPIO.LOW)
    rootWindow.after(
        letterGapLengthMs if isFinal else subLetterGapLengthMs
    )
# Letter
def signalLetter(letter):
    morseLetter = letterToMorse[letter]
    for subLetterType in morseLetter:
        isFinal = subLetterType == morseLetter[-1]
        print(f"signal: {subLetterType}")
        signalSubLetter(subLetterType, isFinal)
        print("end of letter")

# Handle submitted word
def onSubmit():
    currentText = textBox.get("1.0", "end-1c")
    letterCount = 0
    for letter in currentText:
        # Strip capitalisation
        formattedLetter = letter.lower()
        # Skip if still not valid letter (a-z)
        if formattedLetter not in letterToMorse:
            continue
        # Stop processing text at 12 characters
        letterCount += 1
        if letterCount == 12:
            break
        # Attempt to signal letter
        print(f"start letter: {formattedLetter}")
        signalLetter(formattedLetter)

# -- Configure UI widgets
# Window title
titleLabel = tk.Label(
    rootWindow,
    text = "Signal word in Morse with LED",
    font = ("Arial", 16),
    pady = 15
)
titleLabel.pack(fill = tk.X)
# Text box
textBox = tk.Text(
    rootWindow,
    padx = 30,
    pady = 10,
    height = 1
)
textBox.pack(
    fill = tk.BOTH,
    expand = True,
)
# Help message label
helpMsgLabel = tk.Label(
    rootWindow,
    text = "Enter a word. Stops at 12 characters. Non-letters (e.g digit, punctuation) will be ignored.",
    pady = 10
)
helpMsgLabel.pack(fill = tk.X)
# Submit button
submitBtn = tk.Button(
    rootWindow,
    text = "Submit",
    pady = 5,
    command = onSubmit
)
submitBtn.pack(pady = 15)

# Configure window exit action
def onExit():
    GPIO.cleanup()
    rootWindow.destroy()
rootWindow.protocol("WM_DELETE_WINDOW", onExit)

# Render UI
rootWindow.mainloop()
