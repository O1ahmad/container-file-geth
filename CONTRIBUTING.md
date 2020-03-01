# Contributing Guidelines

:heavy_check_mark::tada: Let's make code better together - Thanks for taking the time to contribute! :tada::heavy_check_mark:

The following is a set of guidelines for contributing to *0x0I Container files*, which are hosted under the [0x0I](https://github.com/0x0I?tab=repositories) developer account on GitHub. These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

For general information and guidelines for contributing to these Containerfiles and the Open Containers Initiative community, see the [community page](https://www.opencontainers.org/community).

**Table of Contents**
  - [Pull Requests](#pull-requests)
      - [CI Pipeline](#ci-pipeline)
  - [Issues](#issues)
      - [Issue Types](#issue-types)
  - [Workflow and backlog](#workflow-and-backlog)
  - [Code of Conduct](#code-of-conduct)

## Pull Requests

All [PRs](https://github.com/0x0I/container-file-geth/pulls) are welcome! :+1: The following guidelines and CI pipeline are provided for validating container functionality and avoiding regressions for each submitted request:

**Note:** to build and test this container/image, a working copy of either the `docker` or `podman` container runtimes/engines and the `dgoss` testing framework are necessary.

#### CI Pipeline

| Step | Description | Dependencies | Command |
| --- | --- | --- | --- |
| :construction: `Container file build` | Leverages [Ansible](https://docs.ansible.com/) for defining variable build arguments, per *Containerfile* release/*Image OS distribution*, and building playbooks implementing the end-to-end Containerfile release process. | [ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html) | `ansible-playbook builds/build-playbook.yml` |
| :wrench: `integration testing` | Utilizing the Goss testing framework along with its associated `dgoss` extra package, integration testing of this container file is organized according to the various provisioning phases and should be executed prior to PR submission to validate new modifications and identify/prevent regressions. | [dgoss](https://github.com/aelsabbahy/goss/tree/master/extras/dgoss) | `test/integration_tests.sh` |
| :traffic_light: `Continuous Integration (CI)` | Automatic E2E testing of this role is accomplished leveraging the [Travis-CI](https://travis-ci.com/0x0I/container-file-geth) test infrastructure platform and is executed on each pull request. Requests should not be merged unless all tests pass or the community approves otherwise. | *N/A* | *see* [.travis.yml](https://github.com/0x0I/container-file-geth/blob/master/.travis.yml) for additional details |

## Issues

New GitHub issues can be [opened](https://github.com/0x0I/container-file-geth/issues/new) and [tracked](https://github.com/0x0I/container-file-geth/issues) in a similar fashion as with most Github repositories by making use of the standard Github issue management facilities.

Reference the following issue reporting guide for more details:

#### Issue Types

| Issue Type | Description |
| --- | --- |
| :arrow_up: `:enhancement:` | Feature requests. |
| :bug: `:bug:` | Confirmed bugs or reports that are very likely to be bugs. |
| :question: `:question:` | Questions more than bug reports or feature requests (e.g. how do I do X). |
| :eyeglasses: :heartpulse:`:feedback:` | General feedback more than bug reports or feature requests. |

## Workflow and backlog

Reference this repository's [wiki](https://github.com/0x0I/container-file-geth/wiki) to visualize the project roadmap, workflow and backlog to stay up to speed with development  plans and work in progress.

## Code of Conduct

See the [Open Container Code of Conduct](https://www.opencontainers.org/about/code-of-conduct).
