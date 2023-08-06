import base64
import tempfile

import yaml
from kubernetes import client
from kubernetes.client import Configuration

from .model import (
    ConnectionException,
    ConnectionParameters,
    InvalidKubeConfigException,
    KubeConfig,
    KubeConfigCluster,
    KubeConfigClusterParams,
    KubeConfigContext,
    KubeConfigContextParams,
    KubeConfigUser,
    KubeConfigUserParameters,
    UnusableKubeConfigException,
    connection_schema,
    kubeconfig_schema,
)


def test_kubeconfig() -> str:
    """
    This function returns a test kubeconfig file as a string.

    :return: a test kubeconfig file in string format (for unit testing purposes)
    """  # NOQA
    return """apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUM5ekNDQWQrZ0F3SUJBZ0lVV01PTVBNMVUrRi9uNXN6TSthYzlMcGZISHB3d0RRWUpLb1pJaHZjTkFRRUwKQlFBd0hqRWNNQm9HQTFVRUF3d1RhM1ZpZFc1MGRTNXNiMk5oYkdSdmJXRnBiakFlRncweU1URXlNRFl4T0RBdwpNRFJhRncwek1URXlNRFF4T0RBd01EUmFNQjR4SERBYUJnTlZCQU1NRTJ0MVluVnVkSFV1Ykc5allXeGtiMjFoCmFXNHdnZ0VpTUEwR0NTcUdTSWIzRFFFQkFRVUFBNElCRHdBd2dnRUtBb0lCQVFDNExhcG00SDB0T1NuYTNXVisKdzI4a0tOWWRwaHhYOUtvNjUwVGlOK2c5ZFNQU3VZK0V6T1JVOWVONlgyWUZkMEJmVFNodno4Y25rclAvNysxegpETEoxQ3MwRi9haEV3ZDQxQXN5UGFjbnRiVE80dGRLWm9POUdyODR3YVdBN1hSZmtEc2ZxRGN1YW5UTmVmT1hpCkdGbmdDVzU5Q285M056alB1eEFrakJxdVF6eE5GQkgwRlJPbXJtVFJ4cnVLZXo0aFFuUW1OWEFUNnp0M21udzMKWUtWTzU4b2xlcUxUcjVHNlRtVFQyYTZpVGdtdWY2N0cvaVZlalJGbkw3YkNHWmgzSjlCSTNMcVpqRzE4dWxvbgpaVDdQcGQrQTlnaTJOTm9UZlI2TVB5SndxU1BCL0xZQU5ZNGRoZDVJYlVydDZzbmViTlRZSHV2T0tZTDdNTWRMCmVMSzFBZ01CQUFHakxUQXJNQWtHQTFVZEV3UUNNQUF3SGdZRFZSMFJCQmN3RllJVGEzVmlkVzUwZFM1c2IyTmgKYkdSdmJXRnBiakFOQmdrcWhraUc5dzBCQVFzRkFBT0NBUUVBQTVqUHVpZVlnMExySE1PSkxYY0N4d3EvVzBDNApZeFpncVd3VHF5VHNCZjVKdDlhYTk0SkZTc2dHQWdzUTN3NnA2SlBtL0MyR05MY3U4ZWxjV0E4UXViQWxueXRRCnF1cEh5WnYrZ08wMG83TXdrejZrTUxqQVZ0QllkRzJnZ21FRjViTEk5czBKSEhjUGpHUkl1VHV0Z0tHV1dPWHgKSEg4T0RzaG9wZHRXMktrR2c2aThKaEpYaWVIbzkzTHptM00xRUNGcXAvMEdtNkN1RFphVVA2SGpJMWRrYllLdgpsSHNVZ1U1SmZjSWhNYmJLdUllTzRkc1YvT3FHcm9iNW5vcmRjaExBQmRDTnc1cmU5T1NXZGZ1VVhSK0ViZVhrCjVFM0tFYzA1RGNjcGV2a1NTdlJ4SVQrQzNMOTltWGcxL3B5NEw3VUhvNFFLTXlqWXJXTWlLRlVKV1E9PQotLS0tLUVORCBDRVJUSUZJQ0FURS0tLS0tCg==
    server: https://127.0.0.1:6443
  name: default
contexts:
- context:
    cluster: default
    namespace: default
    user: testuser
  name: default
current-context: default
kind: Config
preferences: {}
users:
- name: testuser
  user:
    client-certificate-data: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUM5ekNDQWQrZ0F3SUJBZ0lVV01PTVBNMVUrRi9uNXN6TSthYzlMcGZISHB3d0RRWUpLb1pJaHZjTkFRRUwKQlFBd0hqRWNNQm9HQTFVRUF3d1RhM1ZpZFc1MGRTNXNiMk5oYkdSdmJXRnBiakFlRncweU1URXlNRFl4T0RBdwpNRFJhRncwek1URXlNRFF4T0RBd01EUmFNQjR4SERBYUJnTlZCQU1NRTJ0MVluVnVkSFV1Ykc5allXeGtiMjFoCmFXNHdnZ0VpTUEwR0NTcUdTSWIzRFFFQkFRVUFBNElCRHdBd2dnRUtBb0lCQVFDNExhcG00SDB0T1NuYTNXVisKdzI4a0tOWWRwaHhYOUtvNjUwVGlOK2c5ZFNQU3VZK0V6T1JVOWVONlgyWUZkMEJmVFNodno4Y25rclAvNysxegpETEoxQ3MwRi9haEV3ZDQxQXN5UGFjbnRiVE80dGRLWm9POUdyODR3YVdBN1hSZmtEc2ZxRGN1YW5UTmVmT1hpCkdGbmdDVzU5Q285M056alB1eEFrakJxdVF6eE5GQkgwRlJPbXJtVFJ4cnVLZXo0aFFuUW1OWEFUNnp0M21udzMKWUtWTzU4b2xlcUxUcjVHNlRtVFQyYTZpVGdtdWY2N0cvaVZlalJGbkw3YkNHWmgzSjlCSTNMcVpqRzE4dWxvbgpaVDdQcGQrQTlnaTJOTm9UZlI2TVB5SndxU1BCL0xZQU5ZNGRoZDVJYlVydDZzbmViTlRZSHV2T0tZTDdNTWRMCmVMSzFBZ01CQUFHakxUQXJNQWtHQTFVZEV3UUNNQUF3SGdZRFZSMFJCQmN3RllJVGEzVmlkVzUwZFM1c2IyTmgKYkdSdmJXRnBiakFOQmdrcWhraUc5dzBCQVFzRkFBT0NBUUVBQTVqUHVpZVlnMExySE1PSkxYY0N4d3EvVzBDNApZeFpncVd3VHF5VHNCZjVKdDlhYTk0SkZTc2dHQWdzUTN3NnA2SlBtL0MyR05MY3U4ZWxjV0E4UXViQWxueXRRCnF1cEh5WnYrZ08wMG83TXdrejZrTUxqQVZ0QllkRzJnZ21FRjViTEk5czBKSEhjUGpHUkl1VHV0Z0tHV1dPWHgKSEg4T0RzaG9wZHRXMktrR2c2aThKaEpYaWVIbzkzTHptM00xRUNGcXAvMEdtNkN1RFphVVA2SGpJMWRrYllLdgpsSHNVZ1U1SmZjSWhNYmJLdUllTzRkc1YvT3FHcm9iNW5vcmRjaExBQmRDTnc1cmU5T1NXZGZ1VVhSK0ViZVhrCjVFM0tFYzA1RGNjcGV2a1NTdlJ4SVQrQzNMOTltWGcxL3B5NEw3VUhvNFFLTXlqWXJXTWlLRlVKV1E9PQotLS0tLUVORCBDRVJUSUZJQ0FURS0tLS0tCg==
    client-key-data: LS0tLS1CRUdJTiBQUklWQVRFIEtFWS0tLS0tCk1JSUV2QUlCQURBTkJna3Foa2lHOXcwQkFRRUZBQVNDQktZd2dnU2lBZ0VBQW9JQkFRQzRMYXBtNEgwdE9TbmEKM1dWK3cyOGtLTllkcGh4WDlLbzY1MFRpTitnOWRTUFN1WStFek9SVTllTjZYMllGZDBCZlRTaHZ6OGNua3JQLwo3KzF6RExKMUNzMEYvYWhFd2Q0MUFzeVBhY250YlRPNHRkS1pvTzlHcjg0d2FXQTdYUmZrRHNmcURjdWFuVE5lCmZPWGlHRm5nQ1c1OUNvOTNOempQdXhBa2pCcXVRenhORkJIMEZST21ybVRSeHJ1S2V6NGhRblFtTlhBVDZ6dDMKbW53M1lLVk81OG9sZXFMVHI1RzZUbVRUMmE2aVRnbXVmNjdHL2lWZWpSRm5MN2JDR1poM0o5QkkzTHFaakcxOAp1bG9uWlQ3UHBkK0E5Z2kyTk5vVGZSNk1QeUp3cVNQQi9MWUFOWTRkaGQ1SWJVcnQ2c25lYk5UWUh1dk9LWUw3Ck1NZExlTEsxQWdNQkFBRUNnZ0VBQ28rank4NW5ueVk5L2l6ZjJ3cjkzb2J3OERaTVBjYnIxQURhOUZYY1hWblEKT2c4bDZhbU9Ga2tiU0RNY09JZ0VDdkx6dEtXbmQ5OXpydU5sTEVtNEdmb0trNk5kK01OZEtKRUdoZHE5RjM1Qgpqdi91R1owZTIyRE5ZLzFHNVdDTE5DcWMwQkVHY2RFOTF0YzJuMlppRVBTNWZ6WVJ6L1k4cmJ5K1NqbzJkWE9RCmRHYWRlUFplbi9UbmlHTFlqZWhrbXZNQjJvU0FDbVMycTd2OUNrcmdmR1RZbWJzeGVjSU1QK0JONG9KS3BOZ28KOUpnRWJ5SUxkR1pZS2pQb2lLaHNjMVhmSy8zZStXSmxuYjJBaEE5Y1JMUzhMcDdtcEYySWp4SjNSNE93QTg3WQpNeGZvZWFGdnNuVUFHWUdFWFo4Z3BkWmhQMEoxNWRGdERjajIrcngrQVFLQmdRRDFoSE9nVGdFbERrVEc5bm5TCjE1eXYxRzUxYnJMQU1UaWpzNklEMU1qelhzck0xY2ZvazVaaUlxNVJsQ3dReTlYNDdtV1RhY0lZRGR4TGJEcXEKY0IydjR5Wm1YK1VleGJ3cDU1OWY0V05HdzF5YzQrQjdaNFF5aTRFelN4WmFjbldjMnBzcHJMUFVoOUFXRXVNcApOaW1vcXNiVGNnNGs5QWRxeUIrbWhIWmJRUUtCZ1FEQUNzU09qNXZMU1VtaVpxYWcrOVMySUxZOVNOdDZzS1VyCkprcjdCZEVpN3N2YmU5cldRR2RBb0xkQXNzcU94aENydmtPNkpSSHB1YjlRRjlYdlF4Riszc2ZpZm4yYkQ0ZloKMlVsclA1emF3RlNrNDNLbjdMZzRscURpaVUxVGlqTkJBL3dUcFlmbTB4dW5WeFRWNDZpNVViQW1XRk12TWV0bQozWUZYQmJkK2RRS0JnRGl6Q1B6cFpzeEcrazAwbUxlL2dYajl4ekNwaXZCbHJaM29teTdsVWk4YUloMmg5VlBaCjJhMzZNbVcyb1dLVG9HdW5xcCtibWU1eUxRRGlFcjVQdkJ0bGl2V3ppYmRNbFFMY2Nlcnpveml4WDA4QU5WUnEKZUpZdnIzdklDSGFFM25LRjdiVjNJK1NlSk1ra1BYL0QrV1R4WTQ5clZLYm1FRnh4c1JXRW04ekJBb0dBWEZ3UgpZanJoQTZqUW1DRmtYQ0loa0NJMVkwNEorSHpDUXZsY3NGT0EzSnNhUWduVUdwekl5OFUvdlFiLzhpQ0IzZ2RZCmpVck16YXErdnVkbnhYVnRFYVpWWGJIVitPQkVSdHFBdStyUkprZS9yYm1SNS84cUxsVUxOVWd4ZjA4RkRXeTgKTERxOUhKOUZPbnJnRTJvMU9FTjRRMGpSWU81U041dXFXODd0REEwQ2dZQXpXbk1KSFgrbmlyMjhRRXFyVnJKRAo4ZUEwOHIwWTJRMDhMRlcvMjNIVWQ4WU12VnhTUTdwcUwzaE41RXVJQ2dCbEpGVFI3TndBREo3eDY2M002akFMCm1DNlI4dWxSZStwa08xN2Y0UUs3MnVRanJGZEhESnlXQmdDL0RKSkV6d1dwY0Q4VVNPK3A5bVVIbllLTUJTOEsKTVB1ejYrZ3h0VEtsRU5pZUVacXhxZz09Ci0tLS0tRU5EIFBSSVZBVEUgS0VZLS0tLS0K
    username: testuser
    password: testpassword
    token: sha256~fFyEqjf1xxFMO0tbEyGRvWeNOd7QByuEgS4hyEq_A9o
"""  # NOQA


def parse_kubeconfig(data: str) -> KubeConfig:
    """
    This function parses a kubeconfig file into a KubeConfig data structure. You may need to use
    kubeconfig_to_connection to convert it into a usable connection configuration.

    Example usage:

    >>> config = test_kubeconfig()
    >>> kube_config = parse_kubeconfig(config)
    >>> kube_config.current_context
    'default'

    >>> kube_config.users[0].name
    'testuser'
    >>> kube_config.clusters[0].name
    'default'
    >>> kube_config.contexts[0].context.cluster
    'default'

    :param data: The KubeConfig data structure.
    :return: The parsed kubeconfig structure.
    """  # NOQA
    try:
        loaded_data = yaml.safe_load(data)
        kubeconfig = kubeconfig_schema.unserialize(loaded_data)
        return kubeconfig
    except Exception as e:
        raise InvalidKubeConfigException(e.__str__()) from e


def kubeconfig_to_connection(
    kubeconfig: KubeConfig, inline_files: bool = True
) -> ConnectionParameters:
    """
    This function converts a KubeConfig structure into ConnectionParameters.

    Example usage:

    .. doctest::
    >>> config = test_kubeconfig()
    >>> connection_config = kubeconfig_to_connection(parse_kubeconfig(config))
    >>> connection_config.host
    'https://127.0.0.1:6443'

    :param kubeconfig: The parsed KubeConfig data structure.
    :param inline_files: Inline referenced external files (e.g. certificates). Defaults to True to support transporting
    credentials across system boundaries.
    :return: The Kubernetes connection parameters.
    :raises InvalidKubeConfigException: If the KubeConfig is structurally invalid or references non-existend key/cert
    files.
    :raises UnusableKubeConfigException: If the KubeConfig does not contain enough data to create the connection
    parameters (e.g. no context is set).
    """  # NOQA
    if kubeconfig.current_context is None or kubeconfig.current_context == "":
        raise UnusableKubeConfigException(
            "Unusable KubeConfig: no current context is set."
        )
    context = None
    for ctx in kubeconfig.contexts:
        if ctx.name == kubeconfig.current_context:
            context = ctx.context
    if context is None:
        raise InvalidKubeConfigException(
            f"Current context {kubeconfig.current_context}"
            f"not found in kubeconfig file."
        )
    current_cluster = context.cluster
    current_user = context.user

    cluster = None
    for cl in kubeconfig.clusters:
        if cl.name == current_cluster:
            cluster = cl.cluster
    if cluster is None:
        raise InvalidKubeConfigException(
            f"Current cluster {current_cluster} not found in kubeconfig file."
        )

    user = None
    for u in kubeconfig.users:
        if u.name == current_user:
            user = u.user
            user.username = u.name
    if user is None:
        raise InvalidKubeConfigException(
            f"Current user {current_user} not found in kubeconfig file."
        )

    if cluster.insecure_skip_tls_verify:
        raise UnusableKubeConfigException(
            "The Kubeconfig is set to skip TLS verification."
            "This is not supported by "
            "Arcaflow and there is no reason to use this option."
            "Please set up your Kubernetes TLS "
            "authentication with CA certificates."
        )

    conn = ConnectionParameters(cluster.server)
    if cluster.certificate_authority is not None:
        if inline_files:
            try:
                with open(cluster.certificate_authority) as f:
                    conn.cacert = f.read()
            except Exception as e:
                raise InvalidKubeConfigException(
                    f"The referenced certificate authority file "
                    f"{cluster.certificate_authority} "
                    f"was not readable: {e.__str__()}."
                ) from e
        else:
            conn.cacert_file = cluster.certificate_authority

    if cluster.certificate_authority_data is not None:
        try:
            conn.cacert = base64.b64decode(
                cluster.certificate_authority_data
            ).decode("ascii")
        except Exception as e:
            raise InvalidKubeConfigException(
                f"Certificate authority data is not readable: {e.__str__()}"
            ) from e

    if user.client_certificate is not None:
        if inline_files:
            try:
                with open(user.client_certificate) as f:
                    conn.cert = f.read()
            except Exception as e:
                raise InvalidKubeConfigException(
                    f"The referenced user certificate"
                    f" file {user.client_certificate} was not "
                    f"readable: {e.__str__()}"
                ) from e
        else:
            conn.cert_file = user.client_certificate

    if user.client_certificate_data is not None:
        try:
            conn.cert = base64.b64decode(user.client_certificate_data).decode(
                "ascii"
            )
        except Exception as e:
            raise InvalidKubeConfigException(
                f"User certificate data is not readable: {e.__str__()}"
            ) from e

    if user.client_key is not None:
        if inline_files:
            try:
                with open(user.client_key) as f:
                    conn.key = f.read()
            except Exception as e:
                raise InvalidKubeConfigException(
                    f"The referenced user key file {user.client_key} was not "
                    f"readable: {e.__str__()}"
                ) from e
        else:
            conn.key_file = user.client_key

    if user.client_key_data is not None:
        try:
            conn.key = base64.b64decode(user.client_key_data).decode("ascii")
        except Exception as e:
            raise InvalidKubeConfigException(
                f"User key data is not readable: {e.__str__()}"
            ) from e

    conn.username = user.username
    conn.password = user.password
    conn.bearer_token = user.token

    try:
        connection_schema.validate(conn)
    except Exception as e:
        raise UnusableKubeConfigException(e.__str__()) from e

    return conn


def connection_to_kubeconfig(data: ConnectionParameters) -> KubeConfig:
    """
    This function converts the ConnectionParameters into an artificial KubeConfig for tools that can only work with that
    type of structure.


    .. doctest::
    >>> config = test_kubeconfig()
    >>> connection_config = kubeconfig_to_connection(parse_kubeconfig(config))
    >>> kbconf = connection_to_kubeconfig(connection_config)
    >>> kbconf.api_version
    'v1'
    >>> len(kbconf.clusters)
    1
    >>> kbconf.clusters[0].name
    'default'
    >>> kbconf.clusters[0].cluster.server
    'https://127.0.0.1:6443'
    >>> kbconf.clusters[0].cluster.certificate_authority_data
    'LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUM5ekNDQWQrZ0F3SUJBZ0lVV01PTVBNMVUrRi9uNXN6TSthYzlMcGZISHB3d0RRWUpLb1pJaHZjTkFRRUwKQlFBd0hqRWNNQm9HQTFVRUF3d1RhM1ZpZFc1MGRTNXNiMk5oYkdSdmJXRnBiakFlRncweU1URXlNRFl4T0RBdwpNRFJhRncwek1URXlNRFF4T0RBd01EUmFNQjR4SERBYUJnTlZCQU1NRTJ0MVluVnVkSFV1Ykc5allXeGtiMjFoCmFXNHdnZ0VpTUEwR0NTcUdTSWIzRFFFQkFRVUFBNElCRHdBd2dnRUtBb0lCQVFDNExhcG00SDB0T1NuYTNXVisKdzI4a0tOWWRwaHhYOUtvNjUwVGlOK2c5ZFNQU3VZK0V6T1JVOWVONlgyWUZkMEJmVFNodno4Y25rclAvNysxegpETEoxQ3MwRi9haEV3ZDQxQXN5UGFjbnRiVE80dGRLWm9POUdyODR3YVdBN1hSZmtEc2ZxRGN1YW5UTmVmT1hpCkdGbmdDVzU5Q285M056alB1eEFrakJxdVF6eE5GQkgwRlJPbXJtVFJ4cnVLZXo0aFFuUW1OWEFUNnp0M21udzMKWUtWTzU4b2xlcUxUcjVHNlRtVFQyYTZpVGdtdWY2N0cvaVZlalJGbkw3YkNHWmgzSjlCSTNMcVpqRzE4dWxvbgpaVDdQcGQrQTlnaTJOTm9UZlI2TVB5SndxU1BCL0xZQU5ZNGRoZDVJYlVydDZzbmViTlRZSHV2T0tZTDdNTWRMCmVMSzFBZ01CQUFHakxUQXJNQWtHQTFVZEV3UUNNQUF3SGdZRFZSMFJCQmN3RllJVGEzVmlkVzUwZFM1c2IyTmgKYkdSdmJXRnBiakFOQmdrcWhraUc5dzBCQVFzRkFBT0NBUUVBQTVqUHVpZVlnMExySE1PSkxYY0N4d3EvVzBDNApZeFpncVd3VHF5VHNCZjVKdDlhYTk0SkZTc2dHQWdzUTN3NnA2SlBtL0MyR05MY3U4ZWxjV0E4UXViQWxueXRRCnF1cEh5WnYrZ08wMG83TXdrejZrTUxqQVZ0QllkRzJnZ21FRjViTEk5czBKSEhjUGpHUkl1VHV0Z0tHV1dPWHgKSEg4T0RzaG9wZHRXMktrR2c2aThKaEpYaWVIbzkzTHptM00xRUNGcXAvMEdtNkN1RFphVVA2SGpJMWRrYllLdgpsSHNVZ1U1SmZjSWhNYmJLdUllTzRkc1YvT3FHcm9iNW5vcmRjaExBQmRDTnc1cmU5T1NXZGZ1VVhSK0ViZVhrCjVFM0tFYzA1RGNjcGV2a1NTdlJ4SVQrQzNMOTltWGcxL3B5NEw3VUhvNFFLTXlqWXJXTWlLRlVKV1E9PQotLS0tLUVORCBDRVJUSUZJQ0FURS0tLS0tCg=='
    >>> kbconf.clusters[0].cluster.insecure_skip_tls_verify
    False
    >>> kbconf.current_context
    'default'
    >>> len(kbconf.contexts)
    1
    >>> kbconf.contexts[0].name
    'default'
    >>> kbconf.contexts[0].context.cluster
    'default'
    >>> kbconf.contexts[0].context.user
    'testuser'
    >>> kbconf.contexts[0].context.namespace
    'default'
    >>> len(kbconf.users)
    1
    >>> kbconf.users[0].name
    'testuser'
    >>> kbconf.users[0].user.client_certificate_data
    'LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUM5ekNDQWQrZ0F3SUJBZ0lVV01PTVBNMVUrRi9uNXN6TSthYzlMcGZISHB3d0RRWUpLb1pJaHZjTkFRRUwKQlFBd0hqRWNNQm9HQTFVRUF3d1RhM1ZpZFc1MGRTNXNiMk5oYkdSdmJXRnBiakFlRncweU1URXlNRFl4T0RBdwpNRFJhRncwek1URXlNRFF4T0RBd01EUmFNQjR4SERBYUJnTlZCQU1NRTJ0MVluVnVkSFV1Ykc5allXeGtiMjFoCmFXNHdnZ0VpTUEwR0NTcUdTSWIzRFFFQkFRVUFBNElCRHdBd2dnRUtBb0lCQVFDNExhcG00SDB0T1NuYTNXVisKdzI4a0tOWWRwaHhYOUtvNjUwVGlOK2c5ZFNQU3VZK0V6T1JVOWVONlgyWUZkMEJmVFNodno4Y25rclAvNysxegpETEoxQ3MwRi9haEV3ZDQxQXN5UGFjbnRiVE80dGRLWm9POUdyODR3YVdBN1hSZmtEc2ZxRGN1YW5UTmVmT1hpCkdGbmdDVzU5Q285M056alB1eEFrakJxdVF6eE5GQkgwRlJPbXJtVFJ4cnVLZXo0aFFuUW1OWEFUNnp0M21udzMKWUtWTzU4b2xlcUxUcjVHNlRtVFQyYTZpVGdtdWY2N0cvaVZlalJGbkw3YkNHWmgzSjlCSTNMcVpqRzE4dWxvbgpaVDdQcGQrQTlnaTJOTm9UZlI2TVB5SndxU1BCL0xZQU5ZNGRoZDVJYlVydDZzbmViTlRZSHV2T0tZTDdNTWRMCmVMSzFBZ01CQUFHakxUQXJNQWtHQTFVZEV3UUNNQUF3SGdZRFZSMFJCQmN3RllJVGEzVmlkVzUwZFM1c2IyTmgKYkdSdmJXRnBiakFOQmdrcWhraUc5dzBCQVFzRkFBT0NBUUVBQTVqUHVpZVlnMExySE1PSkxYY0N4d3EvVzBDNApZeFpncVd3VHF5VHNCZjVKdDlhYTk0SkZTc2dHQWdzUTN3NnA2SlBtL0MyR05MY3U4ZWxjV0E4UXViQWxueXRRCnF1cEh5WnYrZ08wMG83TXdrejZrTUxqQVZ0QllkRzJnZ21FRjViTEk5czBKSEhjUGpHUkl1VHV0Z0tHV1dPWHgKSEg4T0RzaG9wZHRXMktrR2c2aThKaEpYaWVIbzkzTHptM00xRUNGcXAvMEdtNkN1RFphVVA2SGpJMWRrYllLdgpsSHNVZ1U1SmZjSWhNYmJLdUllTzRkc1YvT3FHcm9iNW5vcmRjaExBQmRDTnc1cmU5T1NXZGZ1VVhSK0ViZVhrCjVFM0tFYzA1RGNjcGV2a1NTdlJ4SVQrQzNMOTltWGcxL3B5NEw3VUhvNFFLTXlqWXJXTWlLRlVKV1E9PQotLS0tLUVORCBDRVJUSUZJQ0FURS0tLS0tCg=='
    >>> kbconf.users[0].user.client_key_data
    'LS0tLS1CRUdJTiBQUklWQVRFIEtFWS0tLS0tCk1JSUV2QUlCQURBTkJna3Foa2lHOXcwQkFRRUZBQVNDQktZd2dnU2lBZ0VBQW9JQkFRQzRMYXBtNEgwdE9TbmEKM1dWK3cyOGtLTllkcGh4WDlLbzY1MFRpTitnOWRTUFN1WStFek9SVTllTjZYMllGZDBCZlRTaHZ6OGNua3JQLwo3KzF6RExKMUNzMEYvYWhFd2Q0MUFzeVBhY250YlRPNHRkS1pvTzlHcjg0d2FXQTdYUmZrRHNmcURjdWFuVE5lCmZPWGlHRm5nQ1c1OUNvOTNOempQdXhBa2pCcXVRenhORkJIMEZST21ybVRSeHJ1S2V6NGhRblFtTlhBVDZ6dDMKbW53M1lLVk81OG9sZXFMVHI1RzZUbVRUMmE2aVRnbXVmNjdHL2lWZWpSRm5MN2JDR1poM0o5QkkzTHFaakcxOAp1bG9uWlQ3UHBkK0E5Z2kyTk5vVGZSNk1QeUp3cVNQQi9MWUFOWTRkaGQ1SWJVcnQ2c25lYk5UWUh1dk9LWUw3Ck1NZExlTEsxQWdNQkFBRUNnZ0VBQ28rank4NW5ueVk5L2l6ZjJ3cjkzb2J3OERaTVBjYnIxQURhOUZYY1hWblEKT2c4bDZhbU9Ga2tiU0RNY09JZ0VDdkx6dEtXbmQ5OXpydU5sTEVtNEdmb0trNk5kK01OZEtKRUdoZHE5RjM1Qgpqdi91R1owZTIyRE5ZLzFHNVdDTE5DcWMwQkVHY2RFOTF0YzJuMlppRVBTNWZ6WVJ6L1k4cmJ5K1NqbzJkWE9RCmRHYWRlUFplbi9UbmlHTFlqZWhrbXZNQjJvU0FDbVMycTd2OUNrcmdmR1RZbWJzeGVjSU1QK0JONG9KS3BOZ28KOUpnRWJ5SUxkR1pZS2pQb2lLaHNjMVhmSy8zZStXSmxuYjJBaEE5Y1JMUzhMcDdtcEYySWp4SjNSNE93QTg3WQpNeGZvZWFGdnNuVUFHWUdFWFo4Z3BkWmhQMEoxNWRGdERjajIrcngrQVFLQmdRRDFoSE9nVGdFbERrVEc5bm5TCjE1eXYxRzUxYnJMQU1UaWpzNklEMU1qelhzck0xY2ZvazVaaUlxNVJsQ3dReTlYNDdtV1RhY0lZRGR4TGJEcXEKY0IydjR5Wm1YK1VleGJ3cDU1OWY0V05HdzF5YzQrQjdaNFF5aTRFelN4WmFjbldjMnBzcHJMUFVoOUFXRXVNcApOaW1vcXNiVGNnNGs5QWRxeUIrbWhIWmJRUUtCZ1FEQUNzU09qNXZMU1VtaVpxYWcrOVMySUxZOVNOdDZzS1VyCkprcjdCZEVpN3N2YmU5cldRR2RBb0xkQXNzcU94aENydmtPNkpSSHB1YjlRRjlYdlF4Riszc2ZpZm4yYkQ0ZloKMlVsclA1emF3RlNrNDNLbjdMZzRscURpaVUxVGlqTkJBL3dUcFlmbTB4dW5WeFRWNDZpNVViQW1XRk12TWV0bQozWUZYQmJkK2RRS0JnRGl6Q1B6cFpzeEcrazAwbUxlL2dYajl4ekNwaXZCbHJaM29teTdsVWk4YUloMmg5VlBaCjJhMzZNbVcyb1dLVG9HdW5xcCtibWU1eUxRRGlFcjVQdkJ0bGl2V3ppYmRNbFFMY2Nlcnpveml4WDA4QU5WUnEKZUpZdnIzdklDSGFFM25LRjdiVjNJK1NlSk1ra1BYL0QrV1R4WTQ5clZLYm1FRnh4c1JXRW04ekJBb0dBWEZ3UgpZanJoQTZqUW1DRmtYQ0loa0NJMVkwNEorSHpDUXZsY3NGT0EzSnNhUWduVUdwekl5OFUvdlFiLzhpQ0IzZ2RZCmpVck16YXErdnVkbnhYVnRFYVpWWGJIVitPQkVSdHFBdStyUkprZS9yYm1SNS84cUxsVUxOVWd4ZjA4RkRXeTgKTERxOUhKOUZPbnJnRTJvMU9FTjRRMGpSWU81U041dXFXODd0REEwQ2dZQXpXbk1KSFgrbmlyMjhRRXFyVnJKRAo4ZUEwOHIwWTJRMDhMRlcvMjNIVWQ4WU12VnhTUTdwcUwzaE41RXVJQ2dCbEpGVFI3TndBREo3eDY2M002akFMCm1DNlI4dWxSZStwa08xN2Y0UUs3MnVRanJGZEhESnlXQmdDL0RKSkV6d1dwY0Q4VVNPK3A5bVVIbllLTUJTOEsKTVB1ejYrZ3h0VEtsRU5pZUVacXhxZz09Ci0tLS0tRU5EIFBSSVZBVEUgS0VZLS0tLS0K'
    >>> kbconf.users[0].user.username
    'testuser'
    >>> kbconf.users[0].user.password
    'testpassword'
    >>> kbconf.users[0].user.token
    'sha256~fFyEqjf1xxFMO0tbEyGRvWeNOd7QByuEgS4hyEq_A9o'

    :param data: The Connection data structure.
    :return: The KubeConfig data structure.
    """  # NOQA

    # clusters
    if data.host is None:
        raise ConnectionException("No cluster host found in connection")

    cluster_params = KubeConfigClusterParams(data.host)
    if data.cacert is not None:
        cluster_params.certificate_authority_data = base64.b64encode(
            data.cacert.encode("ascii")
        ).decode("ascii")
    if data.cacert_file is not None:
        cluster_params.certificate_authority = data.cacert_file

    cluster = KubeConfigCluster("default", cluster_params)

    # contexts
    context_params = KubeConfigContextParams(
        "default", data.username, "default"
    )
    context = KubeConfigContext("default", context_params)
    # users
    user_params = KubeConfigUserParameters()
    if data.key is not None:
        user_params.client_key_data = base64.b64encode(
            data.key.encode("ascii")
        ).decode("ascii")
    if data.key_file is not None:
        user_params.client_key = data.key_file

    if data.cert is not None:
        user_params.client_certificate_data = base64.b64encode(
            data.cert.encode("ascii")
        ).decode("ascii")
    if data.cert_file is not None:
        user_params.client_certificate = data.cert_file
    if data.bearer_token is not None:
        user_params.token = data.bearer_token
    if data.bearer_token_file is not None:
        try:
            with open(data.bearer_token_file) as f:
                user_params.token = f.read()
        except Exception as e:
            raise InvalidKubeConfigException(
                f"The referenced bearer token file"
                f" {data.bearer_token_file} was not "
                f"readable: {e.__str__()}"
            ) from e

    user_params.username = data.username
    user_params.password = data.password

    user = KubeConfigUser(data.username, user_params)
    kubeconfig = KubeConfig("Config", "v1", [cluster], [context], [user])
    kubeconfig.current_context = "default"
    kubeconfig.preferences = {}
    return kubeconfig


def connect(connection: ConnectionParameters) -> client.ApiClient:
    """
    This function creates a usable Kubernetes connection from the connection parameters.

    :param connection: a ConnectionDataStructure
    :return: a configured Kubernetes API Client
    """  # NOQA

    config = Configuration()
    if connection.cert_file is not None:
        config.cert_file = connection.cert_file
    if connection.cert is not None:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(bytes(connection.cert, "ascii"))
            config.cert_file = temp_file.name

    if connection.key_file is not None:
        config.key_file = connection.key_file

    if connection.key is not None:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(bytes(connection.key, "ascii"))
            config.key_file = temp_file.name

    config.username = connection.username
    config.password = connection.password
    config.api_key_prefix = "Bearer"

    if connection.bearer_token is not None:
        config.api_key = connection.bearer_token

    if connection.bearer_token_file is not None:
        try:
            with open(connection.bearer_token_file) as f:
                config.api_key = f.read()
        except Exception as e:
            raise InvalidKubeConfigException(
                f"The referenced bearer token file "
                f"{connection.bearer_token_file} was not "
                f"readable: {e.__str__()}"
            ) from e

    if connection.cacert_file is not None:
        config.ssl_ca_cert = connection.cacert_file
    if connection.cacert is not None:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(bytes(connection.cacert, "ascii"))
            config.ssl_ca_cert = temp_file.name

    config.host = connection.host
    api_client = client.ApiClient(config)
    return api_client


if __name__ == "__main__":
    import doctest

    doctest.testmod()
