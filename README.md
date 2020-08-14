# fed-image-watcher

```sh
fedora-messaging --conf config.toml consume --callback-file=./tcallback/t.py:SaveMessage --routing-key org.fedoraproject.prod.pungi.compose.status.change
```
