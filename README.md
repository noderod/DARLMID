# DARLMID

Expert-Guided ML for 2D car driving trained under intentionally poor demonstrations.



## Objective

To use experts (humans, most likely, although not necessarily) in order to train a neural network in driving a car without crashing, providing
only intentionally poor driving demonstrations.


## Development History

This project was started as a possible final project for CS 5170 in Northeastern University, Spring 2021 semester.

PostgreSQL and Redis ports left open instead of merely exposed in case these databases need to be accessed from other servers, this may be modified.

## Development

```bash
make dev
```

Then visit http://localhost:8080/ to see the website running.

## Space




## Understanding JSON output files







## Required software and libraries

Software:
* Docker

Python3 libraries:
* matplotlib
* numpy
* shapely



## Deployment

1. Generate the necessary matrices and data

Example:

```bash
python3 create_circuit.py --circuit circuits/five.json --output circuits/five_Q_matrix.json --show
```

To show all the options:

```bash
python3 create_circuit.py --help
```


2. Setup the docker containers

Modify the *.env* file to change the credentials.


Note: *sudo* permission may be necessary.

```bash
cd server
make deploy
```


Note, to bring the containers down:
```bash
make teardown
```



## Licensing

Parts of this project utilize software and images which are licensed under different conditions. An overview of these materials, licenses,
and conditions is provided in the [licenses](./server/licenses) subdirectory.



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
80. https://docs.python.org/3/library/sys.html
81. https://docs.python.org/3/howto/argparse.html
82. https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet
83. https://dillinger.io/
84. https://stackoverflow.com/questions/9215658/plot-a-circle-with-pyplot
85. https://matplotlib.org/3.1.1/gallery/lines_bars_and_markers/fill.html
86. https://stackoverflow.com/questions/2849286/python-matplotlib-subplot-how-to-set-the-axis-range
87. https://www.w3schools.com/python/ref_keyword_assert.asp
88. https://stackoverflow.com/questions/26226816/argparse-making-required-flags
89. https://shapely.readthedocs.io/en/stable/manual.html
90. https://gis.stackexchange.com/questions/95670/creating-shapely-linestring-from-two-points
91. https://docs.blender.org/manual/en/latest/getting_started/installing/linux.html
92. https://www.w3schools.com/html/tryit.asp?filename=tryhtml_table
93. https://commons.wikimedia.org/wiki/File:Car_in_Black_Rock_Desert.jpg
94. https://smallbusiness.chron.com/crop-circle-out-picture-gimp-36366.html
95. https://splidejs.com/getting-started/
96. https://www.w3schools.com/tags/att_script_defer.asp
97. https://splidejs.com/
98. https://stackoverflow.com/questions/15121343/how-to-center-a-p-element-inside-a-div-container
99. https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/Storsj%C3%B6n_i_Vindelns_kommun.jpg/1280px-Storsj%C3%B6n_i_Vindelns_kommun.jpg
100. https://web.dev/browser-level-image-lazy-loading/
101. https://davidwalsh.name/lazyload-image-fade
102. https://developer.mozilla.org/en-US/docs/Web/API/Element/removeAttribute
103. Asked some of Carlos' friends for feedback on the front-end's look
104. https://stackoverflow.com/questions/534839/how-to-create-a-guid-uuid-in-python
105. https://aioredis.readthedocs.io/en/v1.3.0/examples.html
106. https://aioredis.readthedocs.io/en/v1.3.0/mixins.html
107. https://aioredis.readthedocs.io/en/v1.3.0/api_reference.html
108. https://redis.io/commands/expire
109. https://www.w3schools.com/tags/tryit.asp?filename=tryhtml5_script_async
110. https://wiki.freecadweb.org/Topological_data_scripting
111. https://json2html.com/
112. https://json2html.com/examples/
113. https://stackoverflow.com/questions/684672/how-do-i-loop-through-or-enumerate-a-javascript-object
114. https://api.jquery.com/jQuery.isEmptyObject/
115. https://code.jquery.com/
116. https://www.quackit.com/html/howto/how_to_make_a_background_image_not_repeat.cfm
117. https://stackoverflow.com/questions/1085801/get-selected-value-in-dropdown-list-using-javascript
118. https://select2.org/getting-started/installation
119. https://select2.org/getting-started/basic-usage
120. https://www.w3schools.com/jsref/jsref_length_array.asp
121. https://stackoverflow.com/questions/30650961/functional-way-to-iterate-over-range-es6-7
122. https://stackoverflow.com/questions/10879045/how-to-set-opacity-in-parent-div-and-not-affect-in-child-div
123. https://github.com/jonobr1/two.js/
124. https://two.js.org/
125. https://www.geeksforgeeks.org/python-os-path-isfile-method/
126. https://www.w3schools.com/jsref/met_element_remove.asp
127. https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Errors/Missing_colon_after_property_id
128. https://jsonlint.com/
129. https://stackoverflow.com/questions/596467/how-do-i-convert-a-float-number-to-a-whole-number-in-javascript
130. https://www.w3schools.com/howto/tryit.asp?filename=tryhow_css_list_without_bullets
131. https://www.w3schools.com/howto/howto_css_list_without_bullets.asp
132. https://code.tutsplus.com/tutorials/drawing-with-twojs--net-32024
133. https://github.com/jonobr1/two.js/issues/144
134. Previous and continuing coursework materials
135. https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Default_parameters
136. https://stackoverflow.com/questions/21227287/make-div-scrollable
137. https://matplotlib.org/stable/gallery/color/named_colors.html
138. https://en.wikiversity.org/wiki/Python_Programming/Classes
