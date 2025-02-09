# Docker Image

## Docker Installation

Follow these steps to install Docker on your system:

1. **Update your package index:**
   ```bash
   sudo apt update
   ```

2. **Install required packages:**
   ```bash
   sudo apt install apt-transport-https ca-certificates curl software-properties-common
   ```

3. **Add Docker's official GPG key:**
   ```bash
   curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
   ```

4. **Set up the Docker repository:**
   ```bash
   echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
   ```

5. **Update your package index again:**
   ```bash
   sudo apt update
   ```

6. **Check available Docker versions:**
   ```bash
   apt-cache policy docker-ce
   ```

7. **Install Docker:**
   ```bash
   sudo apt install docker-ce
   ```

8. **Verify Docker is running:**
   ```bash
   sudo systemctl status docker
   ```

9. **Allow non-root users to manage Docker:**
   ```bash
   sudo usermod -aG docker ${USER}
   ```

   Restart your terminal or log out and log back in to apply the changes.
