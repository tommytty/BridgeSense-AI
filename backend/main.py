import sys
from analyzer import analyze_bridge
from report import print_report, print_criteria
from bridge_profiler import bridge_profiler


if __name__ == "__main__":
    image_path = sys.argv[1]
    profile = (bridge_profiler(image_path))
    result = analyze_bridge(image_path, profile["principles"])
    print_report(result)
