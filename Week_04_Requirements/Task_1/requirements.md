# PINES Management Reporting — Software Requirements Specification (Revised)

## Generation and review

Models: extraction `gpt-4.1-nano`, refinement `gpt-5-mini`, review `gpt-4o-mini`. Review passes: 6.

Review status: NEEDS HUMAN REVIEW (iteration limit reached).

## Priority scale

- **Must:** Essential or explicitly mandatory in the sources.
- **Should:** Important capability, but not explicitly mandatory.
- **Could:** Optional enhancement or tentative stakeholder suggestion.

## Vocabulary

- branch: a physical library location participating in the consortium (also called "location" or "facility").
- consortium/system: a grouping of branches managed together; "system" often refers to the PINES consortium or one member system within PINES.
- item: a physical copy record (barcode-level) representing a physical material in the collection (not the bibliographic record).
- bibliographic_record (bib): the catalog-level record describing a work; may have zero or more item records attached.
- hold/request: a request placed by a patron to borrow an item; also called 'hold'.
- OPAC: Online Public Access Catalog; the patron-facing catalog web interface.
- circ/circulation action: an action recording checkout, check-in, renewal, or related circulation activity.
- transit: in-transit status when an item is moving between branches (includes transit-from and transit-to states).
- status: the item status field (e.g., available/checked_out/missing/longoverdue/discard).
- location / copy_location: the branch (and shelving location) where an item is currently assigned.
- report template: saved query definition and display configuration that can be run later and optionally shared.
- report queue: background processing queue for scheduled or ad-hoc report jobs.
- replica / reporting replica / reporting warehouse: a read-only copy or denormalized store of production data used for long-running or historical reporting.
- role / security group: an administrative construct that defines a set of permissions assigned to users.
- X (configurable parameter): a placeholder used in requirements where a numeric threshold (e.g., days, months) must be configurable by administrators rather than hard-coded.

## Requirements

### REQ-0001 — Material Volume and Status Breakdown Report

**Priority:** Must. Multiple candidate sources explicitly require accurate material volume and status breakdowns for collection management and inventory control.

The system shall provide reports that compute and present counts of items for a specified branch, group of branches, or the consortium/system scope. Reports shall include counts broken down by configurable categories (for example: total items, number of holds, adult fiction, board books, other genres or formats defined by the library) and by item status types including newly acquired (recent acquisitions), items currently on the shelf (checked in/available), and items in circulation (checked out). Items that are checked out shall be included in the total volume counts. The report shall allow producing each count separately (acquisitions / on-shelf / checked-out) and a computed total; categories shall be configurable per report and saved as reusable templates. Numeric limits: counts shall be exact integer values up to the size of the consortium inventory (supporting at least tens of millions of items). Scope: per branch, per group of branches, and per system.

**Sources:** `conversations/conv_pines014_material_volume.eml`; `early_draft_srs_galecia.txt`; `interview_cataloging_2009-05-08.txt`
**Evidence candidates:** C0001, C0002, C0003, C0004, C0005, C0097, C0163, C0099, C0082, C0229, C0244, C0266

### REQ-0002 — Configurable Category and Field Customization

**Priority:** Should. Stakeholders across branches requested customization to accommodate differing local needs; this is important but not blocking.

The reporting system shall support configurable category definitions and customizable breakdown fields so different libraries or administrators can define which genres, formats, and category buckets (e.g., Adult Fiction, Board Books, Holds) to include in volume and shelf-space style reports. Administrators shall be able to create, edit, and save category definitions and expose them to report templates. The system shall support configuring numeric aggregation fields (counts, sums) and selecting which status values are included in each aggregation. Scope includes per-branch, multi-branch, and system-level templates.

**Sources:** `conversations/conv_pines014_material_volume.eml`; `conversations/conv_pines016_shelf_space.eml`; `early_draft_srs_galecia.txt`
**Evidence candidates:** C0006, C0097, C0018, C0019

### REQ-0003 — Acquisition Date Tracking and Trend Reporting

**Priority:** Should. Several inputs indicate acquisition date exists and would enable useful trend reporting; desirable for planning but not mandatory for minimal reporting.

The system shall track acquisition_date (purchase or accession date) for each item record and shall provide reports that use acquisition_date to show volume changes over time (growth/shrink trends). The report shall support configurable date ranges (e.g., quarterly, monthly), and present numeric counts and percent changes for the selected periods. Date-based filters and trend visualizations shall be available per branch and system. The acquisition_date field shall be present on item records and used in queries and aggregates.

**Sources:** `conversations/conv_pines014_material_volume.eml`; `conversations/conv_pines015_capacity_interface.eml`; `conversations/conv_pines016_shelf_space.eml`
**Evidence candidates:** C0007, C0014, C0020, C0018

### REQ-0004 — System Capacity Overview and Branch Capacity Interface

**Priority:** Must. Multiple candidate items explicitly require a consolidated capacity view and drill-down capability for operations and logistics.

The system shall provide an interactive interface that displays capacity-related metrics for all branches and for user-selected subsets (region, system, group). The interface shall allow viewing all branches at once and shall support drill-down into an individual branch's detailed metrics. Capacity metrics shall be definable (see Definition of Capacity Metrics requirement) and the interface shall include sorting and filtering (region, library type, current load). The interface shall permit export of the displayed data to CSV. The interface shall support grouping/aggregation across locations to reduce clutter and allow comparisons across branches. The System Capacity Overview interface shall optionally display capacity status using visual indicators but shall not rely on color alone. The interface shall support configurable status thresholds and present each branch's status with an accessible visual cue set (for example: color plus shape or textual label). Default cues may use green/yellow/red for under/near/over capacity, but the implementation shall also provide textual labels and alternative patterns so the status remains interpretable by users with color-vision deficiency and by assistive technologies. The chosen representation and threshold values shall be recorded in the report/template metadata.

**Sources:** `conversations/conv_pines015_capacity_interface.eml`; `early_draft_srs_galecia.txt`
**Evidence candidates:** C0008, C0009, C0010, C0011, C0012, C0015, C0016, C0098, C0013, C0245, C0267

### REQ-0005 — Definition of Capacity Metrics

**Priority:** Must. Stakeholders requested clarity about what 'capacity' means and consistent calculations across reports.

The system shall provide explicit definitions and configurable options for 'capacity' metrics used in the capacity interface and reports. The definition options shall include, but not be limited to: number_of_items (count of item records at a location), estimated_shelf_space (see Shelf Space Estimation), configured_capacity_limit (an administrator-set numeric capacity limit per branch), circulation_processing_capacity (throughput metric), and current_load (current item count divided by configured_capacity_limit). The system shall store which definition is used for a given report template and display the chosen definition in report metadata.

**Sources:** `conversations/conv_pines015_capacity_interface.eml`; `early_draft_srs_galecia.txt`
**Evidence candidates:** C0017, C0098

### REQ-0006 — Shelf Space Estimation and Comparison Report

**Priority:** Must. Explicit multiple requests for percent circulation vs collection vs shelf space comparison per genre/format are needed for collection management.

The system shall provide a Shelf Space Report that, for each genre and format and for each branch or for the system scope, produces: percentage_of_total_circulations (sum of checkouts for items in genre/format divided by total checkouts), percentage_of_collection (count of items in genre/format divided by total items), and percentage_of_shelf_space (an estimate based on item dimensions or a proxy). Because shelf space is not directly tracked, the system shall support estimating shelf space using either item physical dimension fields when available (height/width/depth and thickness) or an administrator-configurable per-item 'shelf_unit' proxy (e.g., items of type X count as 0.5 shelf units). The report shall support per-library and per-system breakdown, comparison (side-by-side) views, and table/CSV export.

**Sources:** `conversations/conv_pines016_shelf_space.eml`; `early_draft_srs_galecia.txt`; `interview_cataloging_2009-05-08.txt`
**Evidence candidates:** C0018, C0021, C0022, C0023, C0024, C0025, C0099, C0162, C0246, C0268

### REQ-0007 — Shelf Space Report — Outlier Identification and Ranking

**Priority:** Could. Stakeholders suggested outlier identification as useful but indicated lower urgency than core comparisons.

As an adjunct to the Shelf Space Report, the system shall support ranking genre/format buckets and identifying outliers (e.g., genres with disproportionately high shelf_space percentage compared to circulation percentage). The system shall present sortable columns and provide filters for time ranges. Inclusion of this feature is optional (non-blocking) and may be exposed as a 'Could' capability in initial releases.

**Sources:** `conversations/conv_pines016_shelf_space.eml`
**Evidence candidates:** C0026, C0018

### REQ-0008 — Item Transfer Utility with Querying and Batch Actions

**Priority:** Must. Multiple sources emphasized batch transfer utility functionality for mobile units, outreach, and operational needs.

The system shall provide a transfer utility to move batches of items between branches. The utility shall allow ad-hoc queries to identify candidate materials (by criteria such as shelving location, last circulation, genre, call number), saving queries for repeated use, manual selection of individual titles from query results, and performing batch actions to change item record fields to reflect the new location (e.g., copy_location change). The utility shall support mechanisms for transfer such as generating pull lists and changing the location field; all actions shall be previewable before execution and require permission checks per Role-Based Access Control. The utility shall support scheduling or applying an auto-revert (see Auto-Revert Mechanism requirement).

**Sources:** `conversations/conv_pines018_item_transfer.eml`; `early_draft_srs_galecia.txt`; `interview_cataloging_2009-05-08.txt`
**Evidence candidates:** C0027, C0028, C0029, C0030, C0031, C0102, C0156, C0249, C0271

### REQ-0009 — Transfer Permission and Audit Controls

**Priority:** Must. Security and accountability requirements explicitly require limiting transfer capabilities to authorized roles and recording actions for audit.

The transfer utility shall enforce permission controls: only users with appropriate roles (e.g., managers, administrators, transfer coordinators) shall be allowed to perform transfer actions. The system shall log transfer events in an audit trail recording who performed the transfer, timestamp, original and new location values, and any batch identifier. Permissions shall be managed via roles and security groups and shall be administrable by Local and Global Admins.

**Sources:** `conversations/conv_pines018_item_transfer.eml`; `email_staff_login.eml`; `interview_sysadmin_2009-05-10.txt`; `meeting_tech_subcommittee_2009-06-30.txt`
**Evidence candidates:** C0035, C0136, C0137, C0171, C0205

### REQ-0010 — Transfer Preview, Confirmation, Undo and History

**Priority:** Should. Preview and confirmation are required by some candidates; undo and detailed transfer history are highly desired for operational rollback and diagnostics.

The system shall provide a preview screen summarizing candidate items and the intended changes before executing a transfer action; the preview shall display the number of items, sample item identifiers, original locations, and intended destination. The system shall require explicit confirmation before executing the change. The system shall track transfer history per item (transfer events with timestamps and actors) and shall provide an undo capability for recent batch transfers, limited by configurable retention and permission rules (undo functionality may be restricted to manager/admin roles). Transfer history shall be queryable to produce counts of transfers per item over configurable time windows.

**Sources:** `conversations/conv_pines018_item_transfer.eml`; `interview_cataloging_2009-05-08.txt`
**Evidence candidates:** C0033, C0034, C0037, C0042, C0036, C0156

### REQ-0011 — Auto-Revert Mechanism for Temporary Transfers

**Priority:** Must. Multiple candidates request auto-revert functionality as core for temporary transfers to ensure items return to original locations without manual steps.

The system shall support an auto-revert mechanism for items temporarily transferred to a location. Administrators shall be able to configure revert criteria: time-based (revert after X days; X configurable per template), and/or event-based (revert when item is checked out at destination, when status changes to a configured value, or on a specific date). The auto-revert processing shall run as a scheduled background task and shall log reversion events in the transfer history audit. The system shall expose configuration defaults and allow overriding per-transfer operation.

**Sources:** `conversations/conv_pines018_item_transfer.eml`; `early_draft_srs_galecia.txt`
**Evidence candidates:** C0032, C0039, C0040, C0043, C0102

### REQ-0012 — Transit Labels and Transfer Alerts (Optional)

**Priority:** Could. Stakeholders requested transit labels and alerts; useful but not essential to initial transfer mechanics.

The system shall support optional generation of printable transit labels (barcode labels) for items included in transfer batches, and optional alert/notification generation for delayed transfers or transfer issues. These features shall be optional adjuncts and configurable per branch or per transfer operation.

**Sources:** `conversations/conv_pines018_item_transfer.eml`
**Evidence candidates:** C0038, C0041

### REQ-0013 — Missing, Damaged, and In-Transit Reports (Merged)

**Priority:** Must. Explicit requirements for missing/damaged and merged in-transit reports with configurable thresholds are present in multiple sources for accountability and operational follow-up.

The system shall provide reports of missing and damaged items per branch and shall provide an in-transit items report that merges transit-to and transit-from information into a single report. The in-transit report shall allow a configurable threshold X (default 7 days) and list items in-transit longer than X days. Both reports shall be filterable by branch, date range, status, and shall include item identifiers, last known location, transit_from, transit_to, due_date_in_transit (where applicable), and any item condition notes (e.g., 'water damage', 'vandalism') when present. Reports shall be exportable to CSV and sortable (including by due date).

**Sources:** `conversations/conv_pines019_020_missing_intransit.eml`; `early_draft_srs_galecia.txt`; `interview_cataloging_2009-05-08.txt`
**Evidence candidates:** C0044, C0045, C0046, C0047, C0048, C0049, C0103, C0104, C0157, C0158, C0050, C0051, C0250, C0251, C0272, C0273

### REQ-0014 — Item Purging and Last-Copy Controls

**Priority:** Must. Strong operational need to support safe purging, last-copy protections, and batch conversions for catalog maintenance present across inputs.

The system shall provide utilities and reports to identify item records for purging based on configurable criteria (for example: item has been in status 'missing' for more than X months, item has status 'discard/weed', last circulation older than Y, or combinations of these criteria). The system shall produce read-only candidate reports for review and require a separate confirmation step for actual deletion. The system shall support batch status conversion (e.g., convert N items from 'missing' to 'discard/weed') and an effective method to delete volume and copy entries together and to remove bibliographic records with no items attached. The system shall implement safeguards to prevent accidental deletion of the system's last copy: a 'Last Copy Report' shall identify the last copy at the branch scope and at the system/consortium scope; deletion operations that would remove the last copy in the chosen scope shall require explicit elevated confirmation and/or be disallowed by default. Audit trails shall record all purge/delete actions (records deleted, who requested, who confirmed, timestamps, and scope).

**Sources:** `conversations/conv_pines021_item_purging.eml`; `early_draft_srs_galecia.txt`; `interview_cataloging_2009-05-08.txt`
**Evidence candidates:** C0052, C0053, C0054, C0055, C0056, C0057, C0058, C0059, C0105, C0159, C0160, C0252, C0274

### REQ-0015 — Scheduled and Manual Purge Options

**Priority:** Could. Stakeholders asked about scheduling; useful but potentially sensitive operationally, so lower initial priority.

The purge utility shall support manual execution and optional scheduled/automated runs (e.g., run at the end of each year). Scheduling parameters and purge criteria shall be configurable by administrators. Automated purges shall produce candidate reports before deletion and require explicit automated-policy confirmation (configurable), with audit trails retained.

**Sources:** `conversations/conv_pines021_item_purging.eml`
**Evidence candidates:** C0060, C0055

### REQ-0016 — Deletion Audit Logging and Reporting

**Priority:** Must. Explicit need for counting and auditing deletions for compliance and troubleshooting across multiple candidates.

The system shall log all deletion events (including deletes of item, patron, and bibliographic records) into an audit table via database-level triggers or equivalent mechanism. Each logged deletion event shall include record_type, record_id, deleted_by (user id), deleted_at (timestamp), location (user's branch or system), and reason/operation identifier where available. The system shall provide a report interface to query the audit table with filters for date range, user, record type, location, and system, and shall provide aggregated reports of deletion counts per location and per system.

**Sources:** `conversations/conv_pines022_deletions.eml`; `early_draft_srs_galecia.txt`; `interview_cataloging_2009-05-08.txt`
**Evidence candidates:** C0061, C0062, C0063, C0064, C0065, C0066, C0106, C0161, C0253, C0275

### REQ-0017 — Reportable Attempted/Denied Deletions (Optional)

**Priority:** Could. This was suggested for compliance monitoring but is not strictly required by all stakeholders; include as optional enhancement.

The system shall optionally record attempts to delete records that were denied due to permission checks, to support detection of unauthorized attempts. Denied-deletion events shall include the attempting_user_id, attempted_record, timestamp, and reason for denial; these may be stored in a separate audit table and be available to administrators.

**Sources:** `conversations/conv_pines022_deletions.eml`
**Evidence candidates:** C0067

### REQ-0018 — Patron Characteristics Querying and Grouping

**Priority:** Must. Stakeholder requests for demographic and patron-group reporting with configurable age brackets and null handling are numerous and operationally necessary for outreach and analysis.

The system shall support queries and reports that limit and group patrons by characteristics including configurable age ranges (computed from birth_date at query time), zip code, county, home branch, patron type, preferred language, and other patron table fields. The query interface shall support combining filters using logical AND/OR, grouping (GROUP BY) on these fields, and including null values explicitly rather than excluding records when optional patron fields are missing. Reports shall support export to CSV and preserve nulls in output.

**Sources:** `conversations/conv_pines023_patron_characteristics.eml`; `early_draft_srs_galecia.txt`
**Evidence candidates:** C0068, C0069, C0070, C0071, C0072, C0073, C0074, C0107, C0254, C0276

### REQ-0019 — Inactive Patrons Reporting with Electronic Activity and Opt-Outs

**Priority:** Must. Detailed stakeholder requirements to support outreach and privacy opt-outs make this core functionality for member libraries.

The system shall produce lists of patrons defined as 'inactive' by configurable inactivity threshold X days (default typical value 365 days, X configurable). The inactivity calculation shall consider circulation and electronic activity (OPAC/patron account login, online holds, renewals, and integrated digital resource access). Reports shall be configurable for scope (System, Home Library, County), shall include current mailing address fields for outreach, and shall allow exclusion filters (patrons with 'do not disturb' flags, VIPs, staff accounts, or those who have opted out of communications). The report output shall be exportable (CSV) and optimized for background processing to handle large datasets.

**Sources:** `conversations/conv_pines024_inactive_patrons.eml`; `early_draft_srs_galecia.txt`
**Evidence candidates:** C0075, C0076, C0077, C0078, C0079, C0080, C0081, C0108, C0255, C0277

### REQ-0020 — Transaction History Retention and Aggregates

**Priority:** Must. Multiple specifications require configurable retention combined with indefinite aggregate retention for reporting and compliance.

The system shall maintain transaction history (raw transactions) for a configurable retention period X days (X configurable). Monthly and annual aggregate information derived from transaction history shall be maintained indefinitely for reporting. The system shall support archive mechanisms and a historical reporting warehouse for long-term aggregated queries. The retention configuration shall be administrable and documented. Transaction archiving facilities shall include mechanisms to protect patron privacy in accordance with applicable State Law and local policy. When archives are prepared for long-term storage or for public/statistical use, personally-identifiable patron fields shall be removable or anonymized while preserving useful demographic and aggregate statistics. The system shall document which fields are anonymized and provide configurable anonymization options for administrators where required by local policy.

**Sources:** `early_draft_srs_galecia.txt`; `email_report_features.eml`; `survey_results_2009.txt`
**Evidence candidates:** C0109, C0217, C0128, C0223, C0256, C0278

### REQ-0021 — Backroom and Transaction Grouping Statistics

**Priority:** Must. Operational reporting for staffing and branch analytics depends on grouping transactions by time and terminal.

The system shall provide reports grouping transactions by hour, terminal, branch, and system. Transactions to be grouped include check-ins, check-outs, fines collected, patron registrations, and other transaction types. Reports shall support querying all transactions or filtering by transaction type, and shall return counts and aggregates as requested.

**Sources:** `early_draft_srs_galecia.txt`; `survey_results_2009.txt`
**Evidence candidates:** C0110, C0218, C0101, C0248, C0257, C0270, C0279

### REQ-0022 — Check-In and Check-Out Type Counting

**Priority:** Must. Detailed breakdown of circulation activity by method is necessary for operations and staffing metrics and was repeatedly requested.

The system shall count and report all types of check-in and check-out individually and cumulatively. Check-in types include: book-drop, by terminal, by user, self-service. Check-out types include: staff check-out, self check-out, staff renewal, self-check renewal, online renewal, OPAC renewal. Reports shall allow filters and grouping by these modifiers.

**Sources:** `early_draft_srs_galecia.txt`; `survey_results_2009.txt`
**Evidence candidates:** C0111, C0112, C0220, C0219, C0258, C0259, C0280, C0281

### REQ-0023 — Hold Requests Counting and Placement Method

**Priority:** Must. Counting holds by placement method is an explicit reporting need for evaluating service channels.

The system shall count hold requests and report counts by how each hold was placed (staff desk, public computer inside library, remotely/OPAC/phone). Hold reports shall include subtotals by status (active, frozen, frozen-until, unfilled) and be available per patron, per library, and system-level.

**Sources:** `early_draft_srs_galecia.txt`; `survey_results_2009.txt`
**Evidence candidates:** C0113, C0221, C0260, C0282

### REQ-0024 — Transactions per Patron/Group Reports

**Priority:** Must. Necessary for patron-level analysis and aggregate reporting; requested in multiple places.

The system shall generate transaction reports showing holds placed, holds filled, and check-outs per patron, per library, per selected group of libraries, per system, and per county. Reports shall display check-outs and placed holds per patron and allow subtotaling and breakdown by hold status types. Reports shall be exportable and support grouping and filtering.

**Sources:** `early_draft_srs_galecia.txt`; `survey_results_2009.txt`
**Evidence candidates:** C0114, C0222, C0224, C0261, C0283

### REQ-0025 — Value of Items and Financial Reports

**Priority:** Must. Financial reconciliation, auditability, and value reporting were repeatedly requested and are required by accounting practices.

The system shall generate reports computing the monetary value of items (based on item record purchase_price or value fields) for the entire collection or a defined subset (for example: items with status 'longoverdue', all DVDs in children's collection). The system shall provide financial reports for patron accounts including balances by patron/home library/system, fines and charges accrued per configurable time periods (last 12 months, YTD, last month) and per charge type (overdue, damaged, lost), fines waived per period and per branch, and payments made per period and by payment method (staff desk, self-check, OPAC). The system shall maintain a ledger of patron payments recording which charges each payment was applied to for reconciliation.

**Sources:** `early_draft_srs_galecia.txt`; `email_financial_reports.eml`
**Evidence candidates:** C0115, C0116, C0117, C0116, C0115, C0120, C0121, C0262, C0263, C0264, C0284, C0285, C0286

### REQ-0026 — Financial Reporting Compliance and Retention (Advisory)

**Priority:** Should. Stakeholders requested audit-compliance and retention; recommended but specifics may be legal/policy-driven and not purely technical.

The system shall be designed so reports and archived financial data can comply with standard accounting practices and applicable state/county/municipal auditing requirements. Administrators shall be able to configure retention policies (example advisory period: 7 years) and export financial data for external audits. The requirement to enforce retention policies may be a local operational policy; the system shall provide facilities to implement and document those policies.

**Sources:** `early_draft_srs_galecia.txt`; `email_financial_reports.eml`
**Evidence candidates:** C0122, C0116

### REQ-0027 — Query Tool — User Interface and Capabilities

**Priority:** Must. Essential for creating ad-hoc and reusable reports and is repeatedly requested across inputs including usability features.

The system shall provide a user-friendly query/report designer interface that allows staff to create queries against all record types (bibliographic_record, item, patron, action_circulation, action_hold, money, actor). The query tool shall support field selection (drag-and-drop or equivalent), picklist value selection, use of regular expressions (from a dropdown or supported expression field), Boolean operators (AND/OR/NOT), grouping and sorting options, and saving query definitions. The tool shall validate field names and present human-readable labels. The tool shall support selecting output fields, defining aggregation, and previewing sample results before full execution. The query/report designer shall expose an explicit 'last_edit_date' field distinct from circulation timestamps so authors can show last edit events without mixing in last circulation dates. The query tool shall also resolve friendly names to internal identifiers for select lists (for example: resolving survey name to survey ID when filtering) so users may filter by survey name without entering raw IDs.

**Sources:** `early_draft_srs_galecia.txt`; `email_report_features.eml`; `evergreen_reference_2009.txt`; `interview_cataloging_2009-05-08.txt`; `meeting_tech_subcommittee_2009-06-30.txt`
**Evidence candidates:** C0123, C0141, C0148, C0149, C0150, C0142, C0165, C0216, C0288, C0298, C0299

### REQ-0028 — Report Templates Management and Cloning

**Priority:** Must. Critical for governance and to streamline routine reporting; multiple sources require template management and cloning.

The system shall allow administrators to create and manage report templates. Templates shall be runnable as-is or modifiable by permitted users. Administrators shall be able to lock or limit which filters and display fields staff can alter when running a template. The system shall support cloning templates (creating new templates based on existing ones) so users can create variants without editing the original template. Templates shall include metadata indicating creator, last modified, allowed scopes, and permitted parameter overrides.

**Sources:** `email_report_features.eml`; `evergreen_reference_2009.txt`; `meeting_minutes/meeting_2009-03-15_minutes.txt`; `survey_results_2009.txt`
**Evidence candidates:** C0124, C0125, C0225, C0144, C0178, C0301

### REQ-0029 — Report Permissions, Shared Folders and Fine-Grained Access Control

**Priority:** Must. Security and governance needs require fine-grained control to prevent inappropriate data access and to manage template lifecycle.

The system shall implement fine-grained permission levels for report creation, template editing, cloning, and execution. Administrators shall be able to create shared folders (report libraries) to allow or restrict staff access to specific templates and datasets. Permissions shall be role-based and update automatically when user roles change. Permission controls shall include who can schedule, prioritize, cancel, or delete report jobs and who can export or share report outputs.

**Sources:** `email_report_features.eml`; `evergreen_reference_2009.txt`; `meeting_tech_subcommittee_2009-06-30.txt`; `survey_results_2009.txt`
**Evidence candidates:** C0126, C0125, C0205, C0147, C0226, C0227, C0304

### REQ-0030 — Report Queue, Visibility and Prioritization

**Priority:** Must. Queue visibility and processing safeguards are required to prevent long jobs from impacting live services and to provide user feedback; repeatedly requested.

The system shall execute ad-hoc and scheduled reports using a report queue and background processing. Users shall be able to view the status of their submitted reports in the queue, including position, number_of_reports_ahead, submission_time, and status (waiting, running, completed, failed). The system shall support prioritization policies allowing some report jobs (e.g., board reports) to be advanced ahead of lower-priority jobs; prioritization adjustments shall be permitted by administrators and require permission controls. The system shall provide basic job lifecycle management (view, cancel if permitted, download results).

**Sources:** `email_report_features.eml`; `evergreen_reference_2009.txt`; `meeting_tech_subcommittee_2009-06-30.txt`; `survey_results_2009.txt`
**Evidence candidates:** C0130, C0131, C0146, C0213, C0130, C0228

### REQ-0031 — Report Scheduling, Background Processing, and Cancellation

**Priority:** Must. Background processing, scheduling, and the ability to cancel are essential to operational stability and were requested by sysadmins and managers.

The system shall support scheduling reports (Run ASAP, hourly, daily, weekly, monthly, yearly) to run in background processing so that long-running queries do not impact OPAC or circulation client performance. Scheduling shall include options to export outputs to storage or email (see Export Formats and Delivery). The system shall allow cancellation of scheduled or running reports subject to permission checks; running reports shall check for cancellation signals at appropriate processing points to stop execution safely.

**Sources:** `evergreen_reference_2009.txt`; `interview_sysadmin_2009-05-10.txt`; `meeting_minutes/meeting_2009-07-20_minutes.txt`; `meeting_tech_subcommittee_2009-06-30.txt`
**Evidence candidates:** C0146, C0167, C0214, C0213, C0185, C0184, C0303

### REQ-0032 — Report Output Formats and Exports

**Priority:** Must. Stakeholders require exports for directors and external processing; CSV/HTML/Excel were specifically identified as required outputs.

The system shall support exporting report outputs in multiple formats including CSV (required), standards-compliant HTML, and Excel-compatible formats. CSV shall be reliable for data export and support large result sets. HTML output shall be standards-compliant and accessible. Excel-compatible exports should preserve basic formatting and be usable for pivot table analysis. Exports shall include metadata about the query (criteria used, report template ID, run timestamp, user) when feasible.

**Sources:** `conversations/conv_pines015_capacity_interface.eml`; `early_draft_srs_galecia.txt`; `evergreen_reference_2009.txt`; `meeting_tech_subcommittee_2009-06-30.txt`
**Evidence candidates:** C0015, C0143, C0212, C0084, C0201, C0300

### REQ-0033 — Query Criteria Display and Result Traceability

**Priority:** Must. Traceability of queries and results is required for audit, reproducibility, and trust in data; explicitly requested in multiple inputs.

The system shall provide the ability to display the original query criteria alongside the results (criteria + results) and include metadata (who ran it, when, which template and parameter values). Report outputs and saved templates shall retain the selection criteria so results can be audited and reproduced. When templates are modified, modification metadata shall be preserved.

**Sources:** `email_report_features.eml`; `evergreen_reference_2009.txt`; `meeting_tech_subcommittee_2009-06-30.txt`
**Evidence candidates:** C0129, C0124, C0211, C0213, C0141

### REQ-0034 — Report Data Architecture — Replicas and Historical Warehouse

**Priority:** Must. Sysadmins explicitly require reporting replicas/background processing to avoid disrupting OPAC and circulation clients; historical reporting also required for some reports.

The system shall support running reports against a read-only reporting replica or a dedicated reporting warehouse to avoid performance impact on the production transactional database. The architecture shall accommodate near-real-time replicas for real-time reporting and a historical warehouse for time-series/historical reporting (snapshots, monthly/annual aggregates). The system shall include tools to refresh, manage, and document the reporting replicas and warehouse refresh schedules. To support high availability during open hours, the reporting architecture shall include mechanisms (read-only replicas, prioritized queueing, and background processing on separate resources) intended to permit administrators to process searches and reports during normal open hours without disrupting OPAC or core transactional performance. The system shall permit administrators to mark job classes as high-priority for daytime execution, subject to resource and policy controls.

**Sources:** `early_draft_srs_galecia.txt`; `evergreen_reference_2009.txt`; `interview_sysadmin_2009-05-10.txt`; `meeting_minutes/meeting_2009-07-20_minutes.txt`; `meeting_tech_subcommittee_2009-06-30.txt`
**Evidence candidates:** C0167, C0213, C0153, C0152, C0203, C0206, C0083, C0092, C0173, C0194, C0230, C0239

### REQ-0035 — Real-Time vs Historical Report Support

**Priority:** Must. Certain operational reports require live data while many analytic reports require historical data; both were requested explicitly.

The system shall support both real-time queries (current-state reports, e.g., 'overdue today') and historical queries (e.g., 'bill amount on date D') leveraging the reporting architecture. The report interface shall let users specify whether the query should run against live data, a replica at a specific timestamp, or a historical snapshot/warehouse, with appropriate warnings about performance and data currency.

**Sources:** `evergreen_reference_2009.txt`; `meeting_tech_subcommittee_2009-06-30.txt`
**Evidence candidates:** C0213, C0214, C0213, C0153, C0154

### REQ-0036 — Data Model and Data Dictionary Provisioning

**Priority:** Must. Report authors and administrators require accurate data specifications to build correct queries; mandated in multiple inputs.

The software developer/system shall provide complete data specifications and data dictionaries for all relevant records used by Management Processes, including authority records, bibliographic records, order records, item records, hold/request records, patron records, transaction/action records, financial (money) records, and actor (staff) records. Data dictionaries shall include field names, data types, relationships (foreign keys), sample values, and notes about calculated fields (e.g., age range computed from birth_date). The documentation shall be kept current with software releases and be accessible to administrators and report authors. In addition to data dictionaries, the developer shall provide high-level process descriptions for major operational processes (for example: bibliographic record import/export, authority validation flows, item lifecycle from acquisition through purge, transfer workflows, and reporting pipeline refresh processes). These descriptions shall accompany the data dictionary and be kept current with releases.

**Sources:** `early_draft_srs_galecia.txt`; `evergreen_reference_2009.txt`; `meeting_minutes/meeting_2009-07-20_minutes.txt`; `meeting_tech_subcommittee_2009-06-30.txt`
**Evidence candidates:** C0093, C0195, C0207, C0208, C0148, C0149, C0094, C0196, C0209, C0240, C0241, C0305, C0306, C0307

### REQ-0037 — Error Reporting, Validation, and Query Diagnostics

**Priority:** Must. Administrators require meaningful diagnostics to resolve failed reports rather than generic messages; repeatedly emphasized by tech stakeholders.

The system shall provide meaningful high-level and low-level error reporting and feedback in the front-end, including clear messages when a report fails, query-specific diagnostics that help identify table/field/permission or syntax issues, and logging of error details for administrators. Error messages shall be actionable and include references to the failing query clause where possible. The system shall include mechanisms for recovering from common failures and for administrators to obtain the failing SQL when debugging (respecting permission restrictions).

**Sources:** `early_draft_srs_galecia.txt`; `evergreen_reference_2009.txt`; `meeting_minutes/meeting_2009-07-20_minutes.txt`; `meeting_tech_subcommittee_2009-06-30.txt`
**Evidence candidates:** C0096, C0198, C0211, C0153, C0243

### REQ-0038 — Online Help and Training Environments

**Priority:** Must. Training and accessible help reduce operational errors and support adoption; migration between environments is required by sysadmins and managers.

The system shall provide an online, hierarchical, cross-linked help system in standards-compliant HTML describing and illustrating system functions, query tool usage, templates, and role management. The system shall provide separate environments for development, training, and production. The developer shall provide migration/import-export facilities for report templates, permission settings, saved queries, and configurations between environments. The training environment shall be safe for staff experimentation without risk to production data.

**Sources:** `early_draft_srs_galecia.txt`; `interview_sysadmin_2009-05-10.txt`; `meeting_minutes/meeting_2009-07-20_minutes.txt`; `meeting_tech_subcommittee_2009-06-30.txt`
**Evidence candidates:** C0095, C0090, C0203, C0204, C0174, C0192, C0210, C0172, C0197, C0237, C0242

### REQ-0039 — Accessibility and Standards-Compliant Web Output

**Priority:** Must. Legal accessibility requirements and historical browser support constraints were emphasized by stakeholders; HTML standards ensure cross-browser and assistive tech compatibility.

The system shall produce standards-compliant HTML output for web-based components, and the web UI (including report results and online help) shall meet accessibility requirements equivalent to Section 508 (support for screen readers such as JAWS and NVDA, screen magnification tools like ZoomText, use of ARIA attributes where needed, proper alt text for images, semantic markup, and keyboard accessibility). Browser support shall include Microsoft Internet Explorer 6.0 and later and Mozilla Firefox 2.0 and later when web-based access is used (to preserve historical client compatibility).

**Sources:** `early_draft_srs_galecia.txt`; `interview_sysadmin_2009-05-10.txt`; `meeting_minutes/meeting_2009-07-20_minutes.txt`; `meeting_tech_subcommittee_2009-06-30.txt`
**Evidence candidates:** C0086, C0169, C0191, C0201, C0202, C0188, C0087, C0085, C0089, C0168, C0187, C0189, C0232, C0233, C0234, C0236

### REQ-0040 — Server Environment Compatibility

**Priority:** Must. Operational servers in PINES include both Linux and Solaris platforms and PostgreSQL is the production DB; compatibility is mandatory.

The reporting system shall operate on Linux and Solaris server environments (specifically including Red Hat Enterprise Linux 5 and Solaris 10 on SPARC where applicable). The system shall be compatible with the consortium's PostgreSQL-based relational database backend and shall not require an unsupported DB platform. Installer and operations documentation shall include OS-specific instructions and configuration guidance.

**Sources:** `early_draft_srs_galecia.txt`; `interview_sysadmin_2009-05-10.txt`; `meeting_minutes/meeting_2009-07-20_minutes.txt`; `meeting_tech_subcommittee_2009-06-30.txt`
**Evidence candidates:** C0084, C0166, C0190, C0191, C0203, C0166, C0186, C0231

### REQ-0041 — Relational Database Compliance and SQL Semantics

**Priority:** Must. Multiple technical inputs insist the reporting layer must work with, not against, the relational schema and that SQL null semantics be respected.

The reporting system shall be designed to work with a fully relational database back-end (PostgreSQL) using normalized schemas. SQL-based query semantics (including explicit inclusion of nulls and blank fields in results) shall be preserved, and the system shall avoid approaches that create synchronization issues with the authoritative relational store. Database-level triggers or equivalent mechanisms shall be used to capture deletion audit events.

**Sources:** `early_draft_srs_galecia.txt`; `interview_sysadmin_2009-05-10.txt`; `meeting_tech_subcommittee_2009-06-30.txt`
**Evidence candidates:** C0088, C0200, C0215, C0204, C0206, C0169, C0170, C0199, C0235

### REQ-0042 — Role-Based Authentication, Staff Login Options, and Auditability

**Priority:** Must. Strong operational and security needs require role-based permissions and flexible login modes while ensuring auditability.

The system shall implement role-based access control via security groups/roles (Global Admin, Local Admin, Library Manager, Staff, Patron) and administrators shall be able to create and manage these roles. The system shall support streamlined staff login options (optional card-swipe or single-sign methods) but shall also support traditional username/password authentication as a fallback. Card-swipe login shall not bypass per-user authentication and the system shall capture which staff member is logged-in for audit/tracking. Permissions assigned shall drive what reports and actions the logged-in user can perform.

**Sources:** `early_draft_srs_galecia.txt`; `email_staff_login.eml`; `interview_sysadmin_2009-05-10.txt`; `meeting_minutes/meeting_2009-03-15_minutes.txt`; `meeting_minutes/meeting_2009-07-20_minutes.txt`; `meeting_tech_subcommittee_2009-06-30.txt`
**Evidence candidates:** C0132, C0133, C0134, C0135, C0136, C0137, C0138, C0139, C0140, C0205, C0171, C0091, C0182, C0193, C0238, C0289, C0290, C0291, C0292, C0293, C0294, C0295, C0296, C0297

### REQ-0043 — Pre-Defined Canned and Board Reports

**Priority:** Must. Stakeholders expect a baseline set of commonly-used reports available out of the box, including board-level reporting needs.

The system shall provide a library of pre-defined canned reports covering the major categories (circulation, items, bibliographic records, patrons, holds, in-house use, transits, bills) with representative examples (checkout counts, items added, items currently checked out, items overdue by X days, patron counts by home library, bills owed, aged debt). The system shall also include predefined 'Board Reports' templates with key statistics required for executive and board use (traffic, volume of use, checkouts, check-ins, holds placed/filled, cross-tabulated by terminal/branch/hour/age/patron type/location).

**Sources:** `early_draft_srs_galecia.txt`; `email_financial_reports.eml`; `email_report_features.eml`; `evergreen_reference_2009.txt`
**Evidence candidates:** C0145, C0127, C0118, C0119, C0115, C0116, C0151, C0265, C0287, C0302

### REQ-0044 — Uncataloged Material Inventory Control

**Priority:** Must. Multiple interview and early-draft candidates explicitly require the ability to track and report on uncataloged material arrivals and usage for large-volume rapid distribution workflows; this is a distinct operational capability not covered by existing item-based reporting.

The system shall provide inventory management and lightweight tracking for uncataloged material that lack full bibliographic records (for example: mass paperback shipments or children's board books). This capability shall allow staff to create temporary inventory records tied to shipments or lots, assign barcodes or batch identifiers, record minimal required metadata (type, quantity, destination/branch, distribution template), track circulation/usage metrics for uncataloged items, and support quick distribution workflows with minimal per-item labor. Inventory of uncataloged material shall be includable in applicable collection and circulation reports and shall be convertible to full item/bibliographic records when cataloging data become available. The system shall provide controls for administrators to define which uncataloged item attributes are required, and how uncataloged inventory is represented in aggregated reports.

**Sources:** `early_draft_srs_galecia.txt`; `interview_cataloging_2009-05-08.txt`
**Evidence candidates:** C0100, C0155, C0247, C0269, C0274, C0269

### REQ-0045 — Data Quality and Integrity Reporting

**Priority:** Should. Cataloging and technical services stakeholders requested automated detection of common data problems to maintain catalog integrity; this is important to operations and not currently covered in sufficient detail by other requirements.

The system shall provide data quality reports that identify likely data integrity issues, including items with invalid or missing item type, excessively long call numbers, bibliographic records with no attached item records, items with inconsistent or missing status fields, and other anomalies configurable by administrators. Data quality reports shall be runnable on-demand and schedulable, and shall include exportable lists for corrective action. The system shall allow administrators to define rules and thresholds used to detect quality issues and shall record when quality reports were run and who reviewed results.

**Sources:** `interview_cataloging_2009-05-08.txt`
**Evidence candidates:** C0164

## Blacklist — discarded requirements

### BL-0001 — Conflicting and Under-specified Deletion / Purge Candidates (reviewed and merged into Item Purging and Last-Copy Controls / Deletion Audit Logging)

Multiple earlier candidate entries included overlapping, partially conflicting, or under-specified definitions of purging, last-copy behavior, and deletion audit logging. Their substantive behaviors are consolidated into unified requirements to avoid contradictory implementations while preserving original candidate references.

**Sources:** `conversations/conv_pines021_item_purging.eml`; `conversations/conv_pines022_deletions.eml`
**Evidence candidates:** C0052, C0053, C0054, C0055, C0056, C0057, C0061, C0062, C0063, C0064, C0065

### BL-0002 — Project-document editorial and planning notes

These entries describe project-administration decisions, scope framing, or drafting actions rather than software behavior to be implemented. They do not define product functionality or constraints that must be enforced by the software, and therefore are out of scope for the SRS functional requirements.

**Sources:** `meeting_minutes/meeting_2009-03-15_minutes.txt`
**Evidence candidates:** C0175, C0176, C0177, C0183, C0180, C0179, C0181

## Open questions

- What default numeric values should be used for configurable thresholds referenced as X (in-transit days default 7 is suggested; inactivity default 365; purge missing months default unspecified)? Specify authoritative defaults or indicate a policy that admin must set them.
- For auto-revert criteria: should 'checked out at destination' cause immediate revert, or should event-based reversion be expressed as a cancellation of the revert timer? Multiple inputs propose variants; stakeholders must select the final behavior.
- For reporting replicas and historical warehouses: Who is responsible for hardware and refresh schedule policy (consortium central IT vs. member system)? This is operational deployment policy, currently unspecified in source materials.
- Email delivery of reports and hourly scheduling are mentioned in some candidates as desirable but earlier Evergreen behavior lacked email delivery; should the system implement email delivery and hourly schedules as required features or defer to future enhancements?
- Undo semantics for batch transfers/purges: how long shall undo be supported and how shall it interact with subsequent transactions (e.g., item circulated after transfer)? The sources mention undo and limits but do not fix retention periods or conflict resolution rules.
- Retention policy for deletion audit logs: feedback requested clarity on retention period and archival; the source materials require logging but do not specify retention durations. Who sets the retention policy (local admin or consortium), and should the system provide configurable retention enforcement?
- Should attempts to delete records that are denied (due to insufficient permission) be recorded by default, or only when administrators enable that optional monitoring feature? The candidate set suggests this capability but does not make it mandatory.
- Confirm whether color-coding (green/yellow/red) for capacity status is a 'Should' (recommended) UI affordance or must-have accessibility-compliant alternative views (e.g., patterns/labels) to meet Section 508 requirements.
- Clarify whether email delivery of scheduled reports needs integration with an existing consortium SMTP/service account and whether attachments should include query metadata (criteria, user) by default.
- Which stakeholders will own the canonical mapping between local categories (e.g., local genre labels) and system-wide category definitions used for cross-branch comparisons and canned templates?

## Outstanding review findings

- Already extracted (C0120, C0121, C0122, C0288): The specifics regarding the need for accountability in counting significant data metrics regarding financial records and the pressure for scheduled exports to meet operational compliance derived from stakeholder feedback were not compiled into the current candidate set. — Accountability and financial reporting details (counts/metrics for financial records, audit trail, and scheduled exports/retention for compliance) are already reflected across financial reporting and audit trail candidates (C0120–C0122) and scheduling/export features in the reporting interface candidates (e.g., C0288). The user’s phrasing is broad; the underlying behaviors are present in the candidate set.

## Input documents and excluded background

- `conversations/conv_pines014_material_volume.eml`
- `conversations/conv_pines015_capacity_interface.eml`
- `conversations/conv_pines016_shelf_space.eml`
- `conversations/conv_pines018_item_transfer.eml`
- `conversations/conv_pines019_020_missing_intransit.eml`
- `conversations/conv_pines021_item_purging.eml`
- `conversations/conv_pines022_deletions.eml`
- `conversations/conv_pines023_patron_characteristics.eml`
- `conversations/conv_pines024_inactive_patrons.eml`
- `early_draft_srs_galecia.txt`
- `email_financial_reports.eml`
- `email_report_features.eml`
- `email_staff_login.eml`
- `evergreen_reference_2009.txt`
- `interview_cataloging_2009-05-08.txt`
- `interview_sysadmin_2009-05-10.txt`
- `meeting_minutes/meeting_2009-03-15_minutes.txt`
- `meeting_minutes/meeting_2009-07-20_minutes.txt`
- `meeting_tech_subcommittee_2009-06-30.txt`
- `survey_results_2009.txt`

Personal chatter and background topics omitted during extraction:

