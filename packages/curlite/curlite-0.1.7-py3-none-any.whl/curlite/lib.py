import subprocess
import json as json_parser
from curlite.exceptions import get_exception_for_curl_error
from curlite import exceptions



class CurlWrapper:
    def __init__(self):
        self.default_headers = {}

    def get(self, url, params=None, headers=None, timeout=None):
        return self.request("GET", url, params=params, headers=headers, timeout=timeout)

    def post(self, url, data=None, json=None, headers=None, timeout=None):
        return self.request("POST", url, data=data, json=json, headers=headers, timeout=timeout)

    def put(self, url, data=None, json=None, headers=None, timeout=None):
        return self.request("PUT", url, data=data, json=json, headers=headers, timeout=timeout)

    def delete(self, url, headers=None, timeout=None):
        return self.request("DELETE", url, headers=headers, timeout=timeout)

    def request(self, method, url, params=None, data=None, json=None, headers=None, timeout=None):
        cmd = ["curl", "--include", "-X", method, url]

        # Handle headers
        headers = headers or self.default_headers
        for key, value in headers.items():
            cmd.extend(["-H", f"{key}: {value}"])

        # Handle query parameters
        if params:
            query_params = "&".join([f"{key}={value}" for key, value in params.items()])
            cmd.append(f"{url}?{query_params}")

        # Handle timeout
        if timeout:
            _delay = timeout
        else:
            _delay = 60
        cmd.extend(["--max-time", str(_delay)])

        # Handle data for POST and PUT requests
        if data:
            cmd.extend(["--data", data])
        elif json:
            cmd.extend(["--header", "Content-Type: application/json"])
            cmd.extend(["--data", json_parser.dumps(json)])

        # Run the curl command and capture the output
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Handle errors and return the response
        if result.returncode != 0:
            exception = get_exception_for_curl_error(result.stderr, url=url)
            if exception:
                raise exception
            raise Exception(f"curl command failed with error: {result.stderr}")
        response = result.stdout
        return Response(url=url, raw_response=response)



class Response:
    raw_response: str
    status_line: str
    headers: dict
    content: str

    def __init__(self, url:str, raw_response: str):
        self.raw_response = raw_response
        self.status_line, self.headers, self.content = self._parse_response()
        self.url = url

    def _parse_response(self):
        header_section, content_section = self.raw_response.split("\n\n")
        headers = {}
        status_line = ""

        for line in header_section.split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                headers[key.strip()] = value.strip()
            elif "HTTP" in line:
                status_line = line.strip()

        return status_line, headers, content_section

    def json(self):
        if not self.content:
            return {}
        try:
            return json_parser.loads(self.content)
        except json_parser.JSONDecodeError:
            raise ValueError(f"{self.content} can not be decoded as json")

    def text(self):
        return self.content

    @property
    def status_code(self):
        return int(self.status_line.split()[1])

    @property
    def reason(self):
        return " ".join(self.status_line.split()[2:])

    @property
    def ok(self):
        return 200 <= self.status_code < 300
    
    def raise_for_status(self):
        status_code = self.status_code
        message = f"HTTP Error {self.status_code}: {self.reason}\n{self.content}"
        if 100 <= status_code < 200:
            raise exceptions.InformationalError(self.content)
        elif 400 <= self.status_code < 500:
            raise exceptions.ClientError(message)
        elif 500 <= self.status_code < 600:
            raise exceptions.ServerError(message)


requests = CurlWrapper()
