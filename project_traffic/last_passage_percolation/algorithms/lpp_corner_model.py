import random  as random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from last_passage_percolation.graphs.corner import Corner
#nodes_dict => dictionary { index key : vertex object}

class LPPCornerModel:
    
    def __init__(self,sideLength):
        self.corner_graph = Corner()
        self.corner_graph.CreateLattice(sideLength)
      
    def SetExponentialWeights(self):
       
        for k in range(0,self.corner_graph.side_length):
            
            for w in range(0,k+1):
                
                h = k - w 
                
                vertex_weight = random.expovariate(1)
                
                self.corner_graph.nodes_dict[(w, h)].vertex_weight = vertex_weight
   
    
    def ComputeGeodesicFlowFieldOld(self,startPoint =(0,0)):
       
        #We will zero out the passage time relative to the starting point 
        #though I am not certain its really needed 
        self.corner_graph.nodes_dict[startPoint].passage_time = 0; 
        
        for k in range(0,self.corner_graph.side_length - startPoint[0]- startPoint[1]):

            for w in range(0,k+1):
                
                h = k - w 
                
                point = (startPoint[0] + w , startPoint[1] + h)
                
                #Get maximum passage time 
                MaxPassageTime, MaxPassageTimeVertex = self.GetMaxVertexPassageTime(point,startPoint)

                self.corner_graph.nodes_dict[point].passage_time = MaxPassageTime + self.corner_graph.nodes_dict[point].vertex_weight
                self.corner_graph.nodes_dict[point].maximal_vertex = MaxPassageTimeVertex
                
    def ComputeGeodesicFlowField(self,startPoint,targetPoint):
        #We will zero out the passage time relative to the starting point 
        #though I am not certain its really needed 
        self.corner_graph.nodes_dict[startPoint].passage_time = 0; 
        
        for k in range(startPoint[0]+startPoint[1],targetPoint[0] + targetPoint[1]+1):
            
            lower = max(startPoint[0],k-targetPoint[1])
            upper = min(targetPoint[0],k-startPoint[1])
            
            for w in range(lower,upper+1):
                
                h = k - w 
                
                point = (w,h)
                
                #Get maximum passage time 
                MaxPassageTime, MaxPassageTimeVertex = self.GetMaxVertexPassageTime(point,startPoint)

                self.corner_graph.nodes_dict[point].passage_time = MaxPassageTime + self.corner_graph.nodes_dict[point].vertex_weight
                self.corner_graph.nodes_dict[point].maximal_vertex = MaxPassageTimeVertex
                
  
     
     
    
    def ComputeNewFlowField(self):
        self.SetExponentialWeights()
        print("PLEASE FIX ME!")
        self.ComputeGeodesicFlowField()
 
                 

    def ComputeEmpericalCountFromBoundary(self):
        
        #For each point on the upper-right face...
        for w in range(0,self.corner_graph.side_length):
                h = self.corner_graph.side_length - 1 - w 
                
                self.ComputeEmpericalCountFromPoint((w,h))
                
                 
                    
    def ComputeEmpericalCountFromPoint(self,startPoint,relativePoint):
        #Follow the flow field to the root 
        nextVertex = startPoint
        while nextVertex[0] > relativePoint[0] or nextVertex[1] > relativePoint[1]:
            self.corner_graph.nodes_dict[nextVertex].vertex_counter += 1
            nextVertex = self.corner_graph.nodes_dict[nextVertex].maximal_vertex
            
            
            
                
 
    def SelectRandomStartPoint(self,relativePoint = (0,0)):
        L = self.corner_graph.side_length - 1 
        s = relativePoint[0] + relativePoint[1]
        k = random.sample(range(0, L-s+1), 1)[0]
        point = ( relativePoint[0] +  L-s - k  , relativePoint[1]  +  k )  
        
        return point 
        

    def ComputeTrafficFromVertex(self,relativePoint):
         randomPoint = self.SelectRandomStartPoint(relativePoint)
         self.ComputeGeodesicFlowField(relativePoint,randomPoint)
         self.ComputeEmpericalCountFromPoint(randomPoint,relativePoint)
         
         
    def ComputeAllTraffic(self):
       
        for k in range(0,self.corner_graph.side_length):
            
            for w in range(0,k+1):
                
                h = k - w 
                
                self.ComputeTrafficFromVertex((w,h))
    
    def PlotPassageTime(self):
        squareArray = [ [0] * self.corner_graph.side_length for i in range(self.corner_graph.side_length) ]
        # Initialize vertices
        for w in range(0, self.corner_graph.side_length):
            for h in range(1, self.corner_graph.side_length-w):
                squareArray[self.corner_graph.side_length- h][w] = self.corner_graph.nodes_dict[(w, h)].passage_time

        plt.figure()
        plt.imshow( squareArray, cmap='hot', interpolation='nearest' )
        
    def PlotEmpericalCounter(self,plotGrid = False,colorMap = "magma"):
        squareArray = [ [0] * self.corner_graph.side_length for i in range(self.corner_graph.side_length) ]
        # Initialize vertices
        for w in range(0, self.corner_graph.side_length):
            for h in range(1, self.corner_graph.side_length-w):
                squareArray[self.corner_graph.side_length- h][w] =  pow(self.corner_graph.nodes_dict[(w, h)].vertex_counter,1/2)



        

        try:
          _cmap = cm.get_cmap(colorMap)
        except:
          _cmap = cm.hot
        
        if plotGrid:
            fig = plt.figure()
            ax = fig.add_subplot(1, 1, 1)
            
            # Major ticks every 20, minor ticks every 5
            major_ticks = np.arange(0, self.corner_graph.side_length+1, 20)
            minor_ticks = np.arange(0, self.corner_graph.side_length+1, 5)
            
            ax.set_xticks(major_ticks)
            ax.set_xticks(minor_ticks, minor=True)
            ax.set_yticks(major_ticks)
            ax.set_yticks(minor_ticks, minor=True)
            
            # And a corresponding grid
            ax.grid(which='both')
            
            # Or if you want different settings for the grids:
            ax.grid(which='minor', alpha=0.2)
            ax.grid(which='major', alpha=0.5)
            plt.grid(color='white', linestyle='-.', linewidth=0.7)
        
        plt.imshow( squareArray, cmap=_cmap, interpolation='none' )
        #plt.show()
        
    def SaveFigure(self,location):
        plt.savefig(location)
        
        
    
    #----------------------- HELPER METHODS
 
    def GetMaxVertexPassageTime(self,point,relativePoint = (0,0)):
        
        w,h = point
        
        CurrentMaxPassageTime = 0
        CurrentMaxPassageTimeVertex = None
        
        if w > relativePoint[0]:
            weight = self.corner_graph.nodes_dict[(w-1, h)].passage_time
            if weight > CurrentMaxPassageTime:
                CurrentMaxPassageTime = weight
                CurrentMaxPassageTimeVertex = (w-1, h)
                
        if h > relativePoint[1]:
            weight = self.corner_graph.nodes_dict[(w, h-1)].passage_time
            if weight > CurrentMaxPassageTime:
                CurrentMaxPassageTime = weight
                CurrentMaxPassageTimeVertex = (w, h-1)
                
        return CurrentMaxPassageTime, CurrentMaxPassageTimeVertex
        
    
    

                
        
     
        
        
 
                
    
    
     
    
        
         