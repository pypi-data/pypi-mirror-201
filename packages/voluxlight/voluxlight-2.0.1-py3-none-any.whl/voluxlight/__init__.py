# builtin
from typing import Any, List, Callable, Tuple, Dict
from time import sleep
from random import randint
import math

# site
from volux.module import VoluxSource, VoluxTransformer, VoluxDestination
from volux import ResolveCallableParams
from lifxlan import LifxLAN, Device, MultiZoneLight


def _gen_prep_msg(module_name: str) -> Any:
    def _prep_msg() -> None:
        print(f"🔧 {module_name} module prepared!")

    return _prep_msg


def _gen_cleanup_msg(module_name: str) -> Any:
    def _cleanup_msg() -> None:
        print(f"🔧 {module_name} module cleaned up!")

    return _cleanup_msg


device_states: Dict[str, Any] = {}


def _gen_prepare(devices: List[Device]) -> Callable[[], None]:
    def _func() -> None:
        print("saving initial light state...")
        # TODO(Denver): BUG: add support to save/restore device states that have multiple zones (e.g. multizone strips, tiles)
        for device in devices:
            device_states[device.label] = {
                "color": device.get_color(),
                "power": device.get_power(),
            }
            # TODO(Denver): HACK: requires more testing
            # TODO(Denver): should probably be a setting! might not be expected behaviour!
            if device_states[device.label]["power"] == 0:
                turn_on_response = input(f"Turn on device '{str(device.label)}'? [y/n]: ")
                if turn_on_response.lower() == "y":
                    device.set_power(1)
                    print(f"Turned on device '{str(device.label)}'")
                else:
                    print(f"Leaving device powered off '{str(device.label)}'")

        print(device_states)
        print("[TODO!]")
        _gen_prep_msg("VoluxLightLifx")()

    return _func


def _gen_cleanup(devices: List[Device]) -> Callable[[], None]:
    def _func() -> None:
        print("restoring initial light state...")
        # TODO(Denver): BUG: add support to save/restore device states that have multiple zones (e.g. multizone strips, tiles)
        for device in devices:
            color = device_states[device.label]["color"]
            power = device_states[device.label]["power"]
            device.set_color(color, duration=0, rapid=True)
            device.set_power(power, rapid=True)
        print("[TODO!]")
        _gen_cleanup_msg("VoluxLightLifx")()

    return _func


class VoluxLightLifx:
    def __init__(self, lifx_device):
        self.platform = "LIFX"
        self.lifx_device = lifx_device

    def set_color_0D(self, color: Tuple[int, int, int, int]):
        self.lifx_device.set_color(color, rapid=True)

    def get_product(self):
        return self.lifx_device.get_product()


def create_volux_light(platform, device_label, lifxlan_obj=None):
    if platform == "LIFX":
        if device_label is None:
            raise ValueError("please specify a device_label")

        if lifxlan_obj is None:
            raise ValueError(
                "lifxlan_obj must be provided when platform is LIFX"
            )

        while True:
            lifx_device = lifxlan_obj.get_device_by_name(device_label)
            if lifx_device is not None:
                return VoluxLightLifx(lifx_device)
            print(f"Failed to get device '{device_label}'")


class VoluxLightLifxLan(VoluxDestination):
    """Control LIFX smart bulbs on your local network."""

    def __init__(self, device_labels: List[str]) -> None:
        """See class docstring."""
        self.lifx = LifxLAN()
        self.devices = []

        if device_labels is not None and self.devices is not []:
            for label in device_labels:
                while True:
                    try:
                        device = self.lifx.get_device_by_name(label)
                        # device = self.lifx.get_multizone_lights()[0]  # TEMP

                        if device is not None:
                            self.devices.append(device)
                            break
                        else:
                            raise RuntimeError(f"Failed to find device with label '{label}'!")
                    except PermissionError as e:
                        if (e.strerror == "Operation not permitted"):
                            print(
                                "Error: Permission denied to get device '"
                                + label
                                + "': "
                                + "If you are using a VPN client or similar software,"
                                + " ensure your machine isn't blocking local"
                                + " network connections"
                            )
                        raise e
                    except Exception as e:
                        print(f"Failed to get device '{label}': {e}")
                    else:
                        print(f"Failed to get device '{label}' (no exception thrown)")

        self.device_count = len(self.devices)
        self.device_states = {}

        super().__init__(
            prepare=_gen_prepare(self.devices),
            cleanup=_gen_cleanup(self.devices),
        )

    @ResolveCallableParams()
    def set_color(
        self, color: Tuple[int, int, int, int], rapid: bool = True
    ) -> None:
        """Set a light to the given color."""
        for device in self.devices:
            device.set_color(color, rapid=rapid)

    @ResolveCallableParams()
    def set_color_unique_hue_offsets(
        self, color: Tuple[int, int, int, int], rapid: bool = True
    ) -> None:
        """Set a light to the given color. Increment hue so it's unique for every device being affected."""
        hue_offset = 0.0
        invertBrightness = True
        temp = False
        for device in self.devices:
            saturation = color[1]
            brightness = color[2]

            # brightness = (65535 * 0.25) + (
            #     color[2] * 0.50
            # )  # TEMP!: implement properly later on

            # if temp is False:
            #     print(f'{color[0]:<5} {"#" * int(color[0] / 655.35)}')
            #     sin_compat_hue = -65535 + (color[2] * 2)
            #     # sin_compat_hue = -65535 + (color[0] * 2)
            #     print(sin_compat_hue)
            #     hue_driven_x = sin_compat_hue / 65535
            #     print(hue_driven_x)
            #     y = math.sin(hue_driven_x * math.pi)
            #     print(f"[{'#' * (50 + int(y * 50)):<100}]")
            #     saturation = 32767.5 + int(y * 32767.5)
            #     print(saturation)
            #     temp = True

            color = (
                int((color[0] + hue_offset) % 65535),  # H
                saturation,  # S
                max(
                    brightness if invertBrightness else 65535 - brightness, 1
                ),  # B
                color[3],  # K
            )
            # NOTE: BELOW IS TEMP, ORIGINAL CODE ABOVE
            # color = (
            #     # int((color[0] + hue_offset) % 65535),  # H
            #     0,  # H
            #     saturation if invertBrightness else 65535 - saturation,  # S
            #     brightness if invertBrightness else 65535 - brightness,  # B
            #     color[3],  # K
            # )

            device.set_color(color, rapid=rapid)
            # def gen_zone_colors():
            #     zones = 8
            #     col_zones = []
            #     for idx in range(zones - 1):
            #         col_zones.append(
            #             [
            #                 (color[0] + (65535 / zones - 1) * idx) % 65535,
            #                 color[1],
            #                 color[2],
            #                 color[3],
            #             ]
            #         )
            #     # print(col_zones)
            #     return col_zones

            # device.set_zone_colors(
            #     gen_zone_colors(),
            #     duration=0,
            #     rapid=True,
            # )
            hue_offset += 65535 / (self.device_count + 1)
            invertBrightness = not invertBrightness

    # @ResolveCallableParams()
    # def set_color_unique_hue_offsets(
    #     self, color: Tuple[int, int, int, int], rapid: bool = True
    # ) -> None:
    #     """Print a bar with x many segments. Increment hue so it's unique for every device being affected"""
    #     hue_offset = 0.0
    #     device_count = len(self.devices)
    #     on_device = randint(0, device_count - 1)
    #     for idx in range(device_count):
    #         # print("idx:", idx)
    #         # print("choice:", on_device)
    #         if idx == on_device:
    #             print("idx chosen!:", idx)
    #             color = (
    #                 int((color[0] + hue_offset) % 65535),
    #                 color[1],
    #                 color[2],
    #                 color[3],
    #             )
    #         else:
    #             print("idx dimmed!:", idx)
    #             color = (
    #                 int((color[0] + hue_offset) % 65535),
    #                 color[1],
    #                 0,
    #                 color[3],
    #             )
    #         self.devices[0].set_color(color, rapid=rapid)
    #         hue_offset += 65535 / (self.device_count + 1)
