from last_passage_percolation.graphs import Vertex
from last_passage_percolation.graphs import Graph
import math

class LineToLineGraph(Graph):
    
    def CreateLattice(self,half_side_length, *args):
    
        self.half_side_length = half_side_length
        self.line_scale = 0.5
    
        # 1) Change the extent of the domain 
        
        lowerSlice = -math.floor(self.half_side_length*self.line_scale)
        upperSlice = math.floor(self.half_side_length*self.line_scale)
        # Initialize vertices
        for k in range(lowerSlice, upperSlice + 1):
            
            
            lower = max( -self.half_side_length, k -self.half_side_length )
            upper = min(k  + self.half_side_length  , self.half_side_length  )
            for s in range(lower,upper+1):
                point = (s,k-s)
                self.nodes_dict[point] = Vertex()
                
                
                
    def SetVertexWeight(self,vertex,weight):
        self.nodes_dict[vertex].vertex_weight = weight
                
     
    
        
         