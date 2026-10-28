# Before the Workshop: Prerequisites Checklist

**Workshop:** From Code to Cloud: Deploy a Containerised App with Amazon ECR & ECS Fargate
**When:** 30 October 2026 (Friday), 11:00 AM · Seminar Hall, Siddhant College of Engineering

Please finish this **before** the session. It takes about 10 minutes.

## 1. An AWS account
- [ ] You can sign in to the AWS Console. A **free account works** for this workshop.
- [ ] You're signed in as an **IAM user with AdministratorAccess** (or an IAM Identity Center user), **not the root user**.
  - Only have root? **IAM** → **Users** → **Create user** → tick **Provide user access to the AWS Management Console** → **Attach policies directly** → `AdministratorAccess` → **Create user**. Sign out and sign in as that user.

## 2. The right region
- [ ] Top-right of the Console: **Asia Pacific (Mumbai) ap-south-1**. Use it for every step.

## 3. CloudShell and Docker work
CloudShell is a terminal inside the AWS Console. It already has Docker and the AWS CLI, so you install nothing.

1. - [ ] Check the region (top right) says **Asia Pacific (Mumbai)**.
2. - [ ] Click the **CloudShell icon `>_`** in the top bar, next to the search box. (Or type `CloudShell` in the search box and open it.)
3. - [ ] First time only: a **Welcome to AWS CloudShell** box appears. Click **Close**.
4. - [ ] Wait about 30 seconds until you see a prompt like `[cloudshell-user@ip-10-...  ~]$`.
5. - [ ] Click in the terminal, paste this line and press **Enter**:
   ```bash
   docker --version
   ```
   ✅ You see something like `Docker version 25.0.x`.
6. - [ ] Paste this line and press **Enter**:
   ```bash
   aws sts get-caller-identity
   ```
   ✅ You see your 12-digit **Account** number, and an **Arn** ending in `user/<your-name>` (not `root`).

> To paste in CloudShell, use **Ctrl+Shift+V** on Windows/Linux or **Cmd+V** on Mac. If the browser asks to allow pasting, click **Allow**.

## 4. Download the workshop code and test the upload
1. - [ ] Download **`from-code-to-cloud.zip`** from the WhatsApp group to your laptop. Don't unzip it.
2. - [ ] In CloudShell, click **Actions** (top right of the CloudShell window) → **Upload file** → **Choose file** → pick the zip → **Upload**.
3. - [ ] Run:
   ```bash
   ls
   ```
   ✅ You see `from-code-to-cloud.zip`. That's all for now. You'll unzip it in the workshop.

## 5. ECS is ready
- [ ] Open **Elastic Container Service (ECS)** in the Console and check that the page loads without an error.

## Cost
Less than **US$0.10** if you clean up at the end (Part 10 of the README).

If any step fails, message the instructor **before** the workshop with a screenshot.
