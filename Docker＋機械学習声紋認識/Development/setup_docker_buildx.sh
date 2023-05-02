#!/usr/bin/env bash
# 必要なパッケージ
sudo apt-get install -y qemu qemu-user-static binfmt-support debootstrap

# linuxではbuildxランタイムの手動インストールが必要
# 参考: https://docs.docker.com/buildx/working-with-buildx/
mkdir -p ~/.docker/cli-plugins/
cd ~/.docker/cli-plugins/ || exit
wget https://github.com/docker/buildx/releases/download/v0.6.3/buildx-v0.6.3.linux-amd64
mv buildx-v0.6.3.linux-amd64 docker-buildx
chmod a+x ~/.docker/cli-plugins/docker-buildx

sudo cp /etc/docker/daemon.json /etc/docker/daemon.json.backup$(date '+%Y%m%d_%H%M%S')
echo '{"experimental":true}' | sudo tee /etc/docker/daemon.json
sudo systemctl restart docker