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
        for candidate, mention in vote.items():
            candidates_results[candidate][mention] += 1
    return candidates_results

############### CALCULATE MEDIAN ##################

def cumulate(numbers):
    cumulated = [numbers[0]] * len(numbers)
    for i in range(1, len(numbers)):
        cumulated[i] = numbers[i] + cumulated[i - 1]
    return cumulated

def majoritary_mentions_hash(candidates_results):
    r = {}
    for candidate, candidate_result in candidates_results.items():
        cumulative_res = cumulate(candidate_result)
        for i in range(0, len(cumulative_res) - 1):# bug?
            if cumulative_res[i-1] <= MEDIAN < cumulative_res[i]:
                r[candidate] = {
                    "mention": i,
                    "score": cumulative_res[i]
                }
                break
    return r

############### SORT CANDIDATES #####################

def sort_candidates_by(mentions):
    ## bubble sort here we go!
    unsorted = [[key, mention["mention"], mention["score"]] for key, mention in mentions.items()]
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

def print_results(results):
    for i, result in enumerate(results):
        candidate = result[0]
        mention = MENTIONS[result[1]]
        score = result[2] * 100. / VOTES
        if i == 0:
            print("Gagnant: {} avec {:.2f}% de mentions {} ou inférieures".format(
                CANDIDATES[candidate], score, mention
            ))
            continue
        else:
            print("- {} avec {:.2f}% de mentions {} ou inférieures".format(
                CANDIDATES[candidate], score, mention
            ))


##################################################
#################### MAIN FUNCTION ###############
##################################################

def main():
    votes = create_votes()
    results = results_hash(votes)
    majoritary_mentions = majoritary_mentions_hash(results)
    sorted_candidates = sort_candidates_by(majoritary_mentions)
    print_results(sorted_candidates)

if __name__ == '__main__':
    main()
