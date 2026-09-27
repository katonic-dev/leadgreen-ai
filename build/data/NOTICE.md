# Notices for the data snapshots in build/data

Every figure on leadgreen.ai is computed by `build/build.py` from the files in this folder, each kept exactly as retrieved. This file records, per snapshot, where it came from, when, and on what terms it is reproduced. The compilation and the derived figures are CC BY 4.0; the code is Apache 2.0 (`LICENSE` at the site root). Each source keeps its own licence, which this site never overrides.

## mlenergy-v3-lm-arena-chat-2026-09-26.json, mlenergy-v3-gpqa-2026-09-26.json

- Source: ML.ENERGY Leaderboard, The ML.ENERGY Initiative (started at SymbioticLab, University of Michigan), https://ml.energy/leaderboard/
- Files: https://raw.githubusercontent.com/ml-energy/leaderboard/master/public/data/tasks/lm-arena-chat.json and .../gpqa.json
- Version: 3.0, released 1 December 2025; data compiled 16 February 2026 (the leaderboard's public/data/index.json last_updated)
- Retrieved: 26 September 2026
- Licence as stated by the source: Apache-2.0 on the Hugging Face dataset ml-energy/benchmark-v3 (tag, LICENSE file and dataset card) and in the leaderboard web app's footer.
- Licence evidence and its gap: the leaderboard repository (github.com/ml-energy/leaderboard) carries no licence file. The JSON is reproduced as published measurements on the basis of the dataset card while the ML.ENERGY team is asked to confirm that the licence covers the leaderboard files. The Apache License 2.0 text is in `LICENSE` at the site root, as section 4(a) requires for redistribution.
- Cite: Chung et al., The ML.ENERGY Benchmark: Toward Automated Inference Energy Measurement and Optimization, NeurIPS 2025 Datasets and Benchmarks, arXiv 2505.06371.
- Changes: none to the files. The site selects rows, converts units and states the selection rule.

## ember-yearly-total-generation-extract-2026-09-26.csv

- Source: Ember, Yearly electricity data, https://ember-energy.org/data/yearly-electricity-data/
- Version: September 2026 release
- Retrieved: 26 September 2026
- Licence: CC BY 4.0
- Changes: an extract of the columns the site uses (area, ISO 3 code, year, emissions intensity); values unchanged.

## aienergyscore-text_generation-2026-09-26.csv

- Source: AI Energy Score leaderboard (Hugging Face and Salesforce, with Neuralwatt, Cohere, Meta and Carnegie Mellon University), https://huggingface.co/spaces/AIEnergyScore/Leaderboard
- File: data/energy/text_generation.csv in the Space
- Retrieved: 26 September 2026
- Licence: Apache-2.0 as tagged on the Space; the project states no separate licence for the results file, which is reproduced as facts with attribution.
- Changes: none to the file. The API keeps the source's model string in source_label and carries a clean Hugging Face id in model.

## nvidia-hardware-2026-09-26.json

- Sources: NVIDIA Multi-Instance GPU User Guide, supported MIG profiles (https://docs.nvidia.com/datacenter/tesla/mig-user-guide/supported-mig-profiles.html); NVIDIA product specifications for A100, H100, H200 and DGX B200; NVIDIA, Product Carbon Footprint Summary for HGX B200 (July 2025).
- Retrieved: 26 September 2026
- Terms: manufacturer specifications transcribed as facts; NVIDIA retains its rights in the source documents. NVIDIA grants no licence and none is claimed.

## iso3166-1-alpha3-to-alpha2-2026-09-27.json

- Source: the ISO 3166-1 table in pycountry 26.2.16 (from the Debian iso-codes project), read from the downloaded wheel on 27 September 2026.
- Licence: pycountry is LGPL-2.1; the table holds country codes, which are facts. Used only to add the alpha-2 code beside Ember's alpha-3 code.
- Kosovo has no ISO 3166-1 code and carries none.
