from typing import List, Tuple, Set
from collections import Counter


# Implementation of the super-stable-matching algorithm described in
# "Stable marriage and indifference" by Robert W. Irving (1990).
# Both preference inputs should be lists of preference lists in descending order for each
# group member; the preference lists should consist of sets of indices in the opposite group
# list which are tied in priority.
def super_stable_matching(g1_prefs: List[List[Set[int]]], g2_prefs: List[List[Set[int]]]):
    pairings: Set[Tuple[int, int]] = set()  # A simple set of pairs for now

    while True:
        # Find the first unpaired member of group 1 (this_g1_index)
        paired_g1s = set(g1 for g1, _ in pairings)
        this_g1_index = next((i for i in range(len(g1_prefs)) if i not in paired_g1s), None)

        # If there are none, then all members of group 1 are paired, and we have a maximum matching.
        if this_g1_index is None:
            return pairings

        this_g1_list = g1_prefs[this_g1_index]

        # If this preference list is empty, then this member cannot be paired, so a full matching
        # cannot exist.
        if len(this_g1_list) == 0:
            return None
        else:
            # Add pairings from the member of group 1 to all first-ranked members of group 2.
            # At the same time, discard any inferior entries from the group 2 members' lists as well
            # as the corresponding entries in the group 1 lists and any pairings involving these entries.
            for this_g2_index in this_g1_list[0]:
                pairings.add((this_g1_index, this_g2_index))
                g2_list_index = next(i for i in range(len(g2_prefs[this_g2_index]))
                                     if this_g1_index in g2_prefs[this_g2_index][i])
                for inferior_g1_index in (index for i in range(g2_list_index + 1, len(g2_prefs[this_g2_index]))
                                                for index in g2_prefs[this_g2_index][i]):
                    pairings.discard((inferior_g1_index, this_g2_index))
                    for inferior_g1_pref_set in g1_prefs[inferior_g1_index]:
                        inferior_g1_pref_set.discard(this_g2_index)

                g2_prefs[this_g2_index] = g2_prefs[this_g2_index][:g2_list_index + 1]

        # Find members of group 2 which are involved in multiple pairings, and remove all
        # of their pairings.
        # Also, remove the bottom layer from such members' preference lists as well as the
        # respective preferences in group 1.
        g2_pairing_counts = Counter(g2_index for (_, g2_index) in pairings)
        for (g2_index, g2_pair_count) in g2_pairing_counts.items():
            if g2_pair_count >= 2:
                pairings_to_remove = {(g1, g2) for (g1, g2) in pairings if g2 == g2_index}
                pairings.difference_update(pairings_to_remove)

                for worst_g1_index in g2_prefs[g2_index][-1]:
                    for g1_pref_set in g1_prefs[worst_g1_index]:
                        g1_pref_set.discard(g2_index)

                g2_prefs[g2_index].pop()

        # Prune any empty tie sets from group 1 (since some set members may have been discarded).
        for g1_pref_list in g1_prefs:
            g1_pref_list[:] = [this_set for this_set in g1_pref_list if len(this_set) >= 1]


# Run a couple of test examples
if __name__ == "__main__":
    print(super_stable_matching([[{0}, {1, 2}], [{2}, {0, 1}], [{1}, {2}, {0}]],
                                [[{0}, {1}, {2}], [{2, 0}, {1}], [{1}, {2, 0}]]))
    print(super_stable_matching([[{0}, {1}], [{0}, {1}]],
                                [[{0}, {1}], [{0}, {1}]]))
