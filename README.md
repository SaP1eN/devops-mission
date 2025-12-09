# 🚀 DevOps Mission: Automated Microservices Architecture

This project is a 3-tier microservices application deployed to AWS using a CI/CD pipeline. It demonstrates the move from "Code on Laptop" to "Production Cloud Architecture."

---

# 🏗️ The Architecture

We are not running a simple script. We are orchestrating a team of containers:

  _**1. Nginx (The Bodyguard):**_  Listens on Port 80. Blocks direct access to the backend. Forwards valid requests to Python.
  
  _**2. Python Flask (The Backend):**_  Listens on Port 5000 (Internal only). Handles logic and talks to the database.
  
  _**3. Redis (The Brain):**_  Stores the "Hit Counter" data. Uses AOF persistence so data survives restarts.
  
  _**4. Portainer (Mission Control):**_  A GUI to manage containers without using SSH.

---

# 💻 1. The "Cheat Sheet" (Commands I Need)
## Running Locally (On Laptop)

    Command	                          Description	          Why we use it
    
    docker compose up -d --build	  Start Everything	      -d runs in background. --build forces Python to update if code changed.
    
    docker compose ps	              Check Status	          Shows if containers are Up or Exit.
    
    docker compose logs -f	          Watch Logs	          Streams logs like a movie. Ctrl+C to stop watching.
    
    docker compose down	              Stop Everything	      Stops and removes containers (but keeps data).
    
    docker compose restart nginx	  Fix "Bad Gateway"	      Forces Nginx to refresh its DNS cache if Python IP changed.

## Emergency AWS Fixes (Inside SSH)

    Command	                              Description
    
    ssh -i "key.pem" ubuntu@<IP>	      Log into the remote server.
    
    sudo docker rm -f <container_name>	  Force kill a specific container (e.g., database-redis).
    
    git pull origin main	              Manually download the latest code to the server.

---

# 📂 2. Configuration Explained (The "Why")

### docker-compose.yml Secrets

#### 1. expose: "5000" vs ports: "5000:5000":
     
   -> We used expose for Python. This opens the port to Nginx only, not the outside internet. Secure!
  
   -> We used ports for Nginx (80:80) to let the public in.
  
#### 2. depends_on:
     
   -> Tells Docker: "Start the Database first, THEN Python. Start Python first, THEN Nginx." prevents crashes on startup.
   
#### 3. volumes: - redis_data:/data:
     
   -> Maps a folder on the Server (Host) to the Container. Without this, if the Redis container dies, our counter resets to 0.
  
### nginx/default.conf Secrets

#### 1. proxy_pass http://flask-app:5000;:
    
   -> Nginx doesn't know IPs. It uses the Service Name (flask-app) defined in docker-compose. Docker's internal DNS resolves this to the correct IP.

---

# 🚀 3. Automation (CI/CD Pipeline)

We don't deploy manually. The .github/workflows/ci.yml file does it:

**1. Trigger:** Happens on every git push.

**2. Secrets:** Uses HOST_IP and EC2_SSH_KEY (stored in GitHub Settings) to log in.

**3. The Logic:**
   
   -> SSH into AWS.
  
   -> git pull the latest docker-compose config.
  
   -> docker compose pull the latest images.
  
   -> docker compose up -d --build to smoothly swap old containers for new ones.

---

# 🛠️ 4. Troubleshooting Guide

### Problem: "502 Bad Gateway"

**1. Cause:** Nginx is running, but Python is dead OR Nginx has the wrong IP address for Python.
  
**2. Fix:** Check Python logs (docker compose logs flask-app). If Python is fine, restart Nginx (docker compose restart nginx).

### Problem: Counter resets to 1 after restart

**1. Cause:** The Volume link is broken, or Redis AOF is off.
   
**2. Fix:** Ensure command: redis-server --appendonly yes is in docker-compose.
  
### Problem: "Permission Denied" on AWS

**1. Cause:** You forgot sudo.

**2. Fix:** Run sudo docker compose ... or add user to docker group.
