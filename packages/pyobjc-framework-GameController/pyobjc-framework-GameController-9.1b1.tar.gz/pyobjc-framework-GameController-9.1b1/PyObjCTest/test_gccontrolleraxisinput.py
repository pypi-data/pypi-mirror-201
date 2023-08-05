from PyObjCTools.TestSupport import TestCase, min_os_level
import objc
import GameController


class TestGCControllerAxisInput(TestCase):
    @min_os_level("10.9")
    def testClasses(self):
        self.assertIsInstance(GameController.GCControllerAxisInput, objc.objc_class)

    @min_os_level("10.9")
    def testMethods(self):
        self.assertResultIsBlock(
            GameController.GCControllerAxisInput.valueChangedHandler, b"v@f"
        )
        self.assertArgIsBlock(
            GameController.GCControllerAxisInput.setValueChangedHandler_, 0, b"v@f"
        )
