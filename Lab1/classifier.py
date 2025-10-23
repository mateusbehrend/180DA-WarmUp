def classify_action(max_accx, max_accy):
    if max_accx > 30.0:  # You pick this 30.0 threshold
        return "push"
    elif max_accy > 30.0:
        return "lift"
    else:
        return "unknown"