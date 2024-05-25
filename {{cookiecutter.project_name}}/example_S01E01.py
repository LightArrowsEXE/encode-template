import warnings

from boilerplate import Log, ScriptBoilerplate, get_src_paths, script_info
from encode_framework import DiscordEmbedder, Encoder, Preview, Zones
from vspreview import is_preview
from vstools import core, vs

try:
    from filterchain import filterchain, prefilterchain
    loaded_filterchain = True
except ModuleNotFoundError:
    warnings.warn("filterchain module not found. Returning source clip.")
    loaded_filterchain = False

# Boilerplate.
core.set_affinity()
boilerplate = ScriptBoilerplate(script_info)

# Indexing the clip.
src = script_info.index(
    get_src_paths("src/", __file__, ".m2ts"), [(None, None)], name="src"  # type:ignore[arg-type]
)

# Zoning. [(start, end, multiplier)].
zones: Zones = []


def script(clip: vs.VideoNode) -> vs.VideoNode | tuple[vs.VideoNode, ...]:
    """
    The script to run on an episode.

    The clip returned from this function will be passed to the encoder.

    If you want multiple video output nodes to be shown alongside the source clip in vspreview,
    return a tuple of the (pre)filtered clips. Else this will return a single clip.

    Scenefiltering should ideally be done in the filterchain function,
    using the information retrieved from the script info object.

    :param clip:    The clip to filter.

    :return:        The filtered clip or clips.
    """

    from encode_framework import get_chapter_frames

    if is_preview():
        get_chapter_frames(script_info)

    script_info.generate_keyframes()

    flt = filterchain(clip, script_info)

    if not isinstance(flt, vs.VideoNode):
        return flt

    return flt.std.SetFrameProps(Name="flt")


if loaded_filterchain:
    prefiltered_clip = prefilterchain(src, script_info)

    if prefiltered_clip != src:
        src = prefiltered_clip


if __name__ == "__vspreview__":  # Previewing filtering.
    preview = Preview(script_info)
elif __name__ == "__main__":  # Running muxtools.
    enc = Encoder(script_info, filterchain(src, draft=False))  # type:ignore
    embed = DiscordEmbedder(script_info, (enc, boilerplate.audio_encoder))  # type:ignore

    embed.start()

    try:
        enc.get_chapters()

        enc.find_audio_files()
        enc.encode_audio(
            track_args=[
                dict(lang="ja", default=True, name="Opus 2.0 @ 192kb/s"),
            ]
        )

        enc.encode_video(zones=zones)

        out = enc.mux(move_once_done=True)
        out = enc.move_nc_to_extras_dir()
        out = enc.move_specials_to_specials_dir()

        embed.success()
    except KeyboardInterrupt as e:
        raise embed.fail("The script was interrupted by the user.", e)
    except BaseException as e:
        raise embed.fail(exception=e)
elif __name__ == "__vapoursynth__":  # Running vspipe or an external package.
    Log.warn("Running via an external package.", script_info.show_title)
    enc = Encoder(boilerplate.script_info, filterchain(src, draft=False))  # type:ignore
    enc.prepare_vspipe()
else:  # Running something else...?
    Log.debug(f"Running via an unsupported method. __name__ == {__name__}", script_info.show_title)
    Log.critical("This method of running the script is not supported. Exiting...", script_info.show_title)
