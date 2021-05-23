import requests

class DynamicDns:

    r"""
    This object, when supplied with the correct parameters, will automatically update
    A records that are held by GoDaddy. It works by pointing the object towards a domain.
    It will then iterate through all the A records attached to that domain, updating the IP
    address within the record as it goes.

    The IP address that it updates is the public address wherever this code is run.

    This program works on the principle of exclusion. The program will update ALL A records unless
    you tell it otherwise. To exclude a subdomain during the update process, add the subdomain string
    to the :list[str]:`exclusions` parameter when initialising an instance of this class.

    Parameters
    ----------
    key: :class:`str`
        The key portion of the API Key generated at https://developer.godaddy.com/keys
    
    secret: :class:`str`
        The secret portion of the API Key generated at https://developer.godaddy.com/keys

    domain: :class:`str`
        The domain registered with GoDaddy

    exclusions: Optional[:class:`list[str]`]
        A list of the subdomains that will be excluded during the update process
    """

    def __init__(self, key: str, secret: str, domain: str, exclusions: list[str] = list()):

        self.domain = domain
        self.api_key = f"{key}:{secret}"
        self._exclusions = exclusions
        self.update_a_records()

    @property
    def __godaddy_url(self) -> str:

        return f"https://api.godaddy.com/v1/domains/{self.domain}/records/A/"

    @property
    def __ip(self) -> str:

        return requests.get(url="https://api.ipify.org").text

    @property
    def exclusions(self) -> list[str]:

        return list(map(str.upper, self._exclusions))

    def update_a_records(self):

        ip = self.__ip
        for subdomain in self.grab_subdomains():
            requests.put(
                url=self.__godaddy_url + subdomain,
                headers={
                    "Authorization": f"sso-key {self.api_key}",
                    "Content-Type": "application/json"
                },
                json=[{"data": ip}]
            )

    def grab_subdomains(self) -> str:

        response = requests.get(
            url=self.__godaddy_url, 
            headers={"Authorization": f"sso-key {self.api_key}"}
        )
        for record in response.json():
            if record.get("name").upper() not in self.exclusions:
                yield record.get("name")
