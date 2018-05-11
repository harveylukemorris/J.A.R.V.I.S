Installation Steps:

1.  Run:
        - pip install evernote==1.23.2
        - pip install hashlib
        - python -c 'from evernote.api.client import EvernoteClient'
        
    If the last line runs and quietly exits, you’re ready to go.
        
2.  Go to https://www.evernote.com/api/DeveloperToken.action and get your developer token. (one year access)

3.  Add the Developer Token to your profile.yml in jasper/client
        EVERNOTE_TOKEN: <your developer token>
        
4.  In raspberry pi home directory run
        - git clone https://github.com/JasonTwente/Jasper-Evernote

5.  Copy the Evernote.py from Jasper-Evernote to jasper/client/modules

6.  add to __init__.py
        from modules import Evernote
        
7. The installation is complete! Now you are able to let Jasper take notes for you.

Example:
JASPER:  How can I be of service?
YOU:     Note
JASPER:  What would you like me to write down?
YOU:     Don't forget to bring potatoes tomorrow!
JASPER:  I succesfully wrote down your note.











import hashlib
import binascii
import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as Types

from evernote.api.client import EvernoteClient

import sys
import time
import re

# Written by Jason van Eunen - jasonvaneunen.com


WORDS = ["NOTE"]

PRIORITY = 1


def handle(text, mic, profile):

        auth_token = profile["EVERNOTE_TOKEN"]

        client = EvernoteClient(token=auth_token, sandbox=False)
        user_store = client.get_user_store()
        note_store = client.get_note_store()

        if bool(re.search(r'\Note\b', text, re.IGNORECASE)):
                writeNote(text, mic, note_store)

def writeNote(text, mic, note_store):
        note = Types.Note()						# Creates a new note
        note.title = "Jasper Note"

        mic.say("What would you like me to write down?")
        theNote = mic.activeListen()					# Listens to the input and stores it

        note.content = '<?xml version="1.0" encoding="UTF-8"?>'
        note.content += '<!DOCTYPE en-note SYSTEM ' \
    '"http://xml.evernote.com/pub/enml2.dtd">'
        note.content += '<en-note>Note:<br/>'
        note.content += ('%s' % theNote)
        note.content += '</en-note>'

        created_note = note_store.createNote(note)			# Stores the new note in Evernote
        mic.say("I successfully wrote down your note.")

def isValid(text):
        return bool(re.search(r'\Note\b', text, re.IGNORECASE))
