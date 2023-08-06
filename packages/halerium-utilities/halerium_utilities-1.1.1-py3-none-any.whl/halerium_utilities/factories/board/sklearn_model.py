import re

from halerium_utilities.board.board import create_card, add_card_to_board
from halerium_utilities.utilities.model_description import get_model_description


def add_card_from_sklearn_model(board,
                                title,
                                model,
                                describe_params=True,
                                describe_data=True,
                                card_properties=None):
    """Add card with info from sklearn model to board.

    Parameters
    ----------
    board :
        Board or file path or descriptor of the board file.
    title :
        The title of the card.
    model :
        The model.
    describe_params : bool
        Whether to describe model parameters.
    describe_data : bool
        Whether to describe data.
    card_properties :
        A dictionary with properties to be added to the card.

    Returns
    -------
    node_id :
        The unique id of the card added.

    """
    model_name = model.__class__.__name__
    model_name = re.sub(r'((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))', r' \1', model_name)

    description = get_model_description(model,
                                        describe_params=describe_params,
                                        describe_data=describe_data)

    content = f"#### {model_name}\n"
    content += description

    card = create_card(title=title, content=content, card_properties=card_properties)
    add_card_to_board(board=board, card=card)
    return card['id']
