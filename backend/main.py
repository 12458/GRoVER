from fastapi import FastAPI
from fastapi.responses import FileResponse

from scidownl import scihub_download
from scholarly import scholarly


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/paper")
def read_item(doi: str):
    scihub_download(doi, paper_type="doi", out=f"/tmp/{doi}.pdf")
    # serve the file
    return FileResponse(path=f"/tmp/{doi}.pdf")

@app.get("/paper/search")
def search_paper(q: str):
    scihub_download(q, paper_type="search", out=f"/tmp/{query}.pdf")
    # serve the file
    return FileResponse(path=f"/tmp/{query}.pdf"