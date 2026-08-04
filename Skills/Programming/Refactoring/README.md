# Python refactoring branch

Three skills implement approved plans without repeating review:

- `python-refactoring` enforces the common authorization envelope and applies general approved items;
- `style-refactoring` applies approved naming/import/format/readability items;
- `code-simplifier-refactoring` applies approved duplication and complexity reductions.

Each skill requires explicit approval evidence, finding IDs, allowed paths, an authorized change, preserved public behavior, and required checks. It must stop on baseline drift, path expansion, behavior change, unavailable mandatory checks, or a need to edit a rejected/deferred item.

Every edit maps to exactly one approved finding ID. A successful report has `unexpected_changes: []`; passing implementation-detail tests alone does not establish behavior preservation.
