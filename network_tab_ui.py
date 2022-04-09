import networkx as nx
from PyQt5.QtWidgets import QDialog, QTextEdit, QLineEdit, QVBoxLayout

from key_event_thread import KeyEventThread
from command_line_thread import CommandLineThread



class NetworkTabUi(QDialog):
    def __init__(self, U, B):
        super().__init__()
        self.B = B
        self.U = U
        self.textEdit = QTextEdit(self)
        self.textEdit.setReadOnly(True)
        self.lineEdit = QLineEdit('', self)
        KeyEventThread(self.run_thread)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.textEdit)
        self.layout.addWidget(self.lineEdit)

        self.thread = CommandLineThread(self)
        self.thread.line_printed.connect(self.handle_line)

        self.thread.start_message()

    def add_node_and_generate(self, id):
        self.B.add_node(id)
        self.U.generate_tab_ui()

    def remove_node_and_generate(self, id):
        self.B.remove_node(id)
        self.U.generate_tab_ui()

    def add_edge_and_generate(self, id1, id2, new_weight):
        self.B.add_edge(id1, id2, weight=new_weight)
        self.U.generate_tab_ui()

    def remove_edge_and_generate(self, id1, id2):
        self.B.remove_edge(id1, id2)
        self.U.generate_tab_ui()

    def prims_algoritm(self, id):
        H = nx.Graph()
        H.add_nodes_from(sorted(self.B.nodes(data=True)))
        H.add_edges_from(self.B.edges(data=True))
        self.B = H
        self.refresh()

        A = nx.adjacency_matrix(self.B)
        INF = 10000
        V = len(A.toarray())
        G = A.toarray()
        selected = [0] * len(A.toarray())
        no_edge = 0
        print(list(self.B.nodes()))
        selected[list(self.B.nodes()).index(id)] = True
        while no_edge < V - 1:
            minimum = INF
            x = 0
            y = 0
            for i in range(V):
                if selected[i]:
                    for j in range(V):
                        if (not selected[j]) and G[i][j]:
                            if minimum > G[i][j]:
                                minimum = G[i][j]
                                x = i
                                y = j
            self.thread.line_printed.emit(
                str(x) + "-" + str(y) + ":" + str(G[x][y]) + "\n")
            print(str(x) + "-" + str(y) + ":" + str(G[x][y]))
            selected[y] = True
            no_edge += 1
        self.U.generate_tab_ui()

    def refresh(self):
        self.U.generate_tab_ui()

    def run_thread(self):
        self.thread.run(self.lineEdit, self.B)

    def handle_line(self, line):
        cursor = self.textEdit.textCursor()
        cursor.movePosition(cursor.End)
        cursor.insertText(line)
        self.textEdit.ensureCursorVisible()