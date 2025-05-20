# CHANGELOG


## v1.0.0 (2025-05-20)

### Bug Fixes

- Fixed update and reset command
  ([`6a17c52`](https://github.com/Aydin-ab/cardwise/commit/6a17c5242644997e79bf4f2e370516da03474353))

### Build System

- Updated deps
  ([`c89e78d`](https://github.com/Aydin-ab/cardwise/commit/c89e78d47f858585e7cf4085a50d489d260e6851))

### Continuous Integration

- Adding dev commands (lint, type, tox)
  ([`20d73a9`](https://github.com/Aydin-ab/cardwise/commit/20d73a915d8e7c4658e6877233a1029d46ff000b))

- Adding extra md files
  ([`c486a36`](https://github.com/Aydin-ab/cardwise/commit/c486a363064e259fc4ed75597912ab818c461f0f))

- Adding pre-commit config file
  ([`7cedaa0`](https://github.com/Aydin-ab/cardwise/commit/7cedaa09db425fb0385ee74b6977dd89837f9a60))

- Remove prod data
  ([`ae781b3`](https://github.com/Aydin-ab/cardwise/commit/ae781b38d401cfb102f951d91e4b77e9845db31e))

- Removed hardcoded version in favor of importlib.metadata
  ([`3d1016c`](https://github.com/Aydin-ab/cardwise/commit/3d1016c2e51b54ca7e899c7287dd3e0ea7a3722d))

### Documentation

- Added template + fixed gitgnore
  ([`3b90da5`](https://github.com/Aydin-ab/cardwise/commit/3b90da54ba011ab7098c3e29c5e1dcb329ec1269))

- Adding a README.md
  ([`2557c2d`](https://github.com/Aydin-ab/cardwise/commit/2557c2d7301b921e91f8db08f66a767e91ac4264))

- Adding a todo list and contributing new banks tutorial
  ([`9df87b5`](https://github.com/Aydin-ab/cardwise/commit/9df87b59f4088bf30f7261580786cee82f646afe))

- Adding contributions.md
  ([`571d554`](https://github.com/Aydin-ab/cardwise/commit/571d5547b190771460ee5328536db7cb13b5295b))

- Adding placeholder bofa
  ([`5b959c2`](https://github.com/Aydin-ab/cardwise/commit/5b959c2d76cae182fd2d4549ca65071d3f7ea692))

- Adding placeholder capital one
  ([`4801dc9`](https://github.com/Aydin-ab/cardwise/commit/4801dc936e9258ad88d8905506b23cb6d49aae6e))

- Adding placeholder chase
  ([`1751810`](https://github.com/Aydin-ab/cardwise/commit/175181067155ccfa5ea7f1a82b02cdc3c4126779))

- Remove htmls/
  ([`174d3cd`](https://github.com/Aydin-ab/cardwise/commit/174d3cd219a801f552007eb4af182d0c220bfa47))

### Refactoring

- Refactor to OOP design
  ([`facd35f`](https://github.com/Aydin-ab/cardwise/commit/facd35fca1084b0bf56e94dc523e203ba11e8232))

The cardwise package has been deeply refactored, using a more OOP approach. All classes and
  functions have been reorganized into separate modules, and the CLI has been moved to a new module.
  This refactor aims to enhance the maintainability and readability of the codebase. The following
  changes have been made:

BREAKING CHANGE: the CLI is not used the same way anymore.

### Testing

- Adapted tests to new OOP design
  ([`6c6a040`](https://github.com/Aydin-ab/cardwise/commit/6c6a040da444d9fb750dfce94c66aa3c94c757f2))

### Breaking Changes

- The CLI is not used the same way anymore.


## v0.0.4 (2025-05-17)

### Bug Fixes

- Test again to see if it changes the verison numbers
  ([`de81c2e`](https://github.com/Aydin-ab/cardwise/commit/de81c2e2d3f9f0f757a200e3245e8ca602818b86))


## v0.0.3 (2025-05-17)

### Bug Fixes

- To see if it triggers semantic relase gh actions
  ([`c0cafb9`](https://github.com/Aydin-ab/cardwise/commit/c0cafb922e3a48172b9fcc54c74c6268ef1d9ffa))

### Continuous Integration

- Add config for semantic release
  ([`1a4fb60`](https://github.com/Aydin-ab/cardwise/commit/1a4fb60a6a4102a42638359855a116a1608c40cf))

- Add config for semantic release
  ([`3dffcdf`](https://github.com/Aydin-ab/cardwise/commit/3dffcdfb87ca7ea9d00c2187ec1498815a4bd571))

- Added a test container
  ([`49a9817`](https://github.com/Aydin-ab/cardwise/commit/49a9817d1486ba34ade1cce3348a61824164435c))

- Added config parameters for semantic release
  ([`fbc086e`](https://github.com/Aydin-ab/cardwise/commit/fbc086e16038f27673735ebcbbe5b2b24c260ddb))

- Changed commitlint precommit
  ([`2d9c7f8`](https://github.com/Aydin-ab/cardwise/commit/2d9c7f88eb19116c6d2db3a10d67b6a6d7c63bb0))

- Changed location of __init__ and version number
  ([`8e2d8e9`](https://github.com/Aydin-ab/cardwise/commit/8e2d8e994b203877a20fe41e495313b8a8dc8b09))

- Changed location of __init__ and version number
  ([`bf7e964`](https://github.com/Aydin-ab/cardwise/commit/bf7e964574f463380e13307e25cc190800414361))

- Changed location of __init__ and version number
  ([`86d868c`](https://github.com/Aydin-ab/cardwise/commit/86d868c90416e31f47f217fa9b48af815472ba0d))

- Remove useless command
  ([`5525192`](https://github.com/Aydin-ab/cardwise/commit/5525192610affde77e91147510716105a44ea8c1))

- Try next version ?
  ([`9fd5085`](https://github.com/Aydin-ab/cardwise/commit/9fd50851f9a54fad5fdb8e5ebfcc6ae6d0878d2a))


## v0.0.2 (2025-05-15)

### Bug Fixes

- Fix import errors in mocks
  ([`35cea9c`](https://github.com/Aydin-ab/cardwise/commit/35cea9c503d72667627814be1bbab8adde8bff7b))

### Build System

- Dockerfile, compose and dev container
  ([`f4af47d`](https://github.com/Aydin-ab/cardwise/commit/f4af47d7043494a3760859e3c8dc158e09bc31dd))

- Redesign src/ tree to follow poetry pattern
  ([`64f8450`](https://github.com/Aydin-ab/cardwise/commit/64f8450c947bf0ef24349e0572666310f0530992))

### Code Style

- Add reference link to semantic release
  ([`6df3753`](https://github.com/Aydin-ab/cardwise/commit/6df375337108dedf607df93304cef1ca9a9d5311))

- Added list of types to help doing good commits
  ([`7a41d02`](https://github.com/Aydin-ab/cardwise/commit/7a41d02470134ebc155389bc5de61c5cef8cca10))

- Fix style and format from import
  ([`3e7cb01`](https://github.com/Aydin-ab/cardwise/commit/3e7cb01aed09128800a51b8da153a9d295717453))


## v0.0.1 (2025-03-28)

### Bug Fixes

- Example
  ([`6923c62`](https://github.com/Aydin-ab/cardwise/commit/6923c62f8ad24ed1baa0b4a3f3b06ae767f70fc7))

- Just a test
  ([`19c04f7`](https://github.com/Aydin-ab/cardwise/commit/19c04f76355165e1444d8c953dff033d7ca46604))

- Smthg
  ([`1cad8ec`](https://github.com/Aydin-ab/cardwise/commit/1cad8ecf44efc0018a7081f843b11bec626ebd14))

- Try again
  ([`95c42ce`](https://github.com/Aydin-ab/cardwise/commit/95c42ce1d16e6a27779188159e89f1c103e80653))

- Trying againn
  ([`8ea7488`](https://github.com/Aydin-ab/cardwise/commit/8ea74888ea129b493747f20454382ec7f03434f7))

### Chores

- **release**: 0.0.0
  ([`7cb2fb5`](https://github.com/Aydin-ab/cardwise/commit/7cb2fb5476d760092f1820b52dea049325eb6ea2))


## v0.0.0 (2025-03-25)
