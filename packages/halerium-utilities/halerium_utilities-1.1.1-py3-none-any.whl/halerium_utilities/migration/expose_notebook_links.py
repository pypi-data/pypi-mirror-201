import copy
#import json
import os
from ..file.io import (get_board_notebook_and_text_filenames_in_tree,
                       read_notebook, write_notebook)


def expose_notebook_links(notebook, inplace=True):
    """
    Transports the notebooks links from the cell metadata to the source code.

    Parameters
    ----------
    notebook : dict
        The json structure of the notebook.
    inplace : bool, optional
        Whether to modify the notebook in-place or to return a modified copy.
        The default is True.

    Returns
    -------
    notebook : dict
        The modified notebook.
    """

    if not inplace:
        notebook = copy.deepcopy(notebook)

    for cell in notebook["cells"]:
        if "connections" in cell:
            output_links = []

            source = cell["source"]
            inserted_lines = []  # needed for corrective shifts
            # count backwards to zero to allow the popping of list elements
            for ind in range(len(cell["connections"])-1, -1, -1):
                conn = cell["connections"][ind]

                start_line = int(conn["startLine"])
                end_line = int(conn["endLine"])
                if start_line == end_line == -1:  # special case for output links
                    output_links.append(
                        conn["id"]
                    )
                    continue

                start_line = start_line - 1  # -1 to correct counting from 0 vs counting from 1
                end_line = end_line - 1  # -1 to correct counting from 0 vs counting from 1
                card_id = conn["id"]

                # need to shift the line to account for already inserted lines
                shift = sum([l < start_line for l in inserted_lines])
                start_insert = start_line + shift
                source.insert(
                    start_insert,
                    '# <halerium id="{}">\n'.format(card_id)
                )
                inserted_lines += [start_line, end_line]

                end_insert = end_line - start_line + 2 + start_insert
                # special case if a new line is added at the bottom
                # we might need a line-break in the line before
                if end_insert == len(source):
                    if not source[-1].endswith("\n"):
                        source[-1] += "\n"
                source.insert(
                    end_insert,
                    '# </halerium id="{}">\n'.format(card_id)
                )

                cell["connections"].pop(ind)  # remove the exposed connection

            for output_link_id in output_links:
                source.append(
                    '# <halerium-output id="{}"/>\n'.format(output_link_id)
                )

            cell.pop("connections")

    return notebook


def migrate_notebook_links(notebook_path, backup=False, encoding="utf-8"):
    """
    Fetches all links that are contained in the notebook cell metadata
    and puts them into the cell source code as special comments.
    Links that are migrated this way are removed from the metadata.

    Parameters
    ----------
    notebook_path : str, path
        The path of the notebook file
    backup : bool, optional
        Whether to create a backup of the unmodified notebook file.
        Will have "_backup" as a suffix.
        The default is False.
    encoding : str, optional
        The encoding of the notebook.
        The default is "utf-8".

    Returns
    -------
    None

    """
    notebook = read_notebook(notebook_path, encoding=encoding, code_format="jupyter")

    if backup:
        os.rename(notebook_path, str(notebook_path)+"_backup")

    expose_notebook_links(notebook, inplace=True)

    write_notebook(notebook, notebook_path, encoding=encoding, code_format="jupyter")


def migrate_notebooks_links_in_tree(path, backup=False, encoding="utf-8"):
    """
    Migrates the links in all notebooks in a directory tree.

    Fetches all links that are contained in the notebook cell metadata
    and puts them into the cell source code as special comments.
    Links that are migrated this way are removed from the metadata.

    Parameters
    ----------
    path : str, path
        The path of the root of the directory tree.
    backup : bool, optional
        Whether to create a backups of the unmodified notebook files.
        Will have "_backup" as a suffix.
        The default is False.
    encoding : str, optional
        The encoding of the notebook.
        The default is "utf-8".

    Returns
    -------
    None

    """
    try:
        all_notebook_paths = get_board_notebook_and_text_filenames_in_tree(path)[1]
    except Exception as e:
        print('Error retrieving notebook file names in path: {}\nError Message: {}'.format(
            path, e))
        return

    for notebook_path in all_notebook_paths:
        try:
            migrate_notebook_links(notebook_path, backup=backup, encoding=encoding)
        except Exception as e:
            print('Error exposing links in notebook {}.\n'.format(notebook_path) +
                  'Error message: {}'.format(e))
