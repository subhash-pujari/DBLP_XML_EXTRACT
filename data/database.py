import MySQLdb

debug = True
insertArticle = True
insertInProceedings = True
insertProceedings = False

class DBHandler():

    def __init__(self):
        self.db = MySQLdb.connect("localhost", "root", "", "dblp", charset="utf8")
        self.cursor = self.db.cursor()
        if debug:
            print "init DB"

    def createDatabaseVariable(self, articleDict):
        keys = articleDict.keys()
        values = str()
        columns = str()
        if "title" in keys:
            title = articleDict["title"]
            title = title.encode("ascii", "ignore")
            title = title.replace("%","")
            values = values + "'" +title.replace("'","\\")+"'"
            columns = columns + "title"

        if "author" in keys:
            authors = articleDict["author"]
            maxCount = len(authors)
            if maxCount > 15:
                maxCount = 15

            for i in range(15):
                values = values + ", %s"
                columns = columns + ", author" + str(i+1)

        if "editor" in keys:
            editors = articleDict["editor"]
            maxCount = len(editors)
            if maxCount > 10:
                maxCount = 10

            for i in range(maxCount):
                values = values + ", '"+editors[i].replace("'","\\")+ "'"
                columns = columns + ", editor" + str(i+1)

        if "journal" in keys:
            journal = articleDict["journal"]
            values = values + ", '" +journal.replace("'","\\") +"'"
            columns = columns + ", journal"

        if "number" in keys:
            number = articleDict["number"]
            print number
            #number = number.replace("")
            values = values + ", '" +number.replace("'","\\") +"'"
            columns = columns + ", number"

        if "volume" in keys:
            volume = articleDict["volume"]
            values = values + ", '" +volume.replace("'","\\") +"'"
            columns = columns + ", volume"

        if "cdrom" in keys:
            cdrom = articleDict["cdrom"]
            values = values + ", '" +cdrom.replace("'","\\") +"'"
            columns = columns + ", cdrom"

        if "pages" in keys:
            pages = articleDict["pages"]
            values = values + ", '" +pages.replace("'","\\") +"'"
            columns = columns + ", pages"

        if "crossref" in keys:
            crossref = articleDict["crossref"]
            values = values + ", '"+crossref.replace("'","\\") +"'"
            columns = columns + ", crossref"

        if "publisher" in keys:
            publisher = articleDict["publisher"]
            values = values + ", '" +publisher.replace("'","\\") +"'"
            columns = columns + ", publisher"

        if "url" in keys:
            url = articleDict["url"]
            values = values + ", '" +url.replace("'","\\") +"'"
            columns = columns + ", url"

        if "note" in keys:
            note = articleDict["note"]
            values = values + ", '" + note.replace("'","\\") +"'"
            columns = columns + ", note"

        if "booktitle" in keys:
            booktitle = articleDict["booktitle"]
            booktitle = booktitle.encode("ascii", "ignore")
            values = values + ", '" +booktitle.replace("'","\\") +"'"
            columns = columns + ", booktitle"

        if "cite" in keys:
		cite = articleDict["cite"]
        	values = values + ", '" + cite.replace("'","\\") +"'"
        	columns = columns + ", cite"

        if "year" in keys:
		year = articleDict["year"]
		values = values + ", '" + year.replace("'","\\") +"'"
		columns = columns + ", year"
        
	if "ee" in keys:
            ee = articleDict["ee"]
            values = values + ", '" + ee.replace("'","\\") +"'"
            columns = columns + ", ee"

        if "isbn" in keys:
            isbn = articleDict["isbn"]
            values = values + ", '" + isbn.replace("'","\\") +"'"
            columns = columns + ", isbn"

        if "series" in keys:
            series = articleDict["series"]
            values = values + ", '" + series.replace("'","\\") +"'"
            columns = columns + ", series"
        return (values, columns)

    def insertBook(self, bookDict):
        pass

    def insertArticle(self, articleDict):
        """
        if insertArticle:
            databaseVar = self.createDatabaseVariable(articleDict)
            values = databaseVar[0]
            columns = databaseVar[1]
            sql = "insert into article("+columns+") values (" + values + ");"
            if debug:
                print sql
            self.cursor.execute(sql)
            self.db.commit()
        """
        
        if debug:
            print "insert into articleDict"
        if insertArticle:
            databaseVar = self.createDatabaseVariable(articleDict)
            values = databaseVar[0]
            columns = databaseVar[1]
            
            if debug:
                print columns
                print values
            
        if "author" not in articleDict:
            return
        else:
            print "author present"
            
        authors = articleDict["author"]
        maxCount = len(authors)
        if maxCount > 15:
            maxCount = 15
            
        sql = "insert into article("+columns+") values (" + values + ");"
        if debug:
            print sql
            
        authorsSize = len(authors)
        print "author size"
        print authorsSize
            
        for i in range(15-authorsSize):
            if authorsSize > 0:
                authors.append('NULL')
                
        print "before insertion"
            
        self.cursor.execute(sql, (authors[0], authors[1],authors[2],authors[3],authors[4],authors[5],authors[6],authors[7],authors[8],authors[9],authors[10], authors[11],authors[12],authors[13],authors[14],))
        self.db.commit()
        
    def insertProceedings(self, proceedingsDict):
        """
        if insertProceedings:
            databaseVar = self.createDatabaseVariable(proceedingsDict)
            values = databaseVar[0]
            columns = databaseVar[1]
            if debug:
                print columns
                print values
                
            sql = "insert into proceedings("+columns+") values (" + values + ");"
            if debug:
                print sql
                
            try:
                self.cursor.execute(sql, )
                self.db.commit()
            except:
                print "exception"
        """     
                
        if debug:
            print "insert into inProceedings"
            if insertInProceedings:
                databaseVar = self.createDatabaseVariable(proceedingsDict)
                values = databaseVar[0]
                columns = databaseVar[1]
                
                if debug:
                    print columns
                    print values
            
            if "author" not in proceedingsDict:
                return
            else:
                print "author present"
            
            authors = proceedingsDict["author"]
            maxCount = len(authors)
            if maxCount > 15:
                maxCount = 15
            
            sql = "insert into proceedings("+columns+") values (" + values + ");"
            if debug:
                print sql
            
            authorsSize = len(authors)
            print "author size"
            print authorsSize
            
            for i in range(15-authorsSize):
                if authorsSize > 0:
                    authors.append('NULL')
                
            print "before insertion"
            
            try:
                self.cursor.execute(sql, (authors[0], authors[1],authors[2],authors[3],authors[4],authors[5],authors[6],authors[7],authors[8],authors[9],authors[10], authors[11],authors[12],authors[13],authors[14],))
                self.db.commit()
                print "insertion done"
            except:
                print "exception"
                
    def insertInProceedings(self, inProceedingsDict):
        if debug:
            print "insert into inProceedings"
            if insertInProceedings:
                databaseVar = self.createDatabaseVariable(inProceedingsDict)
                values = databaseVar[0]
                columns = databaseVar[1]
                
                if debug:
                    print columns
                    print values
            
            if "author" not in inProceedingsDict:
                return
            else:
                print "author present"
            
            authors = inProceedingsDict["author"]
            maxCount = len(authors)
            if maxCount > 15:
                maxCount = 15
            
            sql = "insert into inproceedings("+columns+") values (" + values + ");"
            if debug:
                print sql
            
            authorsSize = len(authors)
            print "author size"
            print authorsSize
            
            for i in range(15-authorsSize):
                if authorsSize > 0:
                    authors.append('NULL')
                
            print "before insertion"
            
            try:
                self.cursor.execute(sql, (authors[0], authors[1],authors[2],authors[3],authors[4],authors[5],authors[6],authors[7],authors[8],authors[9],authors[10], authors[11],authors[12],authors[13],authors[14],))
                self.db.commit()
                print "insertion done"
            except:
                print "exception"
                
    def insertMasterThesis(self, masterThesisDict):
        print "insert into masterThesis"
        
    def insertPHDThesis(self, phdThesisDict):
        print "insert into phdThesis"

    def insertWWW(self, wwwDict):
        print "insert into www"
