"""Implements a variety of prediction models."""
from collections import Counter
from copy import deepcopy


def principal_delta(principal, other, potential):
    modification = abs(principal - other) * potential
    if other < principal:
        return principal - modification
    elif other > principal:
        return principal + (abs(other - principal) * potential)


def model_per_emotive(ensemble, emotive, potential_normalization_factor):
    """Using a Weighted Moving Average, though the 'moving' part refers to the prediction index.

    Args:
        ensemble (list, required): The prediction ensemble to use in computations
        emotive (_type_): The emotive to compute a moving average of
        potential_normalization_factor (_type_): Divisor to normailize the potential value of each prediction

    Returns:
        _type_: _description_
    """
    # using a weighted posterior_probability = potential/marginal_probability
    # FORMULA: pv + ( (Uprediction_2-pv)*(Wprediction_2) + (Uprediction_3-pv)*(Wprediction_3)... )/mp
    _found = False
    while not _found:
        for i in range(0, len(ensemble)):
            if emotive in ensemble[i]['emotives'].keys():
                _found = True
                principal_value = ensemble[i]['emotives'][emotive]  # Let's use the "best" match (i.e. first showing of this emotive) as our starting point. Alternatively, we can use,say, the average of all values before adjusting.
                break
        if i == len(ensemble) and not _found:
            return 0
        if i == len(ensemble) and _found:
            return principal_value
    # marginal_probability = sum([x["potential"] for x in ensemble])
    v = principal_value
    for x in ensemble[i + 1:]:
        if emotive in x['emotives']:
            v += (x["potential"] / potential_normalization_factor) * (principal_value - x['emotives'][emotive])
            potential_normalization_factor
    return v


def average_emotives(record):
    """
    Averages the emotives in a list (e.g. predictions ensemble or percepts).
    The emotives in the record are of type: [{'e1': 4, 'e2': 5}, {'e2': 6}, {'e1': 5 'e3': -4}]

    Args:
        record (list): List of emotive dictionaries to average emotives of

    Returns:
        dict: Dictionary of Averaged Emotives

    Example:
        ..  code-block:: python

            from ia.gaius.prediction_models import average_emotives
            record = [{'e1': 4, 'e2': 5}, {'e2': 6}, {'e1': 5 'e3': -4}]
            averages = average_emotives(record=record)

    """
    new_dict = {}
    for bunch in record:
        for e, v in bunch.items():
            if e not in new_dict:
                new_dict[e] = [v]
            else:
                new_dict[e].append(v)
    avg_dict = {}
    for e, v in new_dict.items():
        avg_dict[e] = float(sum(v) / len(v))
    return avg_dict


def bucket_predictions(ensemble):
    bucket_dict = {}

    for pred in ensemble:

        if pred['potential'] in bucket_dict.keys():
            bucket_dict[pred['potential']].append(pred)
        else:
            bucket_dict[pred['potential']] = [pred]

    new_ensemble = []
    for v in bucket_dict.values():

        singular_pred = v[0]
        singular_pred['emotives'] = average_emotives([p['emotives'] for p in v])

        new_ensemble.append(singular_pred)

    return new_ensemble


def make_modeled_emotives(ensemble):
    """
    The emotives in the ensemble are of type: 'emotives':[{'e1': 4, 'e2': 5}, {'e2': 6}, {'e1': 5 'e3': -4}]
    First calls :func:`average_emotives` on each prediction in the ensemble, then calls :func:`bucket_predictions` on the ensemble.
    After bucketing predictions, the function :func:`model_per_emotives` is called for each emotive present in the ensemble.
    Dict returned contains { emotive: model_per_emotive } for each emotive in the ensemble

    Args:
        ensemble (list): Prediction ensemble containing emotives to model

    Returns:
        dict: Dictionary of modelled emotive values
    """

    emotives_set = set()
    potential_normalization_factor = sum([p['potential'] for p in ensemble])

    filtered_ensemble = []
    for p in ensemble:
        new_record = deepcopy(p)
        new_record['emotives'] = average_emotives([new_record['emotives']])
        filtered_ensemble.append(new_record)

    filtered_ensemble = bucket_predictions(filtered_ensemble)

    for p in filtered_ensemble:
        emotives_set = emotives_set.union(p['emotives'].keys())
    return {emotive: model_per_emotive(ensemble, emotive, potential_normalization_factor) for emotive in emotives_set}


def hive_model_emotives(ensembles):
    """Compute average of emotives in model by calling :func:`average_emotives` on `ensembles`

    Args:
        ensembles (list): Prediction ensemble to compute average emotives of

    Returns:
        _type_: _description_
    """
    return average_emotives(ensembles)


def prediction_ensemble_model_classification(ensemble):
    """For classifications, we don't bother with marginal_probability because classifications are discrete symbols, not numeric values."""
    boosted_prediction_classes = Counter()
    for prediction in ensemble:
        for symbol in prediction['future'][-1]:
            if "|" in symbol:
                symbol = symbol.split("|")[-1]  # grab the value, remove the piped keys
            boosted_prediction_classes[symbol] += prediction['potential']
    if len(boosted_prediction_classes) > 0:
        return boosted_prediction_classes.most_common(1)[0][0]
    else:
        return None


def hive_model_classification(ensembles):
    """Compute the "hive predicted model classification" based on the ensembles provided from each node

    Args:
        ensembles (dict): should be dictionary of { node_name: prediction_ensemble }

    Returns:
        str: hive predicted classification
    """
    if ensembles:
        # This just takes the first "most common", even if there are multiple that have the same frequency.
        boosted_classifications = [prediction_ensemble_model_classification(c) for c in ensembles.values()]
        votes = Counter([p for p in boosted_classifications if p is not None]).most_common()
        if votes:
            return votes[0][0]
    return None
