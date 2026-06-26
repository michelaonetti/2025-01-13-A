import flet as ft
from UI.view import View
from model.model import Model


class Controller:

    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._localization = None

    def load(self, dd: ft.Dropdown()):

        localizations = self._model.getLocalizations()  # prende tutti gli aeroporti

        if dd.label == "Localization":  # se dobbiamo popolar eil menu di partenza
            for f in localizations:
                dd.options.append(ft.dropdown.Option(text=f,
                                                     data=f,
                                                     on_click=self.read_DD_local))
        elif dd.label == "Aeroporto di Arrivo":
            for f in localizations:
                dd.options.append(ft.dropdown.Option(text=f,
                                                     data=f,
                                                     on_click=self.read_DD_Arrivo))


    def read_DD_local(self, e):
        print("read_DD_local called ")
        if e.control.data is None:
            self._localization = None
        else:
            self._localization = e.control.data

    def handle_graph(self, e):
        if self._localization is None:
            self._view.txt_result.controls.append(ft.Text("Scegliere una localization."))
            return
        self._model.buildGraph(self._localization)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato."))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo è costituito da {self._model.getNumNodes()} nodi."))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo è costituito da {self._model.getNumEdges()} archi."))
        archi = self._model.get_edges()
        for o1,o2,p in archi:
            self._view.txt_result.controls.append(
                ft.Text(f"{o1}-->{o2}---{p["weight"]}"))
        self._view.update_page()

    def analyze_graph(self, e):

        connessioni =self._model.getConnessi()
        for comp in connessioni:
            if len(comp)>1:
                self._view.txt_result.controls.append(
                    ft.Text(f"Componente di {len(comp)} nodi."))
                for s in comp:
                    self._view.txt_result.controls.append(
                        ft.Text(f"{s}"))
        self._view.update_page()



    def handle_path(self, e):
        path= self._model.getBestPath()

