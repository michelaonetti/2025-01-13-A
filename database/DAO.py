from database.DB_connect import DBConnect
from model.classification import Classification
from model.gene import Gene
from model.interaction import Interaction


class DAO():

    @staticmethod
    def get_all_genes():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT * 
                        FROM genes"""
            cursor.execute(query)

            for row in cursor:
                result.append(Gene(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_interactions():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT * 
                           FROM interactions"""
            cursor.execute(query)

            for row in cursor:
                result.append(Interaction(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_classifications():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT c.GeneID as GeneID, c.Localization as Localization, g.Essential as Essential
                        FROM classification c, genes g where c.GeneID = g.GeneID"""
            cursor.execute(query)

            for row in cursor:
                result.append(Classification(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getEdges(localization):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select i.GeneID1 as id1 , cromo1.chromo as cr1, I.GeneID2  as id2, cromo2.chromo as cr2
from interactions i , (select g.GeneID , sum(distinct g.Chromosome) as chromo
from genes g 
group by g.GeneID ) cromo1, (select g.GeneID , sum(distinct g.Chromosome) as chromo
from genes g 
group by g.GeneID ) cromo2


where cromo1.GeneID =i.GeneID1 and cromo2.GeneID =i.GeneID2 and
i.GeneID1 in 
(SELECT c.GeneID
from classification c where c.Localization =%s) and
i.GeneID2 in 
(SELECT c.GeneID
from classification c where c.Localization =%s)
"""
            cursor.execute(query, (localization, localization))

            for row in cursor:
                result.append((row["id1"], row["cr1"], row["id2"], row["cr2"]))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getLocalizations():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT distinct Localization from classification group by Localization desc"""
            cursor.execute(query)

            for row in cursor:
                result.append(row['Localization'])

            cursor.close()
            cnx.close()
        return result
