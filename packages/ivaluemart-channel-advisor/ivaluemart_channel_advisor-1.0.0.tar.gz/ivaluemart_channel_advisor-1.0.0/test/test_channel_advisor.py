import logging
from unittest import TestCase
from unittest.mock import patch, MagicMock

import channel_advisor
import testutil


class TestChannelAdvisor(TestCase):
    @classmethod
    def setUpClass(cls):
        testutil.setup_logging(logging.INFO)
        testutil.setup_logging(logging.DEBUG)
        logging.info('TestChannelAdvisor => Start Tests')

    @classmethod
    def tearDownClass(cls):
        logging.info('TestChannelAdvisor => End Tests')

    @patch('channel_advisor.helper.request.urlopen')
    def test_get_response_call_thrice(self, mock_response):
        logging.info('TestShipFromTags => Run Test test_get_response_call_thrice')
        channel_advisor.helper.RETRY_GET_RESPONSE_AFTER = 0

        mock_response.side_effect = [ConnectionResetError, ConnectionResetError, MagicMock(response={})]
        channel_advisor.helper.get_response('https://api.channeladvisor.com/v1/Products/')

        self.assertEqual(mock_response.call_count, 3)

    @patch('channel_advisor.helper.request.urlopen')
    def test_get_response_exception_handle(self, mock_response):
        logging.info('TestShipFromTags => Run Test test_get_response_exception_handle')
        channel_advisor.helper.RETRY_GET_RESPONSE_AFTER = 0

        mock_response.side_effect = [ConnectionResetError, ConnectionResetError, ConnectionResetError,
                                     MagicMock(response={})]
        try:
            channel_advisor.helper.get_response('https://api.channeladvisor.com/v1/Products/')
            self.fail('Fail the test, if exception not raised')
        except ConnectionResetError:
            logging.info('Catch ConnectionResetError')

        self.assertEqual(mock_response.call_count, 3)

    @patch('channel_advisor.helper.request.urlopen')
    def test_get_response_exception_raise(self, mock_response):
        logging.info('TestShipFromTags => Run Test test_get_response_exception_raise')

        channel_advisor.helper.RETRY_GET_RESPONSE_AFTER = 0
        mock_response.side_effect = [ConnectionResetError, ConnectionResetError, ConnectionResetError,
                                     MagicMock(response={})]

        self.assertRaises(ConnectionResetError, channel_advisor.helper.get_response,
                          'https://api.channeladvisor.com/v1/Products/')
