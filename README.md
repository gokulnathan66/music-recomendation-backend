### In this project we used function calling method by geminin API
### Running the Project Using Python and Docker

#### **Running the Project Normally with Python**
1. **Clone the Repository**  
   If you haven't already, clone the project repository:
   ```sh
   git clone https://github.com/gokulnathan66/music-recomendation-backend.git
   cd music-recomendation-backend
   ```

2. **Set Up a Virtual Environment (Optional but Recommended)**
   ```sh
   python -m venv venv
   source venv/bin/activate  # For macOS/Linux
   venv\Scripts\activate     # For Windows
   ```

3. **Install Dependencies**  
   Ensure you have `pip` installed, then install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**  
   Create a `.env` file in the project root and add the required variables:
   Use `.env.example`for declaring variables
   ```ini
   GEMINI_API_KEY="your-gemini-api-key"
   MUSIC_API_KEY="your-lastfm-api-key"
   MONGO_DB_CLUSTER_URL="your-mongodb-cluster-url"
   DB_NAME="your-database-name"
   FLASK_HOST=0.0.0.0
   FLASK_PORT=5000
   FLASK_DEBUG=False
   ```

5. **Run the Flask Application**  
   Start the server:
   ```sh
   python leader-follower/org_api.py
   ```

6. **Access the Application**  
   The API will be available at:  
   ```
   http://127.0.0.1:5000/
   ```

---

#### **Running the Project with Docker**
1. **Ensure Docker Is Installed**  
   If you haven't installed Docker, download and install it from [Docker's official website](https://www.docker.com/get-started/).
   Working with docker will be easy for deployment.

2. **Build the Docker Image**  
   Inside the project directory, run:
   ```sh
   docker build -t my-flask-app .
   ```

3. **Run the Docker Container**  
   ```sh
   docker run -d -p 5000:5000 --env-file .env --name flask_container my-flask-app
   ```
   - `-d`: Runs the container in detached mode (background).
   - `-p 5000:5000`: Maps port 5000 on the host to port 5000 in the container.
   - `--env-file .env`: Loads environment variables from the `.env` file.
   - `--name flask_container`: Names the container `flask_container`.
   - `my-flask-app`: The name of the built Docker image.

4. **Check Running Containers**  
   ```sh
   docker ps
   ```

5. **Stop the Container**  
   ```sh
   docker stop flask_container
   ```

6. **Restart the Container**  
   ```sh
   docker start flask_container
   ```

7. **Remove the Container (If Needed)**  
   ```sh
   docker rm flask_container
   ```

8. **Access the Application in Docker**  
   Open your browser or use Postman to access:  
   ```
   http://localhost:5000/
   ```

---

This should get your project up and running both in Python and Docker! 🚀 Let me know if you need further assistance.