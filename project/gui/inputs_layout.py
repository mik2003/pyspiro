"""Module for the layout of inputs."""

import os

from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSlider,
    QVBoxLayout,
)

from project.core.geometry import Spirograph
from project.core.svg_encoder import SVGEncoder
from project.gui.preview_layout import PreviewLayout


class InputsLayout(QVBoxLayout):
    """Class for the layout of inputs."""

    def __init__(self, preview: PreviewLayout) -> None:
        super().__init__()
        # Initialize inputs layout
        self.internal_layout = QVBoxLayout()
        self.preview = preview

        # Define button slot
        @Slot()
        def add_input_slot() -> None:
            self.add_input(self.add_input_name.text(), 0)

        # Initialize add input layout (DEACTIVATED)
        self.add_input_layout = QHBoxLayout()
        self.add_input_name = QLineEdit("input_name")
        self.add_input_button = QPushButton("Add Input")
        self.add_input_button.clicked.connect(add_input_slot)
        self.add_input_layout.addWidget(self.add_input_name)
        self.add_input_layout.addWidget(self.add_input_button)

        # Save SVG dialog
        self.save_layout = QHBoxLayout()
        self.save_buttton = QPushButton("Save Spirograph as SVG")
        self.save_buttton.clicked.connect(self.save_file)
        self.save_layout.addStretch()
        self.save_layout.addWidget(self.save_buttton)
        self.save_layout.addStretch()

        # Initialize sliders
        self._active = False
        self.add_input("l", 0.8, s_scale=0.01)
        self.add_input("k", 0.67, s_min=1, s_scale=0.01)
        self.add_input("t", 4, s_scale=10)
        self.add_input("steps", 1000, s_max=10000)
        self._active = True

        # Update preview
        self.update_spirograph()

        # Populate layout
        self.addLayout(self.internal_layout)
        self.addStretch()
        self.addLayout(self.save_layout)
        # self.addLayout(self.add_input_layout)

    @Slot()
    def save_file(self) -> None:
        save_file = QFileDialog().getSaveFileName(
            dir=str(os.path.join(os.getcwd(), "out")),
            filter="*.svg",
        )[0]
        with open(save_file, "w", encoding="utf-8") as f:
            svg = SVGEncoder.encode_path(self.spiro)
            f.write(svg)

    def add_input(
        self,
        name: str,
        init: float,
        s_min: int = 0,
        s_max: int = 100,
        s_scale: float = 1.0,
    ) -> None:
        """Function to add a new input."""
        # Check if name is free to avoid deleting previous inputs
        if hasattr(self, name + "_layout"):
            raise ValueError("Input name already exists.")

        # Initialize input layout
        input_layout = QHBoxLayout()
        input_name = QLabel(name)
        input_value = QLineEdit()
        input_slider = QSlider(Qt.Orientation.Horizontal)

        # Define slots
        @Slot()
        def update_input_value() -> None:
            """Slot to update input text from slider value."""
            input_value.setText(f"{(input_slider.value() * s_scale):0.2f}")

        @Slot()
        def update_input_slider() -> None:
            """Slot to update slider value from input text."""
            # Check input value
            try:
                value = float(input_value.text()) / s_scale
            except ValueError as e:
                raise ValueError("Input must be a float.") from e
            input_slider.setValue(value)
            if self._active:
                self.update_spirograph()

        # Connect signals to slots
        input_value.textChanged.connect(update_input_slider)
        input_slider.valueChanged.connect(update_input_value)

        # Modify slider
        input_slider.setRange(s_min, s_max)
        input_value.setText(str(init))

        # Populate the layout
        input_layout.addWidget(input_name)
        input_layout.addStretch()
        input_layout.addWidget(input_value)
        input_layout.addWidget(input_slider)
        self.internal_layout.addLayout(input_layout)
        update_input_value()

        # Add slider to the class attributes so they can be accessed later
        setattr(self, name + "_input_layout", input_layout)
        setattr(self, name + "_input_name", input_name)
        setattr(self, name + "_input_value", input_value)
        setattr(self, name + "_input_slider", input_slider)
        setattr(self, name + "_input_s_scale", s_scale)

    def update_spirograph(self) -> None:
        self.t = Spirograph.angles(
            0,
            self.t_input_slider.maximum() * self.t_input_s_scale,
            int(float(self.steps_input_value.text())),
        )
        self.spiro = Spirograph.trajectory(
            float(self.l_input_value.text()),
            float(self.k_input_value.text()),
            self.t,
        )
        t_s = int(
            self.t_input_slider.value()
            / self.t_input_slider.maximum()
            * self.spiro.shape[1]
        )
        self.preview.graph.setData(self.spiro[0, :t_s], self.spiro[1, :t_s])
