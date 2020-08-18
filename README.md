# fed-image-watcher

```sh
fedora-messaging --conf config.toml consume --callback-file=./tcallback/t.py:SaveMessage --routing-key org.fedoraproject.prod.pungi.compose.status.change
```

```
https://apps.fedoraproject.org/datagrepper/raw?rows_per_page=1&delta=127800&topic=org.fedoraproject.prod.pungi.compose.status.change
```

```
docker run -it quay.io/mgugino.redhat/fed-image-watcher:master fedora-messaging --conf config.toml consume --callback-file=./tcallback/t.py:SaveMessage --routing-key org.fedoraproject.prod.buildsys.task.state.change
```
