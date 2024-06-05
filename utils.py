from itertools import combinations


def findPairs(cards):
    count = 0
    values = [10 if card.value > 10 else card.value for card in cards]  # Adjusting card values for face cards
    for value in set(values):
        occurrences = values.count(value)
        if occurrences > 1:
            count += (occurrences * (occurrences - 1)) // 2
    return 2 * count


def findRuns(cards):
    score = 0
    # Adjusting card values for face cards
    adjusted_cards = [{'value': 10 if card.value > 10 else card.value, 'suit': card.suit} for card in cards]
    sorted_cards = sorted(adjusted_cards, key=lambda x: x['value'])
    length = len(sorted_cards)
    for run_length in range(3, length + 1):
        for start in range(length - run_length + 1):
            run = sorted_cards[start:start + run_length]
            if all(run[i]['value'] - run[i - 1]['value'] == 1 for i in range(1, run_length)):
                score += run_length
    return score


def isRun(cards):
    if len(cards) < 3:
        return False
    sorted_cards = sorted(cards, key=lambda x: x.value)
    return all(sorted_cards[i].value - sorted_cards[i - 1].value == 1 for i in range(1, len(sorted_cards)))


def findFifteens(cards):
    score = 0
    # Adjusting card values for face cards
    # adjusted_values = [10 if card.value > 10 else card.value for card in cards]
    for r in range(2, len(cards) + 1):
        for combo in combinations(cards, r):
            if sum(10 if card.value > 10 else card.value for card in combo) == 15:
                score += 2
    return score


def scoreFlush(hand, starter_card):
    if all(card.suit == hand[0].suit for card in hand):
        return 5 if all(card.suit == starter_card.suit for card in hand + [starter_card]) else 4
    return 0


def scoreNobs(hand, starter_card):
    return 1 if any(card.name == 'Jack' and card.suit == starter_card.suit for card in hand) else 0


def score_hand(hand, starter_card):
    total_score = 0
    all_cards = hand + [starter_card]

    total_score += findPairs(all_cards)
    total_score += findRuns(all_cards)
    total_score += findFifteens(all_cards)
    total_score += scoreFlush(hand, starter_card)
    total_score += scoreNobs(hand, starter_card)

    return total_score


def calculatePotentialScore(cards):
    score = 0
    score += findFifteens(cards)
    score += findPairs(cards)
    score += findRuns(cards)
    return score


def evaluateCardScore(card, current_total, history):
    potential_score = 0

    # Calculate new total
    new_total = current_total + card.value

    # Score for reaching 15 or 31
    if new_total == 15 or new_total == 31:
        potential_score += 2

    # Evaluating potential for pairs, triples, and quadruples
    same_value_count = sum(1 for h_card in history if h_card.value == card.value)
    if same_value_count == 1:
        potential_score += 2  # Pair
    elif same_value_count == 2:
        potential_score += 6  # Triple
    elif same_value_count == 3:
        potential_score += 12  # Quadruple

    # Evaluating runs, considering the current card with the history
    all_cards = history + [card]
    for length in range(3, len(all_cards) + 1):  # Runs must be at least 3 cards long
        for subset in combinations(all_cards, length):
            if isRun(list(subset)):
                potential_score += length  # Score equals the length of the run

    return potential_score


def defensiveScore(card, current_total, history):
    risky_score = 0
    new_total = current_total + card.value

    if new_total == 15 or new_total == 31:
        risky_score += 2

    if any(h_card.value == card.value for h_card in history):
        risky_score += 2

    potential_run_completion = [card.value - 1, card.value + 1]
    for potential_value in potential_run_completion:
        if any(h_card.value == potential_value for h_card in history):
            risky_score += 1

    return -risky_score
