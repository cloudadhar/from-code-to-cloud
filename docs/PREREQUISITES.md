# Before the Workshop: Prerequisites Checklist

**Workshop:** From Code to Cloud: Deploy a Containerised App with Amazon ECR & ECS Fargate
**When:** 30 October 2026 (Friday), 11:00 AM · Seminar Hall, Siddhant College of Engineering

Please finish this **at home, before** the session. It takes 30–45 minutes, mostly downloads. College Wi-Fi is too slow for Docker Desktop, so don't leave it for the workshop.

## 1. An AWS account
- [ ] You can sign in to the AWS Console. A **free account works** for this workshop.
- [ ] You're signed in as an **IAM user with AdministratorAccess** (or an IAM Identity Center user), **not the root user**.
  - Only have root? **IAM** → **Users** → **Create user** → tick **Provide user access to the AWS Management Console** → **Attach policies directly** → `AdministratorAccess` → **Create user**. Sign out and sign in as that user.

## 2. The right region
- [ ] Top-right of the Console: **Asia Pacific (Mumbai) ap-south-1**. Use it for every step.

## 3. Install VS Code
1. - [ ] Download and install **Visual Studio Code** (free): https://code.visualstudio.com
2. - [ ] Open it. ✅ It starts.

## 4. Install Docker Desktop
1. - [ ] Download **Docker Desktop**: https://www.docker.com/products/docker-desktop/
   - **Windows:** run the installer and keep **Use WSL 2** ticked. Restart when asked.
   - **Mac:** pick **Apple chip** (M1–M4) or **Intel chip** (Apple menu → **About This Mac** tells you). Drag Docker to Applications.
2. - [ ] Open **Docker Desktop**, accept the terms (you can skip signing in) and wait for **Engine running** (green, bottom left).

> 🪟 Windows error about **virtualization** or **WSL**? Turn on virtualization in your BIOS (often called *Intel VT-x* or *AMD-V/SVM*), then in **PowerShell as administrator** run `wsl --update` and restart. Still stuck? Send a screenshot to the instructor. You can use CloudShell instead (Plan B in the README).

## 5. Install the AWS CLI (version 2.32 or newer)
1. - [ ] Follow the installer for your OS: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html
   - **Windows:** download and run the **MSI installer**.
   - **Mac:** download and run the **macOS .pkg installer**.
2. - [ ] **Close and reopen VS Code** so it finds the new tools.

## 6. Get the code and check everything in VS Code
1. - [ ] Download **`from-code-to-cloud.zip`** from the WhatsApp group and unzip it (Windows: right-click → **Extract All**; Mac: double-click).
2. - [ ] VS Code → **File → Open Folder** → the `from-code-to-cloud` folder that has `README.md` inside (on Windows it's often one folder deeper: `from-code-to-cloud\from-code-to-cloud`).
3. - [ ] Open `README.md` and press **Ctrl+Shift+V** (Mac: **Cmd+Shift+V**). ✅ You see the workshop guide.
4. - [ ] **Terminal → New Terminal**, then run these one at a time:
   ```bash
   docker --version
   aws --version
   docker run --rm hello-world
   ```
   ✅ A Docker version, `aws-cli/2.32` or higher, and `Hello from Docker!`.

## 7. Sign the AWS CLI in (no access keys)
1. - [ ] In the VS Code terminal:
   ```bash
   aws configure set region ap-south-1
   aws login
   ```
2. - [ ] Your browser opens. Pick your Console session (or sign in as your IAM user) → **Allow**.
3. - [ ] Back in the terminal:
   ```bash
   aws sts get-caller-identity
   ```
   ✅ You see your 12-digit **Account** number, and an **Arn** ending in `user/<your-name>` (not `root`).

## 8. ECS is ready
- [ ] Open **Elastic Container Service (ECS)** in the Console and check that the page loads without an error.

## Cost
Less than **US$0.10** if you clean up at the end (Part 10 of the README).

If any step fails, message the instructor **before** the workshop with a screenshot.
