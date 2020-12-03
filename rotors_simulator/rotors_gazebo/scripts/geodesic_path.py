# PyVisiLibity: a Python binding of VisiLibity1
# Copyright (C) 2018 Yu Cao < University of Southampton> Yu.Cao at soton.ac.uk
# Originally by Ramiro C. of UNC, Argentina
#
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 3 of the License, or 
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details. 
# 
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA


from __future__ import print_function 
import visilibity as vis
import datetime

from workspace import Workspace

# Used to plot the example
import matplotlib.pylab as p

# Used in the create_cone function
import math

class Geodesic(object):
    
    def __init__(self, workspace, threshold = 0.6):
        self.plot_images = False
        
        self.workspace = workspace.workspace
        self.obs = workspace.padded_obs
        self.landmark = workspace.landmark
        # Define an epsilon value (should be != 0.0)
        self.epsilon = threshold
        self.holes_array = []
        
        self.hole_x_array = []
        self.hole_y_array = []
        self.build_fixed_env()
        
        self.discretization=6
        
        
    def build_fixed_env(self):
        # Define the points which will be the outer boundary of the environment
        # Must be COUNTER-CLOCK-WISE(ccw)
        # p1 = vis.Point(0-self.epsilon*2.0, 0-self.epsilon*2.0)
        # p2 = vis.Point(self.workspace[0]+self.epsilon*2.0, 0-self.epsilon*2.0)
        # p3 = vis.Point(self.workspace[0]+self.epsilon*2.0, self.workspace[1]+self.epsilon*2.0)
        # p4 = vis.Point(0-self.epsilon*2.0,self.workspace[1]+self.epsilon*2.0)
        
        p1 = vis.Point(0-5, 0-5)
        p2 = vis.Point(self.workspace[0]+5, 0-5)
        p3 = vis.Point(self.workspace[0]+5, self.workspace[1]+5)
        p4 = vis.Point(0-5,self.workspace[1]+5)
        
        # Load the values of the outer boundary polygon in order to draw it later
        self.wall_x = [p1.x(), p2.x(), p3.x(), p4.x(), p1.x()]
        self.wall_y = [p1.y(), p2.y(), p3.y(), p4.y(), p1.y()]
        
        # Outer boundary polygon must be COUNTER-CLOCK-WISE(ccw)
        # Create the outer boundary polygon
        walls = vis.Polygon([p1, p2, p3, p4])
        self.holes_array.append(walls)
        
        
        for (obs, boundary) in iter(self.obs.items()):
            xx,yy = boundary.exterior.coords.xy
            hole_x = []
            hole_y = []
            point_array = []
            
            for i in range(len(xx)):
                point =vis.Point(xx[i], yy[i])
                hole_x.append(point.x())
                hole_y.append(point.y())
                if i != (len(xx)-1):
                    point_array.append(point)
            hole = vis.Polygon(point_array)
            # print('Hole in standard form: ',hole.is_in_standard_form())
            self.holes_array.append(hole)
            self.hole_x_array.append(hole_x)
            self.hole_y_array.append(hole_y)
        
        # avoid_target = [('l10', 10), ('l4', 1)]
        # for avoid,dist in avoid_target:
        #     avoid_x = self.landmark[avoid][0][0]
        #     avoid_y = self.landmark[avoid][0][1]
        #     dist_buffer = dist + self.epsilon
        #     hole_x = []
        #     hole_y = []
        #     point_array=[]
        #     theta=-math.pi
        #     discretization=10
        #     for i in range(discretization+1):
        #         xx = dist_buffer*math.cos(theta) + avoid_x
        #         yy = dist_buffer*math.sin(theta) + avoid_y
        #         theta=theta-2*math.pi/discretization
        #         pt=vis.Point(round(xx,2),round(yy,2))
        #         hole_x.append(pt.x())
        #         hole_y.append(pt.y())
        #         if i != (discretization):
        #             point_array.append(pt)
        #     hole = vis.Polygon(point_array)
        #     # print('Hole in standard form: ',hole.is_in_standard_form())
        #     self.holes_array.append(hole)
        #     self.hole_x_array.append(hole_x)
        #     self.hole_y_array.append(hole_y)
        # p1 =vis.Point(40-4, 60-4)        
        # p2 =vis.Point(40-4, 80+4)
        # p3 =vis.Point(45+4, 80+4)
        # p4 =vis.Point(45+4, 60-4)
        
        # # Load the values of the hole polygon in order to draw it later
        # hole2_x = [p1.x(), p2.x(), p3.x(), p4.x(),p1.x()]
        # hole2_y = [p1.y(), p2.y(), p3.y(), p4.y(),p1.y()]
        
        # # Create the hole polygon
        # hole2 = vis.Polygon([p1,p2,p3,p4])
        
        # self.holes_array.append(hole2)
        # self.hole_x_array.append(hole2_x)
        # self.hole_y_array.append(hole2_y)
        
    def get_geodesic_target(self, rob_pos, target, node_landmark, avoid_target=[]):
        
        holes_array = self.holes_array.copy()
        hole_x_array = self.hole_x_array.copy()
        hole_y_array = self.hole_y_array.copy()
        
        # start = datetime.datetime.now()
        
        # Define the point of the "observer"
        observer = vis.Point(rob_pos[0],rob_pos[1])
        
        # Now we define some holes for our environment. A hole blocks the 
        # observer vision, it works as an obstacle in his vision sensor.
        # The newly defined holes in this part are tha landmarks that need 
        # to be avoided.
        
        for avoid,dist in avoid_target:
            avoid_x = node_landmark.landmark[avoid][0][0]
            avoid_y = node_landmark.landmark[avoid][0][1]
            dist_buffer = dist + self.epsilon
                
            if math.sqrt((rob_pos[0]-avoid_x)**2+(rob_pos[1]-avoid_y)**2) < dist_buffer+14:
                if math.sqrt((target[0]-avoid_x)**2+(target[1]-avoid_y)**2) < dist_buffer:
                    return rob_pos
                hole_x = []
                hole_y = []
                point_array=[]
                theta=-math.pi
                for i in range(self.discretization+1):
                    xx = dist_buffer*math.cos(theta) + avoid_x
                    yy = dist_buffer*math.sin(theta) + avoid_y
                    theta=theta-2*math.pi/self.discretization
                    pt=vis.Point(round(xx,2),round(yy,2))
                    hole_x.append(pt.x())
                    hole_y.append(pt.y())
                    if i != (self.discretization):
                        point_array.append(pt)
                hole = vis.Polygon(point_array)
                # print('Hole in standard form: ',hole.is_in_standard_form())
                holes_array.append(hole)
                hole_x_array.append(hole_x)
                hole_y_array.append(hole_y)
        
        
        # Create environment, wall will be the outer boundary because
        # is the first polygon in the list. The other polygons will be holes
        env = vis.Environment(holes_array)
        
        
        # Check if the environment is valid
        # print('Environment is valid : ',env.is_valid(epsilon))
        
        
        # Define another point, could be used to check if the observer see it, to 
        # check the shortest path from one point to the other, etc.
        end = vis.Point(target[0], target[1])
        
        
        # Necesary to generate the visibility polygon
        observer.snap_to_boundary_of(env, self.epsilon)
        observer.snap_to_vertices_of(env, self.epsilon)
            
        # Obtein the visibility polygon of the 'observer' in the environmente
        # previously define
        isovist = vis.Visibility_Polygon(observer, env, self.epsilon)
        
        # Uncomment the following line to obtein the visibility polygon 
        # of 'end' in the environmente previously define
        #polygon_vis = vis.Visibility_Polygon(end, env, epsilon)
        
        # Obtein the shortest path from 'observer' to 'end' and 'end_visible' 
        # in the environment previously define
        shortest_path = env.shortest_path(observer, end, self.epsilon)
        
        
        
        route = shortest_path.path()
        path_x = []
        path_y = []
        # print ('Points of Polygon: ')
        for i in range(len(route)):
            x = route[i].x()
            y = route[i].y()
            
            path_x.append(x)
            path_y.append(y)
        
        # Print the length of the path
        """
        print("\nx\nx\nx\n")
        print("Shortest Path length from observer to end: ", shortest_path.length())
        print("\nx\nx\nx\n")
        
        # Check if 'observer' can see 'end', i.e., check if 'end' point is in
        # the visibility polygon of 'observer'
        print( "Can observer see end? ", end._in(isovist, self.epsilon))
        """
        # Print the point of the visibility polygon of 'observer' and save them 
        # in two arrays in order to draw the polygon later
        point_x , point_y  = self.save_print(isovist)
        
        # Add the first point again because the function to draw, draw a line from
        # one point to the next one and to close the figure we need the last line
        # from the last point to the first one
        point_x.append(isovist[0].x())
        point_y.append(isovist[0].y())    
        
        if self.plot_images:
            # Set the title
            p.title('VisiLibity Test')
            
            # Set the labels for the axis
            p.xlabel('X Position')
            p.ylabel('Y Position')
           
            # Plot the outer boundary with black color
            p.plot(self.wall_x, self.wall_y, 'black')
            
            # Plot the position of the observer with a green dot ('go')
            p.plot([observer.x()], [observer.y()], 'go')
            
            # Plot the position of 'end' with a green dot ('go')
            p.plot([end.x()],[end.y()], 'go')
            
            # Plot the position of 'end_visible' with a green dot ('go')
            
            # Plot the visibility polygon of 'observer'
            p.plot(point_x, point_y)
            p.plot(path_x, path_y, 'b')
            
            
            
            for i in range(len(hole_x_array)):
                p.plot(hole_x_array[i], hole_y_array[i], 'r')
            
            # Show the plot
            p.show()
            
        
        """
        print("\nx\nx\nx\n")
        print("Shortest Path length from observer to end: ", shortest_path.length())
        print("\nx\nx\nx\n")

        print ('Points of Polygon: ')
        for i in range(len(route)):
            x = path_x[i]
            y = path_y[i]
            print("%f, %f" %(x,y))
        print("\nx\nx\nx\n")
        print("\nx\nx\nx\n")
        print("\nx\nx\nx\n")
        print("\nx\nx\nx\n")
        """
        # NBA_time = (datetime.datetime.now() - start).total_seconds()
        # print('Time for constructing the NBA: {0:.4f} s'.format(NBA_time))
        #If start and goal are within threshold distance then return the start point itself
        if len(path_x)<2:
            return path_x[0], path_y[0]
        return path_x[1], path_y[1]
    
    def save_print(self,polygon):
        end_pos_x = []
        end_pos_y = []
        # print ('Points of Polygon: ')
        for i in range(polygon.n()):
            x = polygon[i].x()
            y = polygon[i].y()
            
            end_pos_x.append(x)
            end_pos_y.append(y)
                    
            # print( x,y) 
            
        return end_pos_x, end_pos_y 
    
    
    # Desc: This function creates a cone-shape polygon. To do that it use
    # five inputs(point, radius, angle, opening, resolution).
    #   'point': is the vertex of the cone.
    #   'radius': is the longitude from 'point' to any point in the arc.
    #   'angle': is the direcction of the cone.
    #   'resolution': is the number of degrees one point and the next in the arc.
    # Return: The function returns a Polygon object with the shape of 
    #   a cone with the above characteristics.
    def create_cone(self,point, radio, angle, opening, resolution=1):
        
        # Define the list for the points of the cone-shape polygon
        p=[]
        
        # The fisrt point will be the vertex of the cone
        p.append(vis.Point(point[0], point[1]))
    
        # Define the start and end of the arc
        start = angle - opening
        end = angle + opening
        
        for i in range(start, end, resolution):
            
            # Convert start angle from degrees to radians
            rad = math.radians(i)
            
            # Calculate the off-set of the first point of the arc
            x = radio*math.cos(rad)
            y = radio*math.sin(rad)
            
            # Add the off-set to the vertex point
            new_x = point[0] + x
            new_y = point[1] + y
            
            # Add the first point of the arc to the list
            p.append( vis.Point(new_x, new_y) )
        
        # Add the last point of the arc
        rad = math.radians(end)
        x = radio*math.cos(rad)
        y = radio*math.sin(rad)
        new_x = point[0] + x
        new_y = point[1] + y
        p.append( vis.Point(new_x, new_y) )
        
        return vis.Polygon(p)
    
if __name__ == "__main__":
    w=Workspace()
    path_plan=Geodesic(w)
    for i in range(1):
        start = datetime.datetime.now()
        target = path_plan.get_geodesic_target([25,18],[25, 88], w, [('l10', 10), ('l4', 10)])
        NBA_time = (datetime.datetime.now() - start).total_seconds()
        print('Time for constructing the NBA: {0:.4f} s'.format(NBA_time))