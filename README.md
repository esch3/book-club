# book-club
An app that allows user to read and create book reviews.

To install:
Spin up an EC2 Ubuntu Server. Configure security group to allow hosts on 80 as this app is a demo on how to hit the ground running and serve external clients on port 80 for motivation. 
Log into ubuntu server.
Type the following commands.

$ sudo apt update
$ sudo apt install python3-pip
$ git clone <this-repo>
$ cd book-club/
$ pip3 install -e .
$ flask run
  
Type the DNS or IP of your instance into your browser and check out the Bookclub!
  

 
