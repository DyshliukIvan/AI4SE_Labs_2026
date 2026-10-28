# Task 1 — Teamify: architecture discussion

Requirements: data/Teamify.txt  
Discussion: 27–28 October 2026

Discussion notes on three architectures for Teamify.

## Project and starting assumptions

The assistant read the system description and 31 user stories. Teamify needs accounts, personal tasks, teams with administrator roles, shared agendas and events, invitations, group chat, polls and real-time notifications.

For the first version, the priority is simple development. We treat it as a small initial application; expected traffic, budget and availability targets still need to be defined.

## 1. Modular monolith

**Assistant's proposal:** One backend application, divided into accounts, teams, tasks/events, chat, polls and notifications, with one database. Modules have separate responsibilities but run and deploy as one application.

```text
Client -> Backend modules -> Database
             |
             +-> Real-time chat and notifications
```

**Student's position:** The application is small, so several backend applications do not currently appear necessary.

**Trade-offs discussed:** A single backend is easier to deploy and debug. Related changes can use one database transaction. Modules deploy together, however, and scaling only chat is less straightforward. Clear module boundaries are needed to avoid tightly coupled code.

**Implementation discussion:** For a chat message, the backend authenticates the user, checks team membership, stores the message and delivers it to connected members. The student explained that client-side permission checks are insufficient because users can modify the client or send false permission claims. The server must check trusted membership and role records instead.

We also discussed creating an event and invitations. A transaction can save the related records together or roll them back together. The student preferred saving first and retrying notification delivery afterwards. The assistant explained that pending notification work can be stored durably and processed by a background task; retries need delays, limits and duplicate handling. This does not require a separate microservice.

**Assessment:** A suitable small-system architecture. It keeps development straightforward while still supporting real-time features, but we retain responsibility for operating the backend.

## 2. Microservices

**Assistant's proposal:** Separate applications for accounts, collaboration (teams/tasks/events), and messaging (chat/notifications). Each service owns its data and communicates through APIs or events.

```text
Client -> Accounts service      -> Owned data
       -> Collaboration service -> Owned data
       -> Messaging service     -> Owned data
```

Separate services do not necessarily require separate physical machines.

**Student's position:** There is no clear need to scale parts independently in the first version. We discussed that chat traffic could eventually differ from task or profile operations, so future scaling should be based on actual usage.

**Trade-offs discussed:** Chat can be deployed and scaled independently. The cost is more deployment configuration, monitoring and network communication. Calls between services can fail, and changes involving several services are harder to keep consistent than a transaction in one database.

**Implementation discussion:** When someone leaves a team, the messaging service must revoke chat access. A delayed membership update can leave stale permissions. We would need a defined membership-checking mechanism, revocation of existing subscriptions and failure handling. Splitting services adds this coordination to otherwise simple team operations.

**Assessment:** The requirements do not establish a need for independent services. For the assumed small first version, the extra coordination work is difficult to justify. This could change if measured load or separate development teams require independent releases.

## 3. Managed/serverless backend

**Assistant's proposal:** Assemble the backend from managed authentication, a managed database, server-side functions and real-time delivery. The provider runs the service infrastructure; Teamify's business logic and access rules remain our responsibility.

```text
Client -> Managed authentication
       -> Business functions -> Managed database
       <- Authorized real-time updates
```

**Student's position:** When offered a self-managed backend or ready-made services, the student preferred ready-made services. The student explicitly accepted provider dependence because simplifying development is more important for a small initial application.

**Trade-offs discussed:** Managed services reduce infrastructure administration and provide common capabilities such as login and password reset. Platform limits, usage-based costs and dependence on provider APIs must be considered. A later migration may require changes to authentication, functions and real-time subscriptions. Costs depend on usage and the selected provider.

**Implementation discussion:** We still define task ownership, team membership, administrator privileges, event invitations and poll operations. A function that creates a team event must verify administrator rights on the server. Database access and chat subscriptions must also enforce membership. Reconnecting users need to retrieve missed messages from persistent storage. Ready-made services provide the infrastructure, not these application-specific rules.

**Assessment:** Best aligned with the student's preference to reduce infrastructure work. A provider must still be checked against Teamify's database, authorization and real-time needs before implementation.

## Discussion outcome

We compared three architectures for the same requirements. A modular monolith is a reasonable alternative; microservices introduce complexity without a demonstrated present need. The student prefers a managed backend for the first version and accepts provider dependence in exchange for simpler development.

The options can overlap: a monolith can use a managed database or authentication. Our comparison concerns one backend we operate, independently deployed services, and a backend built primarily from managed services and functions. No provider has been selected.
