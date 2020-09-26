echo "=======Building the cclookup image from the Dockerfile======="
docker build -t grajappan4401/cclookup:latest .
echo "=======Pushing the image to my docker hub public repo grajappan4401/cclookup======="
docker push grajappan4401/cclookup:latest
echo "=======Installing Minikube======="
brew install minikube
echo "=======Starting the minikube cluster====="
minikube start --vm-driver=virtualbox
echo "=======Install kubectl in local machine======"
brew install kubectl
echo "=======Set kubeconfig context to minikube====="
kubectl config set-context minikube
echo "=======Deploying the cclookup API========"
kubectl create -f cclookup.yaml
echo "========Waiting for a minute and a half the POD to comeup====="
sleep 90
echo "========Forwarding the requests on localhost to the cclookup pod listening on minikube======"
kubectl get pods -l app=cclookup -o name | sed 's/^.*\///' | xargs -I{} kubectl port-forward {} 4080:4080 > /dev/null 2>&1 &
echo "======Testing the cclookup API======="
curl -s localhost:4080/health
curl -X post localhost:4080/convert/AU
curl localhost:4080/diag
echo "If curl fails please check whether the pod is running and the port forwarding is working using netstat -an | grep 4080"

