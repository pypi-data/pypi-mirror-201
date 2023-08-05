from __future__ import annotations

import httpx
import xmltodict
from loguru import logger

from depend.helper import make_url


class LicensePlugin:
    key = "pkg_lic"

    def __init__(self, client: httpx.AsyncClient) -> None:
        self.client = client

    async def resolve(
        self,
        language: str,
        package: str,
        version: str,
        context: dict,
    ) -> list[str]:
        api_url = make_url(language, package, version)

        api_response = await self.client.get(api_url)
        if language == "go":
            api_data = api_response.text
        elif language == "cs":
            api_data = xmltodict.parse(api_response.text)
        else:
            api_data = api_response.json()

        license = self.get_license(language, api_data)
        if not license:
            # TODO: get the repo url from api response and stuff and use dep files
            logger.debug("License ({}:{}): License not found via API", package, version)
            return ["Other"]

        if isinstance(license, list):
            return license
        else:
            return [license]

    @staticmethod
    def get_license(language: str, api_data: dict) -> str | list[str] | None:
        if language == "cs":
            root = api_data.get("package", {}).get("metadata", {})
            if root.get("license", {}).get("@type") == "expression":
                return root.get("license", {}).get("#text", "").strip()

        elif language == "go":
            # soup = BeautifulSoup(api_data, "html.parser")
            # details_element = soup.find("div", class_="go-Main-headerDetails").getText()
            # details = dict(re.findall(r"([^ \n:]+): ([- ,.\w]+)", details_element))
            # details.get("License", "").strip()
            return "Not Implemented"

        elif language == "javascript":
            license_data = api_data.get("license") or api_data.get("licenses")

            if isinstance(license_data, str):
                return license_data.split(",")

            #  The cases below are just to as to add support for older packages
            if isinstance(license_data, dict):
                return license_data.get("type")

            if isinstance(license_data, list):
                if all(isinstance(item, dict) for item in license_data):
                    licenses = []
                    for data in license_data:
                        license_type = data.get("type")
                        if license_type is not None:
                            licenses.append(license_type)
                    return licenses
                if all(isinstance(item, str) for item in license_data):
                    return license_data

        elif language == "php":
            version_data = api_data.get("package", {}).get("versions", {})
            return version_data.get("license")

        elif language == "python":
            package_license = api_data.get("info", {}).get("license")
            if package_license:
                return package_license

            licenses = []
            classifiers = api_data.get("info", {}).get("classifiers", [])
            for classifier in classifiers:
                _, is_license, license_name = classifier.partition("License ::")
                if is_license:
                    licenses.append(license_name.strip())

            return licenses

        elif language == "rust":
            return api_data.get("version", {}).get("license")
