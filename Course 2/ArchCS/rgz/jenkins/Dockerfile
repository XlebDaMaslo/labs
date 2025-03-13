FROM jenkins/jenkins:lts

USER root

RUN apt-get update && \
    apt-get install -y \
    curl \
    lsb-release \
    apt-transport-https \
    ca-certificates && \
    curl -fsSL https://get.docker.com -o get-docker.sh && \
    sh get-docker.sh && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* get-docker.sh

USER jenkins
