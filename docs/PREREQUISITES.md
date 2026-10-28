# Before the Workshop: Prerequisites Checklist

**Workshop:** Deploy Your First Container on AWS: Hands-on with Amazon ECR & ECS Fargate

Please finish this **before** the session. It takes about 10 minutes.

## 1. An AWS account
- [ ] You can sign in to the AWS Console. A **free account works** for this workshop.
- [ ] You're signed in as an **IAM user with AdministratorAccess** (or an IAM Identity Center user), **not the root user**.
  - Only have root? **IAM** → **Users** → **Create user** → tick **Provide user access to the AWS Management Console** → **Attach policies directly** → `AdministratorAccess` → **Create user**. Sign out and sign in as that user.

## 2. The right region
- [ ] Top-right of the Console: **Asia Pacific (Mumbai) ap-south-1**. Use it for every step.

## 3. CloudShell and Docker work
- [ ] Click the **CloudShell icon `>_`** in the top bar and wait for the terminal.
- [ ] Run:
  ```bash
  docker --version
  aws sts get-caller-identity
  ```
  ✅ A Docker version number, and your account ID.

## 4. ECS is ready
- [ ] Open **Elastic Container Service (ECS)** in the Console and check that the page loads without an error.

## Cost
Less than **US$0.10** if you clean up at the end (Part 10 of the README).

If any step fails, message the instructor **before** the workshop with a screenshot.
