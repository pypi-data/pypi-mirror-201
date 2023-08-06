import doctest
import os
import unittest

from . import convert
from .model import InvalidKubeConfigException, UnusableKubeConfigException


class TestFixtures:
    caCrt: str
    clientCrt: str
    clientKey: str
    kubeconfig: str
    kubeconfigNoData: str
    kubeconfigNoHost: str
    kubeconfigNoContext: str
    kubeconfigSkipTLS: str
    kubeconfigExtensions: str
    tokenFile: str

    def __init__(self):
        root_dir = os.path.dirname(os.path.abspath(__file__))
        test_data = os.path.join(root_dir, "../testdata")
        try:
            with open(os.path.join(test_data, "ca.crt")) as f:
                self.caCrt = f.read()
        except Exception:
            raise Exception("impossible to read ca.crt fixture")

        try:
            with open(os.path.join(test_data, "client.crt")) as f:
                self.clientCrt = f.read()
        except Exception:
            raise Exception("impossible to read client.crt fixture")

        try:
            with open(os.path.join(test_data, "client.key")) as f:
                self.clientKey = f.read()
        except Exception:
            raise Exception("impossible to read client.key fixture")

        try:
            with open(os.path.join(test_data, "kubeconfig-data.yaml")) as f:
                self.kubeconfig = f.read()
        except Exception:
            raise Exception("impossible to read kubeconfig-data fixture")

        try:
            with open(os.path.join(test_data, "kubeconfig-nodata.yaml")) as f:
                self.kubeconfigNoData = f.read()
        except Exception:
            raise Exception("impossible to read kubeconfig-nodata fixture")

        try:
            with open(os.path.join(test_data, "kubeconfig-nohost.yaml")) as f:
                self.kubeconfigNoHost = f.read()
        except Exception:
            raise Exception("impossible to read kubeconfig-nohost fixture")

        try:
            with open(
                os.path.join(test_data, "kubeconfig-nocontext.yaml")
            ) as f:
                self.kubeconfigNoContext = f.read()
        except Exception:
            raise Exception("impossible to read kubeconfig-nocontext fixture")

        try:
            with open(os.path.join(test_data, "kubeconfig-tlsskip.yaml")) as f:
                self.kubeconfigSkipTLS = f.read()
        except Exception:
            raise Exception("impossible to read kubeconfig-tlsskip fixture")

        try:
            with open(os.path.join(test_data, "tokenfile")) as f:
                self.tokenFile = f.read()
        except Exception:
            raise Exception("impossible to read tokenfile fixture")

        try:
            with open(
                os.path.join(test_data, "kubeconfig-extensions.yaml")
            ) as f:
                self.kubeconfigExtensions = f.read()
        except Exception:
            raise Exception("impossible to read kubeconfig-extensions fixture")


class TestConvert(unittest.TestCase):
    fixtures = TestFixtures()

    def test_parse_kubeconfig(self):
        try:
            kubeconfig = convert.parse_kubeconfig(self.fixtures.kubeconfig)
            kubeconfig_nodata = convert.parse_kubeconfig(
                self.fixtures.kubeconfigNoData
            )
            self.assertIsNotNone(kubeconfig)
            self.assertIsNotNone(kubeconfig_nodata)
        except Exception as e:
            self.fail(f"Parse raised exception : {e}")

    def test_kubeconfig_to_connection(self):
        kubeconfig = convert.parse_kubeconfig(self.fixtures.kubeconfigNoData)
        kubeconfig_nocontext = convert.parse_kubeconfig(
            self.fixtures.kubeconfigNoContext
        )
        try:
            # test data inlining
            connection = convert.kubeconfig_to_connection(kubeconfig, True)
            self.assertEqual(connection.key, self.fixtures.clientKey)
            self.assertEqual(connection.cacert, self.fixtures.caCrt)
            self.assertEqual(connection.cert, self.fixtures.clientCrt)
            # test without data inlining
            connection = convert.kubeconfig_to_connection(kubeconfig, False)
            self.assertEqual(connection.key_file, "./src/testdata/client.key")
            self.assertEqual(connection.cacert_file, "./src/testdata/ca.crt")
            self.assertEqual(connection.cert_file, "./src/testdata/client.crt")

            # test failing with kubeconfig with no context
            with self.assertRaises(UnusableKubeConfigException):
                convert.kubeconfig_to_connection(kubeconfig_nocontext)

            # test failing with kubeconfig with tls skip verify
            with self.assertRaises(InvalidKubeConfigException):
                convert.parse_kubeconfig(self.fixtures.kubeconfigSkipTLS)

            with self.assertRaises(InvalidKubeConfigException):
                convert.parse_kubeconfig(self.fixtures.kubeconfigNoHost)

            # test success on parsing kubeconfig with extensions
            kubeconfig = convert.parse_kubeconfig(
                self.fixtures.kubeconfigExtensions
            )
            self.assertIsNotNone(kubeconfig)

        except Exception as e:
            self.fail(f"kubeconfig_to_connection exception : {e}")

    def test_connection_to_kubeconfig(self):
        try:
            # test without file inlining
            kubeconfig_data = convert.parse_kubeconfig(
                self.fixtures.kubeconfigNoData
            )
            connection = convert.kubeconfig_to_connection(
                kubeconfig_data, False
            )
            kubeconfig_back = convert.connection_to_kubeconfig(connection)
            self.assertEqual(kubeconfig_back, kubeconfig_data)
            # test with file inlining
            kubeconfig_data = convert.parse_kubeconfig(
                self.fixtures.kubeconfig
            )
            connection = convert.kubeconfig_to_connection(
                kubeconfig_data, False
            )
            kubeconfig_back = convert.connection_to_kubeconfig(connection)
            self.assertEqual(kubeconfig_back, kubeconfig_data)

            # test without inlining with token file in connection

            kubeconfig_data = convert.parse_kubeconfig(
                self.fixtures.kubeconfigNoData
            )
            connection = convert.kubeconfig_to_connection(
                kubeconfig_data, False
            )
            connection.bearer_token = None
            connection.bearer_token_file = "./src/testdata/tokenfile"
            kubeconfig_back = convert.connection_to_kubeconfig(connection)
            self.assertEqual(kubeconfig_back, kubeconfig_data)
        except Exception as e:
            self.fail(f"kubeconfig_to_connection exception : {e}")


def load_tests(loader, tests, ignore):
    """
    This function adds the doctests to the discovery process.
    """
    tests.addTests(doctest.DocTestSuite(convert))
    return tests


if __name__ == "__main__":
    unittest.main()
