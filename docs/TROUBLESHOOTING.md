# Troubleshooting

Back to the [workshop guide](../README.md).

## Common errors

| Problem | Fix |
|---|---|
| `docker: command not found` | **Mac:** Docker was opened from the installer disk. Quit it, drag **Docker.app** into **Applications**, eject the Docker disk, open Docker from Applications. **Windows:** restart VS Code (or the laptop) after installing |
| `Cannot connect to the Docker daemon` / `error during connect` | Docker Desktop isn't running. Open it and wait for **Engine running** |
| Docker Desktop won't start | See [Docker Desktop won't start?](#docker-desktop-wont-start) below. Still stuck after 3 minutes? Switch to **AWS CloudShell** |
| `aws: command not found` or `Invalid choice: 'login'` | Install or update the AWS CLI to **2.32 or newer**, then restart VS Code |
| `Unable to locate credentials` | Run `aws login` again (it lasts up to 12 hours) |
| `aws login`: *Profile 'default' is already configured with Access Key credentials* | Old access keys are saved on your laptop. Sign in under a new profile instead: `aws login --profile workshop --region ap-south-1`, then `export AWS_PROFILE=workshop` (Windows PowerShell: `$env:AWS_PROFILE="workshop"`). Run the `export` again in every new terminal |
| `The security token included in the request is invalid` | Same cause: old access keys. Use the `--profile workshop` fix above |
| `zsh: command not found: #` (Mac) | You pasted a comment line. Paste only the command lines |
| `no basic auth credentials` on `docker push` | Run the `aws ecr get-login-password ... docker login` line again |
| `repository ... does not exist` on push | The repo name, account ID or region doesn't match. It must be `from-code-to-cloud` in **ap-south-1** |
| `429 Too Many Requests` / `toomanyrequests` when building | Too many anonymous downloads of the base image from your network. Sign Docker in to ECR Public, then build again: `aws ecr-public get-login-password --region us-east-1 \| docker login --username AWS --password-stdin public.ecr.aws` |
| Port `8080` already in use on your laptop | Run `docker ps`, then `docker stop` and `docker rm` the old container |
| Task stops with `exec format error` | The image was built for ARM (Apple chip). Rebuild with `--platform linux/amd64` and push again |
| Task stops with `CannotPullContainerError` | **Public IP** was off, or the Image URI is wrong. Check the URI ends in `:v1`, and recreate the service with Public IP **Turned on** |
| Task stops with `ResourceInitializationError` | Same as above: usually no public IP, so the task can't reach ECR |
| Browser keeps loading / times out | Use `http://` (not https) and port `:8080`. Check the security group allows **TCP 8080** from **Anywhere** |
| Page shows `Application version: v1` after deploying v2 | The service still uses the old revision, or you pushed v2 to a different tag. Check the task's image URI ends in `:v2` |
| Task status is **Pending** for a long time | Wait 2 minutes. Still pending? Open the task → **Stopped reason** |
| Can't delete the cluster | The service still has tasks. Delete the service first and wait until the tasks stop |
| Can't delete the security group | A task is still using it. Wait until all tasks have stopped |

---

## Docker Desktop won't start?

Try these in order. Give it **3 minutes**, then switch to **AWS CloudShell** ([README → Before you start](../README.md#before-you-start)). You can still do the whole workshop.

**Any laptop**
1. Quit Docker Desktop and open it again. The first start can take **2 minutes**: wait for **Engine running**.
2. Restart the laptop.
3. Check free disk space: Docker needs about **10 GB** free.
4. Docker Desktop → **Troubleshoot** (bug icon, top right) → **Restart Docker Desktop**. Still stuck? **Reset to factory defaults** in the same menu.

**Mac**
| You see | Do this |
|---|---|
| `docker: command not found` | Docker was opened from the installer disk. Quit it, drag **Docker.app** into **Applications**, eject the Docker disk, open Docker from Applications, restart VS Code |
| Stuck on **Docker Desktop is starting…** | Quit it → open again → **Troubleshoot** → **Clean / Purge data** |
| "This version of macOS is not supported" | Docker Desktop needs a recent macOS. Use AWS CloudShell |

**Windows**
| You see | Do this |
|---|---|
| **WSL 2 installation is incomplete** / WSL needs updating | PowerShell **as administrator**: `wsl --install`, then `wsl --update`. Restart |
| **Virtualization support not detected** | Turn on virtualization in the BIOS (*Intel VT-x* or *AMD-V/SVM*). In **Turn Windows features on or off**, tick **Virtual Machine Platform** and **Windows Subsystem for Linux**. Restart |
| **Unexpected WSL error** | PowerShell: `wsl --shutdown`, then open Docker Desktop again |
| No admin rights (college or office laptop) | You can't install Docker. Use AWS CloudShell |
