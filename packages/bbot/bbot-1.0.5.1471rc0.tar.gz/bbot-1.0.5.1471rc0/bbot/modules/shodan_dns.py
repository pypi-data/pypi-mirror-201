from .crobat import crobat


class shodan_dns(crobat):
    """
    A typical module for authenticated, API-based subdomain enumeration
    Inherited by several other modules including securitytrails, c99.nl, etc.
    """

    watched_events = ["DNS_NAME"]
    produced_events = ["DNS_NAME"]
    flags = ["subdomain-enum", "passive", "safe"]
    meta = {"description": "Query Shodan for subdomains", "auth_required": True}
    options = {"api_key": ""}
    options_desc = {"api_key": "Shodan API key"}

    base_url = "https://api.shodan.io"

    def setup(self):
        super().setup()
        return self.require_api_key()

    def ping(self):
        r = self.request_with_fail_count(f"{self.base_url}/api-info?key={self.api_key}")
        resp_content = getattr(r, "text", "")
        assert getattr(r, "status_code", 0) == 200, resp_content

    def request_url(self, query):
        url = f"{self.base_url}/dns/domain/{self.helpers.quote(query)}?key={self.api_key}"
        return self.request_with_fail_count(url)

    def parse_results(self, r, query):
        json = r.json()
        if json:
            for hostname in json.get("subdomains"):
                yield f"{hostname}.{query}"
