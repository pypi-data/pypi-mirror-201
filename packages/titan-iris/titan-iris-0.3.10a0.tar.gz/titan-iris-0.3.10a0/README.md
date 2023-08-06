# IRIS CLI Package

Simple overview of use/purpose.

## Description

An in-depth paragraph about your project and overview of use.

## Getting Started

### Dependencies

* TODO

### Installing

* TODO 

### Executing program

TODO


**iris get usage**

**iris post usage**


**iris pull usage**

Description: 

The Iris pull command is designed to simplify the process of downloading models from cloud databases. With this command, you can easily download the specified model to your local file system. Once the download is complete, the Iris pull command automatically generates a Docker container that includes both the __Triton__ server image and the __Hephaestus__ code. This provides a seamless, ready-to-go solution that makes it straightforward for users to use and deploy models with minimal effort.

```
iris pull <experiment_id>:<job_tag>
```
- <experiment_id>: the UUID assigned to each experiment.
- <job_tag> the job tag the user would like to download.

job_tag examples: 
- M
- S
- XS
- baseline

__demo:__

Assume we have an experiment with an experiment_id "_4_" that has already been completed and stored in our database. We start by running the following command:

```
iris pull 4:XS 
``` 

Once the command has executed successfully, a new Docker image will be created and saved on the user's machine. You can verify its existence by running:

```
docker images 
```

Now that the Docker image is ready, we can start the Docker container using the following command:

```
docker run -it iris-triton-4:XS
```

After the container starts, you should see the following output. Congratulations! You now have a ready-to-deploy Docker container.

```
root@dec4c93611a0:/usr/local/triton# ls
README.md  VERSION  build  models  requirements.txt  run.sh  setup.py  src
```


## Help

Any advise for common problems or issues.
```
command to run if program contains helper info
```

## Authors

Contributors names and contact info

ex. TODO

## Version History

* 0.1
    * TODO

## License

TODO

## Acknowledgments

TODO
