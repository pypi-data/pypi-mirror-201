![Image size](https://badgen.net/badge/docker/size/banayaki/vidis-algorithms)
![Latest update](https://badgen.net/badge/docker/metadata/build-date/banayaki/vidis-algorithms/latest)

# Vidis Algorithms API

This package was build to add new functionality to the ours hyperspectral service (Vidis).
It helps users to add theirs custom algorithms to the service and test them rapidly using hyperspecters uploaded in the service.
In order to accomplish this goal a user must satisfy requirements provided by this API.

# How to use

1. Install `vidis_algorimths_api`
2. Inherit `Task` abstract class and implement it's methods.
3. Prepare docker image
4. Test it
5. Push docker image to any public image repository such as **DockerHub**
6. Add algorithm to the service using special form
![Form](./images/algorithm-adding-dialog.png)

In the [examples](examples/Readme.md) folder some examples are provided

# Restrictions

Beer in mind that some restrictions must be satisfyied before using the algorithm in the service.

1. `get_type_name()` must returns string which satisfies the following regexp
   
    `^([a-z]+|\d+|[-]+)$`

    *(In other words it should be writtent in lower case using only letters, numberse and dashes (-))*
1. `get_type_name()` must not return already occupaied name in the service. 

    *(there is no any sanity checks for this case right now)*