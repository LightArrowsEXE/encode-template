from encode_framework import ScriptInfo
from vstools import vs

__all__: list[str] = [
    "prefilterchain",
    "filterchain"
]


def filterchain(clip: vs.VideoNode, script_info: ScriptInfo) -> vs.VideoNode:
    """
    The filtering performed on the clip.

    This is where all the magic happens.
    Adjust the filtering to your liking.

    :param clip:            The clip to filter.
    :param script_info:     The script info object containing information about the script.

    :return:                The filtered clip.
    """

    clip = clip.std.RemoveFrameProps("Name")

    return clip


def prefilterchain(clip: vs.VideoNode, script_info: ScriptInfo) -> vs.VideoNode:
    """
    The prefiltering performed on the clip.

    This clip is what gets passed to the filterchain function,
    as well as vspreview when run from the main script.

    :param clip:            The clip to prefilter.
    :param script_info:     The script info object containing information about the script.

    :return:                The prefiltered clip.
    """

    return clip
