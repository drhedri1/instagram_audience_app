# Instagram Audience Analysis App - Deployment Guide

This guide provides instructions for deploying the Instagram Audience Analysis application using Docker and Docker Compose, suitable for environments like a DigitalOcean Droplet.

## Prerequisites

1.  **DigitalOcean Account**: You need an account to create a Droplet (or use another cloud provider/server).
2.  **Docker & Docker Compose**: Install Docker Engine and Docker Compose on your server (Droplet). Follow the official Docker installation guides for your server's operating system.
3.  **Git**: Install Git on your server to clone the application repository.
4.  **Domain Name (Optional)**: If you want to use a custom domain, configure its DNS records to point to your server's IP address.
5.  **New Instagram API Credentials**: You **must** generate new API credentials (App ID, App Secret) in your Instagram Developer account, as the ones shared previously are compromised. Configure the correct Redirect URI in your Instagram App settings (e.g., `http://yourdomain.com/api/auth/instagram/callback` or `http://<server_ip>/api/auth/instagram/callback`).
6.  **Strong JWT Secret Key**: Generate a strong, random secret key for JWT signing.

## Deployment Steps

1.  **SSH into your Server**:
    Connect to your DigitalOcean Droplet (or other server) via SSH.

2.  **Clone the Application Repository**:
    ```bash
    git clone <your-repository-url> instagram-audience-app
    cd instagram-audience-app
    ```
    (Replace `<your-repository-url>` with the actual URL where the code is hosted).

3.  **Configure Environment Variables**:
    Navigate to the `server` directory and create a `.env` file by copying the example or creating a new one:
    ```bash
    cd server
    # cp .env.example .env # If you have an example file
    # nano .env # Or use another editor
    ```
    Populate the `.env` file with your actual credentials. **Do not commit this file to Git.**

    ```dotenv
    # Database Configuration (Defaults match docker-compose, change if needed)
    # DB_HOST=db # Handled by docker-compose
    # DB_PORT=3306 # Handled by docker-compose
    # DB_USERNAME=root # Handled by docker-compose
    DB_PASSWORD=your_strong_mysql_root_password # Set a strong password here
    DB_NAME=mydb # Or your preferred database name

    # Instagram API Credentials (Replace with YOUR NEW credentials)
    INSTAGRAM_APP_ID=YOUR_NEW_INSTAGRAM_APP_ID
    INSTAGRAM_APP_SECRET=YOUR_NEW_INSTAGRAM_APP_SECRET
    INSTAGRAM_REDIRECT_URI=http://yourdomain.com/api/auth/instagram/callback # IMPORTANT: Use your actual domain/IP and ensure it matches Instagram settings

    # JWT Secret Key (Generate a strong random key)
    JWT_SECRET_KEY=your_very_strong_random_secret_key_here

    # Flask specific (Optional - defaults are usually fine)
    # FLASK_APP=src/main.py
    # FLASK_DEBUG=0 # Should be 0 for production
    ```
    *   Replace placeholders with your actual **new** Instagram credentials, your chosen database password, and a generated JWT secret key.
    *   Ensure `INSTAGRAM_REDIRECT_URI` matches exactly what you configured in the Instagram Developer dashboard and uses `http` or `https` based on your setup.

4.  **Build and Run with Docker Compose**:
    Navigate back to the project root directory (where `docker-compose.yml` is located) and run:
    ```bash
    cd .. # Go back to the instagram-audience-app directory
    docker-compose up --build -d
    ```
    *   `--build`: Forces Docker to rebuild the images based on the Dockerfiles.
    *   `-d`: Runs the containers in detached mode (in the background).

5.  **Access the Application**:
    Once the containers are running, you should be able to access the application in your web browser:
    *   If using an IP address: `http://<your_server_ip>`
    *   If using a domain: `http://yourdomain.com`

    The Nginx container (frontend) listens on port 80 and proxies API requests or serves the React app.

## Important Notes

*   **Database Persistence**: The `docker-compose.yml` uses a named volume (`mysql_data`) to persist MySQL data even if the container is removed and recreated. Ensure your server has sufficient disk space.
*   **HTTPS/SSL**: For production, it is highly recommended to use HTTPS. You can:
    *   Use a reverse proxy like Nginx or Caddy *outside* Docker (or in another container) to handle SSL termination and proxy requests to the `frontend` container on port 80.
    *   Use DigitalOcean Load Balancers with SSL termination.
    *   Modify the `frontend` service in `docker-compose.yml` and its Nginx configuration to handle HTTPS directly (more complex).
    *   If using HTTPS, update `INSTAGRAM_REDIRECT_URI` to use `https`.
*   **Firewall**: Ensure your server's firewall (e.g., `ufw` on Ubuntu, or DigitalOcean Cloud Firewalls) allows traffic on port 80 (HTTP) and potentially port 443 (HTTPS).
*   **Monitoring & Logging**: Check container logs using `docker-compose logs backend` or `docker-compose logs frontend`.
*   **Stopping**: To stop the application, run `docker-compose down` in the project directory.

## Troubleshooting

*   **Permissions**: Ensure Docker has the necessary permissions to run and manage volumes.
*   **Port Conflicts**: If port 80 or 5000 is already in use on your server, adjust the `ports` mapping in `docker-compose.yml` (e.g., `"8080:80"`) and access the app via the new port.
*   **Database Connection Issues**: Check the `backend` container logs (`docker-compose logs backend`). Ensure the `DB_HOST` is set to `db` (the service name in `docker-compose.yml`) and credentials in the `.env` file match the database setup.
*   **Instagram Callback Errors**: Double-check that the `INSTAGRAM_REDIRECT_URI` in your `.env` file exactly matches the one configured in your Instagram App settings, including `http` vs `https`. Check `backend` logs for specific OAuth errors.

