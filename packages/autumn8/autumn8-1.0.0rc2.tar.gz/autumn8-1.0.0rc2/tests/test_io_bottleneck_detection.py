import unittest

from autumn8.common.config.settings import Quantization
from perf_predictor.io.bottleneck_detection import calculate_data_file_size_in_kb


class TestDataFileSizeCalculation(unittest.TestCase):
    def test_fp32(self):
        self.assertEqual(
            calculate_data_file_size_in_kb([2, 3, 4], Quantization.FP32), 0.096
        )
        self.assertEqual(
            calculate_data_file_size_in_kb(
                [[3, 5, 1], [1, 4, 1]], Quantization.FP32
            ),
            0.076,
        )
        self.assertRaises(
            ValueError,
            calculate_data_file_size_in_kb,
            [2, [1, 4]],
            Quantization.FP32,
        )
