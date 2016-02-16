import xml.sax
import sys
from data import database
import codecs
from data import saveToRawFiles

debug = False

class DBLPContentHandler(xml.sax.ContentHandler):
    """
	this class is Content Handler whcih gets a callback in case a particular tag is encountered in case of of parsing xml document. In case of DBLP we have added a condition
	"""
    def __init__(self, output_path):
        """
        :param output_path:
        :return:
        """
        
        # this list contains the current open tags. Its a stack to which push and pop the tags as they arrive
        self.elementStack = list()
        # This is the dict element which stores the current tags and their values
        self.currentElementDict = dict()
        # this stores the current tag that we are considering currently
        self.currentElement = ""
        # this is string buffer to store the content for the current tag
        self.content = ""
        # this is just to get the name of the tags inside main tag its not used in the main program
        self.mainElementDict = dict()

        # count variable to track the current iteration. This we can use to check the program for finite iteration
        self.count = 0
        # These tags are used for formatting like <i></i> for italic text. This can be removed as we want to get the complete text for a tag

        self.stoptags = {"i", "sup", "sub", "tt"}
        # print "hello"
        # database handler object
        self.dbHandler = database.DBHandler()
        # self.rawFileHndl = saveToRawFiles.saveToRawFiles(output_path)

    def storeIntoDB(self, pubDict):
        """
        :param pubDict:
        :return:
        """

        if debug:
            print "database"

        keys = pubDict.keys()
        pubType = ""
        if "article" in keys:
            pubType = self.dbHandler.insertArticle(pubDict)
        if "proceedings" in keys:
            pubType = self.dbHandler.insertProceedings(pubDict)
        if "inproceedings" in keys:
            print pubDict
            pubType = self.dbHandler.insertInProceedings(pubDict)
        if "book" in keys:
            print pubDict
            pubType = self.dbHandler.insertBook(pubDict)
        if "www" in keys:
            print pubDict
            pubType = self.dbHandler.insertWWW(pubDict)
        if "masterthesis" in keys:
            print pubDict
            pubType = self.datastructure.insertMasterThesis(pubDict)
        if "phdthesis" in keys:
            print pubDict
            pubType = self.dbHandler.insertPHDThesis(pubDict)
        
    def startElement(self, name, attrs):

        if name in self.stoptags:
            return

        if len(self.elementStack) - 1 == 0:
            if debug:
                print "start tag>>" + name

        self.elementStack.append(name)
        self.currentElement = name

    def endElement(self, name):
        """
        @param name: name of the end element that is encountered by the sax parser. 
        @return: 
        """
        
        # filter unwanted character from content
        self.content = self.content.replace("\n", "")
        
        # in case of stop tags (the one used for string formatting) return without doing anything
        if name in self.stoptags:
            return
        
        # Pop the tag from the stack
        self.elementStack.pop()
        
        # the first tag in the stack is dblp and represent the whole collection
        if len(self.elementStack) - 1 == 0:

            # store the main element also to the dict
            self.currentElementDict[name] = self.content

            # store the main tags into the database
            self.storeIntoDB(self.currentElementDict)
            
            # clear the dict for current element and get it ready for new main tag
            self.currentElementDict.clear()
            
        # for all the elements inside dblp tag represent some entity
        else:
            # to get multiple authors
            if name == "author":

                # store the author name in existing list if it is present
                if "author" in self.currentElementDict.keys():
                    author = self.content
                    authorList = self.currentElementDict[name].append(author)
                    if debug:
                        print "type>>" + str(type(authorList))
                        print self.currentElementDict

                # create a new list for the author in case one is not present
                else:
                    self.currentElementDict[name] = list()
                    author = self.content
                    # author = author.decode('iso-8859-1')
                    # author = author.encode('utf-8')
                    self.currentElementDict[name].append(author)
                    # print the self and currentElementDict
                    if debug:
                        print self.currentElementDict[name]
                        print name
                        print "list created and inserted"
                        print self.currentElementDict

            # to get multiple editors
            elif name == "editor":

                # append to the list of editor if one is present
                if "editor" in self.currentElementDict.keys():
                    self.currentElementDict[self.currentElement].append(self.content)

                # append to the list of editor if one is present
                else:
                    self.currentElementDict[self.currentElement] = list()
                    self.currentElementDict[self.currentElement].append(self.content)

            # for all other tags
            else:
                self.currentElementDict[self.currentElement] = self.content

                if debug:
                    print "else case>>" + name
                    print self.content

            # clear the content to make it ready to store the content for new tag
            self.content = ""
            if debug:
                print "content_clear"

    def characters(self, content):
        # content = content.encode('ascii', 'ignore')
        content.replace("\n", "")
        # append the content to existing tag
        self.content = self.content + content
        if debug:
            print self.content

def main():

    input_path = "/home/spujari/dataset/DBLP_dataset"
    output_path = "/home/spujari/dataset/DBLP_dataset"

    t = DBLPContentHandler(output_path)
    dblpFile = codecs.open(input_path + '/dblp.xml', 'r', encoding='iso-8859-1')
    xml.sax.parse(dblpFile, t)

if __name__ == "__main__":
	main()

