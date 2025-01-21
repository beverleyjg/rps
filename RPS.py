# The example function below keeps track of the opponent's history and plays whatever the opponent played two plays ago. It is not a very good player so you will need to change the code to pass the challenge.
import random
import numpy

def player(prev_play, opponent_history=[], own_play_history=[], own_strat_history=[], Q_table=[0 , 0 , 0 , 0 , 0 , 0], epsilon=0.7, alpha=0.9, gamma=0.0, counter=[0],
          play_order=[{
              "RR": 0,
              "RP": 0,
              "RS": 0,
              "PR": 0,
              "PP": 0,
              "PS": 0,
              "SR": 0,
              "SP": 0,
              "SS": 0,
          }],          play_order2=[{
              "RR": 0,
              "RP": 0,
              "RS": 0,
              "PR": 0,
              "PP": 0,
              "PS": 0,
              "SR": 0,
              "SP": 0,
              "SS": 0,
          }]):

    max_plays = 1000
    if (counter[0] == max_plays):
      opponent_history[:]=[]
      own_play_history[:]=[]
      own_strat_history[:]=[]
      Q_table[:] = [0,0,0,0,0,0] 
      counter[0] = 0
      for key, value in play_order[0].items():
        play_order[0][key] = 0
      for key, value in play_order2[0].items():
        play_order2[0][key] = 0
      
    opponent_history.append(prev_play)

    if counter[0] > 10:
      prev_own_play = own_play_history[-1]
      prev_action = own_strat_history[-1]
      if (prev_own_play == "P" and prev_play == "R") or (prev_own_play == "R" and prev_play == "S") or (prev_own_play == "S"
                                                        and prev_play == "P"):
        reward = 2  ## WIN
      elif (prev_own_play == prev_play):
        reward = 1 ## TIE
      else:
        reward = 0

      Q_table[prev_action] = Q_table[prev_action] + alpha*(reward + gamma*max(Q_table) - Q_table[prev_action])

    if prev_play == '':
      prev_play = "R"
    
    counter[0] += 1

    last_two2 = "".join(opponent_history[-2:])
    if len(last_two2) == 2:
        play_order2[0][last_two2] += 1
    last_two = "".join(own_play_history[-2:])
    if len(last_two) == 2:
        play_order[0][last_two] += 1

    # Choose action
    if random.uniform(0, 1) < epsilon:
      action = random.choice(range(6)) 
    else:
      action = numpy.argmax(Q_table)

    if epsilon > 0:
      epsilon = epsilon - 0.001
    else:
      epsilon = -1

    # Apply chosen strategy
    if action == 0:   ## to beat quincy's strategy
      choices = ["P", "P", "S", "S", "R"]
      move = choices[counter[0] % len(choices)]

    elif action == 1:   ## to beat abbey's strategy with something modified in prev_play record
      if counter == [1]:
        own_play_history.append('R')

      prev_own_play = own_play_history[-1]

      potential_plays = [
          prev_own_play + "R",
          prev_own_play + "P",
          prev_own_play + "S",
      ]

      sub_order = {
          k: play_order[0][k]
          for k in potential_plays if k in play_order[0]
      }

      prediction = max(sub_order, key=sub_order.get)[-1:]

      ideal_response = {'P': 'R', 'R': 'S', 'S': 'P'}
      move = ideal_response[prediction]

    elif action == 2:   ## kris's strategy
      ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}
      move = ideal_response[prev_play]

    elif action == 3:  ## mrugesh's strategy
      last_ten = opponent_history[-10:]
      most_frequent = max(set(last_ten), key=last_ten.count)

      if most_frequent == '':
          most_frequent = "S"

      ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}
      move = ideal_response[most_frequent]

    elif action == 4:
      if counter[0] < 2:
        prev_own_play = random.choice(['R', 'P', 'S'])
      else:
        prev_own_play = own_play_history[-1]
      
      ideal_response = {'P': 'R', 'R': 'S', 'S': 'P'}
      move = ideal_response[prev_own_play]

    elif action == 5:   ## abbey's strategy with something modified in prev_play record
      potential_plays = [
          prev_play + "R",
          prev_play + "P",
          prev_play + "S",
      ]

      sub_order = {
          k: play_order2[0][k]
          for k in potential_plays if k in play_order2[0]
      }

      prediction = max(sub_order, key=sub_order.get)[-1:]

      ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}
      move = ideal_response[prediction]
   
    else:
      print("Invalid action")

    own_play_history.append(move)
    own_strat_history.append(action)

    return move