class Parser (object):
    '''Parser for soundwidget file lists (playlists, master playlists,
    cue lists. 
    '''


    def __init__(self, path_to_root, index_file_name = "playlist"):
        '''Initialise a parser for a particular root directory '''
        import re
        self.root_path = path_to_root
        self.index_file_name = index_file_name
        self.filepath = "/".join([self.root_path, self.index_file_name])
        self.index_file = open(self.filepath)  # should check for presence of file
        self.res = {}   # regexen used in parsing
        self.parsed = False

    def playlist(self):
        return Playlist(self.root_path, self.mappings, self.comments)

    def parse(self):
        '''Process a playlist and return a mapping from index numbers
        to filenames, as a dictionary
        '''
        import os
        self.files = os.listdir(self.root_path)

        self.define_parse_expressions()
        comment = self.comment
        simple_mapping = self.simple_mapping
        mapping_with_comment = self.mapping_with_comment
        whitespace = self.whitespace

        self.mappings = {}    # the mappings from indices to file 
                              # names or paths
        self.overmatched_indices = {}     # indices matched on 
                                          # more than one line
        self.overmatched_files = {}  # files mapped to more than
                                      # one index
        self.undermatch = {}    # files mentioned but not present
        self.unmarked_comments={}  # text parsed as comment but not
                                   # set off with hash mark
        self.comments = {}      # inline comments, keyed to their lines

        for line_num, line in enumerate(self.index_file.readlines()):
            line = line.strip()
            if comment.match(line):
                continue            # If this line is a comment, 
                                    # skip it
            elif mapping_with_comment.match(line):
                key, val, rest = whitespace.split(line, 2) 
                key = int(key)      # safe, see regex 

                register = self.line_with_comment(key, val, rest, line_num)
                if register:
                    # okay, register the mapping
                    self.mappings[key] = val
                    self.comments[key] = rest

            elif simple_mapping.match(line):
                key,val = whitespace.split(line)
                key = int(key)
                register = self.simple_line(key,val, line_num)
                if register:
                    # okay, register the mapping
                    self.mappings[key] = val
        self.notice_unmatched_files()


    def notice_unmatched_files(self):
        fileset = set(self.files)
        trackset = set(self.mappings.values())
        self.unmatched = list(fileset.difference(trackset))
        self.unmatched.remove(self.index_file_name)

    def simple_line(self,key,val, line_num):
        '''match a simple line, which is a key and a value'''
        map_this_line = True
                # check for overmatched index
        if self.mappings.get(key):
            self.overmatched_index(key, val, line_num)

                # check for overmatched track
        if val in self.mappings.values():
            self.overmatched_track(key, val, line_num)

                # is this file in the directory?
        if not val in self.files:
            self.undermatched_file(key, val, line_num)
            map_this_line = False
        return map_this_line

    def line_with_comment(self,key,val,rest, line_num):
        '''match a commented line, which is a key, value and anything
        else we find, which is the comment
        if the comment is not set off with a hash, make a note and
        complain
        either way, save the comment in a separate map'''
        map_this_line = self.simple_line(key, val, line_num)
  
                # if the rest of the line isn't marked as a comment,
                # we want to issue a warning
        if not self.comment.match(rest):
            self.unmarked_comments[line_num]= rest
        return map_this_line

    def overmatched_index(self, key, val, line_num):
        '''This index already used. Make a note of it. 
        '''
        old = self.overmatched_indices.get(key, [])
        self.overmatched_indices[key] = old + [(val, line_num)] 

    def overmatched_track(self, key, val, line_num):
        '''This track already indexed. Make a note of it. '''
        old = self.overmatched_files.get(val, [])
        self.overmatched_files[val] = old+[(key, line_num)]

    def undermatched_file(self, key, val, line_num):
        '''This file not found in the playlist directory. 
        Make a note of it.'''
        old = self.undermatch.get(key,[])
        self.undermatch[val] = old + [line_num]


    def report(self):
        '''Issue a list of problems and potential problems encountered
        in parsing the playlist.
    
        Potential errors include
        1) files not matched to index numbers
        2) files defined twice
        3) lines not matching [^\s*[0-9]+\s+\w+\.\w+]|[^\s*\#]
        etc.
        
        To do: something a little less brutal than this would be nice!
        '''
        report_text = ""
        report_text += self.check_overmatched_indices()
        report_text += self.check_overmatched_files()
        report_text += self.check_undermatch()
        report_text += self.check_unmarked_comments()
        report_text += self.check_unmatched()
        return report_text

    def check_overmatched_indices(self):
        text = ""
        if len(self.overmatched_indices) > 0:
            text +=("\nSome indices were assigned to more " +
                    "than one file. See normalised playlist for "+
                    "actual assignments. \nOvermatched indices:\n")
            for key, pair in self.overmatched_indices.items():
                text +="\t".join([str(key), 
                                  str(pair[0][0]), 
                                  str(pair[0][1])]) + "\n"
        return text

    def check_overmatched_files(self):
        text = ""
        if len(self.overmatched_files) > 0: 
            text +=("\nSome tracks were assigned to more " +
                    " than one index. This is probably not what "+ 
                    "you meant to do." +
                    " \nOvermatched tracks: \n")
            for key, pair in self.overmatched_files.items():
                text +="\t".join([str(key), 
                                  str(pair[0][0]), 
                                  str(pair[0][1])]) +"\n"
        return text

    def check_undermatch(self):
        text = ""
        if len(self.undermatch) >0:
            text += ("\nSome files named in the playlist " +
                     "index were not found in the playlist" +
                     "directory.  These files will not play, "+ 
                     "and references to these index " +
                     "numbers will be silently ignored. " +
                     "You probably want to " + 
                     "fix this. \nUnmatched files: \n")
            for name, locs in self.undermatch.items():
                text +="\t".join([name,
                                  ", ".join([str(i) for i in
                                             locs])]) +"\n"
        return text

    def check_unmarked_comments(self):
        text = ""
        if len(self.unmarked_comments) > 0:
            text += ("\nSome lines were ill-formed. I'm " +
                     "assuming that you meant extra text to be" +
                     " comments, but you might want to review " +
                     "the normalised playlist to make sure "+
                     "it's what you actually wanted.\n")
            for key, comment in self.unmarked_comments.items():
                text += "\t".join([str(key), comment]) +"\n"
        return text

    def check_unmatched(self):
        text = ""
        if len(self.unmatched) >0:
            text += ("\nSome files in the playlist directory were "+
                     "not assigned to any index number. This may " +
                     "be what you meant to do, but you might want to " +
                     "review this list and  make sure there's nothing " +
                     "you need here.  \nUnmatched files:\n") 
            text +=", ".join(self.unmatched)
        return text


class PlaylistParser (Parser):
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
    def define_parse_expressions(self):
        import re
        # a line starting with a hash is just a comment
        self.comment = re.compile('^\s*\#')

        # a mapping without a comment is just index and filename, with
        # possibly trailing whitespace
        self.simple_mapping = re.compile('(^\s*[0-9]+\s+\w+(\.\w+)?\s*$)')

        # a commented mapping is an index and a filename, plus stuff
        self.mapping_with_comment = re.compile('(^\s*[0-9]+\s+\w+(\.\w+)?\s+.*)')

        # compile a whitespace re 
        self.whitespace = re.compile('\s+')




class MasterPlaylistParser (Parser):

    def define_parse_expressions(self):
        import re
        # a line starting with a hash is just a comment
        self.comment = re.compile('^\s*\#')

        # a mapping without a comment is just index and directory, with
        # possibly trailing whitespace
        self.simple_mapping = re.compile('(^\s*[0-9]+\s+/?\w+(/\w+)*\s*$)')

        # a commented mapping is an index and a filename, plus stuff
        self.mapping_with_comment = re.compile('(^\s*[0-9]+\s+/?\w+(/\w+)*\s+.+)')

        # compile a whitespace re 
        self.whitespace = re.compile('\s+')


class Playlist(object):
    def __init__(self, root_path, tracks, comments):
        self.tracks = tracks
        self.root_path = root_path
        self.comments = comments


    def track(self, index):
        if index in tracks.keys():
            return self.tracks[index]
        else:
            pass         # log an error, please


    def root(self):
        return self.root_path

    def valid_indices(self):
        '''Returns a list of valid indices in this playlist'''
        return self.tracks.keys()

    def track_names(self):
        '''Returns a list of file names mapped in this playlist'''
        return self.tracks.values()

    def normalised_index(self):
        import datetime
        now = datetime.datetime.now()
        output =  "#Normalised Index for Playlist %s\n" %self.root_path 
        output += "#Generated from PlaylistParser %s\n" %str(now)
        tracks_list = ["\t".join (items) for items in self.list_tracks()]
        output += "\n".join(self.tracks_list)
        return output

    def list_tracks(self):
        return [(str(ix), self.tracks[ix], 
                self.comments.get(ix, "")) for ix in  self.tracks.keys()]


 
                
test_playlist = "sample"

