from note_handler import *

"""
    This file does three things:
        (1) it combs through a file ("FN.xml") for us and makes a list of every note
        it finds. It writes this list to a JSON file, along with a renumbered list
        from 1 to n.
        (2) It then uses that JSON file to remap note numbers in any files we
        specify ("NO.xml", "PP.xml", "SS.xml", "FN.xml" for us).
        (3) It then checks how well this has worked by remaking another list of notes
        from the newly-edited original file ("FN.xml" for us) and comparing them with
        a list numbered from 1 to n. Any discrepancies are highlighted to the user in 
        the terminal.
        
    To accomplish this we use custom NoteMapper and NoteHandler objects, held in
    note_handler.py and imported here at the top of the file.
"""
# we get a new NoteMapper object, point it at our file containing notes and give it
# a regex pattern to match. A full description of the regex pattern is found in
# regex.txt
note_file = NoteMapper("FN.xml", r'<p xml:id="(note-[0-9.]*)">')

note_file.map_note_numbers()
note_file.write_to_file("data.json")



# Part (2) begins
with open('data.json') as json_file:
    # dictionary like: notes = {"note-25": "note-1", "note-27.3": "note-2"}
    notes = json.load(json_file)

xml_files = ["NO.xml", "SS.xml", "PP.xml", "FN.xml"]

for xml_file in xml_files:
    xml_file = NoteHandler(xml_file)
    xml_file.read_file()
    
    for key, value in notes.items():
        # a simple string find and replace works in all files bar FN.xml
        if "FN" not in xml_file.file_name:
            # perform find and replace on note locations
            current_string = 'FN.html#' + key + '"/>'
            new_string = 'FN.html#' + value + '"/>'
            xml_file.find_and_replace(current_string, new_string)
    
        else:
            # perform find and replace on note locations in FN.xml           
            # these strings (see regex.txt for explanations of the patterns)
            # renumber the notes and the text data in the body:
            # they make
            #   <p xml:id="note-345.6.3">345.6.4 blah blah</p>
            # into
            #   <p xml:id="note-22">22. Blah blah</p>
            # doing this means there's no need to handle them in the XSL files
            # though I've left a commented out line in FN.xsl that can be 
            # used is needed. In that case, you'd comment out the two lines
            # immediately below and uncomment the two below that. Those lines
            # make: 
            #   <p xml:id="note-345.6.3">345.6.4 blah blah</p>
            # into
            #   <p xml:id="note-22">Blah blah</p>
            current_string = r'<p xml:id="' + key + '"> ?' + key[5:] + '\.? {1,2}'
            new_string = r'<p xml:id="' + value + '">' + value[5:] + '. '
            # current_string = r'<p xml:id="' + key + '"> ?' + key[5:] + '\.? {1,2}'
            # new_string = r'<p xml:id="' + value + '">'
            
            xml_file.find_and_replace(current_string, new_string, True)
            
            # perform find and replace on asset targets for images
            current_string = r'(assets\/)([a-zA-Z]{1,2}-[0-9]{1,3}.png)'
            new_string = r'image.html?asset=\2'
            xml_file.find_and_replace(current_string, new_string, True)

    xml_file.write_to_file()


# using same object from above, but regenerating dictionary on newly-renumbered notes
# dictionary like: notes = {"note-1": "note-1", "note-2": "note-2"}
note_file.map_note_numbers()
note_file.write_to_file("data.json")

notes_to_check = 0
redone_notes = note_file.read_file("data.json")
for key, value in redone_notes.items():
    if key != value:
        notes_to_check += 1
        print("Look in '" + note_file.file_name + "' for the old note string '" + key \
            + "' or for the new note string '" + value + "' because something's not quite right.")

if notes_to_check == 0:
    print("All done -- you're notes have been renumbered and the files are ready to use")