from typing import Iterable

from encode_framework import Preview
from stgpytools import CustomTypeError
from vstools import vs

from .boilerplate import ScriptBoilerplate
from .logger import Log


def preview(
    boilerplate: ScriptBoilerplate,
    video_nodes: vs.VideoNode | Iterable[vs.VideoNode] = [],
    audio_nodes: vs.AudioNode | Iterable[vs.AudioNode] = []
) -> Preview:
    """
    Set Vapoursynth nodes to preview.

    :: warning ::
        Audio previewing is not supported yet.

    :param boilerplate:         The script boilerplate object.
    :param video_nodes:         The video nodes to preview.
    :param audio_nodes:         The audio nodes to preview.

    :return:                    The preview object.

    :raises CustomTypeError:    If no clips are provided to preview.
    :raises CustomTypeError:    If video_nodes is not an iterable or a single clip.
    """

    prev = Preview(boilerplate.script_info)

    if not video_nodes:
        raise CustomTypeError("No clips provided to preview.", preview)

    vnodes = list[vs.VideoNode]()

    if isinstance(video_nodes, vs.VideoNode):
        vnodes += [video_nodes]  # type:ignore[list-item]
    elif not isinstance(video_nodes, Iterable):
        raise CustomTypeError("video_nodes must be an iterable or a single clip.", preview)
    else:
        vnodes += video_nodes

    if audio_nodes:
        Log.warn("Audio previewing is not supported yet.", preview)

    prev.set_video_outputs(tuple(vnodes))
    # prev.set_audio_outputs()

    return prev
