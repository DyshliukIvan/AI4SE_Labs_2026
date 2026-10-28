# Task 3 — Architecture skill and comparison

Project: Teamify  
Date: 2026-10-28

## Created skill

[architecture-adr](../.github/skills/architecture-adr/SKILL.md) was created from the recorded discussions in Tasks 1 and 2. It guides the assistant to read requirements, discuss three suitable architectures, keep notes, explain implementation trade-offs, select an option with the user, and create and revise an ADR.

The skill also carries forward the review preferences: clear diagrams, practical examples, concise writing and an explicit division of responsibilities. It is reusable: it does not prescribe Teamify, a particular provider or a managed backend as the answer.

## Repeat in a new session

A new VS Code session used the skill and the same Teamify requirements. It was instructed not to read the previous discussions or ADR and saved separate outputs in with_skill.

The assistant discussed a modular monolith, a core application with a separate chat/live-delivery service, and a managed backend. After discussing the trade-offs, the user selected the managed backend. The assistant created ADR v1, replaced its responsibilities list with a table at the user's request in v2, and saved the accepted document as v3 after approval.

## Comparison

| Aspect | Without the skill | With the skill |
| --- | --- | --- |
| Discussion | The three options were covered, but we returned to Task 1 to focus the discussion before completing the ADR work. | Each option was presented with components, an operation, benefits, drawbacks and an implementation difficulty. |
| Diagrams | The ADR diagram was clarified during review. | The first ADR already included a diagram showing identity, functions, database access and real-time delivery. |
| Responsibilities | A clearer provider/team split was requested during review. | The initial ADR already explained the responsibilities; review changed their presentation into a table. |
| Implementation detail | We discussed authorization, transactions and notification retries. | The assistant addressed these concerns from the start and also made active-subscription revocation explicit. |
| ADR review | Changes included wording, the diagram, a chat example and a responsibility table. | One content revision changed the responsibility section into a table; a later version recorded acceptance. |
| Result | Managed backend, with provider selection open. | Same direction, with provider selection open. |

## Conclusion

The skill made the second run more structured and reduced the need to repeat instructions about the expected discussion and ADR contents. It did not remove the need for user choices or review: the responsibilities table still required feedback.

The second run reached an acceptable ADR through a more direct process. Completion time was not measured, so no numerical speed improvement can be reported. The user already knew Teamify and the alternatives from the first run; this also helped the repeat and means the difference cannot be attributed only to the skill.

## Compared records

- [First architecture discussion](Task_1_discussion.md)
- [First ADR review](Task_2_discussion.md)
- [First accepted ADR](docs/architecture/ADR-001.md)
- [New-session discussion](with_skill/discussion-2026-10-28-354b6a64.md)
- [New-session accepted ADR](with_skill/adr-2026-10-28-354b6a64-v3.md)
