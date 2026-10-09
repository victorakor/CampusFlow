#am wroking here

def calculate_priority(urgency, affected_users):

    is_high = urgency == "high"
    is_medium = urgency == "medium"
    many_users = affected_users >= 10
    some_users = affected_users >= 3

    if is_high and many_users:
        return "critical"
    if is_high or many_users:
        return "high"
    if is_medium or some_users:
        return "medium"
    return "low"