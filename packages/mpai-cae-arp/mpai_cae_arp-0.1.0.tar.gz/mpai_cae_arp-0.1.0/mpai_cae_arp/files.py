import json
import yaml


def get_file_content(file_name: str, format: str) -> dict:
    """
    Parameters
    ----------
    file_name : str
        the path to the file to read
    format : str
        the format of the file to read (yaml or json)
    
    Raises
    ------
    ValueError
        if the format is not supported
    
    Returns
    -------
    dict
        the parsed content of the file
    """

    with open(file_name) as fd:
        if format == "yaml":
            content = yaml.safe_load(fd)
            return content
        elif format == "json":
            content = json.load(fd)
        else:
            raise ValueError("Format not supported")

    return content
