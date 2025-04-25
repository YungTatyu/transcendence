# transcendence
A web-based multiplayer Pong tournament application that allows players to compete in real-time matches. The application is built using a microservices architecture and ensures high security, performance, and scalability.

## Running Locally
### 1. Update `/etc/hosts`
Add the following entry to your `/etc/hosts` file to map required domains:
```
127.0.0.1   www.transcen.com auth-proxy.transcen.com game-proxy.transcen.com match-proxy.transcen.com friends-proxy.transcen.com friends-activity-proxy.transcen.com tournament-proxy.transcen.com user-proxy.transcen.com
```

### 2. Clone and Generate Certificates
Run the following commands to clone the project and generate SSL certificates:
```bash
git clone https://github.com/YungTatyu/transcendence.git
cd transcendence
./certs/create_all_certs.sh
```
Then, import the `./certs/ca.crt` file into your browser’s certificate store to enable HTTPS connections.

### 3. Build the Project
Execute the following command to build and launch the application:
```bash
make
```
### 4. Access the Application
Once the setup is complete, open your browser and navigate to:  
**[https://www.transcen.com/](https://www.transcen.com/)**

### 5. Set Up GitHub OAuth Application(If you want to monitor with grafana)
Visit GitHub Developer Settings.  
Click on New OAuth App.  
Fill in the fields as follows:
```
Application Name: Choose a name of your choice.
Homepage URL: https://localhost:3000
Authorization Callback URL: https://localhost:3000/login/github
```
After registering the application, note down the Client ID and Client Secret.  
Add the Client ID and Client Secret to the docker_env/grafana.env environment file.  
Go to https://localhost:3000/login and log in with your GitHub account.  
(If you want to publish grafana externally, please change localhost to your domain name.)

### 6. Set Up Alerts with Prometheus(If you want to receive alerts on Discord)
Go to the Edit Channel page in your Discord server.  
Navigate to Integrations and click on Webhooks.  
Create a new webhook and copy the generated URL.  
Paste the copied URL into the `docker_env/alert.url` file.
