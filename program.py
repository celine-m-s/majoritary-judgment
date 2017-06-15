#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import random

# Initialize seed so we always get the same result between two runs.
# Comment this out if you want to change results between two runs.
# More on this here: http://stackoverflow.com/questions/22639587/random-seed-what-does-it-do
# random.seed(0)

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
    "Excellent",
    "Très bien",
    "Bien",
    "Assez Bien",
    "Passable",
    "Insuffisant",
    "A rejeter"
]

def create_votes():
    return [
        {
            "hermione": random.randint(0, 1),
            "balou": random.randint(2, 4),
            "chuck-norris": random.randint(4, 6),
            "elsa": random.randint(3, 4),
            "gandalf": random.randint(5, 6),
            "beyonce": random.randint(0, 2)
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

def majoritary_mentions_hash(candidates_results):
    r = {}
    for candidate, candidate_result in candidates_results.items():
        cumulated_votes = 0
        for mention, vote_count in enumerate(candidate_result):
            cumulated_votes += vote_count
            if MEDIAN < cumulated_votes:
                r[candidate] = {
                    "mention": mention,
                    "score": cumulated_votes
                }
                break
    return r

############### SORT CANDIDATES #####################

def sort_candidates_by(mentions):
    ## bubble sort here we go!
    unsorted = [(key, (mention["mention"], mention["score"])) for key, mention in mentions.items()]
    swapped = True
    while swapped:
        swapped = False
        for j in range(0, len(unsorted) - 1):
            ## but we need REVERSE bubble sort ;-)
            # (note that here we compare tuples, which is pretty neat)
            if unsorted[j+1][1] < unsorted[j][1]:
                unsorted[j+1], unsorted[j] = unsorted[j], unsorted[j+1]
                swapped = True

    # Begin another loop in case of equalty
    swapped = True
    while swapped:
        swapped = False
        for i in range(0, len(unsorted) - 1):
            if unsorted[i][1][0] == unsorted[i+1][1][0]:
                if unsorted[i+1][1][1] > unsorted[i][1][1]:
                    unsorted[i+1], unsorted[i] = unsorted[i], unsorted[i+1]
                    swapped = True

    return [
        {
            "name": candidate[0],
            "mention": candidate[1][0],
            "score": candidate[1][1],
        }
        for candidate in unsorted
    ]

############### FORMAT RESULTS #####################

def print_results(results):
    for i, result in enumerate(results):
        name = CANDIDATES[result["name"]]
        mention = MENTIONS[result["mention"]]
        score = result["score"] * 100. / VOTES
        if i == 0:
            print("Gagnant: {} avec {:.2f}% de mentions {}".format(
                name, score, mention
            ))
            continue
        else:
            print("- {} avec {:.2f}% de mentions {}".format(
                name, score, mention
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
