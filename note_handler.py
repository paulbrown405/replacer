import json
import re

class NoteHandler:
    """
    Class that handles reading, writing, and manipulating notes in a file.

    Attributes:
        file_name (str): Name of the file to be processed.
        file_contents (str): Contents of the file after reading.

    Methods:
        __init__(self, file: str) -> None:
            Constructor that initializes the NoteHandler object with a file name.
        read_file(self, file_name: str|None = None, open_method: str = "r") -> str:
            Reads the contents of the file and returns them as a string.
        update_file_name(self, new_file_name: str) -> str:
            Updates the file name associated with the NoteHandler object.
        write_to_file(self, file_name: str|None = None, write_method: str = "w") -> None:
            Writes the contents of the NoteHandler object to a file.
        list_regex_matches(self, pattern: str) -> list:
            Returns a list of all matches of a regular expression pattern in the file contents.
        find_and_replace(self, current: str, new: str, use_regex = False) -> str:
            Finds and replaces a substring or a regular expression pattern in the file contents.
    """

    def __init__(self, file: str) -> None:
        """
        Constructor that initializes the NoteHandler object with a file name.

        Args:
            file (str): Name of the file to be processed.

        """
        self.file_name = file

    def read_file(self, file_name: str|None = None, open_method: str="r") -> str:
        """
        Reads the contents of the file and returns them as a string.

        Args:
            file_name (str|None, optional): Name of the file to be read. If None, the default file name associated
                with the NoteHandler object is used. Defaults to None.
            open_method (str, optional): File open mode. Defaults to "r".

        Returns:
            str: Contents of the file as a string.

        """
        file_name = file_name if file_name is not None else self.file_name
        with open(file_name, open_method) as file:
            if "json" not in file_name:
                self.file_contents = file.read()
            else:
                self.file_contents = json.load(file)

        return self.file_contents

    def update_file_name(self, new_file_name: str) -> str:
        """
        Updates the file name associated with the NoteHandler object.

        Args:
            new_file_name (str): New file name to be associated with the NoteHandler object.

        Returns:
            str: Updated file name.

        """
        self.file_name = new_file_name
        return self.file_name
    
    
    def write_to_file(self, file_name: str|None = None, write_method: str="w") -> None:
        """
        Writes the contents of file_contents to the file.

        Args:
            file_name (str|None, optional): The name of the file to write. Defaults to None.
            write_method (str, optional): The file write mode. Defaults to "w".

        Returns:
            None
        """
        # we can update the file name we're working on so we output to a different file
        # if desired
        file_name = file_name if file_name is not None else self.file_name
        with open(file_name, write_method, encoding="utf-8") as file:
            if "json" not in file_name:
                file.write(self.file_contents)
            else:
                json.dump(self.file_contents, 
                        file,
                        ensure_ascii=False,
                        indent=4)
      
    def list_regex_matches(self, pattern: str) -> list:
        """
        Returns a list of all non-overlapping occurrences of the specified regex pattern in the file contents.

        Args:
            pattern (str): The regex pattern to search for.

        Returns:
            list: A list of all non-overlapping occurrences of the regex pattern in the file contents.
        """
        return re.findall(pattern, self.file_contents)

    def find_and_replace(self, current: str, new: str, use_regex=False) -> str:
        """
        Finds all occurrences of the specified string or regex pattern in the file contents and replaces them with the
        specified new string.

        Args:
            current (str): The string or regex pattern to find and replace.
            new (str): The string to replace the occurrences with.
            use_regex (bool, optional): Specifies whether to treat the
            'current' argument as a regex pattern or not. Defaults to False.

        Returns:
            str: The file contents after performing the find and replace operation.
        """
        if use_regex == False:
            self.file_contents = self.file_contents.replace(current, new)
        else:
            self.file_contents = re.sub(current, new, self.file_contents)

        return self.file_contents




class NoteMapper(NoteHandler):
    """
    A class that maps note numbers in a file based on a given regex pattern.

    Inherits from NoteHandler.

    Attributes:
        file (str): The file to be processed.
        pattern (str): The regex pattern to match against in the file
        contents.
        prefix (str): The prefix to be added to remapped note numbers.
        Defaults to "note-".

    Methods:
        map_note_numbers(): Maps note numbers in the file based on the
            regex pattern and returns a dictionary of remapped note numbers.
    """

    def __init__(self, file: str, pattern: str, prefix: str="note-") -> None:
        """
        Initializes a new instance of the NoteMapper class.

        Args:
            file (str): The file to be processed.
            pattern (str): The regex pattern to match against
                in the file contents.
            prefix (str, optional): The prefix to be added to remapped
                note numbers. Defaults to "note-".
        """
        super().__init__(file)
        self.pattern = pattern
        self.note_prefix = prefix

    def map_note_numbers(self) -> dict:
        """
        Maps note numbers in the file based on the regex pattern and returns
            a dictionary of remapped note numbers.

        Returns:
            dict: A dictionary of remapped note numbers, where the keys are
            the matched note numbers and the values are the corresponding
            remapped note numbers with the prefix added. Like:
            notes = {"note-25": "note-1", "note-27": "note-2" . . .}
        """
        self.read_file()

        matches = self.list_regex_matches(self.pattern)

        notes = {}
        for i in range(len(matches)):
            notes[matches[i]] = self.note_prefix + str(i + 1)

        self.file_contents = notes
        return notes

        