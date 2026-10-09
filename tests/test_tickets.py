import unittest

from campusflow.tickets import calculate_priority, create_ticket, find_ticket


def new_ticket(tickets, urgency="low", users=1):
    return create_ticket(tickets, "Test", "Network", urgency, users)


class PriorityTests(unittest.TestCase):
    def test_rules(self):
        cases = [("high", 10, "critical"), ("high", 9, "high"),
                 ("medium", 10, "high"), ("low", 10, "high"),
                 ("medium", 1, "medium"), ("low", 3, "medium"),
                 ("low", 2, "low"), ("low", 1, "low")]
        for urgency, users, expected in cases:
            self.assertEqual(calculate_priority(urgency, users), expected)


class CreateTests(unittest.TestCase):
    def test_create_normalizes_input_and_generates_ids(self):
        tickets = []
        t = create_ticket(tickets, " Wi-Fi down ", "network", "HIGH", "15")
        self.assertEqual((t["id"], t["title"], t["category"], t["urgency"],
                          t["affected_users"], t["priority"], t["status"],
                          t["assigned_to"]),
                         ("T001", "Wi-Fi down", "Network", "high", 15,
                          "critical", "open", None))
        self.assertEqual(new_ticket(tickets)["id"], "T002")

    def test_invalid_input_is_rejected(self):
        bad = [("", "Network", "low", 1), ("a", "Printers", "low", 1),
               ("a", "Network", "urgent", 1), ("a", "Network", "low", 0),
               ("a", "Network", "low", -3), ("a", "Network", "low", 2.5),
               ("a", "Network", "low", "many")]
        tickets = []
        for args in bad:
            with self.assertRaises(ValueError, msg=str(args)):
                create_ticket(tickets, *args)
        self.assertEqual(tickets, [])

    def test_unknown_id(self):
        tickets = []
        new_ticket(tickets)
        with self.assertRaises(ValueError):
            find_ticket(tickets, "T099")


if __name__ == "__main__":
    unittest.main()
