# 10. Unresolved items

status: unverified unless a row says the measurement exists and the decision does not.

1. **Token budget.** The simulation is over by 6 and 14 tokens. Whether to shorten `AGENTS.md`, `manifest.json`, or skill cards, or to change `BUDGET`, is undecided. The failing checks stay.

2. **Notebook fidelity to the book.** Cells were not diffed one-to-one against code blocks in the PDF. Filename and import alignment is only a candidate mapping.

3. **Third-party notebook execution.** Google ADK, LangChain, CrewAI, OpenAI, FastMCP, OpenEvolve, and Pydantic were not installed. Live API behavior is unknown. Several snippets do not parse, so they would fail before any API call.

4. **Ground-truth emoji lines.** Seventeen lines differ from Poppler 24.02.0. The stored file was not regenerated. Which Poppler version produced the committed extract was not recorded in `ground-truth/README.md`.

5. **Print edition.** `pdfinfo` shows producer PyPDF2 and 458 letter pages. Whether that matches a Springer print copy, and whether "424 pages" referred to a different file, is unknown.

6. **Retail status.** The Amazon URL was not fetched. The README no longer says "pre-order" as a current fact.

7. **Google Drive and the Google Doc TOC.** Not opened. They may or may not still contain the missing appendix notebooks.

8. **Model profiles.** Context windows and costs in `models/*.md` were not checked against vendors.

9. **License.** Notebook headers assert MIT and cite a missing file. No license text was added. The grant, if any, is outside this repository.

10. **Colab user ids.** Numeric ids remain in seven notebooks and in git history. Stripping them from HEAD would not purge history. Left for a human decision.

11. **Deep-dive code.** `skills/*/references/deep-dive.md` was not executed. Some snippets name `localhost:8000` and public HTTP examples. They are documentation, not a running server.

12. **Chapter 19 metrics.** The basic evaluation notebook printed `Response accuracy: 0.0`. Whether that is the intended demonstration was not compared to the chapter.

13. **Secret scan of the PDF binary.** `pdfinfo` reports no encryption and no JavaScript. A dedicated secret scanner over compressed PDF streams was not run.

14. **Issues on the evoiz repository.** This repo has issues and discussions disabled. The evoiz issue tracker was not queried.

15. **Ontology acceptance.** Candidate mappings use this repo's skill ids. No external review has accepted or rejected them.
