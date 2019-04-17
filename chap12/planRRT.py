import numpy as np
from message_types.msg_waypoints import msg_waypoints
from IPython.core.debugger import Pdb

class planRRT():
    def __init__(self):
        self.segmentLength = 300 # standard length of path segments
        self.clearance = 10

    def planPath(self, wpp_start, wpp_end, map):
        # desired down position is down position of end node
        pd = wpp_end.item(2)

        # specify start and end nodes from wpp_start and wpp_end
        # format: N, E, D, cost, parentIndex, connectsToGoalFlag,
        start_node = np.array([wpp_start.item(0), wpp_start.item(1), pd, 0, -1, 0])
        end_node = np.array([wpp_end.item(0), wpp_end.item(1), pd, 0, 0, 0])

        # establish tree starting with the start node
        tree = start_node.reshape(1,len(start_node))

        # check to see if start_node connects directly to end_node
        if ((np.linalg.norm(start_node[0:3] - end_node[0:3]) < self.segmentLength ) and not self.collision(start_node, end_node, map)):
            waypoints = msg_waypoints()
            waypoints.ned[:,0] = start_node[:3]
            waypoints.ned[:,1] = end_node[:3]
            waypoints.num_waypoints = 2
            waypoints.cost[0][0] = 0
            waypoints.parent_idx[0][0] = 0
            waypoints.flag_connect_to_goal[0][0] = 1
            return waypoints

        numPaths = 0
        while numPaths < 3:
            tree, flag = self.extendTree(tree, end_node, self.segmentLength, map, pd)
            numPaths = numPaths + flag

        # find path with minimum cost to end_node
        path = self.findMinimumPath(tree, end_node)
        return self.smoothPath(path, map)

#    def generateRandomNode(map, pd, chi):
#        random_pt = np.random.uniform(0,map.city_width,2)
#        temp = np.array([pd, 0., 0., 0])
#        node = np.hstack([random_pt, temp])
#        return node

    def generateRandomPoint(self, map, pd):
        north_east = np.random.uniform(0,map.city_width,2)
        pt = np.hstack([north_east, pd])
        return pt

    def collision(self, start_node, end_node, map):
        pts = self.pointsAlongPath(start_node, end_node, 5)

        for i in range(len(map.building_north)):
            norths = np.abs(pts[:,0] - map.building_north[i])
            in_north = (norths < map.building_width/2 + self.clearance)
            if np.any(in_north):
                in_north_pts = pts[in_north]
                for j in range(len(map.building_east)):
                    easts = np.abs(in_north_pts[:,1] - map.building_east[j])
                    in_east = (easts < map.building_width/2+self.clearance)
                    if np.any(in_east):
                        in_east_pts = in_north_pts[in_east]
                        pd = end_node[2]
                        if (-pd < map.building_height[j,i]+self.clearance):
#                        if np.any(-in_east_pts[:,2] < map.building_height[j,i]+self.clearance):
                            return True
        return False

    def pointsAlongPath(self, start_node, end_node, Del):
        q = end_node[:3] - start_node[:3]
        L = np.linalg.norm(q)
        num_pts = int(np.ceil(L / Del))
        q /= L
        ned = np.zeros((num_pts,3))

        for i in range(num_pts):
            ned[i,:] = start_node[:3]+q*Del*(i+1)

        return ned

#    def downAtNE(self, map, n, e):

    def extendTree(self, tree, end_node, segmentLength, map, pd):
        success = False
        while not success:
            pt = self.generateRandomPoint(map, pd)
            distances = (pt.item(0)-tree[:,0])**2 + (pt.item(1)-tree[:,1])**2
            idx = np.argmin(distances)

            D = min(np.sqrt(distances[idx]), self.segmentLength)
            q = pt - tree[idx,:3]
            q /= np.linalg.norm(q)
            new_pt = tree[idx,:3] + q*D
            if not self.collision(tree[idx,:3], new_pt, map):
                success = True
                dist_to_goal = np.linalg.norm(new_pt - end_node[:3])
                if dist_to_goal < self.segmentLength and not self.collision(new_pt,end_node[:3],map):
                    flag = 1
                    new_node = np.hstack([new_pt, D+tree[idx,3], idx, 0])
                    tree = np.vstack([tree,new_node])
                    end_D = np.linalg.norm(end_node[:3] - new_pt)
                    cur_end_node = np.hstack([end_node[:3],end_D+new_node[3],idx+1, flag])
                    tree = np.vstack([tree,cur_end_node])
                else:
                    flag = 0
                    new_node = np.hstack([new_pt, D+tree[idx,3], idx, flag])
                    tree = np.vstack([tree,new_node])

                return tree, flag

    def findMinimumPath(self, tree, end_node):
        idxs = np.nonzero(tree[:,-1])
        idxs = idxs[0]
        idx = np.argmin(tree[idxs, 3])
        idx = idxs[idx]

        waypoints = tree[idx]
        while tree[idx,4] != -1:
            idx = int(tree[idx,4])
            waypoints = np.vstack([waypoints, tree[idx]])
        return waypoints[::-1]

    def smoothPath(self, path, map):
        smoothed_path = []
        i = 0
        j = 1

        smoothed_path.append(path[i])
        while j < len(path)-1:
            ws = path[i]
            wp = path[j+1]
            if self.collision(ws, wp, map):
                last_node = path[j]
                smoothed_path.append(last_node)
                i = j
            j += 1
                
        smoothed_path.append(path[-1])
        nodes = np.array(smoothed_path)
        waypoints = msg_waypoints()

        k = 0
        for node in nodes:
            waypoints.ned[:,k] = node[:3]
            waypoints.airspeed[0][k] = 25.
            waypoints.cost[0][k] = node[3]
            waypoints.parent_idx[0][k] = node[4]
            waypoints.flag_connect_to_goal[0][k] = node[5]
            k += 1

        waypoints.flag_wrap_waypoints = False
        waypoints.num_waypoints = k
        return waypoints
