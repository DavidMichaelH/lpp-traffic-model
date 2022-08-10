from last_passage_percolation.graphs import Vertex
from last_passage_percolation.graphs import Graph

class LineToLineGraph(Graph):
    
    def CreateLattice(self,half_side_length, *args):
    
        self.half_side_length = half_side_length
     
    
        # Initialize vertices
        for k in range(-self.half_side_length, self.half_side_length + 1):
            lower = max( -self.half_side_length, k -self.half_side_length )
            upper = min(k  + self.half_side_length  , self.half_side_length  )
            for s in range(lower,upper+1):
                point = (s,k-s)
                self.nodes_dict[point] = Vertex()
                
     
    
        
         