import unittest

from campusflow.tickets import create_ticket
from campusflow.workflow import assign_ticket, change_status, work_queue


def new_ticket(tickets, urgency="low", users=1):
    return create_ticket(tickets, "Test", "Network", urgency, users)


class WorkflowTests(unittest.TestCase):
    def test_assign(self):
        tickets = []
        new_ticket(tickets)
        self.assertEqual(assign_ticket(tickets, "t001", "Ada")["assigned_to"], "Ada")
        with self.assertRaises(ValueError):
            assign_ticket(tickets, "T001", "  ")

    def test_status_rules(self):
        tickets = []
        new_ticket(tickets)
        with self.assertRaises(ValueError):                 # unassigned
            change_status(tickets, "T001", "in_progress")
        assign_ticket(tickets, "T001", "Ada")
        with self.assertRaises(ValueError):                 # cannot skip
            change_status(tickets, "T001", "resolved")
        change_status(tickets, "T001", "in_progress")
        change_status(tickets, "T001", "resolved")
        with self.assertRaises(ValueError):                 # resolved is locked
            assign_ticket(tickets, "T001", "Bob")
        change_status(tickets, "T001", "open")              # explicit reopen
        assign_ticket(tickets, "T001", "Bob")

    def test_queue_order_and_tiebreak(self):
        tickets = []
        for _ in range(10):
            new_ticket(tickets, "low", 1)                   # T001-T010 low
        new_ticket(tickets, "high", 10)                     # T011 critical
        new_ticket(tickets, "high", 1)                      # T012 high
        order = [t["id"] for t in work_queue(tickets)]
        self.assertEqual(order, ["T011", "T012"] + [f"T{n:03d}" for n in range(1, 11)])

    def test_queue_excludes_resolved(self):
        tickets = []
        new_ticket(tickets)
        assign_ticket(tickets, "T001", "Ada")
        change_status(tickets, "T001", "in_progress")
        change_status(tickets, "T001", "resolved")
        self.assertEqual(work_queue(tickets), [])


if __name__ == "__main__":
    unittest.main()
