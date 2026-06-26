import copy
import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._graph = nx.Graph()  # grafico non orientato e semplice, per i pesi aggiungo weight=
        self._AllClassifiations = DAO.get_all_classifications()  # preno dao DAO con query tutti gli aeroporti
        self._idMap = {}  # id_aeroporto = oggetto aeroporto
        for n in self._AllClassifiations:
            # inserico nella id map cosi poi ripesco da qua per ritornare ai valori dell'oggeto aeroporto
            self._idMap[n.GeneID] = n
        self._bestPath = []

    def buildGraph(self, localization):
        self._graph.clear()
        for c in self._AllClassifiations:
            if c.Localization == localization:
                self._graph.add_node(c)

        # aggiunge gli archi
        self.addEdges(localization)  # carica in automatico gli archi

    def addEdges(self, localization):
        archi = DAO.getEdges(localization)
        for id1,p1,id2,p2 in archi:
            if p1!=p2:
                self._graph.add_edge(self._idMap[id1],self._idMap[id2], weight=(p1+p2))
            else:
                self._graph.add_edge(self._idMap[id1],self._idMap[id2], weight=p1)

    def get_edges(self):
        """Ritorna i 5 archi con il peso maggiore"""
        # Ordina tutti gli archi in base all'attributo 'weight' decrescente
        archi_ordinati = sorted(self._graph.edges(data=True), key=lambda x: x[2].get('weight', 0), reverse=False)
        return archi_ordinati

    def getConnessi(self):

        componenti = sorted(nx.connected_components(self._graph), key=len, reverse=True)
        return componenti
    def getBestPath(self):
        """Identificare una lista di nodi appartenenti al grafo di
        cui al punto 1, tale per cui siano verificate le seguenti richieste:
        I. I nodi devono essere presentati nella lista ordinati in senso crescente di GeneID
        II. I nodi devono essere o tutti “Essenziali” oppure tutti “Non-Essenziali”. Vanno esclusi i nodi per i quali
        l’essenzialità non è nota (ovvero in cui il campo è “?”)
        III. La soluzione proposta deve massimizzare il numero di elementi nella lista.
        IV. A parità di lunghezza della soluzione, il numero di componenti connesse del sottografo ottenuto
        considerando solo i nodi del set trovato deve essere minimo (hint: usare il metodo
        Graph.subgraph())
        b. Si stampi la sequenza di cromosomi di lunghezza massima così ottenuta."""

        self._bestPath= []

        parziale=[]

        for nodo in self._graph.nodes:
            if nodo.Essential != '?':
                essential = nodo.Essential
                parziale.append(nodo)
                self._ricorsione(parziale, essential, float('inf'))
                parziale.pop()


    def _ricorsione(self, parziale, essential, num_comp):
        actual_num = self.calcolaConnesse(parziale)
        if len(parziale) > len(self._bestPath):
            self._bestPath = copy.deepcopy(parziale)
        elif len(parziale) == len(self._bestPath):
            if actual_num < num_comp:
                """ il numero di componenti connesse del sottografo ottenuto
considerando solo i nodi del set trovato deve essere minimo (hint: usare il metodo
Graph.subgraph())"""
                num_comp = actual_num
                self._bestPath = copy.deepcopy(parziale)

        for vicino in self._graph.neighbors(parziale[-1]):
            if vicino.Essential == essential and vicino not in parziale and vicino.GeneID>parziale[-1].GeneID:
                parziale.append(vicino)
                self._ricorsione(parziale, essential, num_comp)
                parziale.pop()

    def calcolaConnesse(self,parziale):
        sotto_grafo = self._graph.subgraph(parziale)
        componenti = list(nx.connected_components(sotto_grafo))
        return len(componenti)



    def getLocalizations(self):
        return DAO.getLocalizations()

    def getNumNodes(self):
        return len(self._graph.nodes)

    def getNumEdges(self):
        return len(self._graph.edges)