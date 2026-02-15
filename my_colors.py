from dataclasses import dataclass


@dataclass
class MyColors:
    background: str = "#DBDADA"
    plot_background: str = "#FFFFFF"
    axis_color: str = "#008a6b"
    line: str = "#005090"
    marker: str = "#005090"
    grid: str = "#f2eeee"
    lines: tuple = (
        "#005090",
        "#EF0070",
        "#c7ba0b",
    )
