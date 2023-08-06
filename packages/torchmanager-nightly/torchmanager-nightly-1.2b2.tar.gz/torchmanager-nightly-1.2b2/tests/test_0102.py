import unittest


class Test0102(unittest.TestCase):
    def test_linalg(self):
        try:
            from scipy import linalg
        except ImportError:
            linalg = NotImplemented

        self.assertIs(linalg, NotImplemented)

    def test_sqrtm(self):
        from core import torch
        from scipy import linalg

        x = torch.tensor([[4,9], [16,25]], dtype=torch.float)
        sqrt_x = linalg.sqrtm(x)
        assert not isinstance(sqrt_x, tuple)
        # sqrt_x = sqrt_x.real
        y = sqrt_x @ sqrt_x
        y = torch.from_numpy(y.real)
        diff = x.eq(y)

        self.assertEqual(diff.to(torch.int).sum(), 4)