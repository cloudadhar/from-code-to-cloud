# From Code to Cloud

### Deploy a Containerised App with Amazon ECR & ECS Fargate

**AWS Student Builder Group, Siddhant College of Engineering** · 30 October 2026 (Friday), 11:00 AM · Seminar Hall · Instagram [@aws.scoe](https://instagram.com/aws.scoe)

The hands-on steps for the workshop. The slides explain the *why*; this page is the *how*.

> Built by **[CloudAdhar](https://youtube.com/@cloudadhar)**, Building Cloud Futures

---

## The 9 steps

| Step | What you do |
|---|---|
| [0](#step-0-before-you-start) | Before you start: AWS account, region, Docker or CloudShell |
| [1](#step-1-get-the-code) | Get the code |
| [2](#step-2-build-and-test-the-image) | Build and test the image |
| [3](#step-3-push-the-image-to-amazon-ecr) | Push the image to Amazon ECR |
| [4](#step-4-create-an-ecs-cluster) | Create an ECS cluster |
| [5](#step-5-create-a-task-definition) | Create a task definition |
| [6](#step-6-run-it-and-open-it-live-) | Run it and open it live 🎉 |
| [7](#step-7-make-it-a-service-self-healing) | Make it a service (self-healing) |
| [8](#step-8-ship-version-2) | Ship version 2 |
| [9](#step-9-clean-up) | Clean up |

**Stuck?** See [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md).

---

## Step 0: Before you start

1. Sign in to the **AWS Console** as an **IAM user with AdministratorAccess** (not the root user).
2. Top right: choose region **Asia Pacific (Mumbai) ap-south-1**. Use it for **every** step.
3. Choose **where you'll build** the image:

**Is Docker working on your laptop?** Open VS Code → **Terminal → New Terminal** and run:
```bash
docker run --rm hello-world
```

| You see | Do this |
|---|---|
| ✅ `Hello from Docker!` | Use your **💻 laptop**. You also need the [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) (2.32 or newer) |
| ❌ Docker isn't installed | Install [Docker Desktop](https://www.docker.com/products/docker-desktop/), open it, wait for **Engine running**, try again |
| ❌ Docker won't install or start (give it 3 minutes) | Use **☁️ CloudShell**. It's a terminal in the AWS Console with Docker already installed. Nothing to install |

From here on, each step says what's different for **💻 laptop** and **☁️ CloudShell**.

---

## Step 1: Get the code

**💻 Laptop:**
1. Open https://github.com/cloudadhar/from-code-to-cloud → green **Code** button → **Download ZIP** → unzip it. (Have Git? `git clone https://github.com/cloudadhar/from-code-to-cloud.git` works too. No need to fork.)
2. VS Code → **File → Open Folder** → the folder with `README.md` inside.
3. **Terminal → New Terminal**. Run all commands there.

**☁️ CloudShell:**
1. In the AWS Console, click the **CloudShell icon `>_`** (top bar). Wait about 30 seconds.
2. Run:
```bash
git clone https://github.com/cloudadhar/from-code-to-cloud.git
cd from-code-to-cloud
```

---

## Step 2: Build and test the image

**Build** (same on 💻 and ☁️):
```bash
docker build --platform linux/amd64 -t from-code-to-cloud:v1 .
```
> `-t from-code-to-cloud:v1` gives the image a **name** and a **tag** (version). `.` means "build from this folder".
> `--platform linux/amd64` builds for the Intel/AMD servers AWS uses. Mac M1–M4 users: never skip it.

**Run** it:
```bash
docker run -d --name web -p 8080:8080 from-code-to-cloud:v1
```

**Test** it:
- **💻 Laptop:** open **http://localhost:8080** in your browser. ✅ You see the fireworks page and **v1**.
- **☁️ CloudShell:** run `curl http://localhost:8080/health`. ✅ You see `{"status": "healthy"}`.

**Stop** it:
```bash
docker stop web
docker rm web
```

---

## Step 3: Push the image to Amazon ECR

### 3.1 Create the repository (Console)
1. Search **ECR** → **Elastic Container Registry** → **Private registry → Repositories** → **Create repository**.
2. **Repository name:** `from-code-to-cloud`. Keep everything else as it is.
3. **Create**.

### 3.2 Sign in (💻 laptop only)
```bash
aws configure set region ap-south-1
aws login
```
Your browser opens → **Allow**. ☁️ CloudShell is already signed in: skip this.

### 3.3 Push
Find your **12-digit account ID** (top right of the Console). In the 3 commands below, **replace `123456789012` with it**, then run them one at a time:
```bash
aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 123456789012.dkr.ecr.ap-south-1.amazonaws.com
```
```bash
docker tag from-code-to-cloud:v1 123456789012.dkr.ecr.ap-south-1.amazonaws.com/from-code-to-cloud:v1
```
```bash
docker push 123456789012.dkr.ecr.ap-south-1.amazonaws.com/from-code-to-cloud:v1
```
✅ `Login Succeeded`, then the push ends with `digest: sha256:...`

### 3.4 Check it
Refresh the repository in the Console. ✅ You see tag **v1**. Click it and **copy the Image URI** (it ends in `:v1`).

---

## Step 4: Create an ECS cluster

1. Search **ECS** → **Elastic Container Service** → left menu **Clusters** → **Create cluster**.
   - Sees a page called **Let's set up your app**? Click **Cancel** and use **Clusters** in the left menu.
2. **Cluster name:** delete the random name and type `cloudadhar-cluster`.
3. **Infrastructure:** keep **Fargate only**. Leave everything else empty.
4. **Create**. Wait about 1 minute.

---

## Step 5: Create a task definition

1. ECS → **Task definitions** → **Create new task definition**.
2. **Family:** `from-code-to-cloud`
3. **Launch type:** AWS Fargate · **OS/Architecture:** **Linux/X86_64**
4. **CPU:** `.25 vCPU` · **Memory:** `.5 GB` (change it if the Console shows something else)
5. **Task role:** leave empty
6. **Task execution role:** **Create new role** (this lets ECS pull your image and write logs)
7. **Container:**
   - **Name:** `web`
   - **Image URI:** paste the URI from Step 3.4 (ends in `:v1`)
   - **Container port:** `8080`
8. **Create**.

---

## Step 6: Run it and open it live 🎉

1. ECS → **Clusters** → `cloudadhar-cluster` → **Tasks** tab → **Run new task**.
2. **Launch type:** FARGATE
3. **Family:** `from-code-to-cloud` · **Desired tasks:** `1`
4. **Networking:**
   - **Security group:** **Create a new security group** → name `cloudadhar-web-sg` → rule **Custom TCP**, port **8080**, source **Anywhere**
   - **Public IP:** **Turned on** ⚠️ (the #1 mistake: without it, nothing works)
5. **Create**. Wait until **Last status** is **Running** (1–2 minutes).
6. Click the task → copy the **Public IP** → open in your browser:

```
http://<public-ip>:8080
```
⚠️ Use **http** (not https) and don't forget **:8080**.

✅ The fireworks page, with **Running on: Amazon ECS on AWS Fargate** and your cluster, task ID and Availability Zone. **Your app is live on the internet!** Try it on your phone.

---

## Step 7: Make it a service (self-healing)

1. **Stop** the task from Step 6 (select it → **Stop**). Refresh the browser: it's gone.
2. Cluster → **Services** tab → **Create**:
   - **Launch type:** FARGATE · **Family:** `from-code-to-cloud`
   - **Service name:** `cloudadhar-web` · **Desired tasks:** `1`
   - **Security group:** **Use an existing security group** → `cloudadhar-web-sg` · **Public IP:** on
3. **Create**, wait for the task, open its new **Public IP** on `:8080`. ✅ It works.
4. **Self-healing test:** stop that task. Within a minute, ECS starts a new one **by itself**. 🎉
5. **Scaling:** **Update service** → **Desired tasks** `2` → two copies run. Set it back to `1`.

**Logs:** click a task → **Logs** tab. Every visit to your page is a line here.

---

## Step 8: Ship version 2

1. Edit `index.html`: change the line under `<!-- Part 8 ... -->` to your own message, e.g. `Deployed by Cloudadhar 🚀`.
   - **💻 Laptop:** in VS Code, save.
   - **☁️ CloudShell:** `nano index.html` → edit → `Ctrl+O`, `Enter`, `Ctrl+X`.
2. Build and push **v2** (replace `123456789012` again):
```bash
docker build --platform linux/amd64 --build-arg APP_VERSION=v2 -t 123456789012.dkr.ecr.ap-south-1.amazonaws.com/from-code-to-cloud:v2 .
```
```bash
docker push 123456789012.dkr.ecr.ap-south-1.amazonaws.com/from-code-to-cloud:v2
```
3. ECS → **Task definitions** → `from-code-to-cloud` → latest revision → **Create new revision** → change the image ending from `:v1` to `:v2` → **Create**.
4. Cluster → **Services** → `cloudadhar-web` → **Update service** → choose the new revision → **Update**.
5. Watch the **Deployments** tab until the new task runs. ✅ Open the new task's IP: **v2** with your message.

> Rollback: **Update service** back to the old revision.

---

## Step 9: Clean up

Do this **in order**, so you pay nothing more:

1. **Service:** cluster → **Services** → `cloudadhar-web` → **Delete service** → tick **Force delete**.
2. **Cluster:** `cloudadhar-cluster` → **Delete cluster** (after the tasks stop).
3. **Task definition:** select all revisions of `from-code-to-cloud` → **Deregister**, then **Delete**.
4. **ECR:** repository `from-code-to-cloud` → **Delete**.
5. **Security group:** EC2 → **Security Groups** → `cloudadhar-web-sg` → **Delete**.
6. **Logs:** CloudWatch → **Log groups** → `/ecs/from-code-to-cloud` → **Delete**.

✅ ECS clusters empty + ECR repositories empty = no bill.

---

## Roles used

| Role | Policy | Where |
|---|---|---|
| Your IAM user | `AdministratorAccess` | Step 0 |
| Task execution role | `AmazonECSTaskExecutionRolePolicy` | Step 5 → **Create new role** |
| Task role | none | Step 5 → leave empty |

No **Create new role** option in Step 5? IAM → **Roles** → **Create role** → **AWS service** → **Elastic Container Service** → **Elastic Container Service Task** → tick `AmazonECSTaskExecutionRolePolicy` → name `ecsTaskExecutionRole` → **Create**. Then pick it in Step 5.

---

## More

- **Problems?** [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md): Docker won't start, `aws login` errors, the task stops, the page won't open.
- **Optional pipeline:** [docs/PIPELINE.md](docs/PIPELINE.md): let GitHub Actions build, push and deploy for you (CI/CD with OIDC, no access keys).

---

MIT License. Free for learning and teaching. Please credit **CloudAdhar** when sharing.
**Follow CloudAdhar:** [YouTube](https://youtube.com/@cloudadhar) · [Instagram](https://instagram.com/cloudadhar) · [LinkedIn](https://linkedin.com/in/gangadharure)
