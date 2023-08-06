import uuid
import json

import numpy as np

from ..file.io import read_board, write_board, read_notebook, write_notebook


def is_board(obj):
    return isinstance(obj, dict) and ("nodes" in obj) and ("edges" in obj)


def create_board():
    """Create board.

    Returns
    -------
    board :
        The newly created board.

    """
    board = {
        "nodes": [],
        "edges": []
    }
    return board


def create_card(title=None,
                content=None,
                position=None,
                size=None,
                color=None,
                card_properties=None):
    """Create a card.

    Parameters
    ----------
    title :
        The title of the card.
    content :
        The card content. A markdown string.
    position :
        The position of the card on the board.
    size :
        The size of the card.
    color :
        The color of the card.
    card_properties :
        A dictionary with additional properties to be added to the card.
        This may override any of the other card properties.

    Returns
    -------
    card :
        The card.

    """
    if title is None:
        title = ""

    if content is None:
        content = ""
    else:
        content = str(content)

    if position is None:
        position = {'x': 0.0 + np.random.randint(-100, 100),
                    'y': 0.0 + np.random.randint(-100, 100)}

    if size is None:
        size = {'width': 400,
                'height': 400}

    if color is None:
        color = '#125059'

    node_id = str(uuid.uuid4())

    card = {
        'id': node_id,
        'title': title,
        'type_specific': {'message': content},
        'edge_connections': [],
        'type': 'note',
        'position': position,
        'size': size,
        'color': color,
    }
    if card_properties is not None:
        card.update(card_properties)

    return card


def add_card_to_board(board, card):
    """Add card to board.

    Parameters
    ----------
    board :
        The board or file path or descriptor of the board to add a card to.
    card :
        The card to add.

    Returns
    -------

    """
    if is_board(board):
        board['nodes'].append(card)
    else:
        board_file = board
        board = read_board(board_file)
        board['nodes'].append(card)
        write_board(board, board_file)


def create_card_connection(board, card1_id, card2_id, card1_edge, card2_edge):
    """Add connection between two cards on a board.

    Parameters
    ----------
    board :
        The board or file path or descriptor of the board to add a card to.
    card1_id :
        The id of origin card.
    card2_id :
        The id of destination card.
    card1_edge: 'top', 'bottom', 'left', 'right'
        The edge connected to card1.
    card2_edge: 'top', 'bottom', 'left', 'right'
        The edge connected to card2.

    Returns
    -------

    """
    EDGE_INPUT_ERROR_MESSAGE = "Edge input must be 'top', 'bottom', 'left', 'right'"
    EDGE_INCOMPATIBLE_ERROR_MESSAGE = "Edges not compatible. Only (top, bottom), (bottom, top), (left/right, left/right) are allowed."

    if card1_edge not in ['top', 'bottom', 'left', 'right']:
        raise ValueError(EDGE_INPUT_ERROR_MESSAGE)
    if card2_edge not in ['top', 'bottom', 'left', 'right']:
        raise ValueError(EDGE_INPUT_ERROR_MESSAGE)

    if card1_edge == 'top':
        if card2_edge != 'bottom':
            raise ValueError(EDGE_INCOMPATIBLE_ERROR_MESSAGE)
        arrow_type = 'dashed_arrow'
    if card1_edge == 'bottom':
        if card2_edge != 'top':
            raise ValueError(EDGE_INCOMPATIBLE_ERROR_MESSAGE)
        arrow_type = 'dashed_arrow'
    if card1_edge == 'left':
        if card2_edge not in ['left', 'right']:
            raise ValueError(EDGE_INCOMPATIBLE_ERROR_MESSAGE)
        arrow_type = 'solid_arrow'
    if card1_edge == 'right':
        if card2_edge not in ['left', 'right']:
            raise ValueError(EDGE_INCOMPATIBLE_ERROR_MESSAGE)
        arrow_type = 'solid_arrow'

    connection_id = str(uuid.uuid4())
    connection = {
        'id': connection_id,
        'type': arrow_type,
        'node_connections': [
            card1_id,
            card2_id
        ],
        'type_specific': {
            'annotation': ''
        }
    }
    is_board_file = False
    if not is_board(board):
        is_board_file = True
        board_file = board
        board = read_board(board_file)

    for i, card in enumerate(board['nodes']):
        if card['id'] == card1_id:
            if 'edge_connections' not in card:
                board['nodes'][i]['edge_connections'] = []
            board['nodes'][i]['edge_connections'].append(
                {"id": connection_id, "connector": card1_edge})
        elif card['id'] == card2_id:
            if 'edge_connections' not in card:
                board['nodes'][i]['edge_connections'] = []
            board['nodes'][i]['edge_connections'].append(
                {"id": connection_id, "connector": card2_edge})

    board['edges'].append(connection)

    if is_board_file:
        write_board(board, board_file)

