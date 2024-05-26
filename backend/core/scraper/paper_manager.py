from typing import Any
from scholarly import scholarly
from crossref.restful import Works
from scidownl import scihub_download
from pypdf import PdfReader
import google.generativeai as genai
import re
import os


class PaperManager:
    def __init__(self):
        GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=GOOGLE_API_KEY)
        self.works = Works()
        self.model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")

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

    def summarise_paper(self, text: str) -> str:
        """
        Summarise the content of a paper.

        Args:
            text (str): The text of the paper to be summarised.

        Returns:
            str: The summarised content of the paper.
        """

        sys_prompt = r"""
Provide a comprehensive summary of the given text. The summary should cover all the key points and main ideas presented in the original text, while also condensing the information into a concise and easy-to-understand format. Please ensure that the summary includes relevant details and examples that support the main ideas, while avoiding any unnecessary information or repetition. The length of the summary should be appropriate for the length and complexity of the original text, providing a clear and accurate overview without omitting any important information. The text to summarise is delimited by backticks (```). Delimit the summarised text with curly brackets {SUMMARISED_TEXT}.
"""

        response = self.model.generate_content([sys_prompt, "```" + text + "```"])
        return response.text

    def get_paper_citations(self, doi: str) -> tuple[dict, int]:
        """
        Get the number of citations of a paper using the provided DOI.

        Args:
            doi (str): The DOI (Digital Object Identifier) of the paper.

        Returns:
            tuple[dict, int]: A tuple containing a dictionary of references and the number of citations of the paper.
        """
        work = self.works.query(bibliographic=doi)
        for item in work:
            return item["reference"], item["is-referenced-by-count"]

    @staticmethod
    def extract_text_from_pdf(pdf_path: str) -> str:
        text = ""
        try:
            with open(pdf_path, "rb") as file:
                reader = PdfReader(file)
                for page_num in range(reader.get_num_pages()):
                    page = reader.pages[page_num]
                    text += page.extract_text()
        except Exception as e:
            print(f"Error reading PDF file: {e}")
        return text

    @staticmethod
    def extract_response(text):
        pattern = r"\{([^}]*)\}"
        response = re.search(pattern, text)
        if response:
            return response.group(1)
        return None


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
