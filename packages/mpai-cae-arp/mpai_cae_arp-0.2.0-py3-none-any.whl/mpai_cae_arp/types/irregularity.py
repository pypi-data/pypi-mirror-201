import uuid
from enum import Enum
from typing import Annotated
from pydantic import BaseModel, Field

from mpai_cae_arp.audio.standards import EqualizationStandard, SpeedStandard


class IrregularityType(Enum):
    BRANDS_ON_TAPE = "b"
    SPLICE = "sp"
    START_OF_TAPE = "sot"
    ENDS_OF_TAPE = "eot"
    DAMAGED_TAPE = "da"
    DIRT = "di"
    MARKS = "m"
    SHADOWS = "s"
    WOW_AND_FLUTTER = "wf"
    PLAY_PAUSE_STOP = "pps"
    SPEED = "ssv"
    EQUALIZATION = "esv"
    SPEED_AND_EQUALIZATION = "ssv"
    BACKWARD = "sb"


class Source(Enum):
    AUDIO = "a"
    VIDEO = "v"
    BOTH = "b"


class IrregularityProperties(BaseModel):
    reading_speed: SpeedStandard
    reading_equalisation: EqualizationStandard
    writing_speed: SpeedStandard
    writing_equalisation: EqualizationStandard

    @staticmethod
    def from_json(json_property: dict):
        return IrregularityProperties(
            reading_speed=SpeedStandard(json_property["ReadingSpeedStandard"]),
            reading_equalisation=EqualizationStandard(
                json_property["ReadingEqualisationStandard"]),
            writing_speed=SpeedStandard(json_property["WritingSpeedStandard"]),
            writing_equalisation=EqualizationStandard(
                json_property["WritingEqualisationStandard"]))

    def to_json(self):
        return {
            "ReadingSpeedStandard": self.reading_speed.value,
            "ReadingEqualisationStandard": self.reading_equalisation.value,
            "WritingSpeedStandard": self.writing_speed.value,
            "WritingEqualisationStandard": self.writing_equalisation.value,
        }


class Irregularity(BaseModel):
    irregularity_ID: uuid.UUID
    source: Source
    time_label: str
    irregularity_type: IrregularityType = None
    irregularity_properties: IrregularityProperties | None = None
    image_URI: str | None = None
    audio_block_URI: str | None = None

    @staticmethod
    def from_json(json_irreg: dict):

        properties = None
        if json_irreg.get("IrregularityProperties") is not None:
            properties = IrregularityProperties.from_json(
                json_irreg["IrregularityProperties"])

        raw_irreg_type = json_irreg.get("IrregularityType")
        irregularity_type = None
        if raw_irreg_type is not None:
            if raw_irreg_type is not (
                    IrregularityType.SPEED.value
                    or IrregularityType.SPEED_AND_EQUALIZATION.value):
                irregularity_type = IrregularityType(raw_irreg_type)
            else:
                if properties.reading_equalisation != properties.writing_equalisation:
                    irregularity_type = IrregularityType.SPEED_AND_EQUALIZATION
                else:
                    irregularity_type = IrregularityType.SPEED

        return Irregularity(irregularity_ID=uuid.UUID(
            json_irreg["IrregularityID"]),
                            source=Source(json_irreg["Source"]),
                            time_label=json_irreg["TimeLabel"],
                            irregularity_type=irregularity_type,
                            irregularity_properties=properties,
                            image_URI=json_irreg.get("ImageURI"),
                            audio_block_URI=json_irreg.get("AudioBlockURI"))

    def to_json(self):
        dictionary = {
            "IrregularityID": str(self.irregularity_ID),
            "Source": self.source.value,
            "TimeLabel": self.time_label,
        }

        if self.irregularity_type:
            dictionary["IrregularityType"] = self.irregularity_type.value

        if self.image_URI:
            dictionary["ImageURI"] = self.image_URI

        if self.audio_block_URI:
            dictionary["AudioBlockURI"] = self.audio_block_URI

        if self.irregularity_properties:
            dictionary[
                "IrregularityProperties"] = self.irregularity_properties.to_json(
                )

        return dictionary


class IrregularityFile(BaseModel):
    # TODO: the offset calculation is not implemented yet, so it is set to None
    irregularities: list[Irregularity]
    offset: Annotated[int, Field(gt=0)] | None

    class Config:
        schema_extra = {
            "example": {
                "offset":
                0,
                "irregularities": [{
                    "irregularity_ID":
                    "a0a0a0a0-a0a0-a0a0-a0a0-a0a0a0a0a0a0",
                    "source":
                    "a",
                    "time_label":
                    "00:00:00:00",
                    "irregularity_type":
                    "b",
                    "irregularity_properties": {
                        "reading_speed": "n",
                        "reading_equalisation": "n",
                        "writing_speed": "n",
                        "writing_equalisation": "n"
                    },
                    "audio_block_URI":
                    "https://example.com/audio.wav",
                }]
            }
        }

    def __init__(self,
                 irregularities: list[Irregularity] = [],
                 offset: int | None = None):
        self.irregularities = irregularities
        self.offset = offset

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, IrregularityFile):
            return False

        return self.irregularities == __o.irregularities and self.offset == __o.offset

    @staticmethod
    def from_json(json_irreg: dict):
        irregularities = []

        for irreg in json_irreg["Irregularities"]:
            irregularities.append(Irregularity.from_json(irreg))

        return IrregularityFile(irregularities=irregularities,
                                offset=int(json_irreg["Offset"]))

    def to_json(self):
        dictionary = {
            "Irregularities":
            [irregularity.to_json() for irregularity in self.irregularities],
        }

        if self.offset:
            dictionary["Offset"] = self.offset

        return dictionary

    def add(self, irregularity: Irregularity):
        """Add an irregularity to the list of irregularities.

        Parameters
        ----------
        irregularity : Irregularity
            the irregularity to add

        Raises
        ------
        TypeError
            if the irregularity is not a py:class:`Irregularity` object
        """
        if not isinstance(irregularity, Irregularity):
            raise TypeError(
                "IrregularityFile.add() expects an Irregularity object")
        self.irregularities.append(irregularity)

    def join(self, other):
        """Append the irregularities of other in current irregularity file.

        Parameters
        ----------
        other : IrregularityFile
            the irregularity file you want to append at the current one
        
        Raises
        ------
        TypeError
            if other is not an instance of IrregularityFile
        """
        if not isinstance(other, IrregularityFile):
            raise TypeError("other must be an instance of IrregularityFile")
        self.irregularities += other.irregularities
