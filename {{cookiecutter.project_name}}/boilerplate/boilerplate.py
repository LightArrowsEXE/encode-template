import inspect
from dataclasses import dataclass

from encode_framework import ScriptInfo
from vsmuxtools import Encoder as AudioEncoder
from vsmuxtools import Opus, x265
from vsmuxtools.video.encoders import VideoEncoder

from .logger import Log

__all__: list[str] = [
    "ScriptBoilerplate",
    "ScriptInfo",
]


@dataclass
class ScriptBoilerplate:
    script_info: ScriptInfo
    """The script info object containing information about the script."""

    video_encoder: VideoEncoder = x265  # type:ignore[assignment]
    """The video encoder to use for the script."""

    audio_encoder: AudioEncoder = Opus  # type:ignore[assignment]
    """The audio encoder to use for the script."""

    def __init__(
        self,
        script_info: ScriptInfo | None = None,
        video_encoder: VideoEncoder | None = None,
        audio_encoder: AudioEncoder | None = None
    ):
        """
        Boilerplate for setting up a script.

        :param script_info:     The script info object containing information about the script.
        :param video_encoder:   The video encoder to use for the script.
        :param audio_encoder:   The audio encoder to use for the script.
        """

        self.script_info = script_info or ScriptInfo(inspect.stack()[1].filename)

        self.video_encoder = video_encoder or self.video_encoder
        self.audio_encoder = audio_encoder or self.audio_encoder

        Log.debug("Setting up script boilerplate.", self)
        Log.debug(f"Script info: {self.script_info}", self)
        Log.debug(f"Video encoder: {self.video_encoder}", self)
        Log.debug(f"Audio encoder: {self.audio_encoder}", self)

        Log.debug("Setting up script info.", self)
        self.script_info.setup_muxtools()
