from collections import defaultdict
from functools import partial
import re
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import uuid

from IPython.display import clear_output
from IPython.display import display
from IPython.display import HTML
from IPython.display import Javascript
from ipywidgets import Layout
from ipywidgets import widgets
import pandas as pd
from pandas.io.formats.style import Styler
from traitlets import Dict as DictTrait
from traitlets import HasTraits
from traitlets import Int
from traitlets import link
from traitlets import List as ListTrait
from traitlets import observe
from traitlets import Unicode


@widgets.register
class ReturnedOutput(widgets.Output):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.callable_return = None


def interactive_output_override(
    f: Callable, controls: Dict[str, Union[widgets.Widget, Tuple[widgets.Widget,
                                                                 str]]]
) -> ReturnedOutput:
    """Overrides ipywidgets.interactive_output to handle passing in traits besides value. 
    This avoids the need for creating hidden widgets and instead allows using multiple traits from the same widget

    Args:
        f (Callable): Function to be called
        controls (Dict[str, Union[ipywidgets.Widget, Tuple[ipywidgets.Widget, str]]]): Each key, value can be one of two formats:
        {"arg_name": (widget, "widget_trait")}
            - Passes in widget.widget_trait as f(arg_name=widget.widget_trait)
        {"arg_name": widget}
            - Mirrors above behavior, but the widget_trait is defaulted to "value"

    Returns:
        ipywidgets.Output: Output display of f is captured and returned
    """
    out = ReturnedOutput()

    def observer(change):
        kwargs = {}
        for k, w in controls.items():
            value_name = "value"
            if isinstance(w, tuple):
                w, value_name = w
            kwargs[k] = getattr(w, value_name)
        widgets.interaction.show_inline_matplotlib_plots()

        with out:
            clear_output(wait=True)
            out.callable_return = f(**kwargs)
            widgets.interaction.show_inline_matplotlib_plots()

    for w in controls.values():
        value_name = 'value'
        if isinstance(w, tuple):
            w, value_name = w
        w.observe(observer, value_name)
    widgets.interaction.show_inline_matplotlib_plots()
    observer(None)
    return out


@widgets.register
class RecordIDSelector(widgets.HBox, widgets.ValueWidget):
    value = Int(allow_none=True).tag(sync=True)
    records = ListTrait().tag(sync=True)
    description = Unicode().tag(sync=True)


@widgets.register
class RecordTokenIDSelector(widgets.Dropdown, widgets.ValueWidget):
    token_idx = Int().tag(sync=True)
    ngram_token_idxs = ListTrait([]).tag(sync=True)


@widgets.register
class ConfusionMatrixSelector(widgets.HBox, widgets.ValueWidget):
    value = ListTrait().tag(sync=True)
    group_name = Unicode().tag(sync=True)
    description = Unicode().tag(sync=True)


@widgets.register
class InteractiveDataFrame(widgets.VBox, widgets.ValueWidget, HasTraits):
    # NOTE: Using strings for typing selected row, col
    # Seems to be a ipywidgets bug where changing val to 0 can't be observed
    selected_row = Int(None, allow_none=True).tag(sync=True)
    selected_col = Int(None, allow_none=True).tag(sync=True)
    bold_row_idx = Int(None, allow_none=True).tag(sync=True)
    top_n_tokens = Unicode("10").tag(sync=True)
    selected_area = Unicode(None, allow_none=True).tag(sync=True)
    dataframe_dict = DictTrait(None, allow_none=True).tag(sync=True)
    sort_directions = DictTrait().tag(sync=True)
    description = Unicode().tag(sync=True)

    def __init__(
        self,
        dataframe: pd.DataFrame,
        row_change_callback: Callable = None,
        col_change_callback: Callable = None,
        col_sort: bool = True,
        display_cols: List[str] = None,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        InteractiveDataFrame.disable_output_scroll()

        self.row_change_callback = row_change_callback
        self.col_change_callback = col_change_callback
        self.col_sort = col_sort
        self.display_cols = display_cols
        self.table_key = None
        self.status_key = None
        # trait changes
        self.dataframe = dataframe
        top_n_options = ['10', '20', '50', '100']
        top_n_options = [
            top_n for top_n in top_n_options if int(top_n) < len(dataframe)
        ]
        if top_n_options:
            top_n_options.append('All')
            self.token_table_top_n_widget = widgets.ToggleButtons(
                options=top_n_options,
                description='Top:',
                disabled=False,
                button_style='',
                style={"button_width": "50px"
                      }  # 'success', 'info', 'warning', 'danger' or ''
            )

            def token_table_top_n_widget_click(change):
                self.top_n_tokens = change['new']

            self.token_table_top_n_widget.observe(
                token_table_top_n_widget_click, 'value'
            )
            display(self.token_table_top_n_widget)

    @property
    def dataframe(self):
        # TODO: possible performance issues
        return pd.DataFrame.from_dict(self.dataframe_dict)

    @dataframe.setter
    def dataframe(self, df: pd.DataFrame):
        self.dataframe_dict = df.to_dict()

    def create_keys(self):
        self.table_key = f"_interactive_df_table_{uuid.uuid4().hex}"
        self.status_key = f'{self.table_key}_selected_cell'

    def create_selected_cell(self):
        self.selected_cell = widgets.Text(placeholder=self.status_key)
        self.selected_cell.observe(self.on_table_click, 'value')
        if self.col_sort:
            self.selected_cell.observe(self.col_sort_handler, 'value')

    def on_table_click(self, change: Dict[str, Any]):
        cls = change['new'].split(' ')
        row = col = None
        area = None
        if len(cls) == 2:
            area = cls[0]
            col = re.search(r'\d+', cls[1]).group(0)
        elif len(cls) == 3:
            area = cls[0]
            if 'row' in cls[1]:
                row = re.search(r'\d+', cls[1]).group(0)
            if 'col' in cls[2]:
                col = re.search(r'\d+', cls[2]).group(0)
        # cast to integer
        if row is not None and row.isdigit():
            row = int(row)
        if col is not None and col.isdigit():
            col = int(col)

        self.selected_area = area
        self.selected_row = row
        self.selected_col = col

    def add_click_handlers(self):
        # Injecting some JS to add clickhandlers for row, col in DF widget.
        script = """
        var input
        var xpath = "//input[contains(@placeholder,'%s')]";
        function addHandlers() {
            input = document.evaluate(xpath, document, null, 
                XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
            input.setAttribute("hidden","");
            console.log(input);
            
            var table = document.querySelector("#T_%s");
            console.log(table);
            var headcells = [].slice.call(table.getElementsByTagName("th"));
            var datacells = [].slice.call(table.getElementsByTagName("td"));
            var cells = headcells.concat(datacells);
            for (var i=0; i < cells.length; i++) {
            var createClickHandler = function(cell) {
                return function() { 
                    input = document.evaluate(xpath, document, null,
                        XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                    input.value = cell.className; 
                    var event = new Event('change', { bubbles: true });
                    input.dispatchEvent(event);
            }}
            cells[i].onclick = createClickHandler(cells[i]);
            };
        }
        window.onload = setTimeout(addHandlers, 500);
        """ % (self.status_key, self.table_key)
        # add click handlers to cells
        display(Javascript(data=script))

    def style_table(self, styler: Styler):
        styler.set_uuid(self.table_key)
        if self.bold_row_idx is not None:
            df = pd.DataFrame.from_dict(self.dataframe_dict)
            subset = pd.IndexSlice[df.index[df.index == self.bold_row_idx], :]
            styler.applymap(lambda x: "font-weight: bold", subset=subset)
        styler.hide_index()
        return styler

    def clear_bold_row(self):
        self.bold_row_idx = None

    def apply_styling(self):
        script = """
        <style>
            #T_%s th:hover {
                cursor: pointer;
                filter: invert(.5);
            }
        </style>
        """ % (self.table_key)
        display(HTML(script))

    @staticmethod
    def disable_output_scroll():
        script = """
        <style>
            .jupyter-widgets-output-area .output_scroll {
                height: unset !important;
                border-radius: unset !important;
                -webkit-box-shadow: unset !important;
                box-shadow: unset !important;
            }
            .jupyter-widgets-output-area  {
                height: auto !important;
            }
        </style>
        """
        display(HTML(script))

    @observe("dataframe_dict", "bold_row_idx")
    def render_table(self, change):
        self.create_keys()
        self.create_selected_cell()
        if change['new'] is None:
            self.children = []
            return
        elif change['name'] == "dataframe_dict":
            df = pd.DataFrame.from_dict(change['new'])
        elif change['name'] == 'bold_row_idx':
            df = self.dataframe
        else:
            raise ValueError(f"Invalid trait type {change['name']}")

        if self.display_cols:
            df = df[self.display_cols]
        table = widgets.Output()

        if self.top_n_tokens is not None and self.top_n_tokens is not 'All':
            df = df[:int(self.top_n_tokens)]
            if self.bold_row_idx not in df.index:
                self.bold_row_idx = None
        with table:
            # add table to output
            self.add_click_handlers()
            self.apply_styling()
            display(df.style.pipe(self.style_table))
        self.children = [table, self.selected_cell]

    @observe("selected_row")
    def row_cb_trans(self, change):
        if self.row_change_callback is None:
            return
        val = change['new']
        if val is not None:
            df = self.dataframe
            # set bold row
            self.bold_row_idx = int(df.iloc[val].name)
            return self.row_change_callback(df.iloc[val])

    @observe("top_n_tokens")
    def top_n_change(self, change):
        val = change['new']
        self.render_table(
            {
                'name': 'dataframe_dict',
                'new': self.dataframe_dict
            }
        )

    @observe("selected_col")
    def col_cb_trans(self, change):
        if self.col_change_callback is None:
            return
        val = change['new']
        if val is not None:
            df = self.dataframe
            col = self.display_cols[val]
            return self.col_change_callback(df[col])

    def col_sort_handler(self, change):
        cls = change['new'].split(' ')
        if len(cls) < 2 or cls[0] != "col_heading":
            return
        if len(cls) == 2:
            col = re.search(r'\d+', cls[1]).group(0)
        elif len(cls) == 3 and 'col' in cls[2]:
            col = re.search(r'\d+', cls[2]).group(0)
        else:
            return
        col = int(col)
        col = self.display_cols[col]
        df: pd.DataFrame = self.dataframe

        # configure sort direction
        self.sort_directions[
            col
        ] = col not in self.sort_directions or not self.sort_directions[col]
        ascending = self.sort_directions[col]
        self.dataframe = df.sort_values(
            by=col,
            ascending=ascending,
        )
        # NOTE: Observer doesn't get called here.
        # Possibly because this method observes another component's trait.
        # So need to rerender table manually
        self.render_table(
            {
                'name': 'dataframe_dict',
                'new': self.dataframe_dict,
            }
        )


def get_interactive_df(
    df: pd.DataFrame,
    *,
    display_cols: Optional[List[str]] = None,
    row_change_callback: Optional[Callable] = None,
    col_change_callback: Optional[Callable] = None,
    col_sort: bool = True
):

    return InteractiveDataFrame(
        dataframe=df,
        row_change_callback=row_change_callback,
        col_change_callback=col_change_callback,
        col_sort=col_sort,
        display_cols=display_cols
    )


def single_accordion(name, widget, open=False):
    """
    Creates an accordion widget with just one child, the given widget. Useful
    for creating a collapsable panel.
    """

    acc = widgets.Accordion(children=[widget])
    acc.set_title(0, name)
    if open:
        acc.selected_index = 0
    else:
        acc.selected_index = None
    return acc


def tab_container(tab_names: List[str], tab_contents: List):
    tab_container = widgets.Tab()
    tab_container.children = tab_contents
    for i, name in enumerate(tab_names):
        tab_container.set_title(i, name)
    return tab_container


def resize_children(
    parent: widgets.Widget, sizes: Sequence[str]
) -> widgets.Widget:
    """
    EFFECT: Set the width of the children of the given widget to the given
    sizes. Returns the parent for convenience.
    """

    widgets = parent.children
    for widget, size in zip(widgets, sizes):
        widget.layout.width = size
    return parent


def unisize_children(parent: widgets.Widget) -> widgets.Widget:
    """
    EFFECT: Set the width of the children of the given widget to be equal among
    them. Returns the input for convenience.
    """
    widgets = parent.children
    n = 100.0 / float(len(widgets))
    width = f"{n:0.3}%"
    return resize_children(parent, [width] * len(widgets))


def record_id_nav(
    records: List[Tuple[int, int]], add_na=True
) -> RecordIDSelector:
    """

    Args:
        records (List[Tuple): Should be in form [(original_idx, data_idx)]
        original_idx is the record ID set by the user and used for display purposes
        data_idx is the index of the record in TruEra artifact storage.

    Returns:
        RecordIDSelector: the widget for record ID selection. widget.value is the data_idx of the selected record
    """

    # idx = 0
    inc_value = widgets.Button(description="+", layout=Layout(width='40px'))
    dec_value = widgets.Button(description="-", layout=Layout(width='40px'))
    dec_value.disabled = True

    dropdown = widgets.Dropdown(
        options=records,
        value=records[0][1],
        description=f"Record IDs ({len(records)}):",
        style={'description_width': 'initial'}
    )
    selector = RecordIDSelector(
        [dropdown, inc_value, dec_value], records=records
    )

    def inc_dec(_, inc):
        idx = dropdown.index
        if idx is None:
            return
        idx = idx + 1 if inc else idx - 1
        max_idx = len(dropdown.options) - 1
        idx = max(min(idx, max_idx), 0)
        dropdown.value = dropdown.options[idx][1]

    def handle_records_change(_):
        idx = dropdown.index
        if len(dropdown.options) > 0:
            dropdown.value = dropdown.options[idx][1]
        else:
            dropdown.value = None
        dropdown.description = f"Record IDs ({len(dropdown.options)}):"

    def plus_minus_interactivity(change):
        new_idx = change['new']
        if new_idx is None:
            inc_value.disabled = dec_value.disabled = True
        max_idx = len(dropdown.options) - 1
        inc_value.disabled = new_idx == max_idx
        dec_value.disabled = new_idx == 0

    # Link dropdown and selector values and options
    link(
        (selector, 'value'), (dropdown, 'value')
    )  # allows user input via dropdown
    link(
        (selector, 'records'), (dropdown, 'options')
    )  # allows update dropdown options when selector records change

    # controls +/- enabled/disabled
    dropdown.observe(plus_minus_interactivity, 'index')
    # enables +/- functionality
    inc_value.on_click(partial(inc_dec, inc=True))
    dec_value.on_click(partial(inc_dec, inc=False))

    # What happens when records list changes
    selector.observe(handle_records_change, 'records')
    return selector


def confusion_matrix_nav(group_ind_dict: Dict[str, List[int]]):

    def handle_show_all_click(_):
        if binary_classification:
            cm_cls.value = "All"
        else:
            cm_gt_cls.value = "All"
            cm_pred_cls.value = "All"

    def handle_cls_change(_):
        if binary_classification:
            cm_widget.value = gt_pred_tree[cm_cls.value]
            cm_widget.group_name = cm_cls.value
        else:
            cm_widget.value = gt_pred_tree[cm_gt_cls.value][cm_pred_cls.value]
            cm_widget.group_name = f"(label={cm_gt_cls.value}, pred={cm_pred_cls.value})"

    classes = []
    gt_pred_tree = defaultdict(dict)

    binary_classification = False
    for key, idxs in group_ind_dict.items():
        if key == "All":
            continue  # add All later
        if "_as_" in key:
            gt, pred = key.split("_as_")
            classes.extend([gt, pred])
            gt_pred_tree[gt][pred] = list(idxs)

            if pred not in gt_pred_tree["All"]:
                gt_pred_tree["All"][pred] = set(idxs)
            else:
                gt_pred_tree["All"][pred] |= set(idxs)
        else:
            binary_classification = True
            classes.append(key)
            gt_pred_tree[key] = list(idxs)

    if binary_classification:
        gt_pred_tree["All"] = sorted(list(group_ind_dict['All']))
    else:
        # All: set to sorted list
        gt_pred_tree["All"] = {
            pred: sorted(list(v)) for pred, v in gt_pred_tree["All"].items()
        }
        # Get sorted list All for each gt key
        for v in gt_pred_tree.values():
            all_set = set()
            for sub_v in v.values():
                all_set |= set(sub_v)
            v['All'] = sorted(list(all_set))

    classes = ['All'] + sorted(list(set(classes)))

    cm_label = widgets.Label("Confusion Matrix Cell:")
    cm_show_all = widgets.Button(
        description="Show All", layout=Layout(width='auto')
    )

    cm_show_all.on_click(handle_show_all_click)
    if binary_classification:
        cm_cls = widgets.Dropdown(
            options=classes, value="All", layout=Layout(width='auto')
        )
        cm_cls.observe(handle_cls_change)
        elems = [cm_label, cm_cls, cm_show_all]
    else:

        cm_gt_cls = widgets.Dropdown(
            options=classes, value=classes[0], layout=Layout(width='auto')
        )
        cm_as = widgets.Label(
            "predicted as", layout=Layout(margin="2px 5px 2px 5px")
        )
        cm_pred_cls = widgets.Dropdown(
            options=classes, value=classes[0], layout=Layout(width='auto')
        )

        cm_gt_cls.observe(handle_cls_change)
        cm_pred_cls.observe(handle_cls_change)
        elems = [cm_label, cm_gt_cls, cm_as, cm_pred_cls, cm_show_all]

    cm_widget = ConfusionMatrixSelector(elems)
    if binary_classification:
        cm_widget.group_name = 'All'
        cm_widget.value = gt_pred_tree['All']
    else:
        cm_widget.group_name = f"(label=All, pred=All)"
        cm_widget.value = gt_pred_tree['All']['All']
    return cm_widget
