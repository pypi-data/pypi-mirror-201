import textwrap
import uuid
import re

from IPython.core.oinspect import getdoc


def get_model_name(model):
    """Get model name.

    Parameters
    ----------
    model :
        The model.

    Returns
    -------
    model_name :
        The model name.

    """
    model_name = model.__class__.__name__
    model_name = re.sub(r'((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))', r' \1', model_name)
    return model_name


def get_model_description(model,
                          describe_params=True,
                          describe_data=True):
    """Get model description.

    Parameters
    ----------
    model :
        The model to describe.
    describe_params :
        Whether to describe parameters.
        The default is `True`,
    describe_data :
        Whether to describe data.
        The default is `True`,

    Returns
    -------
    description :
        The model description.

    """
    description = ""

    docstring = getdoc(model)
    if docstring is not None:

        if "Parameters" in docstring:
            ind = docstring.index("Parameters")
            docstring = docstring[:ind]

        docstring = docstring.strip("\n")

        temp_id = str(uuid.uuid4)
        docstring = (docstring.
                     replace("\n\n", f"%{temp_id}%").
                     replace("\n", " ").
                     replace(f"%{temp_id}%", "\n\n"))

        description += docstring

    if describe_params:
        params_descr = "\n\nParameters:"

        parameters = model.get_params() if hasattr(model, "get_params") else {}
        for key, value in parameters.items():
            params_descr += f"\n  {key}: {value}"

        description += params_descr

    if describe_data:
        data_descr = "\n\nData:"

        n_features = model.n_features_in_ if hasattr(model, "n_features_in_") else None
        if n_features is not None:
            data_descr += f"\n  features: {n_features}"

        feature_names = model.feature_names_in_ if hasattr(model, "feature_names_in_") else None
        if feature_names is not None:
            data_descr += f"\n  feature names:\n"
            fnms = ", ".join(feature_names)
            fnms = "\n".join(textwrap.wrap(fnms, 35))
            fnms = textwrap.indent(fnms, "    ")
            data_descr += fnms

        description += data_descr

    return description
