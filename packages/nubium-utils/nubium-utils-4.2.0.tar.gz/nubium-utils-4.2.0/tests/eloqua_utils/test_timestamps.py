from unittest import TestCase

from nubium_utils.eloqua_utils.timestamps import nst_to_eloqua_query_timestamp, eloqua_epoch_to_nst


class TestContactUpdateRetrieverTimestamps(TestCase):

    def setUp(self):
        self.elq_eastern_timestamp = '2019-11-25 15:05:10'
        self.nst = '2019-11-25T20:05:10Z'

    def tearDown(self):
        pass

    def test_nst_to_eloqua_query_timestamp(self):
        self.assertEqual(nst_to_eloqua_query_timestamp(self.nst), self.elq_eastern_timestamp)

    def test_eloqua_epoch_to_nst(self):
        self.assertEqual(eloqua_epoch_to_nst('1581027520'), '2020-02-06T22:18:40Z')
