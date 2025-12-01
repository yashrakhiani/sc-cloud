# ☁️ Deploying to Google Cloud (Free Tier)

This guide uses Google's **Always Free** `e2-micro` instance.

---

## 1. Create the Server
1.  Go to [Google Cloud Console](https://console.cloud.google.com/).
2.  Select your project: **avian-chariot-479711-r6**.
3.  Go to **Compute Engine** > **VM Instances**.
4.  Click **Create Instance**.
5.  **Important Settings for Free Tier:**
    *   **Region:** Choose `us-central1`, `us-west1`, or `us-east1` (Only these are free).
    *   **Machine Type:** `e2-micro` (2 vCPU, 1 GB memory).
    *   **Boot Disk:** Change to **Ubuntu 22.04 LTS**. Increase size to **30 GB** (Standard persistent disk).
6.  **Firewall:** Allow HTTP/HTTPS traffic.
7.  Click **Create**.

---

## 2. Connect & Setup Swap (Crucial!)
Since this server only has 1GB RAM, we **MUST** create "Swap Memory" (fake RAM on the hard drive) or Chrome will crash.

1.  Click **SSH** next to your instance in the Google Console.
2.  Run these commands to add 2GB of Swap:

```bash
# Create a 2GB swap file
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

---

## 3. Install Docker

```bash
# Update and install Docker
sudo apt-get update
sudo apt-get install -y docker.io
sudo usermod -aG docker $USER
newgrp docker
```

---

## 4. Upload Code & Run
(Same as before)

1.  **Upload Code:**
    *   Click the **Gear Icon** in the SSH window > **Upload File**.
    *   Upload your project folder (zip it first on your PC, upload, then `unzip`).

2.  **Configure .env:**
    ```bash
    cd structcrew_leadgen
    nano .env
    # Paste your settings
    ```

3.  **Run:**
    ```bash
    docker build -t structcrew-bot .
    docker run -d --name leadgen --restart unless-stopped -v $(pwd)/data:/app/data structcrew-bot
    ```

---

## ✅ Done!
Your bot is now running on Google Cloud.
