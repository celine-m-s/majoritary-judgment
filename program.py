#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import random

# Initialize seed so we always get the same result between two runs.
# Comment this out if you want to change results between two runs.
random.seed(0)

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

MENTIONS = [
    "A rejeter",
    "Insuffisant",
    "Passable",
    "Assez Bien",
    "Bien",
    "Très bien",
    "Excellent"
    ]

def create_votes():
    return [
        {
            "hermione": random.randint(3, 6),
            "balou": random.randint(0, 6),
            "chuck-norris": random.randint(0, 2),
            "elsa": random.randint(1, 2),
            "gandalf": random.randint(3, 6),
            "beyonce": random.randint(2, 6)
        } for _ in range(0, VOTES)
    ]

##################################################
#################### FUNCTIONS ###################
##################################################

############### CREATE ARRAY #####################

def results_hash(votes):
    """ Count votes per candidate and per mention

    Returns a dict of candidate names containing vote arrays.
    """
    candidates_results = {
        candidate: [0]*len(MENTIONS)
        for candidate in CANDIDATES.keys()
    }
    for vote in votes:
        for candidate, index in vote.items():
            candidates_results[candidate][index] += 1
    return candidates_results

############### CALCULATE MEDIAN ##################

def percent(nb, total):
    # I don't understand why this is useful. If you want to keep only the first
    # two decimals of a float, it's better to do: return int(number*100)/100
    # I suggest you get rid of this function.
    # return nb * 100. / total
    stri = "{0:.2f}".format((nb / total) * 100)
    a = float(stri)
    return a

def cumulate(numbers):
    cumulated = [numbers[0]] * len(numbers)
    for i in range(1, len(numbers)):
        cumulated[i] = numbers[i] + cumulated[i - 1]
    return cumulated

def cumulated_percents_hash(candidates_percents):
    result = {}
    for candidate in candidates_percents:
        result[candidate] = cumulate(candidates_percents[candidate])
    return result

def res_in_percents(candidates_results):
    result = {}
    for candidate in candidates_results:
        result[candidate] = [percent(mentions, VOTES) for mentions in candidates_results[candidate]]
    return result


def majoritary_mentions_hash(candidates_results):
    r = {}
    results_in_percent = res_in_percents(candidates_results)
    cumulative_percents = cumulated_percents_hash(results_in_percent)
    for candidate, candidate_result in candidates_results.items():
        r[candidate] = {}
        cumulative_res = cumulate(candidate_result)
        for i in range(0, len(cumulative_res) - 1):
            if cumulative_res[i-1] <= MEDIAN < cumulative_res[i]:
                r[candidate]["name"] = CANDIDATES[candidate]
                r[candidate]["mention"] = i
                r[candidate]["score"] = cumulative_percents[candidate][i]
    return r

############### SORT CANDIDATES #####################

def sort_candidates_by(mentions):
    ## bubble sort here we go!
    unsorted = [[key, mentions[key]["mention"], mentions[key]["score"]] for key in mentions]
    for _ in range(0, len(unsorted) - 1):
        for j in range(0, len(unsorted) - 1):
            ## but we need REVERSE bubble sort ;-)
            if unsorted[j + 1][1] > unsorted[j][1]:
                ## First we check if the mention is above
                unsorted[j+1], unsorted[j] = unsorted[j], unsorted[j+1]
            elif unsorted[j + 1][1] == unsorted[j][1]:
                ## If they share the same mention, the candidate with the higher percent wins.
                if unsorted[j + 1][2] > unsorted[j][2]:
                    unsorted[j+1], unsorted[j] = unsorted[j], unsorted[j+1]
    return unsorted

############### FORMAT RESULTS #####################

def print_results(results, candidates):
    for i, result in enumerate(results):
        candidate = result[0]
        if i == 0:
            print("Gagnant: {} avec {:.2f}% de mentions {} ou inférieures".format(
                CANDIDATES[candidate],
                candidates[candidate]["score"],
                MENTIONS[candidates[candidate]["mention"]]
            ))
            continue
        else:
            print("- {} avec {:.2f}% de mentions {} ou inférieures".format(
                candidates[candidate]["name"],
                candidates[candidate]["score"],
                MENTIONS[candidates[candidate]["mention"]]
            ))


##################################################
#################### MAIN FUNCTION ###############
##################################################

def main():
    votes = create_votes()
    results = results_hash(votes)
    majoritary_mentions = majoritary_mentions_hash(results)
    sorted_candidates = sort_candidates_by(majoritary_mentions)
    print_results(sorted_candidates, majoritary_mentions)

if __name__ == '__main__':
    main()
