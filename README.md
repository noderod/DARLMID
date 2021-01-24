# Expert-SEAS

Expert-Guided ML for 2D ship piloting



## Objective

To use experts (humans, most likely, although not necessarily) in order to train a neural network in piloting in ship without crashing.
The expert piloting data is expected to lead to an output that ressembles' the pilot.


## Development History

This project was started as a possible final project for CS 5170 in Northeastern University, Spring 2021 semester.


## Deployment

```bash
cd server
docker-compose up -d --build


```


Note, to bring the containers down:
```bash
docker-compose down -v
```



## References

1. https://docs.aiohttp.org/en/stable/deployment.html
2. https://stackoverflow.com/questions/52569051/aiohttp-and-nginx-running-in-docker
3. https://docs.gunicorn.org/en/stable/install.html
4. https://docs.gunicorn.org/en/stable/install.html
5. https://docs.docker.com/storage/volumes/
6. https://docs.nginx.com/nginx/admin-guide/web-server/serving-static-content/
7. http://nginx.org/en/docs/beginners_guide.html#static
8. https://mkyong.com/html/html-tutorial-hello-world/
9. https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Flexible_Box_Layout/Aligning_Items_in_a_Flex_Container
10. https://www.w3schools.com/html/tryit.asp?filename=tryhtml_images_trulli
11. https://www.digitalocean.com/community/tutorials/how-to-configure-nginx-to-use-custom-error-pages-on-ubuntu-14-04
12. https://commons.wikimedia.org/wiki/File:Aft_(PSF).png
13. https://hub.docker.com/_/postgres
14. https://stackoverflow.com/questions/45128902/psycopg2-and-sql-injection-security
15. https://docs.github.com/en/github/importing-your-projects-to-github/adding-an-existing-project-to-github-using-the-command-line
