from .data_frame import add_card_from_data_frame
from halerium_utilities.utilities.flatten import flatten_dict


def add_card_from_runs(board,
                       title,
                       runs,
                       columns=None,
                       card_properties=None):
    """Add card with info from MLflow runs to board.

    Parameters
    ----------
    board :
        Board or file path or descriptor of the board file.
    title :
        The title of the card.
    runs :
        List or dataframe of runs.
    columns :
        List of columns to include in the card.
    card_properties :
        A dictionary with properties to be added to the card.

    Returns
    -------
    node_id :
        The unique id of the card added.

    """
    try:
        import pandas
    except ImportError:
        raise ImportError("Optional dependency `pandas` missing.")

    if not isinstance(runs, pandas.DataFrame):
        runs = [run.to_dictionary() for run in runs]
        runs = [flatten_dict({**run['info'], **run['data']}) for run in runs]
        runs = pandas.DataFrame(runs)

    card_id = add_card_from_data_frame(board=board, title=title, data=runs,
                                       columns=columns,
                                       card_properties=card_properties)

    return card_id


def add_card_from_search_runs(board,
                              title,
                              experiment_ids=None,
                              filter_string='',
                              run_view_type=1,
                              max_results=100000,
                              order_by=None,
                              columns=None,
                              card_properties=None):
    """Add card with info from MLflow runs to board.

    Search runs and add their info to a card on the board.
    For details about how runs are searched, see:
    https://www.mlflow.org/docs/latest/python_api/mlflow.html#mlflow.search_runs

    Parameters
    ----------
    board :
        Board or file path or descriptor of the board file.
    title :
        The title of the card.
    experiment_ids :
        List of experiment IDs. None will default to the active experiment.
    filter_string : str
        Filter query string, defaults to searching all runs.
    run_view_type : int
        One of enum values ACTIVE_ONLY, DELETED_ONLY, or ALL runs
        defined in mlflow.entities.ViewType.
    max_results : int
        The maximum number of runs to put in the dataframe.
        Default is 100,000 to avoid causing out-of-memory issues.
    order_by :
        List of columns to order by (e.g., “metrics.rmse”).
        The order_by column can contain an optional DESC or ASC value.
        The default is ASC.
        The default ordering is to sort by start_time DESC, then run_id.
    columns :
        List of columns to include in the card.
    card_properties :
        A dictionary with properties to be added to the card.

    Returns
    -------
    node_id :
        The unique id of the card added.

    """
    try:
        import mlflow
    except ImportError:
        raise ImportError("Optional dependency `mlflow` missing.")

    runs = mlflow.search_runs(experiment_ids=experiment_ids,
                              filter_string=filter_string,
                              run_view_type=run_view_type,
                              max_results=max_results,
                              order_by=order_by)

    node_id = add_card_from_runs(board=board,
                                 title=title,
                                 runs=runs,
                                 columns=columns,
                                 card_properties=card_properties)

    return node_id
