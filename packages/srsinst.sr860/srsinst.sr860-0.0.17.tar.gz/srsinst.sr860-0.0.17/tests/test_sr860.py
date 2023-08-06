import sys
import unittest
from srsinst.sr860 import SR860, Keys

ConnectionString = "vxi11, 172.25.70.129"


class TestSR860(unittest.TestCase):
    lockin = None

    @classmethod
    def setUpClass(cls) -> None:
        args = [arg.strip() for arg in ConnectionString.split(',')]
        print('connection: ', args)
        cls.lockin = SR860(*args)
        cls.lockin.reset()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.lockin.disconnect()

    def setUp(self) -> None:
        self.lockin = TestSR860.lockin
        self.lockin.reset()

    def tearDown(self) -> None:
        pass

    def test_idn(self):
        print(self.lockin.query_text('*idn?'))
        self.assertIn(',SR86', self.lockin.query_text('*idn?'))

    def test_signal_mode(self):
        self.lockin.signal.input_mode = Keys.Current
        self.assertEqual(self.lockin.signal.input_mode, Keys.Current)
        self.lockin.signal.input_mode = Keys.Voltage
        self.assertEqual(self.lockin.signal.input_mode, Keys.Voltage)

    def test_reference_source(self):
        self.lockin.signal.reference_source = Keys.Internal
        self.assertEqual(self.lockin.signal.reference_source, Keys.Internal)
        self.lockin.signal.reference_source = Keys.External
        self.assertEqual(self.lockin.signal.reference_source, Keys.External)

    def test_reference_frequency(self):
        self.lockin.signal.reference_frequency = 1000
        self.assertEqual(self.lockin.signal.reference_frequency, 1000)
        self.lockin.signal.reference_frequency = 10000
        self.assertEqual(self.lockin.signal.reference_frequency, 10000)

    def test_reference_phase(self):
        self.lockin.signal.reference_phase = 0
        self.assertEqual(self.lockin.signal.reference_phase, 0)
        self.lockin.signal.reference_phase = 180
        self.assertEqual(self.lockin.signal.reference_phase, 180)

    def test_reference_harmonic(self):
        self.lockin.signal.reference_harmonic = 1
        self.assertEqual(self.lockin.signal.reference_harmonic, 1)
        self.lockin.signal.reference_harmonic = 2
        self.assertEqual(self.lockin.signal.reference_harmonic, 2)

    def test_reference_trigger_mode(self):
        self.lockin.ref.trigger_mode = Keys.Sine
        self.assertEqual(self.lockin.ref.trigger_mode, Keys.Sine)
        self.lockin.ref.trigger_mode = Keys.PositiveTTL
        self.assertEqual(self.lockin.ref.trigger_mode, Keys.PositiveTTL)

    def test_reference_trigger_input(self):
        self.lockin.ref.trigger_input = Keys.R50Ohms
        self.assertEqual(self.lockin.ref.trigger_input, Keys.R50Ohms)
        self.lockin.ref.trigger_input = Keys.R1Meg
        self.assertEqual(self.lockin.ref.trigger_input, Keys.R1Meg)

    def test_sine_out_amplitude(self):
        self.lockin.sine_out_amplitude = 0.1
        self.assertEqual(self.lockin.sine_out_amplitude, 0.1)
        self.lockin.sine_out_amplitude = 1
        self.assertEqual(self.lockin.sine_out_amplitude, 1)

    def test_sine_out_offset(self):
        self.lockin.sine_out_offset = 0.0
        self.assertEqual(self.lockin.sine_out_offset, 0.0)
        self.lockin.sine_out_offset = 1.0
        self.assertEqual(self.lockin.sine_out_offset, 1.0)


if __name__ == '__main__':
    unittest.main()
