# Task 2 — Teamify: ADR discussion

## Initial ADR

Based on the Task 1 discussion, the assistant created an ADR comparing a modular monolith, microservices and a managed/serverless backend. The preferred option was a managed backend: the priority was simpler development, and dependence on the provider was acceptable for the first version.

## Review and changes

The ADR was shortened to remove repeated explanations. It retained the decision, comparison of alternatives, benefits, drawbacks and open questions. The event-creation example was clarified so that the event, invitations and pending notifications are saved together before delivery begins.

The student then requested four changes:

1. Simplify the language.
2. Make the architecture diagram clearer, including the connections between the client, functions, database and real-time service.
3. Add a practical example of how group chat works.
4. Show which tasks belong to the provider and which we implement ourselves.

The assistant revised the ADR accordingly. The new diagram shows login, checked requests, database operations and real-time delivery. The chat example covers identity and membership checks, saving messages, delivery and retrieving missed messages. A table separates the provider's infrastructure from our business rules and configuration.

## Final review

The student reviewed the revised ADR and found it satisfactory. The resulting document explains the choice of a managed backend while retaining provider dependence, cost considerations, access checks and the conditions for reconsidering the architecture.

Final ADR: [ADR-001](docs/architecture/ADR-001.md).
