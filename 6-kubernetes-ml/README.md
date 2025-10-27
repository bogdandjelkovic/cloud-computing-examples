```bash
# for delete 
kubectl delete all --all -n bogdan
kubectl delete pvc --all -n bogdan
kubectl delete configmap --all -n bogdan

# creating namespace
kubectl create namespace bogdan

# for creating configmap
kubectl create configmap wine-csv-config --from-file=wine-quality-white-and-red.csv -n bogdan
kubectl get configmap -n bogdan
kubectl describe configmap wine-csv-config -n bogdan

# apply all yaml files
kubectl apply -f . -n bogdan

# get
kubectl get all -n bogdan
kubectl get pods -n bogdan
kubectl get nodes -o wide

# describe
kubectl describe pod wine-ml-85b998d7c6-fpz4k -n bogdan

# test api

```