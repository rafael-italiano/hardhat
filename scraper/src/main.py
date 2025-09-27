from services.categories_services import LeroyMerlinCategoryService

if __name__ == 'main':
    service = LeroyMerlinCategoryService()
    print('iniciando processamento')
    results = service.process()
    ('resultados')
    print(results)
    print('fim do processamento')