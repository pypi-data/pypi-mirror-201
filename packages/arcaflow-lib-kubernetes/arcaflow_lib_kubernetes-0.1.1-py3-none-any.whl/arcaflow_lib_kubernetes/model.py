import abc
import enum
import typing
from dataclasses import dataclass

from arcaflow_plugin_sdk import plugin, schema


@dataclass
class ConnectionParameters:
    """
    This is a connection specification matching the Go connection structure.
    """

    host: typing.Annotated[
        str,
        schema.name("Server"),
        schema.description("Kubernetes API URL"),
    ]
    path: typing.Annotated[
        typing.Optional[str],
        schema.name("API path"),
        schema.description("Kubernetes API path"),
    ] = None
    username: typing.Annotated[
        typing.Optional[str],
        schema.name("Username"),
        schema.description("Username to authenticate with."),
    ] = None
    password: typing.Annotated[
        typing.Optional[str],
        schema.name("Password"),
        schema.description("Password to authenticate with."),
    ] = None
    server_name: typing.Annotated[
        typing.Optional[str],
        schema.id("serverName"),
        schema.name("TLS server name"),
        schema.description("Server name to verify TLS certificate against."),
    ] = None
    cert: typing.Annotated[
        typing.Optional[str],
        schema.name("Client certificate"),
        schema.description("Client cert data in PEM format"),
    ] = None
    cert_file: typing.Annotated[
        typing.Optional[str],
        schema.id("certFile"),
        schema.name("Client certificate file"),
        schema.description("File holding the client cert data in PEM format"),
    ] = None
    key: typing.Annotated[
        typing.Optional[str],
        schema.name("Client key"),
        schema.description("Client key in PEM format"),
    ] = None
    key_file: typing.Annotated[
        typing.Optional[str],
        schema.id("keyFile"),
        schema.name("Client key file"),
        schema.description("Client key in PEM format"),
    ] = None
    cacert: typing.Annotated[
        typing.Optional[str],
        schema.name("CA certificate"),
        schema.description("CA certificate in PEM format"),
    ] = None
    cacert_file: typing.Annotated[
        typing.Optional[str],
        schema.id("cacertFile"),
        schema.name("CA certificate file"),
        schema.description(
            "CA certificate file in PEM format. "
            "Defaults to the service account CA file."
        ),
    ] = None
    bearer_token: typing.Annotated[
        typing.Optional[str],
        schema.id("bearerToken"),
        schema.name("Token"),
        schema.description("Secret token of the user/service account"),
    ] = None
    bearer_token_file: typing.Annotated[
        typing.Optional[str],
        schema.id("bearerTokenFile"),
        schema.name("Token file"),
        schema.description(
            "File holding the secret token of the "
            "user/service account. Defaults to the "
            "service account CA file."
        ),
    ] = None


@dataclass
class KubeConfigClusterParams:
    server: typing.Annotated[str, schema.id("server"), schema.name("Server")]
    certificate_authority: typing.Annotated[
        typing.Optional[str],
        schema.id("certificate-authority"),
        schema.name("Certificate authority path"),
        schema.description(
            "Path to the certificate authority file."
            " This path may not be portable across plugins"
            ", use with care."
        ),
        schema.conflicts("certificate-authority-data"),
    ] = None
    certificate_authority_data: typing.Annotated[
        typing.Optional[str],
        schema.id("certificate-authority-data"),
        schema.name("Certificate authority data"),
        schema.description(
            "Base64-encoded PEM data for the certificate authority."
        ),
        schema.conflicts("certificate-authority"),
    ] = None
    insecure_skip_tls_verify: typing.Annotated[
        bool,
        schema.id("insecure-skip-tls-verify"),
        schema.name("Disable TLS certificate verification"),
        schema.description(
            "Disables checking for the Kubernetes "
            "server certificate validity. Not recommended."
        ),
    ] = False
    extensions: typing.Annotated[
        typing.Optional[typing.Any],
        schema.id("extensions"),
        schema.description(
            "minikube kube config section "
            "introduced to avoid local tests issues"
        ),
    ] = None  # NOQA


@dataclass
class KubeConfigCluster:
    name: typing.Annotated[str, schema.name("Name")]
    cluster: typing.Annotated[KubeConfigClusterParams, schema.name("cluster")]


@dataclass
class KubeConfigContextParams:
    cluster: typing.Annotated[str, schema.name("Cluster")]
    user: typing.Annotated[str, schema.name("User")]
    namespace: typing.Annotated[
        typing.Optional[str],
        schema.name("Namespace"),
        schema.description("Default namespace for operations. Often ignored."),
    ] = None
    extensions: typing.Annotated[
        typing.Optional[typing.Any],
        schema.id("extensions"),
        schema.description(
            "minikube kube config section "
            "introduced to avoid local tests issues"
        ),
    ] = None  # NOQA


@dataclass
class KubeConfigContext:
    name: typing.Annotated[str, schema.name("Name")]
    context: typing.Annotated[KubeConfigContextParams, schema.name("context")]


@dataclass
class KubeConfigUserParameters:
    username: typing.Annotated[
        typing.Optional[str],
        schema.name("Username"),
        schema.description("Username for Kubernetes authentication"),
    ] = None
    password: typing.Annotated[
        typing.Optional[str],
        schema.name("Password"),
        schema.description("Password for Kubernetes authentication"),
    ] = None
    token: typing.Annotated[
        typing.Optional[str], schema.name("Bearer token")
    ] = None
    client_certificate: typing.Annotated[
        typing.Optional[str],
        schema.id("client-certificate"),
        schema.name("Client certificate path"),
        schema.description(
            "Path to the client certificate file. "
            "This path may not be portable across plugins, use with care."
        ),
    ] = None
    client_certificate_data: typing.Annotated[
        typing.Optional[str],
        schema.id("client-certificate-data"),
        schema.name("Client certificate"),
        schema.description(
            "Client certificate data Base64-encoded in PEM format."
        ),
    ] = None
    client_key: typing.Annotated[
        typing.Optional[str],
        schema.id("client-key"),
        schema.name("Client key path"),
        schema.description(
            "Path to the client key file. "
            "This path may not be portable across plugins, use with care."
        ),
    ] = None
    client_key_data: typing.Annotated[
        typing.Optional[str],
        schema.id("client-key-data"),
        schema.name("Client key"),
        schema.description("Client key data Base64-encoded in PEM format."),
    ] = None


@dataclass
class KubeConfigUser:
    """
    This class represents a user entry in a kubeconfig.
    """

    name: typing.Annotated[str, schema.name("Name")]
    user: typing.Annotated[KubeConfigUserParameters, schema.name("User")]


class KubeConfigKindEnum(enum.Enum):
    """
    This enum forces the Kind to always be "Config" for KubeConfig files.
    """

    Config = "Config"


@dataclass
class KubeConfig:
    """
    This class represents a full KubeConfig.
    """

    kind: typing.Annotated[str, schema.id("kind")]
    api_version: typing.Annotated[str, schema.id("apiVersion"), schema.min(2)]
    clusters: typing.Annotated[
        typing.List[KubeConfigCluster], schema.id("clusters")
    ]  # NOQA
    contexts: typing.Annotated[
        typing.List[KubeConfigContext], schema.id("contexts")
    ]  # NOQA
    users: typing.Annotated[typing.List[KubeConfigUser], schema.id("users")]
    current_context: typing.Annotated[
        typing.Optional[str], schema.id("current-context")
    ] = None  # NOQA
    preferences: typing.Annotated[
        typing.Optional[typing.Any], schema.id("preferences")
    ] = None  # NOQA


@dataclass
class KubeConfigException(Exception, abc.ABC):
    """
    This class represents a generic exception while parsing a kubeconfig file.
    """

    message: typing.Annotated[str, schema.name("Message")]

    def __init__(self, message: str):
        self.message = message


@dataclass
class ConnectionException(Exception, abc.ABC):
    """
    This class represents a generic exception while parsing a Kubernetes Connection.
    """  # NOQA

    message: typing.Annotated[str, schema.name("Message")]

    def __init__(self, message: str):
        self.message = message


class InvalidKubeConfigException(KubeConfigException):
    """
    This exception indicates that the kubeconfig file is invalid.
    """

    def __str__(self) -> str:
        return f"Invalid kubeconfig: {self.message}"


"""
    This exception indicates that the kubernetes connection is invalid.
    """  # NOQA


class InvalidConnectionException(ConnectionException):
    def __str__(self) -> str:
        return f"Invalid connection: {self.message}"


class UnusableKubeConfigException(KubeConfigException):
    """
    This exception indicates that the kubeconfig file is valid, but not usable (e.g. no current-context is set).
    """  # NOQA

    def __str__(self) -> str:
        return f"Valid but unusable kubeconfig: {self.message}"


kubeconfig_schema = plugin.build_object_schema(KubeConfig)
connection_schema = plugin.build_object_schema(ConnectionParameters)
