from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.device_disk_configuration import DeviceDiskConfiguration


T = TypeVar("T", bound="DeviceResourcesConfiguration")


@attr.s(auto_attribs=True)
class DeviceResourcesConfiguration:
    """
    Attributes:
        disk (Union[Unset, DeviceDiskConfiguration]):
        stream_throttle_hz (Union[Unset, None, float]):
        low_bandwidth_agent (Union[Unset, None, bool]):
    """

    disk: Union[Unset, "DeviceDiskConfiguration"] = UNSET
    stream_throttle_hz: Union[Unset, None, float] = UNSET
    low_bandwidth_agent: Union[Unset, None, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        disk: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.disk, Unset):
            disk = self.disk.to_dict()

        stream_throttle_hz = self.stream_throttle_hz
        low_bandwidth_agent = self.low_bandwidth_agent

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if disk is not UNSET:
            field_dict["disk"] = disk
        if stream_throttle_hz is not UNSET:
            field_dict["streamThrottleHz"] = stream_throttle_hz
        if low_bandwidth_agent is not UNSET:
            field_dict["lowBandwidthAgent"] = low_bandwidth_agent

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.device_disk_configuration import DeviceDiskConfiguration

        d = src_dict.copy()
        _disk = d.pop("disk", UNSET)
        disk: Union[Unset, DeviceDiskConfiguration]
        if isinstance(_disk, Unset):
            disk = UNSET
        else:
            disk = DeviceDiskConfiguration.from_dict(_disk)

        stream_throttle_hz = d.pop("streamThrottleHz", UNSET)

        low_bandwidth_agent = d.pop("lowBandwidthAgent", UNSET)

        device_resources_configuration = cls(
            disk=disk,
            stream_throttle_hz=stream_throttle_hz,
            low_bandwidth_agent=low_bandwidth_agent,
        )

        device_resources_configuration.additional_properties = d
        return device_resources_configuration

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
