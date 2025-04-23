# transcendence
A web-based multiplayer Pong tournament application that allows players to compete in real-time matches. The application is built using a microservices architecture and ensures high security, performance, and scalability.

## Running Locally
### 1. Update `/etc/hosts`
Add the following entry to your `/etc/hosts` file to map required domains:
```
127.0.0.1   www.transcen.com auth-proxy.transcen.com game-proxy.transcen.com match-proxy.transcen.com friends-proxy.transcen.com friends-activity-proxy.transcen.com tournament-proxy.transcen.com user-proxy.transcen.com grafana
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
