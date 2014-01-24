class PlaylistParser (object):
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
    The playlist loaded at show time by the sound widget is the one
    which is called "playlist". The parser parses this file by
    default, though it can accept an arbitrary file name (for example,
    to test alternative playlist files, if that should be desired)
    Note: comments on the same line as a mapping will be reported back
    in validate mode, in conjunction with the mapping. Comments on
    their own lines will be lost. 
    '''


    def __init__(self, path_to_playlist, playlist = "playlist"):
        '''Initialise a parser for a particular root directory '''
        self.root_path = path_to_playlist
        self.filename = playlist
        self.filepath = self.root_path + "/" + self.filename
        self.playlist = open(self.filepath)  # should check for presence of file

    def parse(self):
        '''Process a playlist and return a mapping from index numbers
        to filenames, as a dictionary
        '''
        import os
        import re
        os.chdir(self.root_path)
        files = os.listdir(".")

        # a line starting with a hash is just a comment
        comment = re.compile('^\s*\#')

        # a mapping without a comment is just index and filename, with
        # possibly trailing whitespace
        simple_mapping = re.compile('(^\s*[0-9]+\s+\w+(\.\w+)?\s*$)')

        # a commented mapping is an index and a filename, plus stuff
        mapping_with_comment = re.compile('(^\s*[0-9]+\s+\w+(\.\w+)?\s+.*)')

        # compile a whitespace re 
        whitespace = re.compile('\s+')

        
        self.tracks_map = {}    # the track mapping
        self.overmatched_indices = {}     # indices matched on 
                                          # more than one line
        self.overmatched_tracks = {}  # tracks mapped to more than
                                      # one index
        self.undermatch = {}    # tracks mentioned but not present
        self.unmarked_comments={}  # text parsed as comment but not
                                   # set off with hash mark
        self.comments = {}      # inline comments, keyed to their lines

        for line_num, line in enumerate(self.playlist.readlines()):
            line = line.strip()
            print line_num, line
            if comment.match(line):
                print "matched a comment on line %d"%line_num
                continue            # If this line is a comment, 
                                    # skip it
            elif mapping_with_comment.match(line):
                print "matched a commented mapping on line %d"%line_num
                key, val, rest = whitespace.split(line, 2) 
                key = int(key)      # safe, see regex 

                # check for overmatched index
                if self.tracks_map.get(key):
                    old = self.overmatched_indices.get(key, [])
                    self.overmatched_indices[key] = old + [(val, line_num)] 
                                 
            
                # check for overmatched track
                if val in self.tracks_map.values():
                    old = self.overmatched_tracks.get(val, [])
                    self.overmatched_tracks[val] = old+[key, line_num]
        
                # if the rest of the line isn't marked as a comment,
                # we want to issue a warning
                if not comment.match(rest):
                    self.unmarked_comments[line_num]= rest
                
                # is this file in the directory?
                if not val in files:
                    old = self.undermatch.get(key, [])
                    self.undermatch[val] =  old + [line_num]
                    continue

                # okay, register the mapping
                self.tracks_map[key] = val
                self.comments[key] = rest


            elif simple_mapping.match(line):
                print "matched a simple mapping on line %d"%line_num
                key,val = whitespace.split(line)
                key = int(key)

                # check for overmatched index
                if self.tracks_map.get(key):
                    old = self.overmatched_indices.get(key, [])
                    self.overmatched_indices[key] = old + [(val, line_num)] 

                # check for overmatched track
                if val in self.tracks_map.values():
                    old = self.overmatched_tracks.get(val, [])
                    self.overmatched_tracks[val] = old+[(key,line_num)]

                # is this file in the directory?
                if not val in files:
                    old = self.undermatch.get(key,[])
                    self.undermatch[val] = old + [line_num]
                    continue

                # okay, register the mapping
                self.tracks_map[key] = val
        fileset = set(files)
        trackset = set(self.tracks_map.values())
        self.unmatched = list(fileset.difference(trackset))
        self.unmatched.remove(self.filename)

    def report(self):
        '''Issue two reports: a list of files successfully matched to
        index numbers and a list of potential errors. 
        Potential errors include
        1) files not matched to index numbers
        2) files defined twice
        3) lines not matching [^\s*[0-9]+\s+\w+\.\w+]|[^\s*\#]
        '''
        pass





test_playlist = "sample"

