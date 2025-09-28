import httpx

from .base_client import BaseAPI

BASE_URL = "https://1cf3zt43zu-dsn.algolia.net/1/indexes/*/queries"
HEADERS = {
    "Accept": "application/json",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Content-Type": "text/plain",
    "Origin": "https://www.leroymerlin.com.br",
    "Referer": "https://www.leroymerlin.com.br/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:143.0) Gecko/20100101 Firefox/143.0"
}
PARAMS={
    "x-algolia-agent": "Algolia for JavaScript (5.10.2); Lite (5.10.2); "
                        "Browser; react (18.2.0); react-instantsearch (7.16.3); "
                        "react-instantsearch-core (7.16.3); JS Helper (3.26.0)",
    "x-algolia-api-key": "150c68d1c61fc1835826a57a203dab72",
    "x-algolia-application-id": "1CF3ZT43ZU",
}

class LeroyMerlinClient(BaseAPI):
    def __init__(self):

        self.session = httpx.Client(
            base_url=BASE_URL,
            params=PARAMS,
            headers=HEADERS
        )

    def get(self, category: str, subcategory: str) -> dict:

        page = 0
        response = self._make_request(page, category, subcategory)
        results = response['results'][0]
        hits = results['hits']
        while results['page']+1 < results['nbPages']:
            page += 1
            response = self._make_request(page, category, subcategory)        
            results = response['results'][0]
            hits.extend(results['hits'])
        return hits
    
    def _make_request(self, page: int, category:str, subcategory:str)-> dict:

        body = {
            "requests": [
                {
                    "indexName": "production_products",
                    "analytics": True,
                    "analyticsTags": [
                        "#vale_do_paraiba",
                        "#loginOff",
                        "#categorypage",
                        "#desktop"
                    ],
                    "clickAnalytics": True,
                    "facetingAfterDistinct": True,
                    "facets": [],
                    "filters": (
                        'regionalAttributes.vale_do_paraiba.promotionalPrice > 0 '
                        'AND regionalAttributes.vale_do_paraiba.available=1 '
                        'AND regionalAttributes.vale_do_paraiba.stock.hasStock=1 '
                        f'AND categoryPageId: "Materiais de Construção > {category} > {subcategory}"'
                    ),
                    "hitsPerPage": 100,
                    "maxValuesPerFacet": 1000,
                    "page": page,
                    "query": "",
                    "userToken": "anonymous-437438c1-eb51-4afb-833a-7c6ad5d0e5fb"
                }
            ]
        }
        response = self.session.post(
            url='',
            json=body
        )
        response.raise_for_status()
        return response.json()

    def close(self):
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()