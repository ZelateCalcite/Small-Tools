git config --global --add http.proxy 127.0.0.1:7890
git config --global --add https.proxy 127.0.0.1:7890

git fetch
git pull

git config --global --unset-all http.proxy
git config --global --unset-all https.proxy

Pause
