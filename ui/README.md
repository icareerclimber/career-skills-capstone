# ICareers UI
## Project structure
- templates/index.html is used for render_template
- static/index.js and style.css is used for send_static_file

## Running locally (Without docker)
### Prereqs
- Python 3.6
- Pip package manager
- From the ui directory, install prereq packages
```
pip install -r requirements.txt
```
### Instructions
To use flask server on local machine, from the ui directory:
```
export FLASK_APP=server.py
export FLASK_ENV=development
flask run
```
Then point web browser to localhost:5000

## Docker instructions:
### Requirements
Have the following installed in your local environment:

- docker
  - https://docs.docker.com/install/
- docker-compose
  - https://docs.docker.com/compose/install/

### Instructions

To build container and try locally

```
cd ui directory
docker build -t flask-ui -f Dockerfile .
docker run -it -p 5000:5000 flask-ui

Then point web browser to localhost:5000
```
#### Docker compose
From the ui root directory run:
```
docker-compose up -d
```
To force a rebuild of the container:
```
docker-compose up -d --build
```

#### Verify installation

Check that the application is working by navigating in the browser to `localhost:5000`

#### To stop the application
From the resume-assistant root direction run:
```
docker-compose down
```

## Deploying to cloud
Instructions based on tutorial found here https://cloud.google.com/kubernetes-engine/docs/tutorials/hello-app
### Prereqs
- Have GCloud SDK installed: https://cloud.google.com/sdk/docs/quickstarts
- Install Kubernetted command line tool
```
gcloud components install kubectl
```
- Make sure default project and compute zone are set
```
gcloud config set project <PROJECT_ID>
gcloud config set compute/zone <COMPUTE_ZONE>
```
### Instructions
1. Set the PROJECT_ID environment variable
```
export PROJECT_ID="$(gcloud config get-value project -q)"
```
2. Build image
```
docker build -t gcr.io/${PROJECT_ID}/icareers-ui .
```
3. Upload image
```
gcloud docker -- push gcr.io/${PROJECT_ID}/icareers-ui
```
4. Test running image locally (optional)
```
docker run --rm -p 5000:5000 gcr.io/${PROJECT_ID}/icareers-ui
curl http://localhost:5000
```
5. Create container cluster (this will take a few minutes)
```
gcloud container clusters create icareers-cluster --num-nodes=1
```
6. Deploy application
```
kubectl run icareers-ui --image=gcr.io/${PROJECT_ID}/icareers-ui --port 8081 
```
7. Expose application on internet
```
kubectl expose deployment icareers-ui --type=LoadBalancer --port 80 --target-port 8081
```
8. Wait for service to become available, External-IP field will be populated in output from following call when the service is available
```
kubectl get service
```
9. Navigate broswer to service's external IP address.

### Cleanup
The following steps will tear down your Kubernettes cluster
1. Stop the service
```
kubectl delete service icareers-ui
```
2. Wait for service to be removed by monitoring the output of the following command
```
gcloud compute forwarding-rules list
```
3. Remove cluster
```
gcloud container clusters delete icareers-cluster
```

### Upgrade
The following steps will deploy a newly-built container.
1. Stop the service
```
kubectl delete service icareers-ui
```
2. Remove deployment
```
kubectl delete deployment icareers-ui
```
3. Build new image (with a different version)
```
docker build -t gcr.io/${PROJECT_ID}/icareers-ui:0.2 .
```
4. Upload image
```
gcloud docker -- push gcr.io/${PROJECT_ID}/icareers-ui:0.2
```
5. Deploy application
```
kubectl run icareers-ui --image=gcr.io/${PROJECT_ID}/icareers-ui:0.2 --port 8081
```
6. Expose application on internet
```
kubectl expose deployment icareers-ui --type=LoadBalancer --port 80 --target-port 8081
```
7. Wait for service to become available, External-IP field will be populated in output from following call when the service is available
```
kubectl get service
```
8. Navigate broswer to service's external IP address.

