"""Utilities for PVT computations"""
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
from numpy import nan
from ia.gaius.prediction_models import average_emotives


def retrieve_emotive_val(emotive_name, actual):
    """Function to parse out emotive value from "actual" response.
    If emotive not present, return NaN

    Args:
        emotive_name (str): name of emotive to retrieve
        actual (dict): dictionary of actual emotive values from test record

    Returns:
        float: value of the specified emotive, or NaN if not present
    """
    if emotive_name in actual:
        return actual[emotive_name]
    else:
        return nan


def init_emotive_on_node(emotive: str, node: str, test_step_info: dict):
    """Helper function to initialize emotive information for live messages.
    Used if new emotive is encountered during testing
    (emotive only seen in specific records, not consistently across all)

    Args:
        emotive (str): emotive name
        node (str): node to initialize emotive on
        test_step_info (dict): dictionary of live information, which should
            be initialized with new emotive
    """
    test_step_info['true_positive'][node][emotive] = 0
    test_step_info['response_counts'][node][emotive] = 0
    test_step_info['true_positive'][node][emotive] = 0
    test_step_info['true_negative'][node][emotive] = 0
    test_step_info['false_positive'][node][emotive] = 0
    test_step_info['false_negative'][node][emotive] = 0
    return


def emotives_value_metrics_builder(lst_of_emotives: list) -> dict:
    """Create Metrics Data Structure for each emotive in testset

    Args:
        lst_of_emotives (list): emotives list to populate data structure

    Returns:
        dict: emotive metrics data structure
    """
    emotives_metrics_data_structure = {}
    for emotive in lst_of_emotives:
        emotives_metrics_data_structure[emotive] = {
            "predictions": [],
            "actuals": [],
            "metrics": {
                "resp_pc": None,  # response rate percentage
                "rmse": None,
                "smape_prec": None
            }
        }
    return emotives_metrics_data_structure


def emotives_polarity_metrics_builder(lst_of_emotives: list) -> dict:
    """
    Create Metrics Data Structure for each emotive in testset
    """
    emotives_metrics_data_structure = {}
    for emotive in lst_of_emotives:
        emotives_metrics_data_structure[emotive] = {
            "predictions": [],
            "actuals": [],
            "metrics": {
                "resp_pc": None,
                "accuracy": None,
                "precision": None
            }
        }
    return emotives_metrics_data_structure


def classification_metrics_builder(lst_of_labels: list) -> dict:
    """Create Metrics Data Structure for a classification problem
    where labels are tracked and used.

    Args:
        lst_of_labels (list): list of class labels

    Returns:
        dict: Classification data structure
    """
    classification_metrics_data_structure = {
        'predictions': [],
        'actuals': [],
        'labels': list(lst_of_labels) + ['UNKNOWN'],
        'metrics': {
            'resp_pc': None,
            'accuracy': None,
            'precision': None
        }
    }
    return classification_metrics_data_structure


def model_per_emotive_(ensemble: dict,
                       emotive: str,
                       potential_normalization_factor: float) -> float:
    """Using a Weighted Moving Average, though the 'moving' part
    refers to the prediction index.

    Args:
        ensemble (dict): prediction ensemble used to model
        emotive (str): emotive name to to model
        potential_normalization_factor (float): normalization factor

    Returns:
        float: final emotive modelled value
    """
    # using a weighted posterior_probability = potential/marginal_probability
    # FORMULA: pv + ( (Uprediction_2-pv)*(Wprediction_2) + (Uprediction_3-pv)*(Wprediction_3)... )/mp
    # A Weighted Moving Average puts more weight on recent data and less on past data. This is done by multiplying each bar’s price by a weighting factor. Because of its unique calculation, WMA will follow prices more closely than a corresponding Simple Moving Average.
    # https://www.fidelity.com/learning-center/trading-investing/technical-analysis/technical-indicator-guide/wma#:~:text=Description,a%20corresponding%20Simple%20Moving%20Average.
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
    marginal_probability = sum([x["potential"] for x in ensemble])  # NOTE: marginal_probability = mp, this might the wrong calculation for this variable.
    weighted_moving_value = 0  # initialized top portion of summation
    for x in ensemble[i + 1:]:
        if emotive in x['emotives']:
            weighted_moving_value += (x['emotives'][emotive] - (principal_value)) * ((x["potential"] / potential_normalization_factor))
    weighted_moving_emotive_average = principal_value + (weighted_moving_value / marginal_probability)
    return weighted_moving_emotive_average


def make_modeled_emotives_(ensemble):
    '''The emotives in the ensemble are of type: 'emotives':[{'e1': 4, 'e2': 5}, {'e2': 6}, {'e1': 5 'e3': -4}]'''
    emotives_set = set()
    potential_normalization_factor = sum([p['potential'] for p in ensemble])

    filtered_ensemble = []
    for p in ensemble:
        new_record = p
        new_record['emotives'] = average_emotives([p['emotives']])  # AVERAGE
        filtered_ensemble.append(new_record)

    # filtered_ensemble = bucket_predictions(filtered_ensemble) # BUCKET

    for p in filtered_ensemble:
        emotives_set = emotives_set.union(p['emotives'].keys())
    return {emotive: model_per_emotive_(ensemble, emotive, potential_normalization_factor) for emotive in emotives_set}


def plot_confusion_matrix(test_num: int, class_metrics_data_structures: dict):
    """
    Takes a node classification test to create a confusion matrix.
    This version includes the i_dont_know or unknown label.
    """

    for node_name, class_metrics_data in class_metrics_data_structures.items():
        print(f'-------------Test#{test_num}-{node_name}-Plots-------------')
        sorted_labels = sorted(class_metrics_data['labels'])
        cm = confusion_matrix(class_metrics_data['actuals'],
                              class_metrics_data['predictions'],
                              labels=sorted_labels)
        disp = ConfusionMatrixDisplay(confusion_matrix=cm,
                                      display_labels=sorted_labels)
        disp.plot()
        if is_notebook():
            plt.show()
        else:
            cf_filename = f'confusion_matrix_{node_name}_test_{test_num}.png'
            print(f'attempting to save confusion_matrix to: {cf_filename}')
            plt.savefig(cf_filename)

def is_notebook() -> bool:
    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True   # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False      # Probably standard Python interpreter