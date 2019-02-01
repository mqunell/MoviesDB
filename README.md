# MoviesDB

![Image of the GUI](https://i.imgur.com/QYlUK3j.png)


<br/>

## Overview

MoviesDB is a project meant to help track the movies I own across various formats. The program...
* Is written in Python
* Uses a PyQt5 GUI to simplify adding individual series/movies and for displaying the database
* Retrieves data from IMDb using the [OMDb API](http://www.omdbapi.com/)
* Stores data in a MariaDB database
* Allows bulk-adding from plaintext files
* Is the expansion of my previous project, [SQL_Insertions](https://github.com/mqunell/SQL_Insertions)


<br/>

## Adding Movies

The amount of information needed as a user is minimal.

Series info:
* The name of the series (such as "MCU" or "Harry Potter")
* The number of movies in the series

Movie info:
* Title
* Whether or not it's part of a series
  * If so, which number it is in the series
* Owned formats (DVD, Blu-ray, 4K Blu-ray, downloaded to hard drive, and/or Movies Anywhere)

<br/>

Thanks to the OMDb API, the following information about movies is retrieved automatically:
* Release year
* MPAA rating
* Runtime
* Genre
* Director
* Main actors
* Plot overview
* Link to poster
* Metacritic score


<br/>

## Database Setup
```
$ sudo mysql_secure_installation

> create user 'username'@'localhost' identified by 'password';
> create database Movies;
> grant all on Movies.* to 'username'@'localhost' identified by 'password';

$ sudo systemctl restart mariadb.service

> source {path}/CreateTables.sql;
```