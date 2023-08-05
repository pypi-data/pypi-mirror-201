from PyObjCTools.TestSupport import TestCase, min_os_level

import MLCompute


class TestMLAdamOptimzer(TestCase):
    @min_os_level("12.0")
    def test_methods12_0(self):
        self.assertResultIsBOOL(MLCompute.MLCAdamOptimizer.usesAMSGrad)

        self.assertArgIsBOOL(
            MLCompute.MLCAdamOptimizer.optimizerWithDescriptor_beta1_beta2_epsilon_usesAMSGrad_timeStep_,
            4,
        )
