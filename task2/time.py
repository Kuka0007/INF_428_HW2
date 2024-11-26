import math
import unittest

def time_to_cyclic_features(time):
    
    if not (0 <= time < 24):
        raise ValueError("Time must be in the range [0, 24).")
    radians = math.radians(360 * time / 24)
    return math.sin(radians), math.cos(radians)

def time_difference_in_hours(time1, time2):
  
    sin1, cos1 = time_to_cyclic_features(time1)
    sin2, cos2 = time_to_cyclic_features(time2)
    dot_product = sin1 * sin2 + cos1 * cos2
    dot_product = max(-1.0, min(1.0, dot_product))  # Защита от ошибок округления
    if dot_product >= 1.0:
        return 0.0
    angle = math.acos(dot_product)
    return (angle / (2 * math.pi)) * 24

class TestCyclicTime(unittest.TestCase):
    def test_time_to_cyclic_features(self):
        sin_time, cos_time = time_to_cyclic_features(23)
        expected_sin = math.sin(2 * math.pi * 23 / 24)
        expected_cos = math.cos(2 * math.pi * 23 / 24)
        self.assertAlmostEqual(sin_time, expected_sin)
        self.assertAlmostEqual(cos_time, expected_cos)

    def test_time_difference_in_hours(self):
        test_cases = [
            (23, 1, 2),
            (10, 15, 5),
            (10, 10, 0),
            (0, 12, 12),
            (23.5, 0.5, 1),
        ]
        for time1, time2, expected in test_cases:
            with self.subTest(time1=time1, time2=time2):
                self.assertAlmostEqual(time_difference_in_hours(time1, time2), expected)

if __name__ == "__main__":
    unittest.main()
