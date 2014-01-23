class PlayListParser (object):
    '''Parser for soundwidget playlists. A playlist is an index for a
    directory of sound tracks, mapping index numbers to file names. 
    The structure of a playlist file is simple: a sequence of lines
    consisting of an integer and a file name. A line not consisting of
    an initial integer followed by a filename in the directory is
    ignored (an error is reported), and any text following a # comment
    indicator is ignored (no error is reported on
    comments). Whitespace is considered a separator (apart from
    newlines, of course), and is otherwise ignored. (ie, a line may
    begin with whitespace and any combination of spaces and tabs may
    separate index number and file name, or follow the file name)
    '''
    def __init__(self, filename):
        pass

    def parse(self):
        '''Process a playlist and return a mapping from index numbers
        to filenames, as a dictionary
        '''
        pass
    
    def report(self):
        '''Issue two reports: a list of files successfully matched to
        index numbers and a list of potential errors. 
        Potential errors include
        1) files not matched to index numbers
        2) files defined twice
        3) lines not matching [^\s*[0-9]+\s+\w+\.\w+]|[^\s*\#]
        '''
        pass
