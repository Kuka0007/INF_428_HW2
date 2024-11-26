import random
import unittest

def generate_random_data(department_count=5, user_range=(10, 200), threat_range=(0, 90)):
    departments = []
    for _ in range(department_count):
        users = random.randint(user_range[0], user_range[1])
        threat_scores = [random.randint(threat_range[0], threat_range[1]) for _ in range(users)]
        departments.append({
            "users": users,
            "threat_scores": threat_scores,
        })
    return departments

def calculate_aggregated_threat_score(departments):
    total_threat_score = 0
    total_users = 0

    for department in departments:
        if len(department["threat_scores"]) == 0:
            continue

        avg_threat_score = sum(department["threat_scores"]) / len(department["threat_scores"])
        total_threat_score += avg_threat_score * department["users"]
        total_users += department["users"]

    if total_users == 0:
        return 0

    aggregated_score = total_threat_score / total_users
    return min(90, max(0, aggregated_score))

class TestCyberSecurityScore(unittest.TestCase):

    def test_all_departments_same_threat_scores(self):
        departments = [{"users": 100, "threat_scores": [70] * 100} for _ in range(5)]
        score = calculate_aggregated_threat_score(departments)
        self.assertEqual(score, 70)

    def test_one_high_score_department(self):
        departments = [
            {"users": 100, "threat_scores": [10] * 100},
            {"users": 100, "threat_scores": [90] * 100},
        ]
        score = calculate_aggregated_threat_score(departments)
        self.assertEqual(score, 50)

    def test_one_high_user_in_low_threat_department(self):
        departments = [
            {"users": 100, "threat_scores": [10] * 99 + [90]},
            {"users": 100, "threat_scores": [30] * 100},
        ]
        score = calculate_aggregated_threat_score(departments)
        self.assertGreater(score, 30)
        self.assertLess(score, 50)

    def test_departments_with_different_user_counts(self):
        departments = [
            {"users": 10, "threat_scores": [10] * 10},
            {"users": 50, "threat_scores": [70] * 50},
            {"users": 100, "threat_scores": [50] * 100},
        ]
        score = calculate_aggregated_threat_score(departments)
        self.assertGreaterEqual(score, 50)
        self.assertLessEqual(score, 70)

    def test_no_users(self):
        departments = [{"users": 0, "threat_scores": []} for _ in range(5)]
        score = calculate_aggregated_threat_score(departments)
        self.assertEqual(score, 0)

    def test_edge_case_min_values(self):
        departments = [{"users": 10, "threat_scores": [0] * 10} for _ in range(5)]
        score = calculate_aggregated_threat_score(departments)
        self.assertEqual(score, 0)

    def test_edge_case_max_values(self):
        departments = [{"users": 200, "threat_scores": [90] * 200} for _ in range(5)]
        score = calculate_aggregated_threat_score(departments)
        self.assertEqual(score, 90)

    def test_high_threat_users_in_department(self):
        departments = [
            {"users": 50, "threat_scores": [10] * 49 + [90]},
            {"users": 100, "threat_scores": [30] * 100},
        ]
        score = calculate_aggregated_threat_score(departments)
        self.assertGreater(score, 30)
        self.assertLess(score, 90)

if __name__ == "__main__":
    unittest.main()
