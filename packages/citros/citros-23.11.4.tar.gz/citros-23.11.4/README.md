```python
# ==============================================
#   ██████╗██╗████████╗██████╗  ██████╗ ███████╗
#  ██╔════╝██║╚══██╔══╝██╔══██╗██╔═══██╗██╔════╝
#  ██║     ██║   ██║   ██████╔╝██║   ██║███████╗
#  ██║     ██║   ██║   ██╔══██╗██║   ██║╚════██║
#  ╚██████╗██║   ██║   ██║  ██║╚██████╔╝███████║
#   ╚═════╝╚═╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚══════╝                                        
# ==============================================
```
# CiTROS CLI

# description:

the CiTROS cli will run by the user. 
inside the ros-project folder. 


## install locally

```bash
python3 -m pip install -e .
```

# TODO


## Docker:
- [ ] Build Dockerfile 
  - [ ] add pip install citros to docker  
- [ ] Push docker to repo 
-  [ ] Repo triggers Batch run?
- [ ] get status from server Monitoring? (batchs, simulations, events?, notifications? )

## ROS
- [ ] build ros project

## DATA analysis
- [ ] get data from DB. (mongo)
  - [ ] Basic queries - number of batchs, simulations. amount of data used... delete batch? simulation? 


# Bugs.
Parser 
- [ ] Fix parser for parameters. parse launch file and extract parameters from it. (file, loaded)
- [ ] requirements.txt 
- [ ] check why doesn't work on non [root] user under devcontainer. 

## Documentation
- [ ] TODO: create documentation for the code, use: 
  - [ ] pyment -w citros_events.py

# Mongo

    docker run -d -p 27017:27017 --name mongo mongo:latest

