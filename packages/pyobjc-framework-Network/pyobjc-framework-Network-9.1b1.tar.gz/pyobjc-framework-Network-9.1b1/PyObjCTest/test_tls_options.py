from PyObjCTools.TestSupport import TestCase

import Network


class TestTLSOptions(TestCase):
    def test_functions(self):
        self.assertResultIsRetained(Network.nw_protocol_copy_tls_definition)

        Network.nw_tls_create_options

        self.assertResultIsRetained(Network.nw_tls_copy_sec_protocol_options)

        Network.nw_protocol_metadata_is_tls

        self.assertResultIsRetained(Network.nw_tls_copy_sec_protocol_metadata)
