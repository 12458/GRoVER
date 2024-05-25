from fastapi import FastAPI
from fastapi.responses import FileResponse

from scidownl import scihub_download


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/paper")
def read_item(doi: str):
    scihub_download(doi, paper_type="doi", out=f"/tmp/{doi}.pdf")
    # serve the file
    return FileResponse(path=f"/tmp/{doi}.pdf")
