from halerium_utilities.file.io import read_board, write_board, get_board_notebook_and_text_filenames_in_tree

from copy import deepcopy


def capitalize_titles_in_board(board, inplace=False):
    """Capitalize the title of nodes in a board.

    Parameters
    ----------
    board :
        The board for which to change the titles of the nodes.
    inplace :
        Whether to capitalize titles in place.

    Returns
    -------
    board :
        The board with the title of every node capitalized.

    """
    if not inplace:
        board = deepcopy(board)

    if 'nodes' not in board:
        raise Exception("Board does not contain key 'nodes'")

    try:
        for node in board['nodes']:
            if node['type'] == 'note':
                node['title'] = node['title'].upper()
    except TypeError:
        raise Exception("Node in board['nodes'] is not iterable")
    except KeyError as e:
        print(e)
        raise Exception(
            "Node does not contain either 'type' or 'title' as its key")

    return board


def capitalize_titles_in_board_file(board_file_name, new_board_file_name):
    """Capitalize the title of nodes in board file.

    Parameters
    ----------
    board_file_name :
        The file to read the board from.
    new_board_file_name :
        The file to write the board with capitalized nodes to.

    Returns
    -------

    """
    board = read_board(board_file_name)

    board = capitalize_titles_in_board(board, inplace=True)

    write_board(board, new_board_file_name)


def capitalize_titles_in_board_file_tree(path):
    """Capitalize the title of nodes in directory tree.

    Capitalize the title of all cards in all board files in a directory tree.
    The nodes are capitalized in-place.

    Parameters
    ----------
    path :
        The root of the directory tree.

    Returns
    -------

    """
    try:
        board_paths = get_board_notebook_and_text_filenames_in_tree(path)[0]
    except Exception as e:
        print('Error retrieving board file names in path: {}\nError Message: {}'.format(
            path, e))
        return

    for board_path in board_paths:
        try:
            capitalize_titles_in_board_file(board_path, board_path)
        except Exception as e:
            print('Error capitalizing card titles in board {}.\n'.format(board_path) +
                  'Error message: {}'.format(e))
