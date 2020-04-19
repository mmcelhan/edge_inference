sudo docker build -t inference -f Dockerfile.inference .
sudo docker run --rm -ti --network car --runtime=nvidia --name inference inference
