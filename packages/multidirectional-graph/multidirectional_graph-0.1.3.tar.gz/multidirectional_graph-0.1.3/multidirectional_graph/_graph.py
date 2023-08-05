from typing import Tuple, Dict, Optional
from functools import reduce
from pkg_resources import resource_filename
import os

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties


FONT_PATH = resource_filename("multidirectional_graph", "fonts")
TITLE_FONT_PATH = os.path.join(FONT_PATH, "Oswald", "Oswald-Regular.ttf")
BASE_FONT_PATH = os.path.join(FONT_PATH, "SourceSerif", "SourceSerifPro-Light.ttf")


class MultidirectionalGraph:
    def __init__(
        self,
        data: Dict[str, Dict[str, float]],
        tipo_avaliacao: str,
        label: str = "Avaliadores",
        linewidth: int = 2,
        revert_data: Optional[bool] = True,
        figsize: Tuple[float] = (5.5, 15),
        aspect_ratio: float = 2.5,
        black_color: str = "#202020",
        odd_group_color: str = "#e3e0d2",
        even_group_color: str = "#efeee6",
        bad_color: str = "#e51951",
        bad_range: Tuple[int] = (1, 4),
        bad_string: str = "Precisa de\ndesenvolvimento",
        neutral_color: str = "#f7a73b",
        neutral_range: Tuple[int] = (5, 7),
        neutral_string: str = "É adequado",
        good_color: str = "#0393e2",
        good_range: Tuple[int] = (8, 9),
        good_string: str = "É alto",
        header_color: str = "#e3e0d2",
        header_height: float = 0.6,
        subheader_color: str = "#efeee6",
        subheader_height: float = 0.4,
        subheader_title_fontsize: int = 9,
        min_x: float = 0.5,
        max_x: float = 9.5,
        min_y: float = -0.5,
        category_width: float = 4.0,
        group_width: float = 2.0,
        title_fontsize: int = 11,
        background_alpha: float = 0.2,
        title_font_path: str = TITLE_FONT_PATH,
        base_font_path: str = BASE_FONT_PATH,
        plot_base_options = dict(zorder=2),
        scatter_base_options = dict(color="white", marker='o', zorder=3),
        legend_displacement = (0.5, -0.06),
    ):
        """
        A class to create a multidirectional graph based on input data.

        Parameters
        ----------
        data : Dict[str, Dict[str, float]]
            Input data in a nested dictionary format, where the keys of the outer
            dictionary represent the categories, and the keys of the inner dictionaries
            represent the groups. The values of the inner dictionaries represent the
            values to be plotted in the graph.
        tipo_avaliacao : str
            The type of evaluation for the input data.
        label: str
            Label of main graph
        linewidth : int, optional
            The width of the lines in the graph, by default 2.
        revert_data : bool, optional
            Whether to revert the order of the categories in the graph, by default True.
        figsize : Tuple[float], optional
            The size of the figure to be plotted, by default (5, 10).
        aspect_ratio : float, optional
            The aspect ratio of the graph, by default 2.5.
        black_color : str, optional
            The color of the lines in the graph, by default "#202020".
        odd_group_color : str, optional
            The background color of odd-numbered groups in the graph, by default "#efeee6".
        even_group_color : str, optional
            The background color of even-numbered groups in the graph, by default "#e3e0d2".
        bad_color : str, optional
            The color used to indicate values that need development, by default "#e51951".
        bad_range : Tuple[int], optional
            The range of values that need development, by default (1, 4).
        bad_string : str, optional
            The string displayed for values that need development, by default "Precisa\nde desenvolvimento".
        neutral_color : str, optional
            The color used to indicate values that are adequate, by default "#f7a73b".
        neutral_range : Tuple[int], optional
            The range of values that are adequate, by default (5, 7).
        neutral_string : str, optional
            The string displayed for values that are adequate, by default "É adequado".
        good_color : str, optional
            The color used to indicate values that are high, by default "#0393e2".
        good_range : Tuple[int], optional
            The range of values that are high, by default (8, 9).
        good_string : str, optional
            The string displayed for values that are high, by default "É alto".
        header_color : str, optional
            The background color of the header in the graph, by default "#e3e0d2".
        header_height : float, optional
            The height of the header in the graph, by default 0.6.
        subheader_color : str, optional
            The background color of the subheaders in the graph, by default "#efeee6".
        subheader_height : float, optional
            The height of the subheaders in the graph, by default 0.4.
        subheader_title_fontsize : int, optional
            The font size of the subheader titles in the graph, by default 9.
        min_x : float, optional
            The minimum value of the x-axis, by default 0.5.
        max_x : float, optional
            The maximum value of the x-axis, by default 9.5.
        min_y : float, optional
            The minimum value of the y-axis, by default -0.5.
        category_width : float, optional
            The width of the categories in the graph, by default 4.0.
        group_width : float, optional
            The width of the groups in the graph, by default 1.
        title_fontsize: int, opitonal
            The fontsize of title
        background_alpha: float, transparency
            The transparency of background.
        title_font_path: str
            The path of title font
        base_font_path: str
            The path of base font
        """
        self.revert_data = revert_data
        self.data = self._set_data(data)
        self.tipo_avaliacao = tipo_avaliacao
        self.label = label
        self.linewidth = linewidth
        self.figsize = figsize
        self.aspect_ratio = aspect_ratio
        self.categories = self._get_categories()
        self.n_categories = len(self.categories)
        self.values = self._get_values()
        self.group_sizes = self._get_group_sizes()
        self.max_y = self.n_categories - 0.5
        self.black_color = black_color
        self.odd_group_color = odd_group_color
        self.even_group_color = even_group_color
        self.bad_color = bad_color
        self.bad_range = bad_range
        self.bad_string = bad_string
        self.neutral_color = neutral_color
        self.neutral_range = neutral_range
        self.neutral_string = neutral_string
        self.good_color = good_color
        self.good_range = good_range
        self.good_string = good_string
        self.header_color = header_color
        self.header_height = header_height
        self.subheader_color = subheader_color
        self.subheader_height = subheader_height
        self.subheader_title_fontsize = subheader_title_fontsize
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.category_width = category_width
        self.group_width = group_width
        self.title_fontsize = title_fontsize
        self.background_alpha = background_alpha
        self.title_font_path = title_font_path
        self.base_font_path = base_font_path
        self.title_font = FontProperties(fname=self.title_font_path)
        self.base_font = FontProperties(fname=self.base_font_path)
        self.rectangle_left = self.min_x - self.category_width - self.group_width
        self.rectangle_bounds = get_rectangle_bounds(self.group_sizes)
        self.group_label_left = self.rectangle_left + 0.5 * self.group_width
        self.group_label_y = [np.mean(x) for x in self.rectangle_bounds]
        self._set_group_colors()
        self._set_background_bins()
        self.group_mean = self._eval_group_mean()
        self.additional_values = []
        self.additional_values_labels = []
        self.additional_values_options = []
        self.scatter_base_options = scatter_base_options
        self.plot_base_options = plot_base_options
        self.legend_displacement = legend_displacement

    def set_param(self, field, value):
        if not hasattr(self, field):
            raise Exception(
                f"Class {self.__class__.__name__} does not have the attribute {field}"
            )
        setattr(self, field, value)

    def add_values(self, new_values: Dict[str,float], label: str, linewidth: int = 2, color: str = "blue", **options):

        additional_values = []
        for cat in self.categories:
            if cat not in new_values:
                raise ValueError(f"You have to pass the value of the category {cat}")
            additional_values.append(new_values[cat])

        options.update(dict(linewidth=linewidth, color=color))

        self.additional_values.append(additional_values)
        self.additional_values_labels.append(label)
        self.additional_values_options.append(options)


    def plot(self):
        self.fig = plt.figure(figsize=self.figsize)
        self.ax = plt.subplot(111, aspect=self.aspect_ratio)
        self._configure_axis(self.ax)

        self.ax.plot(self.values, self.categories, color=self.black_color, label=self.label, linewidth=self.linewidth, **self.plot_base_options)
        self.ax.scatter(self.values, self.categories, edgecolor=self.black_color, linewidth=self.linewidth, **self.scatter_base_options)

        self._plot_additional_values(self.ax)

        self._set_limits(self.ax)
        self._set_y_ticks_colors(self.ax)

        self.ax.legend(
            loc='lower center',
            bbox_to_anchor=self.legend_displacement,
            ncol=2,
            frameon=False,
            borderaxespad=-0.1,
            prop=self.base_font,
        )
        self.fig.tight_layout()

        return self.fig
    
    def _plot_additional_values(self, ax):
        for i, value_list in enumerate(self.additional_values):
            opt = self.additional_values_options[i]
            label = self.additional_values_labels[i]
            ax.plot(value_list, self.categories, label=label, **opt)
            ax.scatter(value_list, self.categories, edgecolor=opt["color"], linewidth=opt["linewidth"], **self.scatter_base_options)

    def _eval_group_mean(self):
        return {group: "{:.2f}".format(np.mean(list(self.data[group].values()))) for group in self.data}
 
    def _configure_axis(self, ax):
        self._set_frame_color(ax)
        self._set_x_ticks(ax)
        self._add_title(ax)
        self._set_background(ax)
        self._set_category_axis(ax)
        ax.grid(zorder=1)


    def _set_limits(self, ax):
        ax.set_xlim([self.min_x, self.max_x])
        ax.set_ylim([self.min_y, self.max_y])

    def _set_x_ticks(self, ax):
        ax.set_xticks(
            range(1, 10),
            range(1, 10),
            fontproperties=self.title_font,
            color=self.black_color,
        )

    def _set_frame_color(self, ax):
        spines = ax.spines
        for spine in spines:
            spines[spine].set_color(self.black_color)

    def _set_y_ticks_colors(self, ax):
        ytick_labels = ax.get_yticklabels()
        for i, label in enumerate(ytick_labels):
            y_value = self.values[i]

            colors = {k[0]: self.background_bins[k]["color"]  for k in self.background_bins}
            label.set_font_properties(self.base_font)                

            if 1 <= y_value <= 4:
                label.set_color(colors[1])
            elif 5 <= y_value <= 7:
                label.set_color(colors[5])
            elif 8 <= y_value <= 9:
                label.set_color(colors[8])
            
            # To-Do: not working
            # for k in self.background_bins:
            #     label.set_font_properties(self.base_font)
            #     # label.set_color(black_color)
            #     if k[0] <= y_value <= k[1]:
            #         label.set_color(self.background_bins[k]["color"])

    def _set_data(self, data):
        if self.revert_data:
            for k in data:
                data[k] = revdict(data[k])
            data = revdict(data)
        return data

    def _set_group_colors(self):
        self.group_colors = {
            group: self.even_group_color if i % 2 == 0 else self.odd_group_color
            for i, group in enumerate(self.data)
        }

    def _set_background_bins(self):
        self.background_bins = {
            self.bad_range: {"color": self.bad_color, "title": self.bad_string},
            self.neutral_range: {
                "color": self.neutral_color,
                "title": self.neutral_string,
            },
            self.good_range: {"color": self.good_color, "title": self.good_string},
        }

    def _get_categories(self):
        return reduce(
            lambda x, y: x + y, [list(self.data[d].keys()) for d in self.data]
        )

    def _get_values(self):
        return reduce(
            lambda x, y: x + y, [list(self.data[d].values()) for d in self.data]
        )

    def _get_group_sizes(self):
        return {d: len(self.data[d]) for d in self.data}

    def _set_title(self):
        self.title = f"AVALIAÇÃO MULTIDIRECIONAL DE\n{self.tipo_avaliacao}".upper()

    def _add_title(self, ax):
        self._set_title()

        skills_width = self.category_width + self.group_width
        left_plot = self.min_x-skills_width

        ax.text(
            self.min_x-self.category_width/2,
            self.max_y + self.subheader_height/2,
            "HABILIDADES",
            ha="center",
            va="center",
            fontproperties=self.title_font,
            fontsize=self.subheader_title_fontsize,
        )

        ax.text(
            np.mean((self.min_x, self.max_x)),
            self.max_y + self.subheader_height + self.header_height / 2,
            self.title,
            ha="center",
            va="center",
            fontproperties=self.title_font,
            fontsize=self.title_fontsize,
        )

        ax.add_patch(
            plt.Rectangle(
                (self.min_x-self.category_width, self.max_y),
                self.max_x - self.min_x+self.category_width,
                self.subheader_height,
                facecolor=self.header_color,
                clip_on=False,
                linewidth=0,
            )
        )

        ax.add_patch(
            plt.Rectangle(
                (self.min_x, self.max_y),
                self.max_x - self.min_x,
                self.header_height+self.subheader_height,
                facecolor=self.header_color,
                clip_on=False,
                linewidth=0,
            )
        )

        ax.add_line(
            plt.Line2D(
                [self.min_x-self.category_width,self.max_x], 
                [self.max_y,self.max_y],
                clip_on=False,
                color=self.black_color,
                linewidth=0.5,
            )
        )

    def _set_background(self, ax):

        for i, bin_ in enumerate(self.background_bins):
            ax.add_patch(
                plt.Rectangle(
                    (bin_[0] - 0.5, self.min_y),
                    bin_[1] - bin_[0] + 1,
                    self.max_y - self.min_y,
                    facecolor=self.background_bins[bin_]["color"],
                    clip_on=False,
                    linewidth=0,
                    alpha=self.background_alpha,
                )
            )

            # ax.add_patch(
            #     plt.Rectangle(
            #         (bin_[0] - 0.5, self.max_y),
            #         bin_[1] - bin_[0] + 1,
            #         self.subheader_height,
            #         facecolor=self.subheader_color,
            #         clip_on=False,
            #         linewidth=0,
            #     )
            # )

            ax.add_line(
                plt.Line2D(
                    [bin_[0] - 0.5,bin_[0] - 0.5], 
                    [self.max_y,self.max_y+self.subheader_height],
                    clip_on=False,
                    color=self.black_color,
                    # alpha=0.5,
                    linewidth=0.5,
                )
            )

            ax.text(
                np.mean(bin_),
                self.max_y + self.subheader_height / 2,
                self.background_bins[bin_]["title"],
                ha="center",
                va="center",
                fontproperties=self.base_font,
                fontsize=self.subheader_title_fontsize,
            )

    def _set_category_axis(self, ax):
        for i, (group, size) in enumerate(self.group_sizes.items()):
            ax.add_patch(
                plt.Rectangle(
                    (
                        self.rectangle_left + self.group_width,
                        self.rectangle_bounds[i][0],
                    ),
                    self.category_width,
                    size,
                    facecolor=self.group_colors[group],
                    clip_on=False,
                    linewidth=0,
                    alpha=0.2,
                )
            )

            ax.add_patch(
                plt.Rectangle(
                    (self.rectangle_left, self.rectangle_bounds[i][0]),
                    self.group_width,
                    size,
                    facecolor=self.group_colors[group],
                    clip_on=False,
                    linewidth=0,
                )
            )

            ax.text(
                self.group_label_left,
                self.group_label_y[i],
                group.upper()+f"\n({self.group_mean[group]})",
                rotation="vertical",
                ha="center",
                va="center",
                fontproperties=self.title_font,
                fontsize=int(0.85*self.title_fontsize),
            )


def revdict(dictionary):
    return dict(reversed(dictionary.items()))


def get_rectangle_bounds(group_sizes):
    rectangle_bounds = [(0, -0.5)]
    for v in group_sizes.values():
        bottom = rectangle_bounds[-1][1]
        top = bottom + v
        rectangle_bounds.append((bottom, top))

    rectangle_bounds = rectangle_bounds[1:]
    return rectangle_bounds
