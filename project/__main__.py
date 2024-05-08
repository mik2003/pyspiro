import argparse
import sys

from PySide6.QtWidgets import QApplication

from project.gui.main_window import MainWindow

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Spirograph",
        description="A Spirograph Tool",
        epilog="by Michelangelo Secondo",
    )
    parser.add_argument(
        "-x",
        "--no-gui",
        action="store_true",
        help="Use the command line version of the application.",
    )
    args = parser.parse_args()
    if args.no_gui:
        print("Command line version not implemented yet.")
    else:
        prog = QApplication(sys.argv)
        main_window = MainWindow()
        main_window.show()
        prog.exec()
