# CHANGELOG


## v1.0.2 (2025-06-17)

### Bug Fixes

- Allow CORS origin
  ([`22a14f1`](https://github.com/Aydin-ab/cardwise/commit/22a14f1b221a3fbb786e116a8ccf1d991d5f7556))

### Chores

- Add error handling in instanciation
  ([`506b77e`](https://github.com/Aydin-ab/cardwise/commit/506b77e163405665e6f4b80d5e887565a565e9c2))

### Continuous Integration

- Add command for fastapi and flutter
  ([`9c47da5`](https://github.com/Aydin-ab/cardwise/commit/9c47da5da6d130ad37c4275a9bc7e9bfa7b38e71))

- Adding dummy readme to keep logs folder alive
  ([`fffdb8b`](https://github.com/Aydin-ab/cardwise/commit/fffdb8b8f5e03e719ba508d019b1b83d116a05e6))

- Fix dockerfile name
  ([`ac76610`](https://github.com/Aydin-ab/cardwise/commit/ac766105a63c839cf28c9f1bf41dbebe9f7147e7))

- Fixed argument to pip audit
  ([`9819a68`](https://github.com/Aydin-ab/cardwise/commit/9819a68117ca76ca3c5d7c733f2ea62a2bcf629b))

- Fixed argument to pip audit
  ([`9660050`](https://github.com/Aydin-ab/cardwise/commit/9660050986bf0ab7624efbe0ca69b79e10dba57b))

- Ignore long log files
  ([`ca54eae`](https://github.com/Aydin-ab/cardwise/commit/ca54eae3ec540b5771802b93eed47d8c4d3b5173))

- Prepare render serving backend
  ([`5ec718d`](https://github.com/Aydin-ab/cardwise/commit/5ec718d647167f5eb0def66a9e5cffb102a2160e))

- Remove data files
  ([`776276c`](https://github.com/Aydin-ab/cardwise/commit/776276c61047d82b637aea339af80584d116ab8a))

- Remove pip audit unneceseary check on specific error
  ([`b70d22e`](https://github.com/Aydin-ab/cardwise/commit/b70d22e1600a0961f67c30996ff29783f4924aba))

- Remove sqlite database
  ([`5a7942c`](https://github.com/Aydin-ab/cardwise/commit/5a7942c6ffba38d89e001e9388279f850302d859))

- Update to backend api
  ([`f3f146a`](https://github.com/Aydin-ab/cardwise/commit/f3f146aca050281602c776f98169774e9de8c469))

### Documentation

- Update text about adding new parser
  ([`0bf60e1`](https://github.com/Aydin-ab/cardwise/commit/0bf60e1dd62a057e9b58f0d92e04be69ce703b35))

### Refactoring

- Abstract objects to higher level CLI script
  ([`c6077d8`](https://github.com/Aydin-ab/cardwise/commit/c6077d8211c905eb30e077db28cb878888b439bb))

- Change string to enum to avoid test error in python 3.11+
  ([`e208f8a`](https://github.com/Aydin-ab/cardwise/commit/e208f8a9ba9c68b768075d8fbf5fa524d11126ed))

- Changed name of OfferRepository class
  ([`a2c6b28`](https://github.com/Aydin-ab/cardwise/commit/a2c6b2872d69c1c2c10c43f1b613720ffe8798d5))

- Deleted data folder
  ([`4e3dc6a`](https://github.com/Aydin-ab/cardwise/commit/4e3dc6ada23afdd12beabc56bbba45162166f382))

- Deleted src/ layout
  ([`b6b7f89`](https://github.com/Aydin-ab/cardwise/commit/b6b7f8955df901bb60534f9b1adf6575abe0a8fe))

- Separate services
  ([`925cc77`](https://github.com/Aydin-ab/cardwise/commit/925cc779efecd1c7441749f68a5110924ddd69b7))

- Updated path to log files to new layout
  ([`6dc12fe`](https://github.com/Aydin-ab/cardwise/commit/6dc12fe35061b8f050ec639e39753b0a9f366c1a))

- Write tests
  ([`f09e2af`](https://github.com/Aydin-ab/cardwise/commit/f09e2afe854c13b2bb5d97fed66a5786d514e0b2))


## v1.0.1 (2025-06-11)

### Bug Fixes

- Fixed search_offers command
  ([`8acaf82`](https://github.com/Aydin-ab/cardwise/commit/8acaf8200054227b5e6cdb3108acf805fc8b3758))

- Intermediate set to handle duplicated Offers
  ([`f35fc03`](https://github.com/Aydin-ab/cardwise/commit/f35fc03d833cc97768a7e2cf22907b7117efb43b))

### Build System

- Added coloredlogs dependency
  ([`8096286`](https://github.com/Aydin-ab/cardwise/commit/80962868f72a8599b6308a8daa0bfc7e4d14e5e9))

- Added sqllite deps
  ([`8e211f5`](https://github.com/Aydin-ab/cardwise/commit/8e211f52ef0d328cf4c44a8ab4a9d5632e12e867))

### Performance Improvements

- Added sqllite sqlmodel logic
  ([`f557702`](https://github.com/Aydin-ab/cardwise/commit/f557702c243003227e9ec0d3a7dab0f7d2013b62))

### Refactoring

- Mobile app friendly layout
  ([`29935f2`](https://github.com/Aydin-ab/cardwise/commit/29935f216e9c210a37c2764f2133676aaf1a34c7))

- Updated imports in tests to new layout
  ([`e58cd3c`](https://github.com/Aydin-ab/cardwise/commit/e58cd3c88528e3453177e59e43dff20c391b844c))


## v1.0.0 (2025-05-20)

### Bug Fixes

- Fixed update and reset command
  ([`6a17c52`](https://github.com/Aydin-ab/cardwise/commit/6a17c5242644997e79bf4f2e370516da03474353))

### Build System

- Remove python 3.9
  ([`60b38a3`](https://github.com/Aydin-ab/cardwise/commit/60b38a3c9b6b26c9752d0ab62eea1d6438aadea8))

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
