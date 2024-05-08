"""Module for the layout of inputs."""

from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSlider,
    QVBoxLayout,
)


class InputsLayout(QVBoxLayout):
    """Class for the layout of inputs."""

    def __init__(self) -> None:
        super().__init__()
        # Initialize inputs layout
        self.internal_layout = QVBoxLayout()

        # Define button slot
        @Slot()
        def add_input_slot() -> None:
            self.add_input(self.add_input_name.text())

        # Initialize add input layout
        self.add_input_layout = QHBoxLayout()
        self.add_input_name = QLineEdit("input_name")
        self.add_input_button = QPushButton("Add Input")
        self.add_input_button.clicked.connect(add_input_slot)
        self.add_input_layout.addWidget(self.add_input_name)
        self.add_input_layout.addWidget(self.add_input_button)

        # Populate layout
        self.addLayout(self.internal_layout)
        self.addStretch()
        self.addLayout(self.add_input_layout)

    def add_input(self, name: str) -> None:
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
            input_value.setText(str(input_slider.value()))

        @Slot()
        def update_input_slider() -> None:
            """Slot to update slider value from input text."""
            # Check input value
            try:
                value = float(input_value.text())
            except ValueError as e:
                raise ValueError("Input must be a float.") from e
            input_slider.setValue(value)

        # Connect signals to slots
        input_value.textChanged.connect(update_input_slider)
        input_slider.valueChanged.connect(update_input_value)

        # Populate the layout
        input_layout.addWidget(input_name)
        input_layout.addStretch()
        input_layout.addWidget(input_value)
        input_layout.addWidget(input_slider)
        self.internal_layout.addLayout(input_layout)

        # Add slider to the class attributes so they can be accessed later
        setattr(self, name + "_input_layout", input_layout)
        setattr(self, name + "_input_name", input_name)
        setattr(self, name + "_input_value", input_value)
        setattr(self, name + "_input_slider", input_slider)
