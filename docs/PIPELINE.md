# Optional: Build, push and deploy with GitHub Actions (CI/CD)

Back to the [workshop guide](../README.md).

> **Optional.** Try it after the workshop. The laptop or CloudShell steps in the README are all you need today.

GitHub builds your image, pushes it to **your** ECR repository, and deploys it to **your** ECS service. You need a free **GitHub account**. No access keys: GitHub signs in to AWS with a short-lived token (OIDC) and an IAM role you create.

The workflow is [.github/workflows/build-and-push.yml](../.github/workflows/build-and-push.yml).

**The order:**

| Step | Where | What |
|---|---|---|
| [1](#step-1-fork-the-repo) | GitHub | Fork the repo, turn on Actions |
| [2](#step-2-let-github-sign-in-to-aws) | AWS IAM | OIDC provider + role for GitHub |
| [3](#step-3-create-ecr-and-add-the-first-3-variables) | AWS + GitHub | ECR repository → **variables, round 1** |
| [4](#step-4-first-run-build-and-push-v1) | GitHub | First run: build and push `v1` |
| [5](#step-5-create-ecs-and-add-the-last-4-variables) | AWS + GitHub | ECS cluster, task definition, service → **variables, round 2** |
| [6](#step-6-test-cicd-commit-and-watch-it-deploy) | GitHub | Edit, commit, watch it deploy |

> **Already did the workshop** (ECR repository and ECS service exist)? Do Steps 1 and 2, add **all 7 variables** (the tables in Steps 3 and 5), then go to Step 6.

---

## How to add or change a variable

Your fork → **Settings** → **Secrets and variables** → **Actions** → **Variables** tab:
- **Add:** **New repository variable** → **Name** and **Value** → **Add variable**
- **Change:** click the ✏️ next to the variable → new value → **Update variable**

⚠️ Use the **Variables** tab, not **Secrets**. The workflow reads variables.

---

## Step 1: Fork the repo
1. Open **https://github.com/cloudadhar/from-code-to-cloud** → **Fork** → **Create fork**.
2. In **your** fork → **Actions** tab → **I understand my workflows, go ahead and enable them**. (Forks have Actions turned off until you do this.)

## Step 2: Let GitHub sign in to AWS
1. **IAM** → **Identity providers** → **Add provider** (already in the list? skip)
   - **Provider type:** OpenID Connect
   - **Provider URL:** `https://token.actions.githubusercontent.com`
   - **Audience:** `sts.amazonaws.com` → **Add provider**
2. **IAM** → **Roles** → **Create role**
   - **Trusted entity type:** Web identity
   - **Identity provider:** `token.actions.githubusercontent.com` · **Audience:** `sts.amazonaws.com`
   - **GitHub organization:** your GitHub username · **GitHub repository:** `from-code-to-cloud` · **GitHub branch:** `main` → **Next**
   - **Permissions:** tick `AmazonEC2ContainerRegistryPowerUser` → **Next**
   - **Role name:** `github-ecr-push` → **Create role**
3. Open the role → **Add permissions** → **Create inline policy** → **JSON** → paste this (replace `123456789012` with your account ID) → name `ecr-public-and-ecs-deploy` → **Create policy**:
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

## Step 3: Create ECR and add the first 3 variables
1. Create the ECR repository: [README Step 3.1](../README.md#31-create-the-repository-console).
2. Add these **variables** in your fork:

| Name | Value | Where to find it |
|---|---|---|
| `AWS_ROLE_ARN` | `arn:aws:iam::123456789012:role/github-ecr-push` | IAM → **Roles** → `github-ecr-push` → **ARN** (copy icon) |
| `AWS_REGION` | `ap-south-1` | Console, top right |
| `ECR_REPOSITORY` | `from-code-to-cloud` | ECR → **Repositories** → **Repository name** (only the name, not the full URI) |

## Step 4: First run: build and push v1
1. Your fork → **Actions** → **Build, push and deploy** → **Run workflow** → **tag:** `v1` → **untick deploy** (ECS doesn't exist yet) → **Run workflow**.
2. Wait about 2 minutes for the green ✅. Open the run: the summary shows your **Image URI** (ends in `:v1`). Copy it.

## Step 5: Create ECS and add the last 4 variables
1. In the Console, follow [README Steps 4–7](../README.md#step-4-create-an-ecs-cluster): cluster → task definition (paste the Image URI from Step 4) → run a task → **service**. Check the app opens on `http://<public-ip>:8080`.
2. Add these **variables** in your fork:

| Name | Value | Where to find it |
|---|---|---|
| `ECS_CLUSTER` | `cloudadhar-cluster` | ECS → **Clusters** → cluster name |
| `ECS_SERVICE` | `cloudadhar-web` | ECS → your cluster → **Services** tab → service name |
| `ECS_TASK_DEFINITION` | `from-code-to-cloud` | ECS → **Task definitions** → the family name (without `:1`) |
| `ECS_CONTAINER_NAME` | `web` | ECS → **Task definitions** → `from-code-to-cloud` → latest revision → **Containers** → name (if it says `Main`, use `Main`) |

✅ Your fork now has **7 variables**.

## Step 6: Test CI/CD: commit and watch it deploy
1. In your fork, open `index.html` → ✏️ → change the line under `<!-- Part 8 ... -->` to your own message → **Commit changes** (to `main`).
2. **Actions** tab: a run starts by itself → **build-and-push** → **deploy** (about 4–6 minutes; it waits until the new task is healthy).
3. ECS → your service → **Deployments** tab: the rolling update.
4. Open the **new** task's Public IP on `:8080`. ✅ Your new message, version `git-xxxxxxx`. No command typed. 🎉

You can also run it by hand: **Run workflow** → any tag (e.g. `v2`) → **deploy** ticked.

---

## Problems

| You see | Fix |
|---|---|
| `Add these in Settings → … Variables` | A variable is missing or misspelled. Check the names exactly (Step 3 and Step 5) |
| Variables are under **Secrets** | Move them to the **Variables** tab |
| No **Run workflow** button | Actions aren't turned on in your fork (Step 1) |
| `Not authorized to perform sts:AssumeRoleWithWebIdentity` | The role's trust policy doesn't match your fork. IAM → `github-ecr-push` → **Trust relationships**: the `sub` must be `repo:YOUR-USERNAME/from-code-to-cloud:ref:refs/heads/main`. Some accounts send an ID-based form instead (`repo:YOUR-USERNAME@OWNER-ID/from-code-to-cloud@REPO-ID:ref:refs/heads/main`): get the IDs from `https://api.github.com/repos/YOUR-USERNAME/from-code-to-cloud` (`owner.id` and `id`) and add that line too |
| `repository ... does not exist` | Create the ECR repo in the same region as `AWS_REGION` |
| `429 Too Many Requests` | The role is missing the inline policy (Step 2.3) |
| `AccessDenied` on `ecs:...` or `iam:PassRole` | The role is missing the inline policy (Step 2.3) |
| `Unable to describe task definition` | `ECS_TASK_DEFINITION` must be the family name, without `:1` |
| `Invalid container name` | `ECS_CONTAINER_NAME` must match the task definition exactly (`web` or `Main`) |
| `ServiceNotFoundException` | Check `ECS_CLUSTER` and `ECS_SERVICE`, and that the service exists |
| Deploy runs for 10+ minutes | The new task keeps stopping. ECS → service → **Tasks** → stopped task → **Stopped reason** |

## Clean up
1. Do [README Step 9](../README.md#step-9-clean-up) (ECS and ECR).
2. IAM → **Roles** → delete `github-ecr-push`. Not using GitHub OIDC elsewhere? Also delete the identity provider.
3. Optional: delete your fork (Settings → **Delete this repository**).
