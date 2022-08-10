from last_passage_percolation.graphs.vertex import Vertex
from last_passage_percolation.graphs.graph import Graph
#nodes_dict => dictionary { index key : vertex object}


class Corner(Graph):
    
    def CreateLattice(self,side_length, *args):
    
        self.side_length = side_length
     
    
        # Initialize vertices
        for w in range(0, self.side_length):
            for h in range(0, self.side_length-w):
                self.nodes_dict[(w, h)] = Vertex()
                
    
    
     
    
        
         