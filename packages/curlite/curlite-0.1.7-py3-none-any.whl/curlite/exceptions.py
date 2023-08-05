import re

_curl_errors = [
    (1, "CURLE_UNSUPPORTED_PROTOCOL", "The URL you passed to libcurl used a protocol that this libcurl does not support.", "UnsupportedProtocol"),
    (6, "CURLE_COULDNT_RESOLVE_HOST", "The given remote host was not resolved.", "CouldNotResolveHost"),
    (7, "CURLE_COULDNT_CONNECT", "Failed to connect() to the host or proxy.", "CouldNotConnect"),
    (23, "CURLE_WRITE_ERROR", "An error occurred when writing received data to a local file.", "WriteError"),
    (28, "CURLE_OPERATION_TIMEDOUT", "The specified time-out period was reached according to the conditions.", "OperationTimedOut"),
    (35, "CURLE_SSL_CONNECT_ERROR", "A problem occurred somewhere in the SSL/TLS handshake.", "SSLConnectError"),
    (42, "CURLE_ABORTED_BY_CALLBACK", "The operation was aborted by an application callback set with CURLOPT_ABORTFUNCTION.", "AbortedByCallback"),
    (47, "CURLE_TOO_MANY_REDIRECTS", "Too many redirects.", "TooManyRedirects"),
    (51, "CURLE_PEER_FAILED_VERIFICATION", "The remote server's SSL certificate or SSH md5 fingerprint was deemed not OK.", "SSLConnectionError"),
    (52, "CURLE_GOT_NOTHING", "The server returned nothing (no headers, no data).", "NoResponse"),
    (54, "CURLE_SEND_ERROR", "Failed sending data to the peer.", "SendError"),
    (55, "CURLE_RECV_ERROR", "Failure in receiving network data.", "ReceiveError"),
    (60, "CURLE_SSL_CACERT", "Problem with the CA cert (path? access rights?)", "SSLCACertError"),
    (61, "CURLE_SSL_CACERT_BADFILE", "Could not load CACERT file, missing or wrong format.", "SSLCACertError"),
    (63, "CURLE_FILESIZE_EXCEEDED", "Maximum file size exceeded.", "FileSizeExceeded"),
    (64, "CURLE_USE_SSL_FAILED", "Requested FTP SSL level failed.", "FTPSSLLevelError"),
    (65, "CURLE_SEND_FAIL_REWIND", "Sending the data requires a rewind that failed.", "SendFailRewind"),
    (66, "CURLE_SSL_ENGINE_INITFAILED", "Initiating the SSL Engine failed.", "SSLEngineInitFailed"),
    (67, "CURLE_LOGIN_DENIED", "The remote server denied curl to login.", "LoginDenied"),
    (78, "CURLE_REMOTE_FILE_NOT_FOUND", "The resource referenced in the URL does not exist.", "RemoteFileNotFound"),
    (79, "CURLE_SSH", "An unspecified error occurred during the SSH session.", "SSHError"),
    (80, "CURLE_SSL_SHUTDOWN_FAILED", "Failed to shut down the SSL connection.", "SSLShutdownFailed"),
    (81, "CURLE_AGAIN", "Socket is not ready for send/recv, wait till it's ready and try again.", "SocketNotReady"),
    (82, "CURLE_SSL_CRL_BADFILE", "Failed to load CRL file.", "SSLBadFile"),
    (83, "CURLE_SSL_ISSUER_ERROR", "Issuer check failed.", "SSLIssuerError"),
    (84, "CURLE_FTP_PRET_FAILED", "The FTP server does not understand the PRET command.", "FTPPretFailed"),
]



def _get_curl_error_number(curl_error_line: str):
    pattern = r"curl: \(([1-9]|[1-9][0-9]|100)\)"
    match = re.search(pattern, curl_error_line)
    if match:
        return int(match.group(1))
    return None

def _get_curl_error_extra_description(curl_error_line: str):
    curl_error_number = _get_curl_error_number(curl_error_line)
    for error in _curl_errors:
        if error[0] == curl_error_number:
            return error
    return None


class RequestError(IOError):
    def __init__(self, error_line: str, url: str, extra_description: str = ""):
        error_statement = error_line.split(":")
        error_message = error_statement[1].strip()
        error_message = f"Error accessing url: {url} due to {{{error_message}}}."
        if extra_description:
            error_message = f"{error_message}\n{extra_description}."
        super().__init__(error_message)


def get_exception_for_curl_error(curl_error: str, url: str):
    curl_error_lines = curl_error.splitlines()
    error_line = curl_error_lines[-1]
    extra_description = _get_curl_error_extra_description(error_line)
    if extra_description:
        ExceptionClass = create_exception_class(extra_description[3], RequestError)
        extra_exception_description = extra_description[2]
    else:
        ExceptionClass = RequestError
        extra_exception_description = ""
    return ExceptionClass(curl_error, url, extra_description=extra_exception_description)


def create_exception_class(name, parent=Exception) -> type[RequestError]:
    return type(name, (parent,), {})



class ResponseError(Exception):
    """Base exception class for HTTP response errors."""

class InformationalError(ResponseError):
    """Exception class for HTTP informational responses (100-199)."""

class ClientError(ResponseError):
    """Exception class for HTTP client error responses (400-499)."""

class ServerError(ResponseError):
    """Exception class for HTTP server error responses (500-599)."""
