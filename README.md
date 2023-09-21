# Atrium API

This small project is a part of a potential larger project, a software that can calculate the Financial Break-Even Point for a glasses sales company, Atrium.

In this stage, we created an API to put into practice everything that was learned during sprint 1, Basic FullStack Development, in the **FullStack Development Specialization** at PUC-Rio

---
## How execute

Will be necessary to have all the Python libraries listed in the `requirements.txt` installed. 
After cloning the repository, will be necessary to navigate to the root directory through the terminal to execute the commands described below.

> It is strongly recommended to use virtual environments like [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

```
(env)$ pip install -r requirements.txt
```

This command installs the dependencies/libraries described in the file `requirements.txt`.

To execute the API, just execute the following command:

```
(env)$ flask run --host 0.0.0.0 --port 5050
```

Open [http://localhost:5050/#/](http://localhost:5050/#/) in the browser, to check the status of the running API.
