import csv
from collections import Counter


def apriori(dataset, min_relative_support):
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
            f.write(str(accepted_entries_counter[entry]) + ":" + list(entry)[0])
            f.write('\n')

    apriori_result = accepted_entries_counter
    with open('patterns.txt', 'w') as f:

        # save the length-1 frequent movies to this file
        for entry in accepted_entries_counter:
            f.write(str(accepted_entries_counter[entry]) + ":" + list(entry)[0])
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

    return apriori_result


# with open('./others/movies-test-subset.txt', 'r') as file:  # uncomment for test purposes
with open('movies.txt', 'r') as file:
    csv_reader = csv.reader(file, delimiter=';')
    # skip header (unneeded row)
    next(csv_reader)

    list_of_csv = list(csv_reader)
    result = apriori(dataset=list_of_csv, min_relative_support=0.05)
