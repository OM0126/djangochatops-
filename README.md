# Django ChatOps – DevOps Project

## About the Project

Django ChatOps is a chat application built using Python and Django.

I created this project to learn how DevOps works in real projects. Instead of only building a web application, I also worked on running it inside Docker containers, managing it with Kubernetes, and checking its performance using monitoring tools.

The main aim of this project is to understand how developers build, run, manage and monitor an application.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Django | Backend framework |
| HTML and CSS | Frontend |
| Git and GitHub | Store and manage code |
| Docker | Create application containers |
| Docker Hub | Store Docker images |
| GitHub Actions | Automate testing and image building |
| Kubernetes | Manage application containers |
| Minikube | Run Kubernetes locally |
| Helm | Install monitoring tools |
| Prometheus | Collect system metrics |
| Grafana | Display metrics and alerts |

## How the Project Works

This is the basic flow of my project:

```text
Developer
    |
    v
  GitHub
    |
    v
GitHub Actions
    |
    v
Run Django Tests
    |
    v
Build Docker Image
    |
    v
Push Image to Docker Hub
    |
    v
Kubernetes (Minikube)
    |
    v
Run Multiple Pods
    |
    v
Horizontal Pod Autoscaler
    |
    v
Prometheus
    |
    v
Grafana Dashboard
```

## 1. Django Application

I developed a chat application using Django and Python.

Some of the work includes:

- Creating the Django project.
- Creating the chat application.
- Working with Django models and views.
- Connecting the application with its database.
- Creating a health-check URL to check whether the application is running.

Health-check URL:

```text
/health/
```

## 2. Docker

I used Docker to run the Django application inside a container.

### Build Docker Image

Run this command from the repository root:

```bash
docker build -t chatops:latest ./djangochat
```

### Check Docker Images

```bash
docker images
```

### Run the Container

```bash
docker run -d --name chatops -p 8000:8000 chatops:latest
```

### Check Running Containers

```bash
docker ps
```

### Check All Containers

```bash
docker ps -a
```

### Check Container Logs

```bash
docker logs chatops
```

### Enter the Container

```bash
docker exec -it chatops bash
```

### Stop and Remove the Container

```bash
docker stop chatops
docker rm chatops
```

### Docker Hub

I pushed my Docker image to Docker Hub.

Repository: [om0126/chatops](https://hub.docker.com/r/om0126/chatops)

Pull the image:

```bash
docker pull om0126/chatops:latest
```

## 3. GitHub Actions – CI/CD

I created a GitHub Actions workflow to automate the testing and Docker image publishing process.

The workflow file is:

```text
.github/workflows/django-ci.yml
```

### What happens in the pipeline?

1. GitHub Actions starts when code is pushed to the main branch or a pull request is created.
2. It downloads the project code.
3. It installs Python and the required packages.
4. It checks the Django project.
5. It applies database migrations.
6. It runs Django tests.
7. If the tests pass, it builds the Docker image.
8. It pushes the image to Docker Hub.

I also configured two Docker image tags:

- `latest`
- Git commit SHA

This helps me identify which version of the code was used to build an image.

## 4. Kubernetes with Minikube

I used Minikube to run Kubernetes on my local system.

Kubernetes helps manage application containers and keeps the required number of application replicas running.

### Start Minikube

```bash
minikube start --driver=docker
```

### Check Minikube Status

```bash
minikube status
```

### Check Kubernetes Nodes

```bash
kubectl get nodes
```

### Check Kubernetes Cluster Information

```bash
kubectl cluster-info
```

### Check Pods

```bash
kubectl get pods
```

### Check Pods in All Namespaces

```bash
kubectl get pods -A
```

### Check Services

```bash
kubectl get services
```

### Check Deployments

```bash
kubectl get deployments
```

### Check ReplicaSets

```bash
kubectl get replicasets
```

### Check HPA

```bash
kubectl get hpa
```

### Deploy the Application

My Kubernetes YAML files are stored inside the `k8s` folder.

Apply the deployment:

```bash
kubectl apply -f k8s/deployment.yaml
```

Apply the service:

```bash
kubectl apply -f k8s/service.yaml
```

Apply the HPA:

```bash
kubectl apply -f k8s/hpa.yaml
```

### Check Deployment Details

```bash
kubectl describe deployment chatops-deployment
```

### Check Pod Details

```bash
kubectl describe pod <pod-name>
```

### Check Pod Logs

```bash
kubectl logs <pod-name>
```

### Follow Pod Logs

```bash
kubectl logs -f <pod-name>
```

### Enter a Running Pod

```bash
kubectl exec -it <pod-name> -- /bin/sh
```

### Check Resource Usage

```bash
kubectl top nodes
kubectl top pods
```

### Watch Pods in Real Time

```bash
kubectl get pods -w
```

### Scale the Deployment Manually

```bash
kubectl scale deployment chatops-deployment --replicas=3
```

### Delete a Deployment

```bash
kubectl delete deployment chatops-deployment
```

### Delete a Service

```bash
kubectl delete service chatops-service
```

### Delete HPA

```bash
kubectl delete hpa chatops-hpa
```

## 5. Kubernetes Auto Scaling – HPA

I configured Horizontal Pod Autoscaling (HPA) to increase or decrease the number of application pods based on CPU usage.

My current HPA configuration:

| Setting | Value |
|---|---:|
| Minimum Pods | 2 |
| Maximum Pods | 5 |
| Target CPU Usage | 50% |

### Check HPA Status

```bash
kubectl get hpa
```

### Get Detailed HPA Information

```bash
kubectl describe hpa chatops-hpa
```

### Watch HPA Changes

```bash
kubectl get hpa -w
```

### Generate Test Traffic

I used a BusyBox container to send repeated requests to the application health-check URL.

```bash
kubectl run load-generator \
  --image=busybox:1.36 \
  --restart=Never \
  -- /bin/sh -c 'while true; do wget -q -O- http://chatops-service:8000/health/ >/dev/null; done'
```

Check the load-generator pod:

```bash
kubectl get pods
```

Remove the load-generator after testing:

```bash
kubectl delete pod load-generator
```

I used this test to observe how Kubernetes HPA increases the number of application pods when CPU usage increases.

## 6. Monitoring with Prometheus and Grafana

I installed Prometheus and Grafana using Helm.

These tools help me understand what is happening inside my Kubernetes cluster.

Prometheus collects metrics, and Grafana displays those metrics in dashboards.

### Add Prometheus Helm Repository

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
```

### Update Helm Repositories

```bash
helm repo update
```

### Create Monitoring Namespace

```bash
kubectl create namespace monitoring
```

### Install Prometheus and Grafana

```bash
helm install monitoring prometheus-community/kube-prometheus-stack \
  --version 92.17.1 \
  -n monitoring
```

### Check Helm Releases

```bash
helm list -n monitoring
```

### Check Monitoring Pods

```bash
kubectl get pods -n monitoring
```

### Check Monitoring Services

```bash
kubectl get services -n monitoring
```

### Upgrade Monitoring Configuration

During installation, I faced an issue with the Prometheus Operator TLS configuration. I fixed it using:

```bash
helm upgrade monitoring prometheus-community/kube-prometheus-stack \
  --version 92.17.1 \
  -n monitoring \
  --reuse-values \
  --set prometheusOperator.tls.enabled=false
```

### Access Grafana

Run:

```bash
kubectl port-forward svc/monitoring-grafana 3000:80 -n monitoring
```

Open:

```text
http://localhost:3000
```

### Get Grafana Admin Password

```bash
kubectl get secret monitoring-grafana -n monitoring \
  -o jsonpath="{.data.admin-password}" | base64 -d; echo
```

### Access Prometheus

Run:

```bash
kubectl port-forward svc/monitoring-kube-prometheus-prometheus 9090:9090 -n monitoring
```

Open:

```text
http://localhost:9090
```

### Metrics I Monitored

- Application CPU usage.
- Application memory usage.
- Number of running pods.
- Current HPA replicas.
- Desired HPA replicas.
- HPA health conditions.

### Grafana Alerts

I also created alerts in Grafana for:

1. High CPU usage.
2. Application pods becoming unavailable.

These alerts help identify problems in the application.

## 7. Useful Kubernetes Troubleshooting Commands

These commands are useful when something does not work properly.

### Check All Resources

```bash
kubectl get all
```

### Check Events

```bash
kubectl get events --sort-by=.metadata.creationTimestamp
```

### Check Pod Information

```bash
kubectl describe pod <pod-name>
```

### Check Logs of a Previous Container

```bash
kubectl logs <pod-name> --previous
```

### Check a Particular Namespace

```bash
kubectl get all -n monitoring
```

### Restart Deployment

```bash
kubectl rollout restart deployment/chatops-deployment
```

### Check Deployment Rollout Status

```bash
kubectl rollout status deployment/chatops-deployment
```

### Check Deployment History

```bash
kubectl rollout history deployment/chatops-deployment
```

## 8. Project Folder Structure

```text
djangochatops-/
│
├── .github/
│   └── workflows/
│       └── django-ci.yml
│
├── djangochat/
│   ├── chat/
│   ├── djangochat/
│   ├── templates/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── manage.py
│
├── k8s/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── hpa.yaml
│
├── monitoring/
│   └── values.yaml
│
└── README.md
```

## 9. What I Learned

While working on this project, I learned:

- How to build and run a Django application.
- How to create Docker images and containers.
- How to push Docker images to Docker Hub.
- How to create a CI/CD pipeline using GitHub Actions.
- How to deploy applications using Kubernetes.
- How to manage pods, deployments and services.
- How to configure Kubernetes auto-scaling.
- How to install tools using Helm.
- How to monitor Kubernetes using Prometheus and Grafana.
- How to create alerts and check application performance.

## 10. Future Improvements

I plan to improve this project by:

- Connecting PostgreSQL to the application.
- Improving the CI/CD pipeline.
- Adding better application monitoring.
- Improving logging and alerting.
- Performing more load and performance tests.
- Exploring cloud deployment after completing the local setup.

## Author

**OM0126**

GitHub: [https://github.com/OM0126](https://github.com/OM0126)

Docker Hub: [https://hub.docker.com/u/om0126](https://hub.docker.com/u/om0126)

---

*This project is part of my hands-on learning journey in DevOps, Docker, Kubernetes and Cloud technologies.*
