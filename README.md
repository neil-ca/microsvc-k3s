# Services in k3s
It's good to have tools like k3s, small and powerful,
you can focus on deploy new features 
Updating the mongo config in `mongod.conf`

Requests to test the services
```sh
curl -X POST http://mp3converter.com/login -u neil@gmail.com:secret

curl -X POST -F 'file=@./test.mp4' -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Im5laWxAZ21haWwuY29tIiwiZXhwIjoxNjk2MTExNzY0LCJpYXQiOjE2OTYwMjUzNjQsImFkbWluIjp0cnVlfQ.oOpTJhC_jgqL87TCaWUdwFDDGksLjHRsWsX7XLzwLrU' http://mp3converter.com/upload
```
