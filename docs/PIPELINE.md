# Optional: Build, push and deploy with GitHub Actions

Back to the [workshop guide](../README.md).

> **Optional.** Use this after the workshop, or watch it as a demo. The laptop or CloudShell steps in the README are all you need today.

A pipeline: GitHub builds the image and pushes it to **your** ECR repository, and (with C.5) deploys it to your ECS service. You need a free **GitHub account**. It takes about 10 minutes to set up once. No access keys: GitHub signs in to AWS with a short-lived token (OIDC) and an IAM role you create.

The workflow is [.github/workflows/build-and-push.yml](../.github/workflows/build-and-push.yml). It runs when you click **Run workflow**, and (once C.5 is set up) on every commit to `main` that changes `app.py`, `index.html` or the `Dockerfile`.

## C.1 Fork the repo (GitHub)
1. Open **https://github.com/cloudadhar/from-code-to-cloud** → **Fork** → **Create fork**.
2. In **your** fork → **Actions** tab → **I understand my workflows, go ahead and enable them**.

## C.2 Let GitHub sign in to AWS (Console, one time)
1. **IAM** → **Identity providers** → **Add provider**
   - **Provider type:** OpenID Connect
   - **Provider URL:** `https://token.actions.githubusercontent.com`
   - **Audience:** `sts.amazonaws.com` → **Add provider**
   - Already in the list? Skip this step.
2. **IAM** → **Roles** → **Create role**
   - **Trusted entity type:** Web identity
   - **Identity provider:** `token.actions.githubusercontent.com` · **Audience:** `sts.amazonaws.com`
   - **GitHub organization:** your GitHub username · **GitHub repository:** `from-code-to-cloud` · **GitHub branch:** `main` → **Next**
   - **Permissions:** tick `AmazonEC2ContainerRegistryPowerUser` (build and push to ECR) → **Next**
   - **Role name:** `github-ecr-push` → **Create role**
3. Open the role → **Permissions** → **Add permissions** → **Create inline policy** → **JSON**, paste this (replace `123456789012` with your account ID) → name it `ecr-public-and-ecs-deploy` → **Create policy**:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "EcrPublicSignInForTheBaseImage",
      "Effect": "Allow",
      "Action": ["ecr-public:GetAuthorizationToken", "sts:GetServiceBearerToken"],
      "Resource": "*"
    },
    {
      "Sid": "EcsDeployForCD",
      "Effect": "Allow",
      "Action": ["ecs:DescribeTaskDefinition", "ecs:RegisterTaskDefinition", "ecs:DescribeServices", "ecs:UpdateService"],
      "Resource": "*"
    },
    {
      "Sid": "LetEcsUseTheTaskExecutionRole",
      "Effect": "Allow",
      "Action": "iam:PassRole",
      "Resource": "arn:aws:iam::123456789012:role/*",
      "Condition": {"StringEquals": {"iam:PassedToService": "ecs-tasks.amazonaws.com"}}
    }
  ]
}
```
4. Check the **Trust relationships** tab. The wizard writes a trust policy like this (your username and repo instead of `YOUR-GITHUB-USERNAME`):
```json
"Condition": {
  "StringEquals": {"token.actions.githubusercontent.com:aud": "sts.amazonaws.com"},
  "StringLike": {"token.actions.githubusercontent.com:sub": "repo:YOUR-GITHUB-USERNAME/from-code-to-cloud:ref:refs/heads/main"}
}
```
   Some GitHub accounts send an ID-based value instead, like `repo:YOUR-GITHUB-USERNAME@12345678/from-code-to-cloud@987654321:ref:refs/heads/main`. If the run fails with `Not authorized to perform sts:AssumeRoleWithWebIdentity`, add that form to the `sub` list too. Your IDs: `https://api.github.com/repos/YOUR-GITHUB-USERNAME/from-code-to-cloud` → `id` (repo) and `owner.id`.
5. Copy the role's **ARN** (`arn:aws:iam::123456789012:role/github-ecr-push`).

## C.3 Add the ECR details as variables (GitHub)
Your fork → **Settings** → **Secrets and variables** → **Actions** → **Variables** tab → **New repository variable**, three times:

| Name | Value |
|---|---|
| `AWS_ROLE_ARN` | the role ARN from C.2 |
| `AWS_REGION` | `ap-south-1` |
| `ECR_REPOSITORY` | `from-code-to-cloud` |

## C.4 Build and push
1. Create the ECR repository first (README Step 3.1).
2. Your fork → **Actions** → **Build, push and deploy** → **Run workflow** → **tag:** `v1`, untick **deploy** for now → **Run workflow**.
3. Wait about 2 minutes for the green ✅. Open the run: the summary shows your **Image URI**.
4. Continue with README **Steps 4–7** (cluster, task definition, task, service) in the Console; then turn on CD (C.5).

**Version 2 (README Step 8) with the pipeline:** in your fork, open `index.html` → pencil icon ✏️ → change your message → **Commit changes**. Then run the workflow again with **tag:** `v2`. (With the CD variables below, the commit itself builds and deploys v2.)

| Problem | Fix |
|---|---|
| `Add these in Settings → … Variables` | A variable is missing or misspelled (C.3) |
| `Not authorized to perform sts:AssumeRoleWithWebIdentity` | The trust policy's `sub` doesn't match. Check the username, repo and branch, and add the ID-based form (C.2 step 4) |
| `Secrets` instead of `Variables` | The workflow reads **Variables**. Add them on the **Variables** tab, not **Secrets** |
| `429 Too Many Requests` on the base image | The role is missing the ECR Public permissions (C.2 step 3) |
| `AccessDenied` on `ecs:...` or `iam:PassRole` in the deploy job | The role is missing the inline policy (C.2 step 3) |
| `repository ... does not exist` | Create the ECR repo (README Step 3.1) in the same region as `AWS_REGION` |
| No **Run workflow** button | Actions aren't enabled in your fork (C.1 step 2) |

## C.5 CD: deploy to ECS automatically (optional)
Once your ECS **service** exists (README Step 7), the same workflow can deploy every new image for you: it takes your latest task definition, swaps in the new image, registers a new revision and updates the service (a rolling deployment, like README Step 8).

Add four more **variables** (C.3):

| Name | Value |
|---|---|
| `ECS_CLUSTER` | `cloudadhar-cluster` |
| `ECS_SERVICE` | `cloudadhar-web` |
| `ECS_TASK_DEFINITION` | `from-code-to-cloud` (the task definition family) |
| `ECS_CONTAINER_NAME` | `web`: the container name in your task definition (check it: if the Console named it `Main`, use `Main`) |

Now:
- **Run workflow** with **deploy** ticked → build, push and deploy in one go.
- Or just **edit `index.html` on GitHub and commit to `main`**: the workflow starts by itself, tags the image `git-<commit>`, and deploys it. Watch the **Deployments** tab in ECS, then refresh the new task's Public IP.

The run waits until the new task is running and healthy, then shows ✅ **Deployed**.

| Problem | Fix |
|---|---|
| `Unable to describe task definition` | `ECS_TASK_DEFINITION` must be the family name, in the same region as `AWS_REGION` |
| `Invalid container name` / image not changed | `ECS_CONTAINER_NAME` must match the container name in the task definition exactly |
| `ServiceNotFoundException` | Check `ECS_CLUSTER` and `ECS_SERVICE`, and that the service exists (README Step 7) |
| Deploy step runs for 10+ minutes | The new task keeps stopping. ECS → the service → **Tasks** → stopped task → **Stopped reason** |

Clean up afterwards: delete the role `github-ecr-push` (and the identity provider if you added it) in IAM.
