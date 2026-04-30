# Packaging Line Manual (Extract)

## Alarm ALM-204 - Transfer station timeout
Definition: Transfer command was issued, but downstream presence sensor PE_14 did not turn ON within timeout window.

### Typical trigger chain
1. Transfer request from upstream station
2. Transfer conveyor or pusher starts
3. Workpiece should reach PE_14 detection area
4. If PE_14 stays OFF beyond 5 seconds, ALM-204 is raised

### Common causes
- Workpiece jam or skew in transfer zone
- PE_14 contaminated, misaligned, or failed
- Pneumatic cylinder motion incomplete due to low pressure
- Manual/Auto mode mismatch causing interlock failure

### Maintenance notes
- Check transfer zone physically before any forced reset
- Confirm no repeated obstruction from upstream feeder
- If PE_14 indicator does not toggle with object present, inspect sensor and wiring
