import NetFS
from PyObjCTools.TestSupport import TestCase


class TestNetFS(TestCase):
    def testStructs(self):
        self.assertNotHasAttr(NetFS, "NetFSMountInterface_V1")
        self.assertNotHasAttr(NetFS, "NetFSInterface")

    def testFunctions(self):
        self.assertNotHasAttr(NetFS, "NetFSInterface_AddRef")
        self.assertNotHasAttr(NetFS, "NetFSInterface_Release")
        self.assertNotHasAttr(NetFS, "NetFS_CreateInterface")
        self.assertNotHasAttr(NetFS, "NetFSQueryInterface")
