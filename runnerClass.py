import numpy as np
class Utils:

    def __init__( self ):
        self.directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def get_neigbours( self, board, position ):
        assert isinstance(position, tuple)
        x, y = position[0], position[1]
        neighbours = []
        for d in self.directions:
            if (0 <= d[0] + x < 8) and (0 <= d[1] + y < 13):
                if board[(x + d[0], y + d[1])] < 9:
                    neighbours.extend([(x + d[0], y + d[1])])

        return neighbours

    def distance( self, p1, p2 ):
        """
        Finds the manhattan distance between 2 points. 
        
        :param p1: Tuple, like (1,2)
        :param p2: Tuple, like (3,4)
        :return: int, distance
        """
        assert isinstance(p1, tuple) and isinstance(p2, tuple)
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


class Runner:

    def __init__( self ):
        # create utils instance for helper functions. 
        self.utils = Utils()

    def __best_location__( self, c1, c2, possible_locations ):
        distances = { }
        # np.where is return tuple of array.
        # this is convert it to tuple of integer positions.
        possible_locations = [(x[0][0], x[1][0]) for x in possible_locations]

        for pos in possible_locations:
            distances[pos] = self.utils.distance(pos, c1) + self.utils.distance(pos, c2)

        # find the farthest point from Runner.
        # if there are two same distance then selects random one.
        # because python dict type has no order.
        return max(distances, key=distances.get)

    def play( self, board ):
        # get the runner and chasers positions.
        r_pos = np.where(board == -1)
        c1_pos = np.where(board == 1)
        c2_pos = np.where(board == 2)
        # find possible positions. 
        possible_locations = self.utils.get_neigbours(board, r_pos)

        # return best position. 
        return self.__best_location__(c1_pos, c2_pos, possible_locations)
    
