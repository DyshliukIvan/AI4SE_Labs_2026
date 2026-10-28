---
name: architecture-adr
description: Discuss software architecture alternatives from project requirements, record the discussion, and create and revise an Architecture Decision Record with the user. Use for architecture selection and ADR work, not for implementing the application.
---

# Architecture discussion and ADR

## Start from requirements

Read the requirements file the user identifies. If a directory contains several projects, use only the assigned project. Ask for its identity only when ambiguous.

Before discussing alternatives, create discussion notes in the requested output directory. In a new trial, use separate files so the previous run is preserved. Record relevant user feedback and changes throughout the session; notes need not be a verbatim transcript.

Summarize the main capabilities and architecture-driving constraints. Separate stated requirements from assumptions and missing information. Ask only questions that affect the comparison. Do not assume that a small application needs microservices, that load is uniform, or that a cloud option is automatically cheaper.

## Discuss alternatives with the user

Propose three credible architectures for the requirements unless the user requests another number. Do not mechanically reuse the same three options or a previous project's chosen solution. When options overlap, explain which deployment or responsibility boundaries differ.

For each option, cover:
- The main components, data ownership and communication, using a small readable diagram.
- How a representative required operation works.
- Benefits and drawbacks in this project's context.
- A concrete implementation difficulty and its consequences, such as authorization across services, data consistency, connection recovery or deployment work.

Use short explanations in the user's language. Let the user ask questions, challenge trade-offs and express priorities. Build on answers already given rather than repeating them as a quiz. Explain implementation details only far enough to make the architectural trade-off clear; do not drift into building the application.

Keep proposals and user preferences distinct in the notes. Do not invent user responses, approvals, performance figures or comparisons. Summarize replies neutrally without turning tentative assumptions into established requirements.

## Select and document

Compare the options against the stated requirements and the user's expressed priorities. Prefer a simple comparison table unless numerical weights and scores have a defensible basis. Do not choose on the user's behalf when a material preference is still unresolved.

After the architecture discussion, create an ADR with:
- Title, date and status.
- Context and important assumptions.
- Decision and concise rationale.
- A diagram with clear component connections.
- Alternatives and their trade-offs.
- Benefits, disadvantages and remaining responsibilities.
- One relevant operation showing how the design works.
- Open questions and conditions for revisiting the decision.
- Links to the requirements and discussion notes.

If managed services are selected, separate the provider's capabilities from the application's business rules and access configuration. Do not select a vendor unless the task requires it or the user requests it.

## Review and revise

Ask the user to inspect clarity, missing or unnecessary content, the diagram and implementation responsibilities. Revise according to their feedback and record what changed. Keep the writing plain and remove repetition; retain material trade-offs.

Preserve prior versions when recording review iterations. Mark the ADR accepted only after the user accepts it. Do not invent review rounds to satisfy a target count.

## Finish

Return the ADR and discussion notes. Do not add application code, a separate audit or unrelated documents unless requested.

For an explicit before/after evaluation, compare the actual recordings for input, model/tool settings when available, coverage, clarification needs and revisions. Report timing or message counts only when measured and defined consistently. State limitations if the same user already knows the project or different tools/models were used. Do not claim improvement before the second run exists.
