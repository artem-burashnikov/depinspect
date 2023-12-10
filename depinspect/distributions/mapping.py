from depinspect.distributions.fedora import Fedora
from depinspect.distributions.package import Package
from depinspect.distributions.ubuntu import Ubuntu

distribution_class_mapping: dict[str, type[Package]] = {
    "ubuntu": Ubuntu,
    "fedora": Fedora,
}
