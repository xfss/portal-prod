# portal

> Portal project

## Build Setup

``` bash
# install dependencies
npm install

# serve with hot reload at localhost:8080
npm run dev

# build for production with minification
npm run build

# build for production and view the bundle analyzer report
npm run build --report

# run unit tests
npm run unit

# run e2e tests
npm run e2e

# run all tests
npm test
```

For a detailed explanation on how things work, check out the [guide](http://vuejs-templates.github.io/webpack/) and [docs for vue-loader](http://vuejs.github.io/vue-loader).


## Semantic UI build

For Semantic UI to work it is needed to build the vendor files with gulp. For that gulp needs to be installed globally:

    npm i gulp -g

After this semantic can be built with the following command:

    gulp build

The command should be run from the semantic folder which is located at:

    frontend/src/vendors/semantic/

 This will populate the dist folder for semantic, which in turn will be used by App.vue to load the minified css file.
