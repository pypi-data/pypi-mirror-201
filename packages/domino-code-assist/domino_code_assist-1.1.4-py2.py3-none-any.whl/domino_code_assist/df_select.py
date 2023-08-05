from typing import Callable, List, Optional

import ipyvuetify as v
import reacton
import traitlets


class DfSelectWidget(v.VuetifyTemplate):
    template_file = (__file__, "df_select.vue")

    label = traitlets.Unicode("").tag(sync=True)
    items = traitlets.List().tag(sync=True)
    value = traitlets.Unicode(allow_none=True).tag(sync=True)


@reacton.component
def DfSelect(label: str, items: List, value: Optional[str], on_value: Callable[[Optional[str]], None]):
    return DfSelectWidget.element(label=label, items=items, value=value, on_value=on_value)
