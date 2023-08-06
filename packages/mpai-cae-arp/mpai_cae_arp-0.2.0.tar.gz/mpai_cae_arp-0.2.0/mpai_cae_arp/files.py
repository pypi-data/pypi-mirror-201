from io import TextIOWrapper
from enum import Enum
import json
import yaml
from pydantic import BaseModel


class FileAction(Enum):
    READ = "r"
    WRITE = "w"
    APPEND = "a"


class FileType(Enum):
    YAML = "yaml"
    JSON = "json"


class File(BaseModel):
    encoding: str
    format: FileType
    path: str

    def __init__(self, path: str, filetype: FileType, encoding: str = 'utf-8'):
        super().__init__(path=path, format=filetype, encoding=encoding)

    def open(self, action: FileAction) -> TextIOWrapper:
        """
        Open the file with the given action        

        Parameters
        ----------
        action : FileAction
            the action to perform on the file at opening

        Returns
        -------
        TextIOWrapper
            the file descriptor
        """
        return open(self.path, action.value, encoding=self.encoding)

    def get_content(self) -> dict:
        """
        Return the file content

        Raises
        ------
        ValueError
            if the format is not supported
        
        Returns
        -------
        dict
            the parsed content of the file
        """
        with self.open(FileAction.READ) as fd:
            if self.format == FileType.YAML:
                content = yaml.safe_load(fd)
                return content
            if self.format == FileType.JSON:
                content = json.load(fd)
            else:
                raise ValueError("Format not supported")

        return content

    def write_content(self, content: dict) -> None:
        """
        Write the given content in the file

        Parameters
        ----------
        content : dict
            the content to write in the file
        """
        with self.open(FileAction.WRITE) as fd:
            if self.format == FileType.YAML:
                yaml.safe_dump(content, fd)
            elif self.format == FileType.JSON:
                json.dump(content, fd)
            else:
                raise ValueError("Format not supported")
