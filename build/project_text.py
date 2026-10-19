"""Identity text and external identifiers for Lead Green, shared by build.py and hf_dataset.py.

One place for the two canonical sentences (GEO strategy section 10, ruling G1), the funder line, and
the project's homes elsewhere (ruling T6: JSON-LD sameAs, CITATION.cff, .zenodo.json, the dataset card).
No number is typed here; figures come only from build/data through build.py.
"""

# The canonical description. Every registry, dataset card, README, profile and talk abstract uses these two sentences.
PROJECT_DESCRIPTION = (
    "Lead Green is a public index of the GPU energy it takes to serve a million output tokens (watt-hours per million "
    "output tokens), by model, GPU and configuration, with grid carbon intensity to price it anywhere, published as open "
    "data with a JSON API and an MCP server under CC BY 4.0. Every figure comes from a named public source with a "
    "retrieval date; it is a Katonic project, run and paid for by Katonic, and takes no money from hardware, cloud or "
    "model vendors."
)

# The funder line, printed on every page that carries a figure.
FUNDING = (
    "Lead Green is run and paid for by Katonic, which sells a sovereign AI platform and benefits when buyers ask the "
    "questions on this site. It takes no money from hardware, cloud or model vendors."
)

# T1 / G2 (ruled 19 October 2026): the public mirror. The working repository sits in an Enterprise Managed Users
# organisation and cannot be public, so every public link points here. "" omits the repository links from the site.
REPO_URL = "https://github.com/katonic-dev/leadgreen-ai"

# T2 / G6: the Hugging Face dataset. HF_DATASET_REPO is the target hf_dataset.py pushes to; HF_DATASET_URL stays ""
# until the first push has landed, so sameAs never points at a page that does not exist yet.
HF_DATASET_REPO = "leadgreen/green-token-index"
HF_DATASET_URL = "https://huggingface.co/datasets/leadgreen/green-token-index"   # first push 19 October 2026

# T3 / G7: the Zenodo concept DOI for the project (one DOI that always resolves to the latest release), e.g.
# "10.5281/zenodo.1234567". "" until the first deposit exists. Per-release DOIs live on Zenodo itself.
ZENODO_CONCEPT_DOI = ""

# T6: the Wikidata item, e.g. "https://www.wikidata.org/wiki/Q123456789". "" until created.
WIKIDATA_URL = ""

# The LinkedIn Showcase Page under the Katonic company page (D-LI1, 19 October 2026): a project page, not a company page.
LINKEDIN_PAGE_URL = "https://www.linkedin.com/showcase/leadgreen-ai/"

ZENODO_DOI_URL = f"https://doi.org/{ZENODO_CONCEPT_DOI}" if ZENODO_CONCEPT_DOI else ""

# The same project elsewhere, for schema.org sameAs. Only homes that exist are listed.
SAME_AS = [u for u in (REPO_URL, HF_DATASET_URL, ZENODO_DOI_URL, WIKIDATA_URL, LINKEDIN_PAGE_URL) if u]
