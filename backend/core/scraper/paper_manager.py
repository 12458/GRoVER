from typing import Any
from scholarly import scholarly
from crossref.restful import Works
from scidownl import scihub_download


class PaperManager:
    def __init__(self):
        self.works = Works()

    def search_paper(self, q: str, limit: int = 20) -> str | None:
        """
        Search for a paper using a given query.

        Args:
            q (str): The search query.
            limit (int, optional): The maximum number of search results to retrieve. Defaults to 20.

        Returns:
            str | None: The DOI (Digital Object Identifier) of the found paper, or None if no paper is found.
        """
        result = []
        search_query = scholarly.search_pubs(q)
        for i in range(limit):
            try:
                result.append(next(search_query))
            except StopIteration:
                break
        return result

    def get_doi(self, bibtex: str) -> str | None:
        """
        Get the DOI of a paper using the BibTeX information.

        Args:
            bibtex (str): The BibTeX information of the paper.

        Returns:
            str | None: The DOI (Digital Object Identifier) of the found paper, or None if no paper is found.
        """

        work = self.works.query(bibliographic=bibtex)
        for item in work:
            print(item)
            return item["DOI"]
        return None

    def download_paper(self, doi: str) -> str:
        """
        Downloads a paper using the provided DOI.

        Args:
            doi (str): The DOI (Digital Object Identifier) of the paper.

        Returns:
            str: The file path of the downloaded paper.
        """
        scihub_download(doi, paper_type="doi", out=f"/tmp/{doi}.pdf")
        return f"/tmp/{doi}.pdf"

    def get_bibtex(self, paper: Any) -> str:
        """
        Get the BibTeX information of a paper.

        Args:
            paper (Any): The paper object.

        Returns:
            str: The BibTeX information of the paper.
        """
        return scholarly.bibtex(paper)


if __name__ == "__main__":
    pm = PaperManager()
    papers = pm.search_paper("Deep Learning")
    bibtex = scholarly.bibtex(papers[0])
    print(bibtex)
    doi = pm.get_doi(
        bibtex=bibtex,
    )
    path = pm.download_paper(doi)
    print(path)
