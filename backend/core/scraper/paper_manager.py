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

    def get_doi(self, title: str, author: str, journal: str) -> str | None:
        """
        Get the DOI of a paper using the title, author, and journal.

        Args:
            title (str): The title of the paper.
            author (str): The author of the paper.
            journal (str): The journal of the paper.

        Returns:
            str | None: The DOI (Digital Object Identifier) of the found paper, or None if no paper is found.
        """
        work = self.works.query(
            bibliographic=title, author=author, publisher_name=journal
        )
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


if __name__ == "__main__":
    pm = PaperManager()
    papers = pm.search_paper("Deep Learning")
    print(papers[0])
    doi = pm.get_doi(
        papers[0]["bib"]["title"],
        papers[0]["bib"]["author"],
        papers[0]["bib"]["venue"],
    )
    path = pm.download_paper(doi)
    print(path)
