# Instructor Notes: Deploy Your First App on Amazon ECS Fargate

## Before the workshop
- [ ] Do a full dry run on a **free** account (Parts 1–10), including opening the app in the browser and deploying v2.
- [ ] Check that `docker --version` works in CloudShell in the workshop region.
- [ ] Send `docs/PREREQUISITES.md` and the repo link to learners at least 1 day before.
- [ ] Keep a recording of Parts 5 and 8 as a backup.

## Agenda (2 hours)

| Time | Section | README |
|---|---|---|
| 0:00–0:10 | Why containers? Image vs container, the words table | — |
| 0:10–0:25 | Build and test the image in CloudShell | Part 2 |
| 0:25–0:40 | ECR: create repo, log in, push v1 | Part 3 |
| 0:40–0:55 | Cluster + task definition | Part 4 |
| 0:55–1:10 | Service + open the app in the browser 🎉 | Part 5 |
| 1:10–1:15 | Logs | Part 6 |
| 1:15–1:30 | Self-healing + scaling | Part 7 |
| 1:30–1:45 | Ship v2 + rollback | Part 8 |
| 1:45–1:55 | **Cleanup** together | Part 10 |
| 1:55–2:00 | Recap + Q&A | Part 9 |

## Most likely problems
1. **Public IP off** when creating the service → `CannotPullContainerError`. Say it twice in 5.1.
2. **Security group** missing port 8080 → browser times out.
3. **https instead of http** in the browser.
4. **Wrong region** between CloudShell and the Console → ECR repo "does not exist".
5. **Docker login expired** or skipped before `docker push`.

## If running behind
- Skip 7.2 (scaling). Keep 7.1 (self-healing): it's the most memorable moment.
- Do Part 8 as a demo while students watch.
- **Never skip Part 10 (cleanup).**
