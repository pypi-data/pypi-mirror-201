from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import Field

from kubernetes_dynamic.formatters import format_selector

from .common import ItemList, get_default
from .resource_item import ResourceItem

if TYPE_CHECKING:
    from .all import V1StatefulSetSpec, V1StatefulSetStatus
    from .pod import V1Pod


class V1StatefulSet(ResourceItem):
    spec: V1StatefulSetSpec = Field(default_factory=lambda: get_default("V1StatefulSetSpec"))
    status: V1StatefulSetStatus = Field(default_factory=lambda: get_default("V1StatefulSetStatus"))

    def get_pods(self) -> ItemList[V1Pod]:
        label_selector = self.spec.selector.matchLabels
        return self._client.pods.get(label_selector=format_selector(label_selector))
