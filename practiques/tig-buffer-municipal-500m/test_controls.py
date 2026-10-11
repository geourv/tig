"""Pure arithmetic checks only: no QGIS import, processing, render or practice run."""
import importlib.util
import math
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("tig_buffer_activity", Path(__file__).with_name("compute.py"))
activity = importlib.util.module_from_spec(spec)
spec.loader.exec_module(activity)


class DistanceControls(unittest.TestCase):
    def test_projection_inside_segment(self):
        self.assertEqual(activity.point_segment_distance((2, 3), (0, 0, 4, 0)), 3)

    def test_endpoints_and_degenerate_segment(self):
        for point, segment in [((-3, 4), (0, 0, 4, 0)), ((7, 4), (0, 0, 4, 0)), ((3, 4), (0, 0, 0, 0))]:
            self.assertEqual(activity.point_segment_distance(point, segment), 5)

    def test_translation_does_not_change_distance(self):
        self.assertEqual(activity.point_segment_distance((344002, 4551003), (344000, 4551000, 344004, 4551000)), 3)

    def test_sampling_has_vertices_midpoints_and_bounded_gaps(self):
        points = activity.sample_contour([(0, 0, 75, 0)], 25)
        self.assertIn((0, 0), points)
        self.assertIn((75, 0), points)
        self.assertIn((37.5, 0), points)
        ordered = sorted(points)
        self.assertLessEqual(max(b[0] - a[0] for a, b in zip(ordered, ordered[1:])), 25)

    def test_invalid_sampling_is_rejected(self):
        for segments, step, limit in [([], 25, 10), ([(0, 0, 100, 0)], 0, 10), ([(0, 0, 100, 0)], 1, 4)]:
            with self.assertRaises(ValueError):
                activity.sample_contour(segments, step, limit)
        with self.assertRaises(ValueError):
            activity.point_segment_distance((math.nan, 0), (0, 0, 1, 0))

    def arc_distances(self, radius, segments):
        # Analytical regular polygon only; this is not a GIS-produced TIG buffer.
        count = 4 * segments
        vertices = [(radius * math.cos(2*math.pi*i/count), radius * math.sin(2*math.pi*i/count))
                    for i in range(count)]
        edges = [(*vertices[i], *vertices[(i+1) % count]) for i in range(count)]
        return [activity.point_segment_distance(point, (0, 0, 0, 0))
                for point in activity.sample_contour(edges, 25)]

    def test_eight_segment_nominal_arc_budget(self):
        distances = self.arc_distances(500, 8)
        self.assertAlmostEqual(500 - min(distances), activity.nominal_sagitta(), places=9)
        self.assertAlmostEqual(activity.nominal_sagitta(), 2.4076366639015356, places=9)
        self.assertGreaterEqual(min(distances), 497)
        self.assertAlmostEqual(max(distances), 500, places=9)

    def test_wrong_radius_and_coarser_arcs_are_detectable(self):
        self.assertGreater(abs(max(self.arc_distances(490, 8)) - 500), 0.01)
        self.assertLess(min(self.arc_distances(500, 4)), 497)

    def test_observed_polygon_sample_still_fails_the_legacy_budget(self):
        # Retained run-02 diagnostic, independently reduced to point/segment maths.
        point = (343086.40574131894, 4555453.787553297)
        segment = (343096.34552661044, 4554957.343159551,
                   343105.55557251733, 4554959.063200004)
        distance = activity.point_segment_distance(point, segment)
        self.assertAlmostEqual(distance, 495.0948411931408, places=9)
        self.assertAlmostEqual(distance, math.hypot(point[0]-segment[2], point[1]-segment[3]), places=9)
        self.assertGreater(500 - distance, activity.LEGACY_CONTOUR_TOLERANCE_M)
        self.assertLess(500 - distance, activity.partial_fillet_sagitta_bound())

    def test_partial_fillet_bound_is_derived_for_all_rounding_intervals(self):
        quantum = math.pi / 16
        bound = activity.partial_fillet_sagitta_bound()
        self.assertAlmostEqual(bound, 5.411745017609492)
        for step in range(1, 10001):
            angle = math.pi * step / 10000
            segments = max(1, int(angle/quantum + 0.5))
            sagitta = 500 * (1 - math.cos(angle/(2*segments)))
            self.assertLessEqual(sagitta, bound + 1e-12)
        self.assertAlmostEqual(activity.PARAMETERS["contour_distance_tolerance_m"], bound + 0.01)

    def test_continuous_segment_distance(self):
        self.assertEqual(activity.segment_pair_distance((0, 0, 4, 0), (1, -2, 1, 2)), 0)
        self.assertEqual(activity.segment_pair_distance((0, 0, 4, 0), (1, 3, 3, 3)), 3)
        self.assertEqual(activity.segment_pair_distance((0, 0, 4, 0), (7, 4, 8, 4)), 5)
        self.assertEqual(activity.segment_pair_distance((0, 0, 4, 0), (2, 0, 8, 0)), 0)
        self.assertEqual(activity.continuous_minimum([(0, 0, 4, 0)], [(1, 3, 3, 3)]), 3)

    def test_continuous_upper_uses_one_reference_segment_per_interval(self):
        result = activity.certify_continuous_upper([(0, 3, 4, 3)], [(0, 0, 4, 0)], 3.01)
        self.assertEqual(result["cells"], 1)
        self.assertEqual(result["upper_bound_m"], 3)
        # Endpoints near different reference points do NOT certify the middle.
        with self.assertRaises(ValueError):
            activity.certify_continuous_upper([(-1, 1, 1, 1)], [(-1, 0, -1, 0), (1, 0, 1, 0)],
                                                1.1, max_cells=200, max_depth=6)


if __name__ == "__main__":
    unittest.main()
