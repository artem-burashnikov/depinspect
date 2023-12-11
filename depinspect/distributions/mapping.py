from depinspect.distributions.fedora import Fedora
from depinspect.distributions.package import Package
from depinspect.distributions.ubuntu import Ubuntu

distro_class_mapping: dict[str, type[Package]] = {
    "ubuntu": Ubuntu,
    "fedora": Fedora,
}
