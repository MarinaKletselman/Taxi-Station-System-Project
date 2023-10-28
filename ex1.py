import search
import itertools

ids = ["213119142", "207283722"]


def create_permotations(actions):
    """Generate permutations from a given list of actions."""
    return (list(itertools.product(*actions)))


def check_move(state, taxi):
    """
    Check valid moves for a given taxi in the current state.

    :param state: The current state of the game, including the grid layout and the positions of taxis and passengers.
    :param taxi: A tuple representing a specific taxi and its properties.
    :return: A tuple containing possible move actions for the given taxi.
    """

    # Possible move actions are initialized as an empty tuple.
    possible_moves = ()

    # Extracting the width and length of the grid for boundary checks.
    grid_width = len(state[0][0])
    grid_length = len(state[0])

    # Extracting the current location (coordinates) of the taxi.
    taxi_location = taxi[3]

    # Checking the possibility of moving UP, ensuring it's within the grid and not into a wall ('I').
    if taxi_location[0] != 0 and state[0][taxi_location[0] - 1][taxi_location[1]] != 'I':
        new_location = (taxi_location[0] - 1, taxi_location[1])
        possible_moves = (*possible_moves, ("move", taxi[0], new_location))

    # Checking the possibility of moving DOWN.
    if taxi_location[0] != grid_length - 1 and state[0][taxi_location[0] + 1][taxi_location[1]] != 'I':
        new_location = (taxi_location[0] + 1, taxi_location[1])
        possible_moves = (*possible_moves, ("move", taxi[0], new_location))

    # Checking the possibility of moving LEFT.
    if taxi_location[1] != 0 and state[0][taxi_location[0]][taxi_location[1] - 1] != 'I':
        new_location = (taxi_location[0], taxi_location[1] - 1)
        possible_moves = (*possible_moves, ("move", taxi[0], new_location))

    # Checking the possibility of moving RIGHT.
    if taxi_location[1] != grid_width - 1 and state[0][taxi_location[0]][taxi_location[1] + 1] != 'I':
        new_location = (taxi_location[0], taxi_location[1] + 1)
        possible_moves = (*possible_moves, ("move", taxi[0], new_location))

    # Returning all possible move actions for the given taxi.
    return possible_moves


def pickup_options(state, taxi, action):
    """
    Returns actions augmented with pickup options for a taxi.

    :param state: The current state of the game, including the grid layout, positions of taxis, and passengers.
    :param taxi: A tuple representing a specific taxi and its properties.
    :param action: A tuple of current actions available to the taxi.
    :return: A tuple of actions, including pickup actions if applicable.
    """

    # Extracting the list of passengers from the state.
    passengers = state[1]

    # Initializing the result to the current set of actions.
    augmented_actions = action

    # Extracting the current location of the taxi.
    taxi_location = taxi[3]

    # Checking if the taxi has available seats for passengers.
    if (taxi[1] - taxi[5]) != 0:
        # Iterating through the list of passengers to check for potential pickups.
        for passenger in passengers:
            # Checking if a passenger is at the same location as the taxi and is waiting (not in a taxi).
            if passenger[2] == taxi_location and passenger[3] == 0:
                # Creating a pickup action tuple.
                pickup_action = ("pick up", taxi[0], passenger[0])

                # Adding the pickup action to the list of actions.
                augmented_actions = (*augmented_actions, pickup_action)

    # Returning the augmented list of actions, including pickup actions if applicable.
    return augmented_actions


def unesting(initial):
    """
    Converts nested dictionaries in 'initial' to tuples.

    :param initial: A dictionary with nested structures, representing the initial state of a game.
    :return: A tuple representation of the initial state.
    """
    # Initializing an empty tuple to hold the converted elements from the dictionary.
    tuple_initial = ()

    # Iterating through the sorted keys of the initial dictionary.
    for key in sorted(initial.keys()):

        # Converting the 'map' key’s list of lists into a tuple of tuples.
        if key == 'map':
            initial['map'] = [tuple(x) for x in initial['map']]
            tuple_initial = (*tuple_initial, tuple(initial['map']))

        # Initializing an empty tuple to hold the taxi information.
        tuple_of_taxis = ()
        # Converting the 'taxis' key's nested dictionary into a tuple of tuples.
        if key == 'taxis':
            for num, taxi_id in enumerate(sorted(initial['taxis'].keys())):
                taxi_tuple = ()
                # Adding the taxi num to the tuple.
                taxi_tuple += (sorted(initial['taxis'].keys())[num],)
                # Adding the rest of the taxi properties to the tuple.
                for property in sorted(initial['taxis'][taxi_id].keys()):
                    taxi_tuple += (initial['taxis'][taxi_id][property],)
                # Adding the taxi tuple to the tuple of taxis.
                tuple_of_taxis = (*tuple_of_taxis, taxi_tuple)
            # Adding the tuple of taxis to the initial tuple.
            tuple_initial = (*tuple_initial, tuple_of_taxis)

        # Initializing an empty tuple to hold the passenger information.
        tuple_of_people = ()
        # Converting the 'passengers' key's nested dictionary into a tuple of tuples.
        if key == 'passengers':
            for num, passenger_id in enumerate(sorted(initial['passengers'].keys())):
                passenger_tuple = ()
                # Adding the passenger ID to the tuple.
                passenger_tuple += (sorted(initial['passengers'].keys())[num],)
                # Adding the rest of the passenger properties to the tuple.
                for property in sorted(initial['passengers'][passenger_id].keys()):
                    passenger_tuple += (initial['passengers'][passenger_id][property],)
                # Adding the passenger tuple to the tuple of passengers.
                tuple_of_people = (*tuple_of_people, passenger_tuple)
            # Adding the tuple of passengers to the initial tuple.
            tuple_initial = (*tuple_initial, tuple_of_people)

    # Returning the converted tuple.
    return tuple_initial


class TaxiProblem(search.Problem):

    def __init__(self, initial):
        for passenger in initial['passengers']:
            initial['passengers'][passenger]['picked_up'] = 0  # unpicked

        for taxi in initial['taxis']:
            initial['taxis'][taxi]['num_people'] = 0  # people in the taxi
            initial['taxis'][taxi]['max_fuel'] = initial['taxis'][taxi]['fuel']
        initial2 = unesting(initial)
        self.best_state=initial2
        search.Problem.__init__(self, initial2)

    def actions(self, state):
        """
        Generates a list of possible actions that can be taken from the current state.

        :param state: The current state of the game.
        :return: A list of possible actions.
        """
        # Initialize an empty tuple to store all possible actions for each taxi.
        action_sep = ()

        # Iterate over each taxi in the state to determine possible actions.
        for taxi in state[2]:
            if isinstance(taxi, tuple):
                loc = taxi[3]  # Get the current location of the taxi.
                action = ()  # Initialize an empty tuple to store actions for this taxi.

                # Check for the possibility to drop off a passenger.
                for passenger in state[1]:
                    if passenger[1] == loc and passenger[3] == 1:
                        action = (*action, ('drop off', taxi[0], passenger[0]))

                # Check for the possibility to refuel the taxi.
                if state[0][loc[0]][loc[1]] == 'G':
                    action = (*action, ('refuel', taxi[0]))

                # Check for possible move actions if the taxi has fuel.
                if taxi[2] > 0:
                    moves = check_move(state, taxi)
                    action = (*action, *moves)

                # Check for the possibility to pick up a passenger.
                action = pickup_options(state, taxi, action)
                # Add the option to wait.
                action = (*action, ('wait', taxi[0]))
                action_sep = (*action_sep, action)

        # If there are actions for more than one taxi, generate all combinations of actions.
        if len(action_sep) > 1:
            actions = action_sep[0]
            for i in range(1, len(action_sep)):
                actions = tuple(itertools.product(actions, action_sep[i]))

            # Initialize an empty tuple to store the final actions after checking for illegal turns.
            final_actions = ()
            for action_combo in actions:
                flat_action_combo = [action for sub_tuple in action_combo for action in sub_tuple]
                if self.is_legal_turn(flat_action_combo, state):
                    final_actions = (*final_actions, flat_action_combo)
            return final_actions
        # If there is only one taxi, return its actions.
        return action_sep[0]

    def is_legal_turn(actions, state):
        """
        Check if a combination of actions is legal.

        In this context, a legal turn means that no two taxis are attempting to move into the same space at the same time,
        and no taxi is trying to pick up or drop off a passenger while moving.

        :param actions: A list of actions, where each action is a tuple (action_type, taxi_index, target_position)
        :param state: The current state of the game, where state[2] contains the taxi information.
        :return: A boolean value indicating whether the actions are legal.
        """
        # Loop through each action in the actions list
        for i, action in enumerate(actions):
            # If the current action is a 'move' action
            if action[0] == 'move':
                # Loop through the remaining actions to check for conflicts
                for j in range(i + 1, len(actions)):
                    # If another 'move' action is found
                    if actions[j][0] == 'move':
                        # Check if both 'move' actions are trying to move to the same position
                        if action[2] == actions[j][2]:
                            return False  # If so, the turn is not legal
                    # Check if a taxi is trying to pick up/drop off a passenger while moving to the position
                    elif action[2] == state[2][j][3]:
                        return False  # If so, the turn is not legal
            # If the current action is not a 'move' action (i.e., pick up or drop off)
            else:
                # Loop through the remaining actions to check for conflicts
                for j in range(i + 1, len(actions)):
                    # Check if there's a 'move' action that conflicts with the pick up/drop off action
                    if actions[j][0] == 'move' and (
                            state[2][i][3] == actions[j][2] or state[2][i][3] == state[2][j][3]):
                        return False  # If so, the turn is not legal

        # If no conflicts are found, the actions are legal
        return True

    def result(self, state, action):
        """
        This function applies an action to the state and returns the resulting state.
        :param state: The current state of the game.
        :param action: The action to be applied.
        :return: The resulting state after applying the action.
        """
        # Initialize a counter for wait actions
        count_waits = 0

        # Check if the action is a tuple, indicating multiple actions for multiple taxis
        if isinstance(action[0], tuple):
            # Iterate through each action in the tuple
            for a in action:
                # Create a new state tuple
                new_state = (state[0],)

                # If the action is "wait", increment the wait counter and skip to the next action
                if a[0] == "wait":
                    count_waits += 1
                    continue

                # Find the index of the taxi in the state that matches the taxi in the action
                taxi_num = 0
                for i, taxi in enumerate(state[2]):
                    if taxi[0] == a[1]:
                        taxi_num = i

                # If the action is not "refuel", find the index of the passenger in the state that matches the passenger in the action
                if a[0] != 'refuel':
                    for i, passenger in enumerate(state[1]):
                        if passenger[0] == a[2]:
                            passenger_num = i

                # Extract the action type from the action tuple
                action_type = a[0]

                # Initialize tuples for passengers and taxis
                tup_passengers = ()
                tup_taxis = ()

                # Handle different action types
                if action_type == "refuel":
                    # Copy all passengers and taxis to the new state, refueling the relevant taxi
                    for passenger in state[1]:
                        tup_passengers = (*tup_passengers, passenger)
                    for i, taxi in enumerate(state[2]):
                        if i == taxi_num:
                            modified_taxi = list(state[2][i])
                            modified_taxi[2] = modified_taxi[4]  # Set fuel to max capacity
                            tup_taxis = (*tup_taxis, tuple(modified_taxi))
                        else:
                            tup_taxis = (*tup_taxis, taxi)
                    new_state = (*new_state, tup_passengers, tup_taxis)

                elif action_type == "move":
                    # Handle moving a taxi and possibly a passenger inside it
                    # Move the passenger if they are in the taxi
                    for passenger in state[1]:
                        if passenger[2] == state[2][taxi_num][3] and passenger[3] == 1:
                            new_x, new_y = a[2]
                            modified_passenger = list(passenger)
                            modified_passenger[2] = (new_x, new_y)
                            tup_passengers = (*tup_passengers, tuple(modified_passenger))
                        else:
                            tup_passengers = (*tup_passengers, passenger)
                    for taxi in state[2]:
                        if taxi[0] == state[2][taxi_num][0]:
                            new_x, new_y = a[2]
                            modified_taxi = list(taxi)
                            modified_taxi[3] = (new_x, new_y)
                            modified_taxi[2] -= 1  # Decrease fuel by 1
                            tup_taxis = (*tup_taxis, tuple(modified_taxi))
                        else:
                            tup_taxis = (*tup_taxis, taxi)
                    new_state = (*new_state, tup_passengers, tup_taxis)

                elif action_type == "pick up":
                    # Handle picking up a passenger
                    for i, passenger in enumerate(state[1]):
                        if i == passenger_num:
                            modified_passenger = list(state[1][i])
                            modified_passenger[3] = 1  # Set passenger status to "in taxi"
                            tup_passengers = (*tup_passengers, tuple(modified_passenger))
                        else:
                            tup_passengers = (*tup_passengers, passenger)
                    for i, taxi in enumerate(state[2]):
                        if i == taxi_num:
                            modified_taxi = list(state[2][i])
                            modified_taxi[5] += 1  # Increase passenger count in taxi
                            tup_taxis = (*tup_taxis, tuple(modified_taxi))
                        else:
                            tup_taxis = (*tup_taxis, taxi)
                    new_state = (*new_state, tup_passengers, tup_taxis)

                elif action_type == "drop off":
                    # Handle dropping off a passenger
                    for i, passenger in enumerate(state[1]):
                        if i == passenger_num:
                            modified_passenger = list(state[1][i])
                            modified_passenger[3] = 0  # Set passenger status to "not in taxi"
                            tup_passengers = (*tup_passengers, tuple(modified_passenger))
                        else:
                            tup_passengers = (*tup_passengers, passenger)
                    for i, taxi in enumerate(state[2]):
                        if i == taxi_num:
                            modified_taxi = list(state[2][i])
                            modified_taxi[5] -= 1  # Decrease passenger count in taxi
                            tup_taxis = (*tup_taxis, tuple(modified_taxi))
                        else:
                            tup_taxis = (*tup_taxis, taxi)
                    new_state = (*new_state, tup_passengers, tup_taxis)

                # Update the state for the next iteration
                state = new_state
        else:
            # If there's only one action, handle it similarly as above but without the need for looping through taxis
            new_state = (state[0],)
            tup_taxis = ()
            tup_passengers = ()

            if action[0] == 'wait':
                new_state = state
            elif action[0] == 'refuel':
                for passenger in state[1]:
                    tup_passengers = (*tup_passengers, passenger)
                modified_taxi = list(state[2][0])
                modified_taxi[2] = modified_taxi[4]  # Refuel the taxi
                tup_taxis = (*tup_taxis, tuple(modified_taxi))
                new_state = (*new_state, tup_passengers, tup_taxis)
            elif action[0] == 'move':
                for passenger in state[1]:
                    if passenger[2] == state[2][0][3] and passenger[3] == 1:
                        new_x, new_y = action[2]
                        modified_passenger = list(passenger)
                        modified_passenger[2] = (new_x, new_y)
                        tup_passengers = (*tup_passengers, tuple(modified_passenger))
                    else:
                        tup_passengers = (*tup_passengers, passenger)
                new_x, new_y = action[2]
                modified_taxi = list(state[2][0])
                modified_taxi[2] -= 1  # Decrease fuel by 1
                modified_taxi[3] = (new_x, new_y)
                tup_taxis = (*tup_taxis, tuple(modified_taxi))
                new_state = (*new_state, tup_passengers, tup_taxis)
            elif action[0] == 'pick up':
                for passenger in state[1]:
                    if passenger[0] == action[2]:
                        modified_passenger = list(passenger)
                        modified_passenger[3] = 1  # Set passenger status to "in taxi"
                        tup_passengers = (*tup_passengers, tuple(modified_passenger))
                    else:
                        tup_passengers = (*tup_passengers, passenger)
                modified_taxi = list(state[2][0])
                modified_taxi[5] += 1  # Increase passenger count in taxi
                tup_taxis = (*tup_taxis, tuple(modified_taxi))
                new_state = (*new_state, tup_passengers, tup_taxis)
            elif action[0] == 'drop off':
                for passenger in state[1]:
                    if passenger[0] == action[2]:
                        modified_passenger = list(passenger)
                        modified_passenger[3] = 0  # Set passenger status to "not in taxi"
                        tup_passengers = (*tup_passengers, tuple(modified_passenger))
                    else:
                        tup_passengers = (*tup_passengers, passenger)
                modified_taxi = list(state[2][0])
                modified_taxi[5] -= 1  # Decrease passenger count in taxi
                tup_taxis = (*tup_taxis, tuple(modified_taxi))
                new_state = (*new_state, tup_passengers, tup_taxis)

        # If there were any "wait" actions, apply them here by copying the state and incrementing the time by the number of waits
        if count_waits > 0:
            modified_time = state[0] + count_waits
            new_state = (modified_time, *state[1:])

        return new_state

    def goal_test(self, state):
        """ Given a state, checks if this is the goal state.
         Returns True if it is, False otherwise."""

        # Iterate through all the passengers in the state
        for passenger in state[1]:  # state[1] contains the list of passengers
            # Check if any passenger has not reached their destination or is still in a taxi
            # passenger[1] is the destination of the passenger
            # passenger[2] is the current location of the passenger
            # passenger[3] is the status of the passenger (0 for not in taxi, 1 for in taxi)
            if (passenger[1] != passenger[2] or passenger[3] != 0):
                # If the passenger has not reached their destination or is still in a taxi, return False
                return False
        # If all passengers have reached their destinations and are not in taxis, return True
        return True

    def h(self, node):

        # Check if there is only one taxi in the current state if so than it is a trivial problem
        if (len(node.state[2]) == 1):
            return 0

        # Initialize variables to store different components of the heuristic.
        sum_unpicked_passengers = 0
        sum_undelivered_passengers = 0
        sum_d_from_taxi_to_passenger = 0
        sum_d_from_taxi_to_destination = 0
        state = node.state

        # Iterate through all passengers to calculate the distances and counts related to passengers.
        for passenger in state[1]:
            # If a passenger is unpicked or undelivered, increase the count.
            if passenger[1] != passenger[2] or passenger[3] == 1:
                sum_undelivered_passengers += 1
                # If a passenger is unpicked, find the closest taxi and calculate the distance.
                if passenger[3] == 0:
                    sum_unpicked_passengers += 1
                    min_d_from_taxi = min(
                        abs(passenger[1][0] - taxi[3][0]) + abs(passenger[1][1] - taxi[3][1])
                        for taxi in state[2]
                    )
                    sum_d_from_taxi_to_passenger += min_d_from_taxi

        # Iterate through all taxis to calculate distances related to taxi destinations.
        for taxi in state[2]:
            # If the taxi is occupied, calculate the distances to passenger destinations.
            if taxi[5] > 0:
                on_taxi_passengers = [passenger for passenger in state[1] if
                                      passenger[3] == 1 and passenger[2] == taxi[3]]
                if on_taxi_passengers:
                    min_d_from_taxi_to_destination = min(
                        abs(passenger[2][0] - taxi[3][0]) + abs(passenger[2][1] - taxi[3][1])
                        for passenger in on_taxi_passengers
                    )
                    sum_d_from_taxi_to_destination += min_d_from_taxi_to_destination
                # If the taxi is not full, calculate the distance to the closest unpicked passenger.
                if taxi[5] < taxi[1]:
                    min_d_from_taxi_to_passenger = min(
                        (abs(passenger[1][0] - taxi[3][0]) + abs(passenger[1][1] - taxi[3][1]))
                        for passenger in state[1] if passenger[3] == 0
                    )
                    sum_d_from_taxi_to_passenger += min_d_from_taxi_to_passenger

        # Calculate the heuristic value based on the accumulated sums.
        heuristic_value = (
                450 * sum_unpicked_passengers +
                150 * sum_undelivered_passengers +
                sum_d_from_taxi_to_destination +
                10 * sum_d_from_taxi_to_passenger
        )

        return heuristic_value

    def h_1(self, node):
        """
        This heuristic function calculates a simple score based on the number of unpicked and undelivered passengers.
        It adds 2 to the score for each unpicked passenger and 1 for each undelivered passenger.
        The final score is normalized by the number of taxis to give the average score per taxi.
        """
        total_score = 0
        state = node.state
        for passenger in state[1]:
            # Check if the passenger is either unpicked or undelivered
            if passenger[1] != passenger[2]:
                if passenger[3] == 0:  # If the passenger is unpicked
                    total_score += 2
                else:  # If the passenger is picked but undelivered
                    total_score += 1
        # Normalize the total score by the number of taxis
        average_score_per_taxi = (total_score / len(state[2]))
        return average_score_per_taxi

    def h_2(self, node):
        """
        This heuristic function calculates a Manhattan distance score for each passenger,
        representing the distance from their current position to their destination.
        The distances for all passengers are summed up and then normalized by the number of taxis
        to give the average Manhattan distance per taxi.
        """
        state = node.state
        total_manhattan_distance = 0
        for passenger in state[1]:
            # Calculate the Manhattan distance for each passenger
            total_manhattan_distance += abs(passenger[1][0] - passenger[2][0])
            total_manhattan_distance += abs(passenger[1][1] - passenger[2][1])
        # Normalize the total Manhattan distance by the number of taxis
        average_manhattan_distance_per_taxi = (total_manhattan_distance / len(state[2]))
        return average_manhattan_distance_per_taxi


def create_taxi_problem(game):
    return TaxiProblem(game)

