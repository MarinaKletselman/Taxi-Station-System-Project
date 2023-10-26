import search
import itertools

ids = ["213119142", "207283722"]


def create_permotations(actions):
    return (list(itertools.product(*actions)))


def check_move(state, taxi):
    moves = ()
    width = len(state[0][0])
    lenth = len(state[0])
    location = taxi[3]


    if location[0] != 0:

        if state[0][location[0] - 1][location[1]] != 'I':
            moves = (*moves, ("move", taxi[0], (location[0] - 1, location[1])))

    if location[0] != lenth - 1:
        if state[0][location[0] + 1][location[1]] != 'I':
            moves = (*moves, ("move", taxi[0], (location[0] + 1, location[1])))

    if location[1] != 0:
        if state[0][location[0]][location[1] - 1] != 'I':
            moves = (*moves, ("move", taxi[0], (location[0], location[1] - 1)))

    if location[1] != width - 1:
        if state[0][location[0]][location[1] + 1] != 'I':
            moves = (*moves, ("move", taxi[0], (location[0], location[1] + 1)))

    return moves
def pickup_options(state, taxi, action):
    names = state[1]
    result = action
    loc = taxi[3]
    if (taxi[1] - taxi[5]) != 0:
        for name in names:
            if name[2] == loc and name[3] == 0:
                t = ("pick up", taxi[0], name[0])
                action = (*action, t)
        result= action
    return result
def unesting(initial):
    tuple_initial = ()
    for key in sorted(initial.keys()):
        if key == 'map':
            initial['map'] = [tuple(x) for x in initial['map']]
            tuple_initial = (*tuple_initial, tuple(initial['map']))

        tuple_of_taxis = ()
        if key == 'taxis':
            for num, i in enumerate(sorted(initial['taxis'].keys())):
                tup = ()
                tup += tuple([sorted(initial['taxis'].keys())[num]])
                for j in sorted(initial['taxis'][i].keys()):
                    tup += tuple([initial['taxis'][i][j]])
                tuple_of_taxis = (*tuple_of_taxis, tup)
            tuple_initial = (*tuple_initial, tuple_of_taxis)

        tuple_of_people = ()
        if key == 'passengers':
            for num, i in enumerate(sorted(initial['passengers'].keys())):
                tup = ()
                tup += tuple([sorted(initial['passengers'].keys())[num]])
                for j in sorted(initial['passengers'][i].keys()):
                    tup += tuple([initial['passengers'][i][j]])
                tuple_of_people = (*tuple_of_people, tup)
            tuple_initial = (*tuple_initial, tuple_of_people)


    return tuple_initial
class TaxiProblem(search.Problem):
    """This class implements a medical problem according to problem description file"""

    def __init__(self, initial):
        """Don't forget to implement the goal test
        You should change the initial to your own representation.
        search.Problem.__init__(self, initial) creates the root node"""
        for passenger in initial['passengers']:
            initial['passengers'][passenger]['picked_up'] = 0  # unpicked

        for taxi in initial['taxis']:
            initial['taxis'][taxi]['num_people'] = 0  # people in the taxi
            initial['taxis'][taxi]['max_fuel'] = initial['taxis'][taxi]['fuel']
        initial2 = unesting(initial)
        self.best_state=initial2
        search.Problem.__init__(self, initial2)


    def actions(self, state):
        actions = ()
        final_actions=()
        action_sep= ()
        #each item for its taxis operations
        for taxi in state[2]:
            if(isinstance(taxi,tuple)):
                loc = taxi[3]
                action = ()

                for passanger in state[1]:

                    if passanger[1] == loc and passanger[3] == 1:
                        action = (*action, ('drop off', taxi[0], passanger[0]))

                if state[0][loc[0]][loc[1]] == 'G':
                    action = (*action, ('refuel', taxi[0]))

                if taxi[2] > 0:
                    moves = check_move(state, taxi)

                    for i in range(len(moves)):
                        action = (*action, moves[i])
                action = pickup_options(state, taxi, action)
                action = (*action, ('wait', taxi[0]))
                action_sep= (*action_sep,action)
        if(len(action_sep)>1):
            actions=action_sep[0]
            for i, taxi_action in enumerate(action_sep):
                if(i<len(action_sep)-1):
                    actions= tuple(itertools.product(list(actions),list(action_sep[i+1])))
            for a in (actions):
                    flag= True
                    #checking for illegal turns
                    for i, mini_a in enumerate(a):
                        if (mini_a[0] == 'move'):
                            for j in range (i,len(a)):
                                if (actions[j][0]=='move'):
                                    if(mini_a[2]==actions[j][2]):
                                        flag=False
                                else:
                                    if (mini_a[2]==state[2][j][3]):
                                            flag= False
                        else:
                            for j in range (i,len(actions)):
                                if(actions[j][0]=='move'):
                                    if(state[2][i][3]==actions[j][2]):
                                        flag= False
                                    else:
                                        if(state[2][i][3]==state[2][j][3]):
                                            flag = False # chck
                    if flag:
                        final_actions= (*final_actions,a)
            return final_actions
        return action_sep[0]

        """Returns all the actions that can be executed in the given
        state. The result should be a tuple (or other iterable) of actions
        as defined in the problem description file"""

    def result(self, state, action):
        count_waits=0
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        if(isinstance(action[0],tuple)):
            for a in action:
                new_state = (state[0],)
                if a[0] == "wait":
                    count_waits+=1
                    continue
                taxi_num = 0
                for i, taxi in enumerate(state[2]):
                    if taxi[0] == a[1]:
                        taxi_num = i
                if(a[0]!='refuel'):
                    for i, people in enumerate(state[1]):
                        if people[0] == a[2]:
                            p_num = i
                a_type = a[0]
                tup_people = ()
                tup_taxi = ()
                if a[0] == "refuel":
                    for people in state[1]:
                        tup_people = (*tup_people, people)
                    for i, taxi in enumerate(state[2]):
                        if i == taxi_num:
                            m = list(state[2][i])
                            m[2] = m[4]
                            new_tup = (tuple(m))
                            tup_taxi = (*tup_taxi, new_tup)
                        else:
                            tup_taxi = (*tup_taxi, state[2][i])
                    new_state = (*new_state, tup_people, tup_taxi)
                elif a_type == "move":
                    for passe in state[1]:
                        if passe[2] == state[2][taxi_num][3] and passe[3] == 1:
                            x = a[2][0]
                            y = a[2][1]
                            m = list(passe)
                            m[2] = (x, y)
                            new_tup = (tuple(m))
                            tup_people = (*tup_people, new_tup)
                        else:
                            tup_people = (*tup_people, passe)
                    for taxi in state[2]:
                        if taxi[0] == state[2][taxi_num][0]:
                            x = a[2][0]
                            y = a[2][1]
                            m = list(taxi)
                            m[3] = (x, y)
                            m[2]-= 1
                            new_tup = (tuple(m))
                            tup_taxi = (*tup_taxi, new_tup)

                        else:
                            tup_taxi = (*tup_taxi, taxi)
                    new_state = (*new_state, tup_people, tup_taxi)
                elif a_type == "pick up":
                    for i, people in enumerate(state[1]):
                        if i == p_num:
                            m = list(state[1][i])
                            m[3] = 1
                            new_tup = (tuple(m))
                            tup_people = (*tup_people, new_tup)
                        else:
                            tup_people = (*tup_people, state[1][i])

                    for i, taxi in enumerate(state[2]):
                        if i == taxi_num:
                            m = list(state[2][i])
                            m[5] += 1
                            new_tup = (tuple(m))
                            tup_taxi = (*tup_taxi, new_tup)
                        else:
                            tup_taxi = (*tup_taxi, state[2][i])
                    if (len(state[2]) == 1):
                        tup_taxi = tup_taxi[0]
                    new_state = (*new_state, tup_people, tup_taxi)
                elif a_type == "drop off":
                    for i, people in enumerate(state[1]):
                        if i == p_num:
                            m = list(state[1][i])
                            m[3] = 0
                            new_tup = (tuple(m))
                            tup_people = (*tup_people, new_tup)
                        else:
                            tup_people = (*tup_people, state[1][i])

                    for i, taxi in enumerate(state[2]):
                        if i == taxi_num:
                            m = list(state[2][i])
                            m[5] -= 1
                            new_tup = (tuple(m))
                            tup_taxi = (*tup_taxi, new_tup)
                        else:
                            tup_taxi = (*tup_taxi, state[2][i])
                    new_state = (*new_state, tup_people, tup_taxi)
                state=new_state
        else:
            tup_taxi=()
            tup_people=()
            new_state = (state[0],)
            if(action[0]=='wait'):
                new_state=state
            elif (action[0]=='refuel'):
                tup_people = ()
                tup_taxi = ()
                for people in state[1]:
                    tup_people = (*tup_people, people)
                m = list(state[2][0])
                m[2] = m[4]
                new_tup = (tuple(m))
                tup_taxi=(*tup_taxi,new_tup)
                new_state = (*new_state, tup_people, tup_taxi)
            elif(action[0]=='move'):
                tup_people = ()
                tup_taxi = ()
                for passe in state[1]:
                    if passe[2] == state[2][0][3] and passe[3] == 1:
                        x = action[2][0]
                        y = action[2][1]
                        m = list(passe)
                        m[2] = (x, y)
                        new_tup = (tuple(m))
                        tup_people = (*tup_people, new_tup)
                    else:
                        tup_people = (*tup_people, passe)
                x = action[2][0]
                y = action[2][1]
                m = list(state[2][0])
                m[2]-= 1
                m[3] = (x,y)
                new_tup = (tuple(m))
                tup_taxi = (*tup_taxi, new_tup)
                new_state = (*new_state, tup_people, tup_taxi)
            elif(action[0]=='pick up'):
                for i, people in enumerate(state[1]):
                    if people[0] == action[2]:
                        m = list(state[1][i])
                        m[3] = 1
                        new_tup = (tuple(m))
                        tup_people = (*tup_people, new_tup)
                    else:
                        tup_people = (*tup_people, state[1][i])
                m = list(state[2][0])
                m[5] += 1
                new_tup = (tuple(m))
                tup_taxi = (*tup_taxi, new_tup)
                new_state = (*new_state, tup_people, tup_taxi)
            elif(action[0]=='drop off'):
                for i, people in enumerate(state[1]):
                    if action[2] ==people[0]:
                        m = list(state[1][i])
                        m[3] = 0
                        new_tup = (tuple(m))
                        tup_people = (*tup_people, new_tup)
                    else:
                        tup_people = (*tup_people, state[1][i])

                m = list(state[2][0])
                m[5] -= 1
                new_tup = (tuple(m))
                tup_taxi = (*tup_taxi, new_tup)
                new_state = (*new_state, tup_people, tup_taxi)
            state=new_state
        return state

    def goal_test(self, state):
        """ Given a state, checks if this is the goal state.
         Returns True if it is, False otherwise."""

        for passanger in state[1]:
            if (passanger[1] != passanger[2] or passanger[3] != 0):
                return False
        return True

    def h(self, node):
        if(len(node.state[2])==1):
            return 0
        sum_unpicked = 0
        sum_undelivered=0
        sum_d_from_taxi=0 ##not using
        sum_d_of_dest=0 ##not using
        sum_d_from_closest_dest=0   ## not using
        sum_d_from_client=0
        state = node.state
        # getting info of unpicked,undelivered,dist from taxi
        '''
        sum = 0
        for taxi in state[2]:
            if (taxi[2]==0):
                sum+=5
        for passenger in state[1]:
            if(passenger[1]!=passenger[2] or passenger[3]==1):
                sum+=10
                if(passenger[3]==0):
                    sum+=15
            sum += abs(passenger[1][0] - passenger[2][0])
            sum += abs(passenger[1][1] - passenger[2][1])
            return sum
            '''
        for  p in state[1]:
            if (p[1]!= p[2] or p[3]==1):
                sum_undelivered+=1
                if(p[3]==0):
                    sum_unpicked+=1
                    min_d_from_taxi=1000
                    for taxi in state[2]:
                        x=abs(p[1][0]-taxi[3][0])+abs(p[1][1]-taxi[3][1])
                        if(x<min_d_from_taxi):
                            min_d_from_taxi=x
                    sum_d_from_taxi+=min_d_from_taxi
        #getting info of destination dist
        for taxi in state[2]:
            min_dist_from_client = 100
            if(taxi[5]-taxi[1]!=0):
                for passe in state[1]:
                    if(passe[3]==0):
                        if(passe[3]==0 and passe[1]!=passe[2]):
                            x=abs(passe[2][0]-taxi[3][0])+abs(passe[2][1]-taxi[3][1])
                            if(x<min_dist_from_client):
                                min_dist_from_client=x
            if(min_dist_from_client!=100):
                sum_d_from_client+=min_dist_from_client
            on_taxi_people=[]
            max_dest_dist=0
            for i, p in enumerate(state[1]):
                if (taxi[3]==p[2] and p[3]==1):
                    on_taxi_people.append(i)
            if(len(on_taxi_people)>0):
                min_dist_dest = 1000
                for  p_number in range(len(on_taxi_people)):
                    x= abs(state[1][on_taxi_people[p_number]][1][0]-taxi[3][0])+abs(state[1][on_taxi_people[p_number]][1][1]-taxi[3][1])
                    if(x<min_dist_dest):
                        min_dist_dest=x
                sum_d_from_closest_dest+=min_dist_dest
        h=(450*sum_unpicked  + 150*sum_undelivered+sum_d_from_closest_dest +10*sum_d_from_client)

        return(h)

    def h_1(self, node):
        """
        This is a simple heuristic
        """
        sum = 0
        state = node.state
        for passenger in state[1]:
            if(passenger[1]!=passenger[2]):
                if (passenger[3] == 0):  # unpicked
                    sum += 2
                else:
                    sum += 1
        x = (sum / len(state[2]))
        return x
    def h_2(self, node):
        """
        This is a slightly more sophisticated Manhattan heuristic
        """
        state = node.state
        sum = 0
        for passenger in state[1]:
            sum += abs(passenger[1][0] - passenger[2][0])
            sum += abs(passenger[1][1] - passenger[2][1])
            return (sum / len(state[2]))

    """Feel free to add your own functions
    (-2, -2, None) means there was a timeout"""


def create_taxi_problem(game):
    return TaxiProblem(game)

