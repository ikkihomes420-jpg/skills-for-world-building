# Retrieval and Evidence

Use retrieval to find relevant context, not to manufacture certainty. The authoritative bundle records remain the source of canon. The derived index, keyword matches, aliases, relationship expansion, and future semantic matches are retrieval aids that can be deleted and rebuilt.

## Retrieval sequence

1. Load the manifest and active snapshot to establish purpose, branch, present state, and capture policy.
2. Apply hard filters first: branch, visibility, record type, status, and scope when known.
3. Resolve explicit IDs, names, aliases, spelling variants, and titles.
4. Rank exact label/ID matches above full-text matches. Rank user-approved and confirmed material above lower-authority material when relevance is otherwise similar.
5. Expand relationship context only when it directly affects the request. Keep the expansion budget small.
6. Return an evidence packet that includes status, authority, confidence, source/support, linked records, and the reason each record was retrieved.
7. Answer from the packet. Clearly label established, provisional, contested, and unknown material.

## Search policy

The default query view is approved mainline canon. Use `--include-noncanonical` only when the user asks for brainstorming, open questions, disputed accounts, provisional work, or an audit. Do not blend provisional material into a canon answer without an explicit label.

Use `query_canon.py <bundle> <query> --hops 1` to retrieve direct causal and relationship context. Use a higher hop count only when the user requests systems analysis or impact reasoning. A larger retrieval set is not automatically better context.

## Evidence packet standard

Every material recall response should be grounded in a compact packet with these fields:

| Field | Function |
|---|---|
| Record ID and label | Allows precise inspection and follow-up. |
| Status and branch | Distinguishes present canon from drafts, disputes, and alternatives. |
| Authority and confidence | Shows how strongly the system should rely on it. |
| Source/support | Gives the author a route back to the conversation, source, or decision. |
| Retrieval reason | Explains why it was selected for the current request. |
| Linked records | Exposes immediately relevant dependencies and effects. |

A good answer may summarize records in fluent prose, but it must preserve the underlying distinction between source evidence and assistant interpretation.

## Alias and identity policy

Use a stable ID for an identity; preserve renamed, translated, shortened, historical, and in-world names in `aliases`. Do not resolve two identities merely because their names are similar. If an alias might denote several entities, treat it as ambiguous and ask, filter by context, or present alternatives.

## Derived index lifecycle

Run `build_index.py` after an approved change, a bulk import, a migration, or a repair. The transaction tool rebuilds it automatically after apply or rollback. Do not manually edit `.canon/index.json`; it is derived state. If it appears stale or corrupt, delete it and rebuild.

Semantic retrieval may be added later as a candidate-finding layer, but it must use status/branch/visibility filters before ranking and must never auto-merge records or promote a similar statement into canon.
