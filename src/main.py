"""
Application entry point.
"""
import sys
import traceback

def main():
    """Launch the CSV Plotter application."""
    from src.ui.main_window import main as ui_main
    ui_main()

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f'Fatal error: {e}', file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)