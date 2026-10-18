# Routing taxonomy

| Label | Route when | Escalate urgently when |
|---|---|---|
| TEMPERATURE_EXCURSION | cold-chain or temperature integrity is threatened | medicine, vaccine, spoilage, or active excursion |
| DAMAGE | packaging or goods are physically damaged | leak, hazard, or safety risk |
| DELAY | schedule or ETA is missed | time-critical language or essential goods |
| WRONG_DESTINATION | address, depot, or route is incorrect | always review if destination is ambiguous |
| DOCUMENTATION | paperwork, invoice, manifest, permit, or signature issue | deadline or border impact |
| CUSTOMS_HOLD | border, duty, tariff, inspection, or clearance hold | perishable or deadline-bound cargo |
| OTHER | none of the above | human review when confidence is low |

Abstention is a deliberate output: predictions below the configured confidence
threshold are routed to `HUMAN_REVIEW` instead of forcing a category.

