import csv
from operator import itemgetter
from itertools import combinations
from collections import Counter
from tkinter.constants import END


def apriori(dataset, min_relative_support, gui_result_area):
    support = int(min_relative_support * len(dataset))

    unique_entries = []
    for row in dataset:
        for entry in row:
            if entry not in unique_entries:
                unique_entries.append(entry)
    unique_entries = sorted(unique_entries)

    entries_counter = Counter()
    for entry in unique_entries:
        for row in dataset:
            if entry in row:
                entries_counter[entry] += 1

    accepted_entries_counter = Counter()
    for entry in entries_counter:
        if entries_counter[entry] >= support:
            accepted_entries_counter[frozenset([entry])] += entries_counter[entry]

    # save the length-1 frequent movies to a file
    with open('oneItems.txt', 'w') as f:
        for entry in accepted_entries_counter:
            f.write(str(accepted_entries_counter[entry]) + ':' + list(entry)[0])
            f.write('\n')
    write_output(
        '1. Length-1 frequent itemsets together with their absolute supports were saved to the file: oneItems.txt',
        gui_result_area)

    apriori_result = accepted_entries_counter
    with open('patterns.txt', 'w') as f:

        # save the length-1 frequent movies to this file
        for entry in accepted_entries_counter:
            f.write(str(accepted_entries_counter[entry]) + ':' + list(entry)[0])
            f.write('\n')

        count = 2
        while True:
            count_length_collection = set()
            accepted_entries_list = list(accepted_entries_counter)

            for i in range(0, len(accepted_entries_list)):
                for j in range(i + 1, len(accepted_entries_list)):
                    temp = accepted_entries_list[i].union(accepted_entries_list[j])
                    if len(temp) == count:
                        count_length_collection.add(temp)

            entries_counter = Counter()
            for entry in count_length_collection:
                entries_counter[entry] = 0
                for row in dataset:
                    temp = set(row)
                    if entry.issubset(temp):
                        entries_counter[entry] += 1

            accepted_entries_counter = Counter()
            for entry in entries_counter:
                if entries_counter[entry] >= support:
                    accepted_entries_counter[entry] += entries_counter[entry]

            # stop when no other frequent set can be found, meaning that the maximal frequent itemsets were found
            if len(accepted_entries_counter) == 0:
                break

            # save all frequent movies to a file
            for entry in accepted_entries_counter:
                f.write(str(accepted_entries_counter[entry]) + ':' + ';'.join(list(entry)))
                f.write('\n')

            count += 1
            apriori_result = accepted_entries_counter
    write_output('2. All frequent itemsets together with their absolute supports were saved to the file: patterns.txt',
                 gui_result_area)

    return apriori_result


# TODO: implement lift, for this probably the patterns file will be needed
def compute_association_rules(dataset, apriori_result, min_confidence, gui_result_area):
    rules = []

    for entry in apriori_result:
        combination_list = [frozenset(i) for i in combinations(entry, len(entry) - 1)]

        for a in combination_list:
            b = entry - a
            ab_union = entry

            ab_count = 0
            a_count = 0
            b_count = 0

            for row in dataset:
                temp = set(row)

                if a.issubset(temp):
                    a_count += 1
                if b.issubset(temp):
                    b_count += 1
                if ab_union.issubset(temp):
                    ab_count += 1

            if ab_count / a_count >= min_confidence:
                rules.append([ab_count / a_count, ';'.join(list(a)) + '->' + ';'.join(list(b))])
            if ab_count / b_count >= min_confidence:
                rules.append([ab_count / b_count, ';'.join(list(b)) + '->' + ';'.join(list(a))])

    rules.sort(key=itemgetter(0), reverse=True)

    # save the association rules, in the descending order of the confidence percentages
    with open('associationRules.txt', 'w') as f:
        for entry in rules:
            f.write(str(round(entry[0], 6)) + ':' + entry[1])
            f.write('\n')
    write_output(
        '3. The association rules together with their confidences, antecedents and consequents were saved to the file: associationRules.txt',
        gui_result_area)


def start_data_mining(gui_result_area):
    # with open('./others/movies-test-subset.txt', 'r') as file:  # uncomment for test purposes
    with open('movies.txt', 'r') as file:
        write_output('Data mining process has started...', gui_result_area)
        csv_reader = csv.reader(file, delimiter=';')

        # skip header (unneeded row)
        next(csv_reader)

        list_of_csv = list(csv_reader)
        apriori_result = apriori(dataset=list_of_csv, min_relative_support=0.05, gui_result_area=gui_result_area)
        compute_association_rules(dataset=list_of_csv, apriori_result=apriori_result, min_confidence=0.6,
                                  gui_result_area=gui_result_area)


def get_length_itemsets(itemset_length, gui_result_area):
    write_output('The itemsets of length ' + str(itemset_length) + ' are the following:\n', gui_result_area)
    length_itemset_found = False

    with open('patterns.txt', 'r') as f:
        for line in f:
            if line.count(';') == itemset_length:
                length_itemset_found = True
                write_output('[' + line.split(';', maxsplit=1)[1][0:-1] + ']', gui_result_area)

    if not length_itemset_found:
        write_output('No itemset of length ' + str(itemset_length) + ' was found.', gui_result_area)


def movie_recommendation():
    association_rules = []
    with open('associationRules.txt', 'r') as f:
        for line in f:
            rule = line.strip().split(':', maxsplit=1)[1].split('->')
            association_rules.append([[i.lower() for i in rule[0].split(';')], rule[1].split(';')])

    unique_movies = []
    with open('oneItems.txt', 'r') as f:
        for line in f:
            movie = line.strip().split(':', maxsplit=1)[1]
            unique_movies.append(movie)

    print('\nWelcome to movie recommendation!\nHere is the list of movies from our database: ' +
          str(unique_movies)[1:-1] + '\nIf you want to exit the program, input "quit".\n')

    while True:
        print('\nInput some movies that you enjoy, separating them by a ";":\n')
        input_list = input()

        if input_list == 'quit' or input_list == 'q':
            break

        # strip the leading/trailing whitespaces and lower case the input
        movies = set([i.strip().lower() for i in input_list.split(';')])

        result = None
        previous_results = []
        recommendation_found = False

        for i in range(len(association_rules) - 1):
            rule = association_rules[i]

            if movies.issubset(set(rule[0])):
                result = str(rule[1])[1:-1]

                if result.lower() not in previous_results:
                    recommendation_found = True
                    print('The movie recommendation result: ' + result + '\n')

            # "try again" mechanism
            if recommendation_found:
                print('\nShould we try giving a new recommendation? Answer with: "yes" or "no"')
                try_again_confirmation = input()

                if try_again_confirmation == 'yes' or try_again_confirmation == 'y':
                    previous_results.append(result.lower())
                    recommendation_found = False
                else:
                    break

        # if a recommendation wasn't found for the entire input, start iterating through the input entries and make recommendations for them
        if not recommendation_found and len(movies) > 1:
            # add the input entries in the previous_results list, after transforming them to the same form
            previous_results.extend(["'" + j + "'" for j in movies])

            for i in range(len(association_rules) - 1):
                rule = association_rules[i]

                for movie in movies:
                    if movie in rule[0]:
                        result = str(rule[1])[1:-1]

                        if result.lower() not in previous_results:
                            recommendation_found = True
                            print('The movie recommendation result: ' + result + '\n')

                    # "try again" mechanism
                    if recommendation_found:
                        print('\nShould we try giving a new recommendation? Answer with: "yes" or "no"')
                        try_again_confirmation = input()

                        if try_again_confirmation == 'yes' or try_again_confirmation == 'y':
                            previous_results.append(result.lower())
                            recommendation_found = False
                        else:
                            break

                if recommendation_found:
                    break

        if not recommendation_found:
            print('We are sorry, but no recommendation could be found for your input.')


def write_output(text, gui_result_area):
    if gui_result_area is not None:
        gui_result_area.insert(END, text)
    else:
        print(text)

# The most relevant functions are the following:
# start_data_mining(None)  # used to start the actual data mining
# get_length_itemsets(1, None)  # used to get the n-length itemsets
movie_recommendation()  # used to make a movie recommendation
