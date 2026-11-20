# Project ZeST (`zest-core`)

**Open-source architecture and discrete-event simulation for European & UK intermodal freight velocity.**

Project ZeST demonstrates how *Data-Precedes-Physical* manifest synchronization—anchored to EU eFTI (Regulation 2020/1056) and DCSA 3.0 eBL standards—eliminates port yard dwell, prevents yard re-handling, and unlocks inland rail capacity across TEN-T and UK corridors.

* **Live Documentation, Policy Briefs & Corridor Series:** [https://open-zest.web.app](https://open-zest.web.app)
* **Lead Architect:** James P. Reefe

## Local Quickstart

```bash
# 1. Run the test suite
pytest

# 2. Preview documentation locally (includes docs/drafts/)
mkdocs serve

# 3. Validate production build (strict mode)
mkdocs build --strict
Repository Structure
solvers/ — SimPy discrete-event terminal/rail simulations and zone-block stowage heuristics
schemas/ — Pydantic v2 eFTI and pre-arrival manifest models
scripts/ — Corridor benchmark runners and diagram generators
docs/ — MkDocs Material source for open-zest.web.app
