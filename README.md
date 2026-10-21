# StudentAi – Student Performance Study

## 1. Project Overview

StudentAi is a machine learning web application built using Streamlit. It estimates students' final mathematics grades based on their background, study habits, and school-related factors.

This project demonstrates Continuous Integration and Continuous Deployment (CI/CD) using Jenkins, Docker, Docker Hub, Kubernetes, and Minikube on an AWS EC2 Ubuntu server.

## 2. Technology Stack

- **Programming Language:** Python
- **Frontend:** Streamlit
- **Machine Learning:** scikit-learn
- **Data Processing:** Pandas, NumPy
- **Testing:** Pytest
- **CI/CD:** Jenkins
- **Containerization:** Docker
- **Container Registry:** Docker Hub
- **Orchestration:** Kubernetes and Minikube
- **Cloud Platform:** AWS EC2

## 3. Project Structure

```text
cca2-cicd/
├── app.py
├── data/
│   └── student-mat.csv
├── test_app.py
├── requirements.txt
├── Dockerfile
├── Jenkinsfile
└── k8s/
    ├── deployment.yaml
    └── service.yaml
```

## 4. CI/CD Pipeline

The Jenkins pipeline automates the following stages:

1. **Checkout:** Retrieves the source code from GitHub.
2. **Build Docker Image:** Creates a Docker image of the application.
3. **Run Tests:** Executes automated tests using Pytest.
4. **Push to Docker Hub:** Publishes the versioned image and the `latest` tag.
5. **Deploy to Kubernetes:** Deploys the application using Kubernetes manifests.
6. **Verify Deployment:** Checks the deployment rollout and Kubernetes resources.

## 5. Run the Application Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the Streamlit application:

```bash
streamlit run app.py
```

## 6. Run Using Docker

Build the image:

```bash
docker build -t studentai:latest .
```

Run the container:

```bash
docker run --rm -p 8501:8501 studentai:latest
```

Open `http://localhost:8501` in a browser.

## 7. Automated Testing

Run the test suite with:

```bash
python -m pytest -v
```

The tests verify that the dataset loads correctly and that the Streamlit application starts without errors.

## 8. Kubernetes Deployment

The Kubernetes configuration files are stored in the `k8s/` directory. Jenkins applies the manifests and waits for the deployment rollout to complete.

The application uses port `8501`, and the Kubernetes Service is configured to expose the application within the cluster through a NodePort.

## 9. Version 2.0 and CI/CD Demonstration

Version 2.0 adds a visible version caption to the application. This change demonstrates how a source-code update can be committed to GitHub and deployed through the Jenkins CI/CD pipeline.

## 10. Project Links

- **GitHub Repository:** https://github.com/arjundhure/cca2-cicd
- **Docker Hub Repository:** https://hub.docker.com/r/arjun1254/studentai
