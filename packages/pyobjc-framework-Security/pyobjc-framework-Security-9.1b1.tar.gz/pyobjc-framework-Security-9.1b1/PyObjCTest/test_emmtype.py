import Security
from PyObjCTools.TestSupport import TestCase


class Testemmtype(TestCase):
    def test_unsuppported(self):
        self.assertFalse(hasattr(Security, "CSSM_MANAGER_SERVICE_REQUEST"))
        self.assertFalse(hasattr(Security, "CSSM_MANAGER_REPLY"))
        self.assertFalse(hasattr(Security, "CSSM_MANAGER_EVENT_NOTIFICATION"))
