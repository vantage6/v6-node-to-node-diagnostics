#!/bin/sh

IMAGE=$1

echo $IMAGE

docker build -t $IMAGE .

docker push $IMAGE