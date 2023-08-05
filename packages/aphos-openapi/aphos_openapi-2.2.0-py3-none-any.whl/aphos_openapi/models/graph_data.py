import csv as _csv
import os as _os
import pprint as _pprint
from typing import Union, Optional, List, Tuple, Iterator, Any, Dict

import matplotlib as _matplotlib  # type: ignore
import matplotlib.pyplot as _plt  # type: ignore
from astropy.time import Time as _Time  # type: ignore
from matplotlib import lines  # type: ignore
from matplotlib.ticker import MultipleLocator, FormatStrFormatter  # type: ignore
from matplotlib.transforms import Bbox as _Box  # type: ignore
from matplotlib.widgets import CheckButtons  # type: ignore

from aphos_openapi.model.comparison_object import ComparisonObject as _Comp

_COMPR_JDATE_MAX = 0.06


class GraphData:
    """
    GraphData class for working with Comparison objects and their data.

    Attributes:
        variable: str, object id of variable space object
        comparison: str, object id of comparison space object
        var_catalog: str, catalog of variable space object
        cmp_catalog: str, catalog of comparison space object
        data_list: list, list of DMDU objects (tuple of date, magnitude, deviation, user)
    """

    def __init__(self, comparison: Union[_Comp, str], users: Optional[List[str]] = None,
                 exclude: bool = False, saturated: bool = False) -> None:
        """
        Constructor for GraphData object.

        Args:
            comparison: Comparison object of astronomy data about fluxes or path to file
            users: list of users to include [optional]
            exclude: if set on true, instead of including users, they will be excluded [optional]
            saturated: should be let on False, only for file work [optional]
        """
        if type(comparison) == _Comp:
            self.data_list = from_comparison(comparison, users, exclude, saturated)
            info = [comparison.variable.id, comparison.variable.catalog,
                    comparison.comparison.id, comparison.comparison.catalog]
        elif type(comparison) == str:
            info, self.data_list = from_file(comparison, users, exclude, saturated)
        else:
            raise TypeError("Expected ComparisonObject or str")
        self.variable, self.var_catalog, self.comparison, self.cmp_catalog = info

    def __repr__(self) -> str:
        return _pprint.pformat(self.__dict__)

    def _info_str(self) -> str:
        """
        Private method to return basic info in string.

        Returns: str, info about the object.

        """
        return f"{self.var_catalog} {self.variable} to {self.cmp_catalog} {self.comparison}"

    def to_file(self, path: str) -> None:
        """
        File represantation of given object.

        File is in csv format, delimiter is ' ',
        starts with 4 rows of basic info and then represantation
        of DMDU objects on each row.

        Args:
            path: str, path to desired location of created file
        """
        _os.makedirs(_os.path.dirname(path), exist_ok=True)
        with open(path, 'w', newline='') as file:
            writer = _csv.writer(file, delimiter=' ')
            writer.writerow(["Variable ID", self.variable])
            writer.writerow(["Variable Catalog", self.var_catalog])
            writer.writerow(["Comparison ID", self.comparison])
            writer.writerow(["Comparison Catalog", self.cmp_catalog])
            for data in self.data_list:
                writer.writerow(data)

    def graph(self) -> Any:
        """
        Graph representation of GraphData object (Light curve in time).
        This representation uses matplotlib to create a graph.

        x-axis: Julian date (normal format)

        y-axis: Magnitude

        Graph has also togglable error bars (deviations) and user filtering based on legend.
        """
        self._create_graph()
        _plt.show()

    def _create_graph(self) -> List[Any]:
        """
        Create pyplot graph from data.
        Returns: Figure of given graph

        """
        d: Dict[str, List[Tuple[float, float, float]]] = dict()
        fig, ax = _plt.subplots(figsize=(11, 7))
        fig.subplots_adjust(right=0.8, bottom=0.15)
        _plt.title(f"Light curve of {self._info_str()}")
        _plt.xlabel("Julian Date (JD)")
        _plt.ylabel("Magnitude")
        for a, b, c, u in self.data_list:
            key = u[0:15]
            d.setdefault(key, []).append((a, b, c))
        errs = []
        plts = []
        for key, val in d.items():
            a, b, c = zip(*val)
            plt, = ax.plot(a, b, "o", label=key)
            plts.append(plt)
            errs.append(ax.errorbar(a, b, yerr=c, fmt=" ", label=key, color="#1f77b4", visible=False))
        _, labels = ax.get_legend_handles_labels()
        legend = ax.legend(plts, labels, loc='upper left', title="Username", bbox_to_anchor=(1, 0, 0.07, 1))
        box = deviations(_plt, errs, plts, legend)

        if len(errs) > 10:
            scroll(fig, legend)
        toggle_legend(legend, plts, errs)

        ax.invert_yaxis()
        ax.ticklabel_format(useOffset=False, style='plain')
        _plt.setp(ax.get_xticklabels(), rotation=10, horizontalalignment='right')
        return plts

    def composite_graph(self) -> None:
        """
        Composite (compressed) graph representation of light curve in time.

        Similar to graph() but biggest "jump" between two measurements is defined by
        constant (currently 0.06 JD -> ~1.5 hour).

        User can see light curve of multiple measurements without too much of zooming,
        date is compromised, but relative time between values in 1 measurement is same.

        Every measurement is seperated by 2 lines, distance is given by the given constant.
        """

        self._create_composite_graph()
        _plt.show()

    def _create_composite_graph(self) -> None:
        """
        Create compressed graph.

        Returns: None

        """
        fig, ax = _plt.subplots(figsize=(11, 7))
        _plt.title(f"Composed night light curve of {self._info_str()}")
        _plt.xlabel("Days")
        _plt.ylabel("Magnitude")
        fig.subplots_adjust(right=0.8)
        errs = []
        my_list = sorted(self.data_list, key=lambda x: x.date)
        if len(my_list) == 0:
            return
        # start from 0
        curr_min: float = 0
        # start from 1. measurement and keep with real
        curr = my_list[0].date
        a = []
        b = []
        c = []
        for x, y, z, _ in my_list:
            if curr + _COMPR_JDATE_MAX < x:
                # measurement pause was bigger than _COMPR_JDATE_MAX
                _plt.axvline(x=curr_min, linewidth=0.5, color="black")
                curr_min = curr_min + _COMPR_JDATE_MAX
                _plt.axvline(x=curr_min, linewidth=0.5, color="black")
            else:
                # keep relative time in days
                curr_min = curr_min + (x - curr)
            curr = x
            a.append(curr_min)
            b.append(y)
            c.append(z)

        plt, = ax.plot(a, b, "o")
        errs.append(ax.errorbar(a, b, yerr=c, fmt=" ", color="#1f77b4", visible=False))
        box = deviations(_plt, errs, [plt], None)
        ax.invert_yaxis()

    def phase_graph(self, moment: float, period: float) -> None:
        """
        Phase graph representation.

        Creates phase curve for given data.

        Args:
            moment: start of epoch, julian date
            period: time period in days
        """
        self._create_phase_graph(moment, period)
        _plt.show()

    def _create_phase_graph(self, moment: float, period: float) -> None:
        """
        Creates phase graph.

        Args:
            moment: start of epoch, julian date
            period: time period in days
        """
        fig, ax = _plt.subplots(figsize=(11, 7))
        _plt.title(f"Phase graph of {self._info_str()}")
        _plt.xlabel("Phase")
        _plt.ylabel("Magnitude")
        fig.subplots_adjust(right=0.8)
        a = []
        b = []
        c = []
        errs = []
        for x, y, z, _ in self.data_list:
            a.append(((x - moment) / period) % 1)
            b.append(y)
            c.append(z)
        plt, = ax.plot(a, b, "o")
        errs.append(ax.errorbar(a, b, yerr=c, fmt=" ", color="#1f77b4", visible=False))
        box = deviations(_plt, errs, [plt], None)
        ax.invert_yaxis()


class DMDU:
    """
    Class for representation of astronomical data.

    Attributes:
        date: float, Julian date rounded to precision 7
        magnitude: float, magnitude rounded to precision 4
        deviation: float, deviation rounded to precision 4
        user: str, user who uploaded the data
    """

    def __init__(self, date: float, mag: float, dev: float, user: str) -> None:
        """
        Constructor for DMDU class.

        Args:
            date: float, Julian date format
            mag: float, magnitude
            dev: float, deviation
            user: str, user
        """
        self.date = round(date, 7)
        self.magnitude = round(mag, 4)
        self.deviation = round(dev, 4)
        self.user = user

    def __str__(self) -> str:
        return f'{self.date}, {self.magnitude}, {self.deviation}, {self.user}'

    def __repr__(self) -> str:
        return str(self)

    def __iter__(self) -> Iterator[Any]:
        for val in self.__dict__.values():
            yield val


def from_comparison(comparison: _Comp, users: Optional[List[str]],
                    exclude: bool, saturated: bool) -> List[DMDU]:
    """
    Helper function for creating GraphData from comparison api object.

    Args:
        comparison: Comparison
        users: list of users to include [optional]
        exclude: if set on True, the users will be excluded [optional]
        saturated: should be let on False, only for file work [optional]

    Returns: List of DMDU objects of given comparison.

    """
    res = []
    for flux in comparison.data:
        if not saturated and (flux.ap_auto == "saturated" or flux.cmp_ap_auto == "saturated"):
            continue
        if users is not None:
            if flux.username in users:
                if exclude:
                    continue
            elif not exclude:
                continue
        date = _Time(flux.exp_middle).jd
        res.append(DMDU(date, flux.magnitude, flux.deviation, flux.username))
    return res


def from_file(comparison: str, users: Optional[List[str]],
              exclude: bool, saturated: bool) -> Tuple[List[str], List[DMDU]]:
    """
    Helper function for GraphData object, creating it from file.

    Args:
        comparison: path to comparison file
        users: list of users to include [optional]
        exclude: if set on True, the users will be excluded [optional]
        saturated: should be let on False, only for file work [optional]

    Returns: Fields (attributes) needed by GraphData object (info and list of DMDU).

    """
    info = []
    res = []
    with open(comparison, 'r', newline='') as file:
        reader = _csv.reader(file, delimiter=' ')
        for row in reader:
            if len(row) < 3:
                info.append(row[1])
                continue
            if row[1] == float('-inf') and not saturated:
                continue
            if users is not None:
                if row[3] in users:
                    if exclude:
                        continue
                elif not exclude:
                    continue
            res.append(DMDU(float(row[0]), float(row[1]), float(row[2]), row[3]))
    return info, res



"""
Graph handling and event handlers for matplotlib graph helper functions.
"""


def deviations(plot: _matplotlib.pyplot, errors: List[Any],
               plts: List[_matplotlib.lines.Line2D],
               legend: Optional[_matplotlib.legend.Legend]) -> CheckButtons:
    """
    Serves as checkbutton for graphs (Errorbar for deviations).

    Args:
        plot: pyplot from matplotlib
        errors: list of Errorbar containers objects
        plts: list of Line2D (x-axis and y-axis values)
        legend: legend of graph [optional]

    Returns: Checkbutton for error bar

    """
    button = plot.axes([0.01, 0.03, 0.18, 0.05], frameon=False)
    box = CheckButtons(button, ["show with deviations"], [False])

    def set_devs(label: str) -> None:
        """
        Helper function for Checkbutton, logic of togglable errorbar.
        Event handler.
        """
        for plt in plts:
            plt.set_visible(True)
        if legend is not None:
            for a in legend.get_lines():
                a.set_visible(True)
        for error in errors:
            for bar in error.lines[2]:
                bar.set_visible(box.get_status()[0])
            plot.draw()

    box.on_clicked(set_devs)
    return box


def scroll(fig: Any, legend: _matplotlib.legend.Legend) -> None:
    """
    Serves as scrolling event for graphs.

    Args:
        fig: figure object from matplotlib.pyplot.subplots()
        legend:
    """
    d = {"down": 40, "up": -40}

    def legend_scroll(evt: Any) -> None:
        """
        Helper function, event handler for scrolling in legend of graph.

        Args:
            evt: Event which occured
        """
        if legend.contains(evt):
            bbox = legend.get_bbox_to_anchor()
            bbox = _Box.from_bounds(bbox.x0, bbox.y0 + d[evt.button], bbox.width, bbox.height)
            tr = legend.axes.transAxes.inverted()
            legend.set_bbox_to_anchor(bbox.transformed(tr))
            fig.canvas.draw_idle()

    fig.canvas.mpl_connect("scroll_event", legend_scroll)


def toggle_legend(legend: _matplotlib.legend.Legend, plts: List[_matplotlib.lines.Line2D],
                  errs: List[Any]) -> None:
    """
    Serves as creating togglable legend for graph (and event handling).

    Args:
        legend: legend of matplotlib.pyplot graph
        plts: list of plots in graph
        errs: list of Errorbar containers objects
    """
    for leg in legend.get_lines():
        leg.set_picker(True)
        leg.set_pickradius(10)

    def on_leg_click(event: Any) -> None:
        """
        Event handler for clicking on legend.

        Args:
            event: Event
        """
        a = event.artist
        label = a.get_label()
        visible = False
        for plt in plts:
            if plt.get_label() == label:
                visible = plt.get_visible()
                plt.set_visible(not visible)
        for err in errs:
            if err.get_label() == label:
                for bar in err.lines[2]:
                    bar.set_visible(False)

        a.set_visible(not a.get_visible())

        _plt.draw()

    _plt.connect("pick_event", on_leg_click)
