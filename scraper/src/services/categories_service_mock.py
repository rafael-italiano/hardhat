from services.base_service import BaseService

class LeroyMerlinCategoryServiceMock(BaseService):

    def process(self) -> list:

        return [
            {
                "category": "Aço para Construção",
                "subcategory": "Acessórios para Aço",
                "url": "https://www.leroymerlin.com.br/acessorios-para-aco"
            },
            {
                "category": "Aço para Construção",
                "subcategory": "Arame",
                "url": "https://www.leroymerlin.com.br/acos-para-construcao-arames"
            },
            {
                "category": "Madeiras para Construção",
                "subcategory": "Acessórios para Madeiras",
                "url": "https://www.leroymerlin.com.br/acessorios-de-madeiras-para-construcao"
            }
        ]