import objc
from PyObjCTools.TestSupport import TestCase, min_os_level, expectedFailure

import GameCenter


class TestGCAchievementDescription(TestCase):
    @min_os_level("10.8")
    def testClasses10_8(self):
        self.assertIsInstance(GameCenter.GKAchievementDescription, objc.objc_class)

        self.assertArgIsBlock(
            GameCenter.GKAchievementDescription.loadAchievementDescriptionsWithCompletionHandler_,
            0,
            b"v@@",
        )

        self.assertArgIsBlock(
            GameCenter.GKAchievementDescription.loadImageWithCompletionHandler_,
            0,
            b"v@@",
        )

    @expectedFailure
    @min_os_level("10.8")
    def testClasses10_8_fail(self):
        self.assertResultIsBOOL(GameCenter.GKAchievementDescription.isHidden)
        self.assertResultIsBOOL(GameCenter.GKAchievementDescription.isReplayable)
