# main.py — BridgeSense AI Entry Point
# ======================================
# TODO: Wire everything together!
#   1. Parse command-line arguments (get the image path)
#   2. Load UDP principles
#   3. Build the prompt
#   4. Run the analysis
#   5. Print the report
#
# Usage: python main.py path/to/bridge_image.jpg
#
# Hint:
#   import sys
#   image_path = sys.argv[1]  # simple approach
#   — or use argparse for something more polished

import sys
from analyzer import analyze_bridge
from report import print_report, print_criteria
from bridge_profiler import bridge_profiler


if __name__ == "__main__":
    image_path = sys.argv[1]
    profile = (bridge_profiler(image_path))
    result = analyze_bridge(image_path, profile["principles"])
    print_report(result)
