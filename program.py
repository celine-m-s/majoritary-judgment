import random
from decimal import Decimal, ROUND_HALF_UP

##################################################
#################### VOTES SETUP #################
##################################################

VOTES = 100000
MEDIAN = VOTES/2
CANDIDATES = {          
    "hermione": "Hermione Granger", 
    "balou": "Balou", 
    "chuck-norris": "Chuck Norris", 
    "elsa": "Elsa", 
    "gandalf": "Gandalf", 
    "beyonce": "Beyoncé"
    }

MENTION = [
    "A rejeter", 
    "Insuffisant", 
    "Passable", 
    "Assez Bien", 
    "Bien", 
    "Très bien", 
    "Excellent"
    ]

def create_votes():
    votes = []
    for n in range(0, VOTES):
        votes.append({
          "hermione": random.randint(3,6), 
          "balou": random.randint(0,6), 
          "chuck-norris": random.randint(0,2), 
          "elsa": random.randint(1,2), 
          "gandalf": random.randint(3,6), 
          "beyonce": random.randint(2,6)
          })
    return votes

##################################################
#################### PROGRAM #####################
##################################################

def results_hash(votes):
    candidates_results = {}
    for vote in votes:
        for candidate in vote:
              index = vote[candidate]
              if candidate not in candidates_results:
                  candidates_results[candidate] = [0, 0, 0, 0, 0, 0, 0]
              candidates_results[candidate][index] += 1
    return candidates_results

def percent(nb, total):
  percent = (nb / total) * 100
  stri = "{0:.2f}".format(percent)
  a = float(stri)
  return a

def cumulate(numbers):
    list = []
    list.append(numbers[0])
    for i,j in enumerate(numbers):
        if i in range(1, len(numbers)):
            list.append(numbers[i] + list[i - 1])
    return list

def cumulated_percents_hash(candidates_percents):
    hash = {}
    for candidate in candidates_percents:
        hash[candidate] = cumulate(candidates_percents[candidate])
    return hash

def res_in_percents(candidates_results):
    hash = {}
    for candidate in candidates_results:
        hash[candidate] = [percent(mentions, VOTES) for mentions in candidates_results[candidate]]
    return hash


def majoritary_mentions_hash(candidates_results):
    r = {}
    for candidate in candidates_results:
        r[candidate] = {}
        cumulative_res = cumulate(candidates_results[candidate])
        cumulative_percents = cumulated_percents_hash(res_in_percents(candidates_results))
        for i in range(0, len(cumulative_res)-1):
            if MEDIAN in range(cumulative_res[i-1], cumulative_res[i]):
                r[candidate]["name"] = CANDIDATES[candidate]
                r[candidate]["mention"] = i
                r[candidate]["score"] = cumulative_percents[candidate][i]
    return r

def sort_candidates_by(hash):
    ## bubble sort here we go!
    unsorted = [[key, hash[key]["mention"], hash[key]["score"]] for key in hash]
    max_value = 0
    for i in range(0, len(unsorted) -1):
        for j in range(0, len(unsorted) -1):
            ## but we need REVERSE bubble sort ;-)
            if unsorted[j + 1][1] > unsorted[j][1]:
                ## First we check if the mention is above
                unsorted[j+1], unsorted[j] = unsorted[j], unsorted[j+1]
            elif unsorted[j + 1][1] == unsorted[j][1]:
                ## If they share the same mention, the candidate with the higher percent wins.
                if unsorted[j + 1][2] > unsorted[j][2]:
                    unsorted[j+1], unsorted[j] = unsorted[j], unsorted[j+1]
    return unsorted


def print_results(results, candidates):
    for i, n in enumerate(results):
        candidate = results[i][0]
        if results.index(n) == 0:
            print("Gagnant: {} avec {:.2f}% de mentions {} ou inférieures".format(CANDIDATES[candidate], candidates[candidate]["score"], candidates[candidate]["mention"]))
            continue
        else:
            print("- {} avec {:.2f}% de mentions {} ou inférieures".format(candidates[candidate]["name"], candidates[candidate]["score"], candidates[candidate]["mention"]))


def main():
    votes = create_votes()
    results = results_hash(votes)
    majoritary_mentions = majoritary_mentions_hash(results)
    sorted_candidates = sort_candidates_by(majoritary_mentions)
    print_results(sorted_candidates, majoritary_mentions)

if __name__ == '__main__':
    main()
