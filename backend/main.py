from fastapi import FastAPI
from fastapi.responses import FileResponse
from core.scraper.paper_manager import PaperManager


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/paper/download")
def read_item(doi: str):
    pm = PaperManager()
    path = pm.download_paper(doi)
    # serve the file
    return FileResponse(path=path)


@app.get("/paper/search")
def search_paper(q: str):
    pm = PaperManager()
    result = pm.search_paper(q)
    return {"result": result}


@app.get("/paper/search_query_download")
def search_query_download(q: str):
    pm = PaperManager()
    result = pm.search_paper(q)
    bibtex = pm.get_bibtex(result[0])
    doi = pm.get_doi(bibtex)
    if doi:
        path = pm.download_paper(doi)
        return FileResponse(path=path)
    return {"error": "No paper found"}
