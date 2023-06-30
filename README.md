# flask-assignment
Note: This repository contains flask application cloned from https://github.com/LintangWisesa/CRUD_Flask_PostgreSQL
However this additionally includes requirements.txt and the code for generating DB tables automatically when the application runs to avoid manual table creation step mentioned in README.md of above repository. Dockerfile in the root repository bundles the application source code with its dependencies. 

Steps for Kubernetes deployment

1. Connect to your Kubernetes cluster(Set KUBECONFIG enveronment variable to the kubeconfig file path)
    Note: I used GKE cluster created manually from GCP console and followed [this](https://porter.sh/best-practices/gke/#generate-a-kubeconfig) documentation for obtaining kubeconfig file. Alternatively it can also be generated using gcloud as mentioned in [this](https://cloud.google.com/kubernetes-engine/docs/how-to/creating-an-autopilot-cluster) documentation.
2. Run `kubectl cluster-info` and ensure that you have connected to right cluster.
3. Run `kubectl apply -f kubernetes_deployments` (kubernetes_deployments directory contains all the yaml files  required for creating deployments and services)
4. Run `kubectl port-forward service/flask-service 8081:80 -n ananthesh-test`
5. Open http://localhost:8081 in browser, which will render home.html inside templates file.
6. Make below POST curl call to add data to database
     `curl -X POST -H 'Content-Type: application/json' -d "{\"name\":\"Ananthesh\", \"age\":\"27\"}" http://localhost:8081/data`
7. Make below GET curl call to get the data from databse
    `curl -X GET -H 'Content-Type: application/json' http://localhost:8081/data`

The Docker image of Flask application is availabe at docker.io/ananthesh30/flask_test:1.0.0-ananthesh




