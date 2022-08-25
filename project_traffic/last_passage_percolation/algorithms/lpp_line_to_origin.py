import random  as random
import math as math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from last_passage_percolation.graphs import LineToLineGraph
#nodes_dict => dictionary { index key : vertex object}

class LPPLineToOriginModel:
    
    def __init__(self,half_side_length):
        self.domain = LineToLineGraph()
        self.domain.CreateLattice(half_side_length)
        self.number_of_plots = 0 
        
        
        
        self.empericalCountOnLine = None
    
                
    def SetExponentialWeights(self):
        for p in self.domain.getCoordinates():
            vertex_weight = random.expovariate(1)
            self.domain.SetVertexWeight(p,vertex_weight)
             
           
    
 
     
    def ComputeGeodesicFlowField(self,startPoint,targetPoint):

        #print(self.domain.nodes_dict.keys())   
        #print(startPoint in self.domain.nodes_dict.keys())  
        self.domain.nodes_dict[startPoint].passage_time = 0; 
        
        for k in range(startPoint[0]+startPoint[1],targetPoint[0] + targetPoint[1]+1):
            
            lower = max(startPoint[0],k-targetPoint[1])
            upper = min(targetPoint[0],k-startPoint[1])
            
            for w in range(lower,upper+1):
                
                h = k - w 
                
                point = (w,h)
                
                #Get maximum passage time 
                MaxPassageTime, MaxPassageTimeVertex = self.GetMaxVertexPassageTime(point,startPoint)

                self.domain.nodes_dict[point].passage_time = MaxPassageTime + self.domain.nodes_dict[point].vertex_weight
                self.domain.nodes_dict[point].maximal_vertex = MaxPassageTimeVertex
                
  
     
     
    
    def ComputeNewFlowField(self):
        self.SetExponentialWeights()
        print("PLEASE FIX ME!")
        self.ComputeGeodesicFlowField()
 
                 

    def ComputeEmpericalCountFromBoundary(self):
        
        #For each point on the upper-right face...
        for w in range(0,self.domain.side_length):
                h = self.domain.side_length - 1 - w 
                
                self.ComputeEmpericalCountFromPoint((w,h))
                
                 
                    
    def ComputeEmpericalCountFromPoint(self,startPoint,relativePoint):
        #Follow the flow field to the root 
        nextVertex = startPoint
        while nextVertex[0] > relativePoint[0] or nextVertex[1] > relativePoint[1]:
            self.domain.nodes_dict[nextVertex].vertex_counter += 1
            nextVertex = self.domain.nodes_dict[nextVertex].maximal_vertex
            
            
            
                
 
    def SelectRandomStartPoint(self,relativePoint):
        #For this domain we need to be 
        #we assume relativePoint[0]+relativePoint[1] = -self.domain.side_length 
        L = math.floor(self.domain.half_side_length*self.domain.line_scale)
        w = relativePoint[0]
        s = random.sample(range(w,2*L+w+1), 1)[0] 
        point = ( s  , L-s )  

        return point 
        

    def SelectMirrorTargetPoint(self,relativePoint):
        L = math.floor(self.domain.half_side_length*self.domain.line_scale)
        point = (relativePoint[0]+L,relativePoint[1]+L)
        
        return point 

    def SelectTargetPoint(self,relativePoint):
         
        point = self.SelectRandomStartPoint(relativePoint)
        
        #point = self.SelectMirrorTargetPoint(relativePoint)
        
        
        
        return point 

    def ComputeTrafficFromVertex(self,relativePoint):
         targetPoint = self.SelectTargetPoint(relativePoint)
         
          
         #Check that the point is in bounds. 
         if max(targetPoint[0],targetPoint[1]) >= self.domain.half_side_length:
             #... and ff not then we reject it and move on
             return 
         
         #... otherwise we continue 
         self.ComputeGeodesicFlowField(relativePoint,targetPoint)
         self.ComputeEmpericalCountFromPoint(targetPoint,relativePoint)
         
         
    def ComputeAllTraffic(self):
        
        L = math.floor(self.domain.half_side_length*self.domain.line_scale)
        lower = self.domain.half_side_length 
        upper = self.domain.half_side_length - math.floor(self.domain.half_side_length*self.domain.line_scale)
        for k in range(-lower,upper+1):
            w = k
            h = -L - k
            point = (w,h)
            
            self.ComputeTrafficFromVertex(point)
    
    def PlotPassageTime(self):
        squareArray = [ [0] * self.domain.side_length for i in range(self.domain.side_length) ]
        # Initialize vertices
        for w in range(0, self.domain.side_length):
            for h in range(1, self.domain.side_length-w):
                squareArray[self.domain.side_length- h][w] = self.domain.nodes_dict[(w, h)].passage_time

        plt.figure()
        plt.imshow( squareArray, cmap='hot', interpolation='nearest' )
        
        
        
    def PlotEmpericalCounter(self,plotGrid = False,colorMap = "magma"):
        
        self.number_of_plots += 1 
        plt.figure(self.number_of_plots)
        
        L = self.domain.half_side_length
        N = 2*L + 1 
        squareArray = [ [0] * N for i in range(N+1) ]
        
        
        for p in self.domain.getCoordinates():
            value = self.domain.nodes_dict[p].vertex_counter  
            squareArray[p[1]+L][p[0] + L]  =  pow(value,1/2)
    
 
        try:
          _cmap = cm.get_cmap(colorMap)
        except:
          _cmap = cm.hot
        
        if plotGrid:
            fig = plt.figure()
            ax = fig.add_subplot(1, 1, 1)
            
            # Major ticks every 20, minor ticks every 5
            major_ticks = np.arange(0, N, 20)
            minor_ticks = np.arange(0, N, 5)
            
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
        
        plt.imshow( squareArray, cmap=_cmap, interpolation='none' ,origin='lower')
        #plt.show()
       
    def ComputeEmpericalCountAlongMiddleSegmnet_OLD(self):
        self.number_of_plots += 1 
        plt.figure(self.number_of_plots)
        
        L = self.domain.half_side_length
        empericalCountOnLine = [ 0 for i in range(2*L+1) ]
        positive_fraction = 0
        numberOfPoints =0 
        for k in range(2*L+1):
            w = k - L
            h = L - k
            point = (w,h)
            val= self.domain.nodes_dict[point].vertex_counter
            if val >0:
                positive_fraction += 1 
                numberOfPoints += val
            
            empericalCountOnLine[k] = val
            
            
        #Experimental stuff
            
        print(f"There we {positive_fraction} many positives out of {L}")
        print(f"The number of geodesics passing through the line is {numberOfPoints}")
        plt.bar([ i for i in range(len(empericalCountOnLine)) ], empericalCountOnLine,color ='maroon', width = 4) 
        
        
    def ComputeEmpericalCountAlongMiddleSegmnet(self):
        self.number_of_plots += 1 
        plt.figure(self.number_of_plots)
        
        L = self.domain.half_side_length
        Lrescaled = math.floor(self.domain.half_side_length*self.domain.line_scale) 
        self.empericalCountOnLine  = [ 0 for i in range(2*Lrescaled+1) ]
        positive_fraction = 0
        numberOfPoints =0 
        for k in range(-Lrescaled , Lrescaled+1):
            w = k
            h = - k
            point = (w,h)
            val= self.domain.nodes_dict[point].vertex_counter
            if val >0:
                positive_fraction += 1 
                numberOfPoints += val
            
            self.empericalCountOnLine[k] = val
            
            
        #Experimental stuff
            
        print(f"There we {positive_fraction} many positives out of {L}")
        print(f"The number of geodesics passing through the line is {numberOfPoints}")
        plt.bar([ i for i in range(len(self.empericalCountOnLine )) ], self.empericalCountOnLine ,color ='maroon', width = 4) 
       
        self.GenerateDistanceHistogram()
        
    def GenerateDistanceHistogram(self):
        distances = []
        current_distance = 0
        for c in self.empericalCountOnLine:
            
            if c > 0: 
                distances.append(current_distance)
                current_distance =0 
            else:
                current_distance += 1 
                
        
        self.number_of_plots += 1 
        fig = plt.figure(self.number_of_plots)
        ax = fig.add_subplot(1, 1, 1)
        
        # Major ticks every 20, minor ticks every 5
        major_ticks = np.arange(0, max(distances), 1)
        minor_ticks = np.arange(0,max(distances), 0.1)
        
        ax.set_xticks(major_ticks)
        ax.set_xticks(minor_ticks, minor=True)
        #ax.set_yticks(major_ticks)
        #ax.set_yticks(minor_ticks, minor=True)
        
        # And a corresponding grid
        #ax.grid(which='both')
        
        # Or if you want different settings for the grids:
        ax.grid(which='minor', alpha=0.2)
        ax.grid(which='major', alpha=0.5)
        plt.grid(color='white', linestyle='-.', linewidth=0.7)
        
        plt.hist(distances)
        
        
        #Stats 
        avg = sum(distances)/len(distances)
        print(f"The average distance is {avg}")
        
         
        
    def SaveFigure(self,location):
        plt.savefig(location)
        
        
    
    #----------------------- HELPER METHODS
 
    def GetMaxVertexPassageTime(self,point,relativePoint):
        
        w,h = point
        
        CurrentMaxPassageTime = 0
        CurrentMaxPassageTimeVertex = None
        
        if w > relativePoint[0]:
            weight = self.domain.nodes_dict[(w-1, h)].passage_time
            if weight > CurrentMaxPassageTime:
                CurrentMaxPassageTime = weight
                CurrentMaxPassageTimeVertex = (w-1, h)
                
        if h > relativePoint[1]:
            weight = self.domain.nodes_dict[(w, h-1)].passage_time
            if weight > CurrentMaxPassageTime:
                CurrentMaxPassageTime = weight
                CurrentMaxPassageTimeVertex = (w, h-1)
                
        return CurrentMaxPassageTime, CurrentMaxPassageTimeVertex
        
    
    

                
        
     
        
        
 
                
    
    
     
    
        
         