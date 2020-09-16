# Test task for "Analysis of Socio-Technical Congruence"

## Description

This project visualizes proximity of top 50 [react's contributors](https://github.com/facebook/react/graphs/contributors?from=2013-05-26&to=2020-09-04&type=c) as a graph where vertices represent contributors and edges represent their proximity.

Lengths of the edges reflect relative amount of files modified by both users on the edges ends.

## Installing dependencies

Python3 and pip3 are required to run this project. Use pip to install essential python packages:
```
pip3 install -r requirements.txt
```

## Collecting contributor's commits

First we need to collect a list of commits for each of top 50 contributors.

You will need a github auth token with public access to be able to send api requests. It can be obtained [here](https://github.com/settings/tokens).

Use collect.py to collect the commits and save them to file:
```
python3 collect.py commits file_to_save_commits
```
You can find already collected commits in data/commits.txt so you don't need to do it manually.

## Collecting files modified by contributors

As there are too many commits in react repo, it is too difficult to collect all needed information through github api. We will use a local clone of the repo instead.

Clone the repo to your file system:
```
cd path/to/clone/repo && git clone https://github.com/facebook/react/
```
Then use collect.py to collect modified files and save them to file:
```
python3 collect.py file_with_commits file_to_save_files path/to/react/
```
You can find already collected files in data/files.txt so you don't need to do it manually.

## Running the visualization

Use visualise.py to see the graph from collected data:
```
python3 visualise.py file_with_files
```

## Visualization control

You can move the picture with 'w', 'a', 's' and 'd' keys.

You can also zoom in and out with 'e', and 'q' keys.

Finally, you can alter edges weight threshold with 'z' and 'c' keys.