from requests import Session
from requests.exceptions import RequestException
from requests.auth import HTTPBasicAuth
from urllib.parse import urljoin


class Medialoopster:
    def __init__(self, url: str, user: str = None, password: str = None, verify: bool = False):
        self.session = Session()
        self.session.verify = verify

        if all([user, password]):
            self.session.auth = HTTPBasicAuth(user, password)

        self.url = url

    def __enter__(self):
        """Enable context management."""
        return self

    def __exit__(self, *args):
        """Clean up."""
        self.session.close()

    def ping(self):
        try:
            response = self.session.get(f"{self.url}ping/")
            response.raise_for_status()
        except RequestException:
            return False

        return True

    def asset_import(self, production=None, asset_type=None, move_asset=False, name=None, description=None, approval=0,
                     path_file=None, meta_field_store=None):
        if meta_field_store is None:
            meta_field_store = {}

        request = {
            "production": production,
            "type": asset_type,
            "move_asset": move_asset,
            "asset": {
                "asset_meta": {
                    "name": name,
                    "description": description,
                    "approval": approval,
                    "path_file": path_file,
                    "meta_field_store": meta_field_store
                }
            }
        }

        response = self.session.post(f"{self.url}asset/import/", json=request)
        response.raise_for_status()

        response_json = response.json()

        return response_json.get("asset_import_id", None)

    def get_from_api(self, asset_type="videoassets", url=None, with_sequences=True):
        if url is None:
            url = f"{self.url}{asset_type}"

            if asset_type == "videoassets" and with_sequences is True:
                url = f"{url}?with_sequences=true"

        while url:
            try:
                response = self.session.get(url=url)
                response.raise_for_status()
            except RequestException:
                continue

            if response.links is not None:
                url = response.links.get("next", {}).get("url", None)
            else:
                url = None

            yield from response.json()

    def get_productions(self):
        return self.get_from_api(asset_type="productions")

    def get_videoassets(self, with_sequences=True):
        return self.get_from_api(asset_type="videoassets", with_sequences=with_sequences)

    def get_asset(self, asset_id=None, asset_type="videoassets", with_sequences=True, path_file=None):
        if asset_id is not None:
            url = f"{self.url}{asset_type}/{asset_id}/"

            if asset_type == "videoassets" and with_sequences is True:
                url = f"{url}?with_sequences=true"
        elif path_file is not None:
            url = f"{self.url}{asset_type}/?path_file={path_file}"

        response = self.session.get(url=url)
        response.raise_for_status()

        return response.json()

    def search_meta_field_store(self, field: str = None, value: str = None, asset_type: str = "videoassets"):
        assets = []

        for asset in self.get_from_api(asset_type=asset_type):
            meta_field_store = asset.get("meta_field_store")
            if meta_field_store is not None:
                field_value = meta_field_store.get(field)
                if field_value is not None and field_value == value:
                    print(asset.get("id"))
                    assets.append(asset.get("id"))

        return assets

    def archiv_asset(self, content_type_id, asset_id, archive_type, archive_connector):
        url = urljoin(self.url, "archiveactivities/")

        request = [{
            "content_type_id": content_type_id,
            "asset_id": asset_id,
            "archive_type": archive_type,
            "archive_connector": archive_connector,
        }]

        response = self.session.post(url, json=request)
        response.raise_for_status()

        return response.json()

    def restore_asset(self, content_type_id, asset_id, archive_type, archive_connector):
        url = urljoin(self.url, "restoreactivities/")

        request = [{
            "content_type_id": content_type_id,
            "asset_id": asset_id,
            "archive_type": archive_type,
            "archive_connector": archive_connector,
        }]

        response = self.session.post(url, json=request)
        response.raise_for_status()

        return response.json()

    def disapprove_asset(self, asset_id, asset_type="videoassets"):
        url = f"{self.url}{asset_type}/{asset_id}/"

        request = {
            "status_approval": 0
        }

        response = self.session.patch(url, json=request)
        response.raise_for_status()

        return response.json()

    def set_date_del_asset(self, asset_id, date_del, asset_type="videoassets"):
        url = f"{self.url}{asset_type}/{asset_id}/"

        request = {
            "date_del": date_del
        }

        response = self.session.patch(url, json=request)
        response.raise_for_status()

        return response.json()

    def set_date_add_asset(self, asset_id, date_add, asset_type="videoassets"):
        url = f"{self.url}{asset_type}/{asset_id}/"

        request = {
            "date_add": date_add
        }

        response = self.session.patch(url, json=request)
        response.raise_for_status()

        return response.json()

    def edit_meta_field_store(self, asset_id, meta_field_store, asset_type="videoassets"):
        url = f"{self.url}{asset_type}/{asset_id}/"

        request = {
            "meta_field_store": meta_field_store
        }

        response = self.session.patch(url, json=request)
        response.raise_for_status()

        return response.json()
