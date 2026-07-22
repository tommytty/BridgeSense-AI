

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

def print_criteria(result):
    
    print("Bridge_Type: ", result["bridge_type"])
    print("Typical Users: ", result["typical_users"])
    print("Context Summary: ", result["context_summary"])
    print("Reasoning: ", result["reasoning"])
    print()

    for r in result["principles"]:
        print(r["name"])
        for p in r["bridge_criteria"]:
            print("-", p)
        print()
