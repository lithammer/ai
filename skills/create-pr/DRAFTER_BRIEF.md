# Drafter Brief

Read the diff against the supplied base and use the supplied context to write
the description. Leave the working tree unchanged. Create the PR as a draft
unless explicitly requested ready for review. Return the URL, or the title,
body, and blocker if creation fails.

Describe the outcome, not the steps taken to implement it. Start with one
sentence. Each additional sentence must supply context the reviewer needs to
understand the change. The description introduces the diff; it does not replace
reading it. Leave explanations already present in the changed code or documents
there. Omit validation summaries. Add an example, traceback, log excerpt, graph,
diagram, or other visualisation only when it makes the outcome clearer than prose
alone.
