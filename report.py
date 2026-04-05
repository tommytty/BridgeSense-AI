# report.py — Report Formatter
# ==============================
# TODO: Write a function called `print_report` that:
#   - Takes the analysis result dict from analyzer.py
#   - Prints a clean, readable report to the terminal
#
# Include:
#   - Overall accessibility score
#   - A breakdown of each principle's score with reasoning
#   - List of detected features
#   - Recommendations for improvement
#
# Tip: Keep it simple at first — just print() statements.
# You can make it fancy with colors (colorama) or tables later.


def print_report(result):

    print("Overall Score: ", result["overall_score"])
    for r in result["principles"]:
        print(r["name"])
        print("Score: ", r["score"])
        print("Reasoning: ",r["reasoning"])

    print("Detected Features: ")
    
    for feature in result["detected_features"]:
        print("-", feature)

    print("Recommendation: ", result["recommendations"])

