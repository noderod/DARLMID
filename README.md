# Expert-SEAS

Expert-Guided ML for 2D ship piloting



## Objective

To use experts (humans, most likely, although not necessarily) in order to train a neural network in piloting in ship without crashing.
The expert piloting data is expected to lead to an output that ressembles' the pilot.


## Development History

This project was started as a possible final project for CS 5170 in Northeastern University, Spring 2021 semester.

PostgreSQL and Redis ports left open instead of merely exposed in case these databases need to be accessed from other servers, this may be modified.


## Deployment

Modify the *.env* file to change the credentials.


Note: *sudo* permission may be necessary.

```bash
cd server
docker-compose up -d --build
```


Note, to bring the containers down:
```bash
docker-compose down -v
```

## Licensing

Parts of this project use libraries ([bleach](https://github.com/mozilla/bleach)) licensed under the terms of the Apache 2 licensed, available in this project [here](/licenses/LICENSE-2.0.txt) and also originally [here](http://www.apache.org/licenses/LICENSE-2.0.txt).


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
16. https://pkgs.alpinelinux.org/package/edge/main/x86/postgresql-dev
17. https://www.w3schools.com/css/css_howto.asp
18. https://www.dummies.com/web-design-development/html5-and-css3/how-to-use-an-external-style-sheet-for-html5-and-css3-programming/
19. https://www.w3schools.com/howto/tryit.asp?filename=tryhow_css_topnav
20. https://stackoverflow.com/questions/8722163/how-to-assign-multiple-classes-to-an-html-container
21. https://www.w3schools.com/colors/colors_names.asp
22. https://www.w3schools.com/howto/howto_css_fixed_footer.asp
23. https://stackoverflow.com/questions/45764517/how-to-return-redirect-response-from-aiohttp-web-server
24. http://demos.aiohttp.org/en/latest/tutorial.html#middlewares
25. https://www.w3schools.com/css/css3_gradients.asp
26. https://stackoverflow.com/questions/29573489/nginx-failing-to-load-css-and-js-files-mime-type-error
27. https://stackoverflow.com/questions/2242086/how-to-detect-the-screen-resolution-with-javascript
28. https://stackoverflow.com/questions/15615552/get-div-height-with-plain-javascript
29. https://stackoverflow.com/questions/19484544/set-height-of-div-to-height-of-another-div-through-css
30. https://www.w3schools.com/js/js_functions.asp
31. https://stackoverflow.com/questions/807878/how-to-make-javascript-execute-after-page-load
32. https://stackoverflow.com/questions/34796085/how-to-stick-footer-to-bottom-not-fixed-even-with-scrolling/34796186
33. https://stackoverflow.com/questions/19039628/how-to-calculate-height-of-viewable-area-i-e-window-height-minus-address-bo
34. https://www.w3schools.com/jsref/event_onresize.asp
35. https://freesvg.org/nemeth-flying-machine
36. https://www.w3schools.com/css/tryit.asp?filename=trycss3_border-radius
37. https://stackoverflow.com/questions/54845686/nginx-wont-serve-svg-files
38. https://www.w3schools.com/tags/tryit.asp?filename=tryhtml_table_test
39. https://www.w3schools.com/html/tryit.asp?filename=tryhtml_form_submit
40. https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/minlength
41. https://stackoverflow.com/questions/1297449/change-image-size-with-javascript
42. https://stackoverflow.com/questions/9686538/align-labels-in-form-next-to-input
43. https://freesvg.org/international-space-station-vector-drawing
44. https://www.w3schools.com/cssref/css_units.asp
45. https://www.w3schools.com/jsref/tryit.asp?filename=tryjsref_form_submit
46. https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/length
47. https://stackoverflow.com/questions/6199773/how-to-enable-disable-an-html-button-based-on-scenarios
48. https://stackoverflow.com/questions/195951/how-can-i-change-an-elements-class-with-javascript
49. https://stackoverflow.com/questions/3547035/javascript-getting-html-form-values
50. https://stackoverflow.com/questions/32459646/removing-the-shadow-from-a-button
51. https://stackoverflow.com/questions/15110484/javascript-how-to-append-div-in-begining-of-another-div
52. https://developer.mozilla.org/en-US/docs/Web/API/ParentNode/prepend
53. https://stackoverflow.com/questions/16584121/change-div-id-by-javascript
54. https://stackoverflow.com/questions/596467/how-do-i-convert-a-float-number-to-a-whole-number-in-javascript
55. https://stackoverflow.com/questions/11722400/programmatically-change-the-src-of-an-img-tag
56. https://stackoverflow.com/questions/21727317/how-to-check-confirm-password-field-in-form-without-reloading-page
57. https://stackoverflow.com/questions/39449739/aiohttp-how-to-retrieve-the-data-body-in-aiohttp-server-from-requests-get
58. https://stackoverflow.com/questions/52246796/await-a-method-and-assign-a-variable-to-the-returned-value-with-asyncio
59. https://stackoverflow.com/questions/46428889/keeping-pycache-out-of-my-repository-when-adding-committing-from-pythonany
60. https://www.w3schools.com/css/tryit.asp?filename=trycss_table_align_center
61. https://stackoverflow.com/questions/29775797/fetch-post-json-data
62. https://github.com/ritua2/gib/blob/master/middle-layer/.env
63. https://github.com/ritua2/gib/blob/master/middle-layer/docker-compose.yml
64. https://hub.docker.com/_/redis
65. https://www.psycopg.org/docs/module.html#psycopg2.connect
66. https://www.postgresqltutorial.com/postgresql-create-table/
67. https://stackoverflow.com/questions/50070877/postgres-psycopg2-create-table
68. https://www.postgresql.org/docs/8.0/sql-createuser.html
69. http://oliviertech.com/python/generate-SHA512-hash-from-a-String/
70. https://stackoverflow.com/questions/4244896/dynamically-access-object-property-using-variable
71. https://stackoverflow.com/questions/45018338/javascript-fetch-api-how-to-save-output-to-variable-as-an-object-not-the-prom/45018619
72. https://tldrlegal.com/license/apache-license-2.0-(apache-2.0)
73. http://www.apache.org/licenses/LICENSE-2.0.txt
74. https://github.com/mozilla/bleach
75. https://bleach.readthedocs.io/en/latest/clean.html
76. https://github.com/aio-libs/aiohttp/blob/master/examples/web_cookies.py
77. https://stackoverflow.com/questions/26745519/converting-dictionary-to-json
78. https://github.com/js-cookie/js-cookie
79. https://docs.aiohttp.org/en/stable/web_reference.html
