# Teamify architecture discussion

Date: 2026-10-28
Status: ADR v3 Accepted by the user on 2026-10-28. Managed backend selected for the first version; provider selection remains open.

Requirements: Teamify
Skill: architecture-adr

## Scope and user instructions

Discuss three suitable architectures with the user, then create and review an ADR. Start by reading requirements and presenting the first option. Save the new discussion and ADR here. Do not read previous discussion notes or ADRs. No previous discussion notes or ADRs were read. This trial uses separate filenames to preserve prior work.

## Stated requirements

- Accounts: registration, login/logout, profile updates, password reset, account deletion with personal-data removal.
- Personal tasks: agenda, creation, editing, deletion and completion.
- Teams: creation, invitations/joining, membership listing/leaving, administrator promotion/demotion, team details and deletion.
- Shared events: team agenda, administrator-controlled creation/editing/deletion/completion, invitations and acceptance/refusal.
- Team group chat and real-time notifications, including a notification history.
- Polls: administrator creation, member voting and result viewing.

## Architecture drivers

- Personal and team data require authorization by ownership, current membership and administrator role.
- Chat and notifications need live delivery alongside durable storage and recovery after disconnects.
- Membership changes and team/account deletion affect data access, notifications and stored personal data across features.
- Shared events, invitations and votes require coherent updates; exact business rules remain unspecified.

## Assumptions and missing information

- No workload, concurrent-user target, budget, delivery deadline, hosting constraint, availability target or development/operations team size is supplied.
- A client application communicates with a backend; client platform is unspecified.
- Do not assume uniform load or a cost advantage for cloud hosting.
- Message retention, account-deletion effects on shared messages, last-administrator handling and notification delivery guarantees need definition before implementation.

## Proposed discussion sequence

1. Modular monolith: feature modules in one backend deployment, one relational database, live connections and a background worker.
2. Split core and real-time services: a core application for accounts/teams/tasks/events/polls, a separate chat/live-delivery service with explicit ownership and event communication.
3. Managed backend: managed identity, storage and real-time delivery, with server-side application functions and access policies for Teamify business rules; vendor undecided.

These are proposals, not user preferences or an accepted decision. Discuss deployment and responsibility boundaries explicitly where options overlap.

## Option 1 proposed: modular monolith

Components: client -> one application backend -> relational database; live channel between client and backend; background worker reads durable pending delivery work and dispatches through the live channel. Feature modules cover identity, teams, personal tasks, shared events, polls, chat and notifications. Modules own their tables logically within the shared database. The worker uses the same codebase and may run as a separate process without becoming an independently owned business service.

Representative operation: an administrator creates a team event. The backend verifies current membership and role, then saves the event, invitations, notification records and pending delivery work in one database transaction. After commit, a worker delivers live updates. Disconnected clients reload persisted state. The pending delivery mechanism is an architectural proposal, not a stated requirement.

Benefits: straightforward transactions and authorization across related features; one main application to deploy; feature boundaries can support later extraction.

Drawbacks: chat/live traffic and ordinary requests share an application scaling boundary; changes share a release cycle; module boundaries require discipline.

Concrete difficulty: a team member may leave while a live connection is open. Membership changes must revoke subscriptions and future delivery access, and reconnects must reload missed persisted data. A successful socket connection alone must not imply ongoing team authorization.

Comparison question to user: is the initial priority quick delivery by a small team, or independent scaling of chat for large concurrent groups? Team size and expected concurrency are currently unknown.

## Initial discussion state

No architecture preference, scale target or review feedback has been received yet. No ADR has been drafted or accepted.
## User feedback after option 1

The user prioritizes simpler development and quick delivery of the first version. Traffic estimates are unavailable. The user sees no current need to scale chat independently and asks to continue with the second architecture. This is a priority statement, not an architecture selection or ADR acceptance.

## Option 2 proposed: core application plus separate chat and live-delivery service

Boundary: the core application owns accounts, team membership and roles, personal tasks, shared events, invitations and polls in its relational database. A separate collaboration service owns chat messages, durable notification history and live client connections in its own store. Clients use the core API for core features and the collaboration service for chat and live updates. The services have independent deployment and scaling boundaries; neither writes the other's database.

Communication: the core application stores pending integration events in the same transaction as its business changes. A background publisher sends these events to the collaboration service over an internal API with retries. The receiving service tracks event identifiers to avoid duplicate notification records. A broker could be introduced later but is not necessary for this comparison. Team authorization remains authoritative in the core application; the collaboration service validates current membership through it and must handle revocation for open connections.

Diagram:
Client <-> Core application <-> Core database
Client <-> Chat/live service <-> Chat and notification store
Core application -> pending-event publisher -> Chat/live service
Chat/live service -> Core application: membership checks

Representative operation: an administrator creates an event through the core API. The core application checks their role and commits the event, invitations and pending integration event. A publisher sends the integration event to the collaboration service, which saves recipient notification records and pushes live updates. The event can be visible before its notification arrives. Retries must avoid duplicate records; disconnected clients reload saved history.

Benefits: chat/live processing can be deployed and scaled separately; its failures may be contained so core agenda features can continue. Authorization dependencies and shared infrastructure limit isolation. The boundary can support separate feature ownership if the development organization later needs it.

Drawbacks for expressed priorities: an additional service, database and inter-service contract increase first-version development and deployment work without a demonstrated independent scaling need. Cross-service changes and data deletion need coordination, and notification history is eventually consistent with core updates.

Concrete difficulty: a user can leave a team while the chat service still has an active connection and stale membership state. The system must invalidate subscriptions and check current authorization for operations; uncertain authorization should deny access, which can make chat unavailable when the core membership check is unavailable. Account and team deletion also require retryable cross-service cleanup.

Assessment proposed by assistant: credible if independent scaling or deployment becomes important, but currently less aligned with the user's simplicity and delivery priorities than option 1. No decision has been made. Option 3 remains to be discussed.

## User feedback after option 2

The user understands the benefit of independent chat scaling but considers it insufficient to justify the additional complexity for the first version. The user requests discussion of the managed backend alternative. Option 2 is not favored for the initial release; the user has not yet selected between options 1 and 3.

## Option 3 proposed: managed backend with application-owned business rules

Boundary: a provider operates identity, database infrastructure and real-time delivery. Teamify owns its client application, data model, access policies and server-side business functions. The client signs in through managed identity, reads/subscribes only to data allowed by access policies, and calls Teamify server-side functions for protected workflows. Those functions validate the caller and current role and update application data. No provider or product has been selected, and no claim is made that every managed backend supports the required transaction, subscription authorization or deletion behavior.

Logical data ownership remains with Teamify: profiles and account references, teams and memberships, personal tasks, shared events and invitations, polls/votes, messages and notification records. The provider operates storage and delivery infrastructure rather than deciding business authorization. Functions, stored policies and client code remain Teamify's implementation and maintenance responsibility.

Diagram:
Client -> Managed identity: sign in
Client -> Teamify server-side functions: protected commands
Client <-> Managed database: authorized reads
Client <-> Managed real-time delivery: authorized subscriptions
Teamify functions -> Managed database: validated writes
Managed database -> Managed real-time delivery: committed changes
Teamify functions -> Managed identity: coordinated account deletion when applicable

Representative operation: an administrator calls a Teamify function to create a shared event. The function validates the identity and current team role and atomically writes the event, invitations and notification records if the selected platform supports that transaction. Authorized subscriptions receive committed changes, and reconnecting clients query persisted state. Durable chat and notification history must be modeled explicitly; a transient real-time channel alone is insufficient.

Benefits: less infrastructure to deploy and operate; integrated identity and live updates can accelerate the first release when the team's experience and the provider's capabilities fit. These are conditional benefits, not measured delivery or cost comparisons.

Drawbacks: provider-specific access policies, APIs and limits influence the design; workflow constraints and portability may require additional work. Usage costs cannot be compared without traffic, retention and platform information. Development can shift from backend infrastructure into policy configuration, functions and integration behavior rather than disappearing.

Concrete difficulty: consistently enforce membership across database reads, function writes and active subscriptions. A user leaving a team must lose access through all paths, including existing connections; the selected platform's revocation behavior needs verification. Privileged functions must perform their own role checks if they bypass ordinary data policies. Team/account deletion also needs explicit cleanup across identity and application storage and a defined treatment of personal data in shared content and backups.

Comparison against expressed priorities:
- Modular monolith: straightforward cross-feature transactions and centralized authorization; Teamify operates backend, database and live delivery.
- Split core/chat services: additional deployments, communication and coordination; independent scaling is not currently a user priority.
- Managed backend: potentially less infrastructure work; Teamify still designs and verifies access policies and business functions, with provider constraints and portability trade-offs.

Assistant's conditional assessment: options 1 and 3 remain credible for the first version. Option 3 may best serve quick delivery if the team accepts provider coupling and has suitable platform experience; option 1 may be preferable for familiar backend development and direct control. No vendor, cost advantage, architecture selection or user acceptance is assumed.

Next material preference: whether the team prefers operating its own backend using familiar tools or relying on a managed platform for identity/storage/live delivery, and whether relevant managed-platform experience exists. Await user feedback before selecting and drafting the ADR.

## User selection after option 3

The user has limited experience with managed backend platforms but prefers this approach to reduce infrastructure work and is willing to learn. The user explicitly selects this direction for the first version and requests an ADR draft with provider selection left open. This resolves the material architecture preference; it does not constitute acceptance of an ADR that has not yet been reviewed.

## ADR draft and review request

Created ADR v1 with status Proposed, recording the selected direction, alternatives, responsibilities, operation, assumptions and revisit conditions. No provider is selected and no cost or delivery-time advantage is quantified. The learning effort is recorded as a trade-off the user is willing to take.

The draft is ready for user inspection of clarity, omissions or unnecessary content, diagram connections and implementation responsibilities. User review and ADR acceptance are pending. Preserve this ADR version when producing any review revision; record actual feedback and changes here.

## Review 1: responsibilities table

User feedback: replace the responsibilities section with a table showing what the provider handles and what Teamify must implement or configure. Keep the existing details and the rest of the ADR unchanged, save a new version and update these notes.

Created ADR v2, preserving ADR v1. The responsibilities section now has columns for the area, provider responsibilities and Teamify implementation/configuration responsibilities. It retains provider service-term qualifications, capability/limit/recovery/pricing checks, all six original Teamify responsibility details and the original consequences paragraph.

Verification: v1 was unchanged; all six original Teamify responsibility details remain in v2; text outside the responsibilities section is identical except for the version number changing from 1 to 2. Provider selection remains open and the ADR remains Proposed. No further feedback or acceptance has been received.

## User approval and acceptance

Date: 2026-10-28.

The user stated: "The responsibilities table is clear, and I'm satisfied with the ADR. Mark it as Accepted and record my approval in the discussion notes."

Saved Accepted ADR v3. Changed the status to Accepted, incremented the version number and replaced the pending-review paragraph with the actual approval record. The reviewed architecture, responsibilities table and all other content remain unchanged. Provider selection remains open. ADR v1 and ADR v2 are preserved.
