import unittest

from campusflow.reports import report
from campusflow.tickets import create_ticket


def new_ticket(tickets, urgency="low", users=1):
    return create_ticket(tickets, "Test", "Network", urgency, users)


class ReportTests(unittest.TestCase):
    def test_zero_tickets(self):
        r = report([])
        self.assertEqual(r["total"], 0)
        self.assertEqual(sum(r["status"].values()) + sum(r["priority"].values()), 0)

    def test_counts(self):
        tickets = []
        new_ticket(tickets, "high", 10)
        new_ticket(tickets, "low", 1)
        r = report(tickets)
        self.assertEqual((r["total"], r["priority"]["critical"], r["status"]["open"]),
                         (2, 1, 2))


if __name__ == "__main__":
    unittest.main()
