from mods_base import Library, build_mod, hook, options
from unrealsdk import find_all
from unrealsdk.hooks import Type


enabled = options.BoolOption(
    "Enabled",
    True,
    description="Automatically skips the startup sequence and continues to the main menu.",
)


mod = build_mod(
    cls=Library,
    options=[enabled],
)

mod.load_settings()


startup_object = None
started = False


@hook(
    "WillowGame.WillowGameViewportClient:Tick",
    Type.POST_UNCONDITIONAL,
    immediately_enable=True,
)
def hook_skip_startup_sequence(obj, args, ret, func):

    global startup_object, started

    if not enabled.value:
        return

    if startup_object is None:

        for movie in find_all("WillowGame.WillowGFxMoviePressStart"):

            if movie.ObjectFlags & (0x400 | 0x200):
                continue

            startup_object = movie
            break

        if startup_object is None:
            return

    if not started:
        started = True

        startup_object.DoDlcEnumeration()
        startup_object.DownloadPatcherFiles()
        startup_object.DoSparkAuthentication()
        startup_object.DoStartupDeviceSelection()
        startup_object.CreateSession()

    else:
        startup_object.ContinueToMenu()
        hook_skip_startup_sequence.disable()
