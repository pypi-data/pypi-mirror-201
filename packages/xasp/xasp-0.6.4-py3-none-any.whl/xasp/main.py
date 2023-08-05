from xasp import utils
from xasp.entities import Explain
from dumbo_asp.primitives import Model


def marcello_example():
    Explain.the_program(
        """
:- block(Block, Cell); block(Block, Cell'); assign(Cell, Value); assign(Cell', Value'); Value == Value'.
:- given(Cell, Value), not assign(Cell, Value).
block((row, Row), (Row, Col)) :- Row = 1..9; Col = 1..9.
block((col, Col), (Row, Col)) :- Row = 1..9; Col = 1..9.
block((sub, (Row-1) / 3, (Col-1) / 3), (Row, Col)) :- Row = 1..9; Col = 1..9.
given((1, 1), 6).
given((1, 3), 9).
given((1, 4), 8).
given((1, 6), 7).
given((2, 4), 6).
given((2, 9), 1).
given((3, 2), 3).
given((3, 3), 5).
given((4, 7), 1).
given((5, 6), 5).
given((6, 7), 3).
given((7, 1), 8).
given((7, 3), 4).
given((7, 4), 7).
given((7, 5), 2).
given((7, 8), 9).
%:- %* truth of assign((7,9),3) is implied by the above rules and... *%  assign((7,9),3). 
        """,
        the_answer_set=Model.of_program("block((sub,0,0),(1,1)). block((sub,0,0),(1,2)). block((sub,0,0),(1,3)). block((sub,0,1),(1,4)). block((sub,0,1),(1,5)). block((sub,0,1),(1,6)). block((sub,0,2),(1,7)). block((sub,0,2),(1,8)). block((sub,0,2),(1,9)). block((sub,0,0),(2,1)). block((sub,0,0),(2,2)). block((sub,0,0),(2,3)). block((sub,0,1),(2,4)). block((sub,0,1),(2,5)). block((sub,0,1),(2,6)). block((sub,0,2),(2,7)). block((sub,0,2),(2,8)). block((sub,0,2),(2,9)). block((sub,0,0),(3,1)). block((sub,0,0),(3,2)). block((sub,0,0),(3,3)). block((sub,0,1),(3,4)). block((sub,0,1),(3,5)). block((sub,0,1),(3,6)). block((sub,0,2),(3,7)). block((sub,0,2),(3,8)). block((sub,0,2),(3,9)). block((sub,1,0),(4,1)). block((sub,1,0),(4,2)). block((sub,1,0),(4,3)). block((sub,1,1),(4,4)). block((sub,1,1),(4,5)). block((sub,1,1),(4,6)). block((sub,1,2),(4,7)). block((sub,1,2),(4,8)). block((sub,1,2),(4,9)). block((sub,1,0),(5,1)). block((sub,1,0),(5,2)). block((sub,1,0),(5,3)). block((sub,1,1),(5,4)). block((sub,1,1),(5,5)). block((sub,1,1),(5,6)). block((sub,1,2),(5,7)). block((sub,1,2),(5,8)). block((sub,1,2),(5,9)). block((sub,1,0),(6,1)). block((sub,1,0),(6,2)). block((sub,1,0),(6,3)). block((sub,1,1),(6,4)). block((sub,1,1),(6,5)). block((sub,1,1),(6,6)). block((sub,1,2),(6,7)). block((sub,1,2),(6,8)). block((sub,1,2),(6,9)). block((sub,2,0),(7,1)). block((sub,2,0),(7,2)). block((sub,2,0),(7,3)). block((sub,2,1),(7,4)). block((sub,2,1),(7,5)). block((sub,2,1),(7,6)). block((sub,2,2),(7,7)). block((sub,2,2),(7,8)). block((sub,2,2),(7,9)). block((sub,2,0),(8,1)). block((sub,2,0),(8,2)). block((sub,2,0),(8,3)). block((sub,2,1),(8,4)). block((sub,2,1),(8,5)). block((sub,2,1),(8,6)). block((sub,2,2),(8,7)). block((sub,2,2),(8,8)). block((sub,2,2),(8,9)). block((sub,2,0),(9,1)). block((sub,2,0),(9,2)). block((sub,2,0),(9,3)). block((sub,2,1),(9,4)). block((sub,2,1),(9,5)). block((sub,2,1),(9,6)). block((sub,2,2),(9,7)). block((sub,2,2),(9,8)). block((sub,2,2),(9,9)). block((col,1),(1,1)). block((col,2),(1,2)). block((col,3),(1,3)). block((col,4),(1,4)). block((col,5),(1,5)). block((col,6),(1,6)). block((col,7),(1,7)). block((col,8),(1,8)). block((col,9),(1,9)). block((col,1),(2,1)). block((col,2),(2,2)). block((col,3),(2,3)). block((col,4),(2,4)). block((col,5),(2,5)). block((col,6),(2,6)). block((col,7),(2,7)). block((col,8),(2,8)). block((col,9),(2,9)). block((col,1),(3,1)). block((col,2),(3,2)). block((col,3),(3,3)). block((col,4),(3,4)). block((col,5),(3,5)). block((col,6),(3,6)). block((col,7),(3,7)). block((col,8),(3,8)). block((col,9),(3,9)). block((col,1),(4,1)). block((col,2),(4,2)). block((col,3),(4,3)). block((col,4),(4,4)). block((col,5),(4,5)). block((col,6),(4,6)). block((col,7),(4,7)). block((col,8),(4,8)). block((col,9),(4,9)). block((col,1),(5,1)). block((col,2),(5,2)). block((col,3),(5,3)). block((col,4),(5,4)). block((col,5),(5,5)). block((col,6),(5,6)). block((col,7),(5,7)). block((col,8),(5,8)). block((col,9),(5,9)). block((col,1),(6,1)). block((col,2),(6,2)). block((col,3),(6,3)). block((col,4),(6,4)). block((col,5),(6,5)). block((col,6),(6,6)). block((col,7),(6,7)). block((col,8),(6,8)). block((col,9),(6,9)). block((col,1),(7,1)). block((col,2),(7,2)). block((col,3),(7,3)). block((col,4),(7,4)). block((col,5),(7,5)). block((col,6),(7,6)). block((col,7),(7,7)). block((col,8),(7,8)). block((col,9),(7,9)). block((col,1),(8,1)). block((col,2),(8,2)). block((col,3),(8,3)). block((col,4),(8,4)). block((col,5),(8,5)). block((col,6),(8,6)). block((col,7),(8,7)). block((col,8),(8,8)). block((col,9),(8,9)). block((col,1),(9,1)). block((col,2),(9,2)). block((col,3),(9,3)). block((col,4),(9,4)). block((col,5),(9,5)). block((col,6),(9,6)). block((col,7),(9,7)). block((col,8),(9,8)). block((col,9),(9,9)). block((row,1),(1,1)). block((row,1),(1,2)). block((row,1),(1,3)). block((row,1),(1,4)). block((row,1),(1,5)). block((row,1),(1,6)). block((row,1),(1,7)). block((row,1),(1,8)). block((row,1),(1,9)). block((row,2),(2,1)). block((row,2),(2,2)). block((row,2),(2,3)). block((row,2),(2,4)). block((row,2),(2,5)). block((row,2),(2,6)). block((row,2),(2,7)). block((row,2),(2,8)). block((row,2),(2,9)). block((row,3),(3,1)). block((row,3),(3,2)). block((row,3),(3,3)). block((row,3),(3,4)). block((row,3),(3,5)). block((row,3),(3,6)). block((row,3),(3,7)). block((row,3),(3,8)). block((row,3),(3,9)). block((row,4),(4,1)). block((row,4),(4,2)). block((row,4),(4,3)). block((row,4),(4,4)). block((row,4),(4,5)). block((row,4),(4,6)). block((row,4),(4,7)). block((row,4),(4,8)). block((row,4),(4,9)). block((row,5),(5,1)). block((row,5),(5,2)). block((row,5),(5,3)). block((row,5),(5,4)). block((row,5),(5,5)). block((row,5),(5,6)). block((row,5),(5,7)). block((row,5),(5,8)). block((row,5),(5,9)). block((row,6),(6,1)). block((row,6),(6,2)). block((row,6),(6,3)). block((row,6),(6,4)). block((row,6),(6,5)). block((row,6),(6,6)). block((row,6),(6,7)). block((row,6),(6,8)). block((row,6),(6,9)). block((row,7),(7,1)). block((row,7),(7,2)). block((row,7),(7,3)). block((row,7),(7,4)). block((row,7),(7,5)). block((row,7),(7,6)). block((row,7),(7,7)). block((row,7),(7,8)). block((row,7),(7,9)). block((row,8),(8,1)). block((row,8),(8,2)). block((row,8),(8,3)). block((row,8),(8,4)). block((row,8),(8,5)). block((row,8),(8,6)). block((row,8),(8,7)). block((row,8),(8,8)). block((row,8),(8,9)). block((row,9),(9,1)). block((row,9),(9,2)). block((row,9),(9,3)). block((row,9),(9,4)). block((row,9),(9,5)). block((row,9),(9,6)). block((row,9),(9,7)). block((row,9),(9,8)). block((row,9),(9,9)). given((1,1),6). given((1,3),9). given((1,4),8). given((1,6),7). given((2,4),6). given((2,9),1). given((3,2),3). given((3,3),5). given((3,6),2). given((3,8),7). given((4,2),6). given((4,3),8). given((4,7),1). given((4,9),2). given((5,1),3). given((5,6),5). given((6,4),2). given((6,7),3). given((6,8),6). given((7,1),8). given((7,2),5). given((7,3),4). given((7,4),7). given((7,5),2). given((7,7),6). given((7,8),9). given((8,4),5). given((8,5),9). given((8,9),8). given((9,1),2). given((9,3),6). given((9,4),4). given((9,5),3). given((9,7),7). given((9,8),1). given((9,9),5). aux((sub,0,0),(1,1),6). aux((sub,0,0),(1,3),9). aux((sub,0,1),(1,4),8). aux((sub,0,1),(1,6),7). aux((sub,0,1),(2,4),6). aux((sub,0,2),(2,9),1). aux((sub,0,0),(3,2),3). aux((sub,0,0),(3,3),5). aux((sub,0,1),(3,6),2). aux((sub,0,2),(3,8),7). aux((sub,1,0),(4,2),6). aux((sub,1,0),(4,3),8). aux((sub,1,2),(4,7),1). aux((sub,1,2),(4,9),2). aux((sub,1,0),(5,1),3). aux((sub,1,1),(5,6),5). aux((sub,1,1),(6,4),2). aux((sub,1,2),(6,7),3). aux((sub,1,2),(6,8),6). aux((sub,2,0),(7,1),8). aux((sub,2,0),(7,2),5). aux((sub,2,0),(7,3),4). aux((sub,2,1),(7,4),7). aux((sub,2,1),(7,5),2). aux((sub,2,2),(7,7),6). aux((sub,2,2),(7,8),9). aux((sub,2,1),(8,4),5). aux((sub,2,1),(8,5),9). aux((sub,2,2),(8,9),8). aux((sub,2,0),(9,1),2). aux((sub,2,0),(9,3),6). aux((sub,2,1),(9,4),4). aux((sub,2,1),(9,5),3). aux((sub,2,2),(9,7),7). aux((sub,2,2),(9,8),1). aux((sub,2,2),(9,9),5). aux((col,1),(1,1),6). aux((col,3),(1,3),9). aux((col,4),(1,4),8). aux((col,6),(1,6),7). aux((col,4),(2,4),6). aux((col,9),(2,9),1). aux((col,2),(3,2),3). aux((col,3),(3,3),5). aux((col,6),(3,6),2). aux((col,8),(3,8),7). aux((col,2),(4,2),6). aux((col,3),(4,3),8). aux((col,7),(4,7),1). aux((col,9),(4,9),2). aux((col,1),(5,1),3). aux((col,6),(5,6),5). aux((col,4),(6,4),2). aux((col,7),(6,7),3). aux((col,8),(6,8),6). aux((col,1),(7,1),8). aux((col,2),(7,2),5). aux((col,3),(7,3),4). aux((col,4),(7,4),7). aux((col,5),(7,5),2). aux((col,7),(7,7),6). aux((col,8),(7,8),9). aux((col,4),(8,4),5). aux((col,5),(8,5),9). aux((col,9),(8,9),8). aux((col,1),(9,1),2). aux((col,3),(9,3),6). aux((col,4),(9,4),4). aux((col,5),(9,5),3). aux((col,7),(9,7),7). aux((col,8),(9,8),1). aux((col,9),(9,9),5). aux((row,1),(1,1),6). aux((row,1),(1,3),9). aux((row,1),(1,4),8). aux((row,1),(1,6),7). aux((row,2),(2,4),6). aux((row,2),(2,9),1). aux((row,3),(3,2),3). aux((row,3),(3,3),5). aux((row,3),(3,6),2). aux((row,3),(3,8),7). aux((row,4),(4,2),6). aux((row,4),(4,3),8). aux((row,4),(4,7),1). aux((row,4),(4,9),2). aux((row,5),(5,1),3). aux((row,5),(5,6),5). aux((row,6),(6,4),2). aux((row,6),(6,7),3). aux((row,6),(6,8),6). aux((row,7),(7,1),8). aux((row,7),(7,2),5). aux((row,7),(7,3),4). aux((row,7),(7,4),7). aux((row,7),(7,5),2). aux((row,7),(7,7),6). aux((row,7),(7,8),9). aux((row,8),(8,4),5). aux((row,8),(8,5),9). aux((row,8),(8,9),8). aux((row,9),(9,1),2). aux((row,9),(9,3),6). aux((row,9),(9,4),4). aux((row,9),(9,5),3). aux((row,9),(9,7),7). aux((row,9),(9,8),1). aux((row,9),(9,9),5). assign((1,1),6). assign((1,3),9). assign((1,4),8). assign((1,6),7). assign((2,4),6). assign((2,9),1). assign((3,2),3). assign((3,3),5). assign((3,6),2). assign((3,8),7). assign((4,2),6). assign((4,3),8). assign((4,7),1). assign((4,9),2). assign((5,1),3). assign((5,6),5). assign((6,4),2). assign((6,7),3). assign((6,8),6). assign((7,1),8). assign((7,2),5). assign((7,3),4). assign((7,4),7). assign((7,5),2). assign((7,7),6). assign((7,8),9). assign((8,4),5). assign((8,5),9). assign((8,9),8). assign((9,1),2). assign((9,3),6). assign((9,4),4). assign((9,5),3). assign((9,7),7). assign((9,8),1). assign((9,9),5). aux((sub,0,0),(1,2),2). assign((1,2),2). aux((sub,0,1),(1,5),1). assign((1,5),1). aux((sub,0,2),(1,7),5). assign((1,7),5). aux((sub,0,2),(1,8),3). assign((1,8),3). aux((sub,0,2),(1,9),4). assign((1,9),4). aux((sub,0,0),(2,1),4). assign((2,1),4). aux((sub,0,0),(2,2),8). assign((2,2),8). aux((sub,0,0),(2,3),7). assign((2,3),7). aux((sub,0,1),(2,5),5). assign((2,5),5). aux((sub,0,1),(2,6),3). assign((2,6),3). aux((sub,0,2),(2,7),9). assign((2,7),9). aux((sub,0,2),(2,8),2). assign((2,8),2). aux((sub,0,0),(3,1),1). assign((3,1),1). aux((sub,0,1),(3,4),9). assign((3,4),9). aux((sub,0,1),(3,5),4). assign((3,5),4). aux((sub,0,2),(3,7),8). assign((3,7),8). aux((sub,0,2),(3,9),6). assign((3,9),6). aux((sub,1,0),(4,1),9). assign((4,1),9). aux((sub,1,1),(4,4),3). assign((4,4),3). aux((sub,1,1),(4,5),7). assign((4,5),7). aux((sub,1,1),(4,6),4). assign((4,6),4). aux((sub,1,2),(4,8),5). assign((4,8),5). aux((sub,1,0),(5,2),7). assign((5,2),7). aux((sub,1,0),(5,3),2). assign((5,3),2). aux((sub,1,1),(5,4),1). assign((5,4),1). aux((sub,1,1),(5,5),6). assign((5,5),6). aux((sub,1,2),(5,7),4). assign((5,7),4). aux((sub,1,2),(5,8),8). assign((5,8),8). aux((sub,1,2),(5,9),9). assign((5,9),9). aux((sub,1,0),(6,1),5). assign((6,1),5). aux((sub,1,0),(6,2),4). assign((6,2),4). aux((sub,1,0),(6,3),1). assign((6,3),1). aux((sub,1,1),(6,5),8). assign((6,5),8). aux((sub,1,1),(6,6),9). assign((6,6),9). aux((sub,1,2),(6,9),7). assign((6,9),7). aux((sub,2,1),(7,6),1). assign((7,6),1). aux((sub,2,2),(7,9),3). assign((7,9),3). aux((sub,2,0),(8,1),7). assign((8,1),7). aux((sub,2,0),(8,2),1). assign((8,2),1). aux((sub,2,0),(8,3),3). assign((8,3),3). aux((sub,2,1),(8,6),6). assign((8,6),6). aux((sub,2,2),(8,7),2). assign((8,7),2). aux((sub,2,2),(8,8),4). assign((8,8),4). aux((sub,2,0),(9,2),9). assign((9,2),9). aux((sub,2,1),(9,6),8). assign((9,6),8). aux((col,2),(1,2),2). aux((col,5),(1,5),1). aux((col,7),(1,7),5). aux((col,8),(1,8),3). aux((col,9),(1,9),4). aux((col,1),(2,1),4). aux((col,2),(2,2),8). aux((col,3),(2,3),7). aux((col,5),(2,5),5). aux((col,6),(2,6),3). aux((col,7),(2,7),9). aux((col,8),(2,8),2). aux((col,1),(3,1),1). aux((col,4),(3,4),9). aux((col,5),(3,5),4). aux((col,7),(3,7),8). aux((col,9),(3,9),6). aux((col,1),(4,1),9). aux((col,4),(4,4),3). aux((col,5),(4,5),7). aux((col,6),(4,6),4). aux((col,8),(4,8),5). aux((col,2),(5,2),7). aux((col,3),(5,3),2). aux((col,4),(5,4),1). aux((col,5),(5,5),6). aux((col,7),(5,7),4). aux((col,8),(5,8),8). aux((col,9),(5,9),9). aux((col,1),(6,1),5). aux((col,2),(6,2),4). aux((col,3),(6,3),1). aux((col,5),(6,5),8). aux((col,6),(6,6),9). aux((col,9),(6,9),7). aux((col,6),(7,6),1). aux((col,9),(7,9),3). aux((col,1),(8,1),7). aux((col,2),(8,2),1). aux((col,3),(8,3),3). aux((col,6),(8,6),6). aux((col,7),(8,7),2). aux((col,8),(8,8),4). aux((col,2),(9,2),9). aux((col,6),(9,6),8). aux((row,1),(1,2),2). aux((row,1),(1,5),1). aux((row,1),(1,7),5). aux((row,1),(1,8),3). aux((row,1),(1,9),4). aux((row,2),(2,1),4). aux((row,2),(2,2),8). aux((row,2),(2,3),7). aux((row,2),(2,5),5). aux((row,2),(2,6),3). aux((row,2),(2,7),9). aux((row,2),(2,8),2). aux((row,3),(3,1),1). aux((row,3),(3,4),9). aux((row,3),(3,5),4). aux((row,3),(3,7),8). aux((row,3),(3,9),6). aux((row,4),(4,1),9). aux((row,4),(4,4),3). aux((row,4),(4,5),7). aux((row,4),(4,6),4). aux((row,4),(4,8),5). aux((row,5),(5,2),7). aux((row,5),(5,3),2). aux((row,5),(5,4),1). aux((row,5),(5,5),6). aux((row,5),(5,7),4). aux((row,5),(5,8),8). aux((row,5),(5,9),9). aux((row,6),(6,1),5). aux((row,6),(6,2),4). aux((row,6),(6,3),1). aux((row,6),(6,5),8). aux((row,6),(6,6),9). aux((row,6),(6,9),7). aux((row,7),(7,6),1). aux((row,7),(7,9),3). aux((row,8),(8,1),7). aux((row,8),(8,2),1). aux((row,8),(8,3),3). aux((row,8),(8,6),6). aux((row,8),(8,7),2). aux((row,8),(8,8),4). aux((row,9),(9,2),9). aux((row,9),(9,6),8)."),
        the_atoms_to_explain=Model.of_atoms("assign((7,9),3)")
    ).compute_minimal_assumption_set()# show_navigator_graph()


    # read the answer set
    with open(utils.PROJECT_ROOT / "examples/xai.answer_set.lp") as f:
        answer_set = Model.of_program('\n'.join(f.readlines()))

    # read the program
    with open(utils.PROJECT_ROOT / "examples/xai.lp") as f:
        program = '\n'.join(f.readlines())

    # compute the DAG
    Explain.the_program(
        program,
        the_answer_set=answer_set,
        the_atoms_to_explain=Model.of_atoms("behaves_inertially(testing_posTestNeg,121)")
    ).show_navigator_graph()


def running_example():
    explain = Explain.the_program(
        """
        assign(Node, green) :- node(Node), not assign(Node, blue), not assign(Node, red).
        assign(Node, blue) :- node(Node), not assign(Node, green), not assign(Node, red).
        assign(Node, red) :- node(Node), not assign(Node, blue), not assign(Node, green).
        :- edge(Node, Node'), assign(Node, Color), assign(Node', Color).

        node(X) :- edge(X,Y).
        node(Y) :- edge(X,Y).
        
        edge(a,b).
        edge(a,c).
        edge(b,c).
        
        edge(b,e).
edge(c,e).

        edge(c,d).
        
        edge(d,e).
        edge(d,f).
        edge(e,f).
        """,
        the_answer_set=Model.of_atoms(atom.strip() for atom in """
            node(b) node(c) node(d) node(e) node(f) node(a) edge(a,b) edge(a,c) edge(b,c) edge(c,d) edge(b,e) edge(c,e) edge(d,e) edge(d,f) edge(e,f) assign(b,red) assign(c,green) assign(d,red) assign(e,blue) assign(f,green) assign(a,blue)
        """.strip().split()),
        the_atoms_to_explain=Model.of_atoms("assign(e,green)")
    )
    print(explain.minimal_assumption_set())
    # explain.compute_explanation_dag()
    # print(explain.explanation_dag().as_facts)
    explain.show_navigator_graph()
    # explain.save_igraph(Path("/tmp/a.png"))
    assert False


    explain = Explain.the_program(
        """
        % 1 <= {arc(X,Y); arc(Y,X)} <= 1 :- edge(X,Y).
        arc(X,Y) :- edge(X,Y), not arc(Y,X).
        arc(Y,X) :- edge(X,Y), not arc(X,Y).
        reach(X,X) :- source(X).
        reach(X,Y) :- reach(X,Z), arc(Z,Y).
        :- source(X), sink(Y), not reach(X,Y).
        
        edge(a,b).
        edge(a,d).
        edge(d,c).
        
        source(a).
        source(b).
        
        sink(c).
        """,
        the_answer_set=Model.of_atoms(atom.strip() for atom in """
            edge(a,b)
            edge(a,d)
            edge(d,c)
            source(a)
            source(b)
            sink(c)
            reach(a,a)
            reach(b,b)
            reach(b,a)
            reach(a,d)
            reach(a,c)
            reach(b,d)
            reach(b,c)
            arc(b,a)
            arc(a,d)
            arc(d,c)
        """.strip().split('\n')),
        the_atoms_to_explain=Model.of_atoms("reach(d,c)")
    )
    # explain.compute_explanation_dag()
    # print(explain.explanation_dag().as_facts)
    explain.show_navigator_graph()
    # explain.save_igraph(Path("/tmp/a.png"))
    assert False



    # explain = Explain.the_program(
    #     """
    #     a :- not b.
    #     a :- b, c.
    #     b :- not a.
    #     c :- a, b.
    #     """,
    #     the_answer_set=Model.of_atoms("b"),
    #     the_atoms_to_explain=Model.of_atoms("c")
    # )
    # explain.compute_explanation_dag()
    # print(explain.explanation_dag().as_facts)
    # explain.show_navigator_graph()
    # explain.save_igraph(Path("/tmp/a.png"))
    # assert False





    # explain = Explain.the_program(
    #     "-a.",
    #     the_answer_set=Model.of_atoms("-a"),
    #     the_atoms_to_explain=Model.of_atoms("-a"),
    # )
    # explain.compute_explanation_dag(repeat=2)
    # print(explain.explanation_dag(index=0).as_facts)
    # print("---")
    # print(explain.explanation_dag(index=1).as_facts)

    explain = Explain.the_program(
        "{a; b} = 1.  c :- a.  c :- b.",
        the_answer_set=Model.empty(),
        the_atoms_to_explain=Model.of_atoms("c"),
    )
    explain.compute_explanation_dag(repeat=2)
    print(explain.explanation_dag(0).drop("original_rule").as_facts)
    print("---")
    # print(explain.explanation_dag(1).drop("original_rule").as_facts)

    # explain.show_navigator_graph(0)
    # explain.show_navigator_graph(1)

    print(explain.navigator_graph())
    # explain.show_navigator_graph()

    # explain.save_igraph(Path("/tmp/a.png"))
    # assert False

    # read the answer set
    with open(utils.PROJECT_ROOT / "examples/xai.answer_set.lp") as f:
        answer_set = Model.of_program('\n'.join(f.readlines()))

    # read the program
    with open(utils.PROJECT_ROOT / "examples/xai.lp") as f:
        program = '\n'.join(f.readlines())

    # compute the DAG
    # start = time.time()
    # explanation = Explain.the_program(
    #     program,
    #     the_answer_set=answer_set,
    #     the_atoms_to_explain=Model.of_atoms("-h(testing_posTestNeg,121)")
    # )
    # dag = explanation.explanation_dag()
    # print(time.time()-start)
    # with open(utils.PROJECT_ROOT / "examples/xai.dag.lp", "w") as f:
    #     f.writelines(dag.as_facts)

    with open(utils.PROJECT_ROOT / "examples/xai.dag.lp") as f:
        dag = Model.of_program('\n'.join(f.readlines()))

    start = time.time()
    explanation = Explain.the_dag(
        dag,
        the_answer_set=answer_set,
        the_atoms_to_explain=Model.of_atoms("-h(testing_posTestNeg,121)")
    )
    explanation.compute_igraph()
    print(time.time() - start)

    # graph = json.dumps(explanation.navigator_graph, separators=(',', ':'))
    # with open("/tmp/xai.dag.js", "w") as f:
    #     f.writelines(graph)
    explanation.show_navigator_graph()
    # graph = explanation.navigator_graph()
    # print('[')
    # for link in graph["links"]:
    #     a, b = link["source"], link["target"]
    #     print(f'["{a}", "{b}"],')
    # print(']')
    # explanation.save_igraph(Path("/tmp/a.png"), bbox=(0, 0, 12000, 2400))

    # frames = []
    # for distance in range(1, 10):
    #     filename = f"/tmp/{distance}.png"
    #     explanation.save_igraph(
    #         Path(filename),
    #         distance=distance,
    #         bbox=(8000, 4000)
    #     )
    #     frames.append(Image.open(filename))
    #     print(time.time() - start)
    #
    # frames[0].save("/tmp/dag.gif", format="GIF", append_images=frames,
    #                save_all=True, duration=1000, loop=0)
    # print(time.time() - start)
    #
    # image = Image.open("/tmp/dag.gif")
    # image.show()


if __name__ == "__main__":
    running_example()