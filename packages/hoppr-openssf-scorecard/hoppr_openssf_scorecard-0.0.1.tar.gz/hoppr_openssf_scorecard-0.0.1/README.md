# Hoppr OpenSSF Scorecard Plugin

Plugin for [Hoppr](https://hoppr.dev) to populate component metadata in a [CycloneDX](https://cyclonedx.org) Software Bill of Materials (SBOM) with data from [OpenSSF Scorecard](https://securityscorecards.dev).

## How to use this plugin

### Get a Libraries.io API key

In order to use this plugin, an API key from `Libraries.io` is required.

- Log in to [Libraries.io](https://libraries.io) using a GitHub, GitLab, or BitBucket account
- Retrieve the API key from [account settings](https://libraries.io/account)

Once you have this API key, you can provide it to the plugin in one of the following ways:

- Set the `LIBRARIES_API_KEY` environment variable in the shell before running Hoppr

    ```shell
    export LIBRARIES_API_KEY="<your key here>"
    ```

- Create a [Hoppr credentials file](https://hoppr.dev/docs/using-hoppr/tutorials/processing-101#credentials) with an entry for `https://libraries.io/api` and an environment variable of your choosing that holds the value of the API key

    ```yaml
    ---
    schemaVersion: v1
    kind: Credentials

    credential_required_services:
      - url: https://libraries.io/api
        user: ""
        pass_env: API_KEY_ENV_VAR
    ```

### Create a transfer file

A [Hoppr transfer file](https://hoppr.dev/docs/using-hoppr/tutorials/processing-101#transfers) defines the stages to be run and which plugins will be run in those stages.

Create a transfer file that defines a stage with this plugin (identified by `hoppr_openssf_scorecard.plugin`) specified. For example:

```yaml
---
schemaVersion: v1
kind: Transfer

stages:
  ScorecardData:
    plugins:
      - name: hoppr_openssf_scorecard.plugin
  Bundle:
    plugins:
      - name: hoppr.core_plugins.bundle_tar
        config:
          tarfile_name: tarfile.tar.gz

max_processes: 10
```

### Run Hoppr

That's everything! Run `hopctl bundle` as normal and the SBOM with Scorecard data will be located in the specified bundle file.

## How does it work?

### Get the source control repository URL

Various API endpoints are leveraged in an attempt to retrieve a component's source control repository URL in order to request a Scorecard report.

First, a REST API or well-known metadata URL for the package manager specific to the PURL type of the component is tried.

| PURL Type | URL Endpoint(s)                                                                                        |
| --------- | ------------------------------------------------------------------------------------------------------ |
| `deb`     | `https://sources.debian.org/api` for Debian, `https://api.launchpad.net/1.0` for Ubuntu                |
| `gem`     | `https://rubygems.org/api/v1`                                                                          |
| `git`     | Searches both `https://api.github.com` and `https://gitlab.com/api/v4`                                 |
| `golang`  | First `https://proxy.golang.org`, then `https://libraries.io/api/Go` if not found |
| `helm`    | `https://artifacthub.io/api/v1/packages/helm`                                                          |
| `maven`   | First, `https://search.maven.org/remotecontent`, then `https://libraries.io/api/Maven` if not found                                                               |
| `npm`     | `https://registry.npmjs.com`                                                                           |
| `pypi`    | `https://pypi.org/pypi`                                                                                |
| `rpm`     | Repository metadata from either `rpm` repositories defined in the manifest file, or sensible defaults. |

These are the defaults for RPM components if not provided.

| Distribution          | Metadata URL                                                                                                                                                                                                                                        |
| --------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Red Hat 7             | `http://mirror.centos.org/centos/7/os/x86_64`<br>`http://mirror.centos.org/centos/7/extras/x86_64`                                                                                                                                                  |
| Red Hat/Rocky Linux 8 | `https://dl.rockylinux.org/pub/rocky/8/AppStream/x86_64/os`<br>`https://dl.rockylinux.org/pub/rocky/8/BaseOS/x86_64/os`<br>`https://dl.rockylinux.org/pub/rocky/8/PowerTools/x86_64/os`<br>`https://dl.rockylinux.org/pub/rocky/8/extras/x86_64/os` |
| Red Hat/Rocky Linux 9 | `https://dl.rockylinux.org/pub/rocky/9/AppStream/x86_64/os`<br>`https://dl.rockylinux.org/pub/rocky/9/BaseOS/x86_64/os`<br>`https://dl.rockylinux.org/pub/rocky/9/CRB/x86_64/os`<br>`https://dl.rockylinux.org/pub/rocky/9/extras/x86_64/os`        |
| Fedora                | `https://dl.fedoraproject.org/pub/fedora/linux/releases/<Fedora release>/Everything/x86_64/os`                                                                                                                                                      |

If a source control repository isn't found this way, the next attempt is to search `Libraries.io` and try to narrow down and intuit the correct repo URL from the results.

Finally, as a last-ditch effort, the GitHub API is queried in a similar fashion. If no repository URL is found by this point, the component is skipped and the plugin will move on to the next one.

If a repository URL was found during any of these passes, it gets added to the SBOM compoment's `externalReferences` as a URL with a type of `vcs`.

### Request the report data from Scorecard API

For components that have a `vcs` repository URL (whether identified as outlined in the previous section or explicitly defined in the SBOM), a request is made to the OpenSSF Scorecard API using that project URL.

The response data is then used to populate the SBOM according to the taxonomy outlined below.

## SBOM property taxonomy

Properties generated by this plugin consist of a `name` prefixed with `hoppr:scorecard` and a `value` corresponding to the associated Scorecard field.

| Name                                         | Description                                             |
| -------------------------------------------- | ------------------------------------------------------- |
| hoppr:scorecard:date                         | Date of the Scorecard report                            |
| hoppr:scorecard:metadata                     | Metadata for the Scorecard report                       |
| hoppr:scorecard:repo:commit                  | Commit ref/SHA the report was run on                    |
| hoppr:scorecard:repo:name                    | Name of the repository                                  |
| hoppr:scorecard:score                        | Aggregate score for all checks                          |
| hoppr:scorecard:scorecard:commit             | Commit ref/SHA of Scorecard used to generate the report |
| hoppr:scorecard:scorecard:version            | Version of Scorecard used to generate the report        |
| hoppr:scorecard:check:Binary-Artifacts       | Score for the `Binary-Artifacts` check                  |
| hoppr:scorecard:check:Branch-Protection      | Score for the `Branch-Protection` check                 |
| hoppr:scorecard:check:CI-Tests               | Score for the `CI-Tests` check                          |
| hoppr:scorecard:check:CII-Best-Practices     | Score for the `CII-Best-Practices` check                |
| hoppr:scorecard:check:Code-Review            | Score for the `Code-Review` check                       |
| hoppr:scorecard:check:Contributors           | Score for the `Contributors` check                      |
| hoppr:scorecard:check:Dangerous-Workflow     | Score for the `Dangerous-Workflow` check                |
| hoppr:scorecard:check:Dependency-Update-Tool | Score for the `Dependency-Update-Tool` check            |
| hoppr:scorecard:check:Fuzzing                | Score for the `Fuzzing` check                           |
| hoppr:scorecard:check:License                | Score for the `License` check                           |
| hoppr:scorecard:check:Maintained             | Score for the `Maintained` check                        |
| hoppr:scorecard:check:Packaging              | Score for the `Packaging` check                         |
| hoppr:scorecard:check:Pinned-Dependencies    | Score for the `Pinned-Dependencies` check               |
| hoppr:scorecard:check:SAST                   | Score for the `SAST` check                              |
| hoppr:scorecard:check:Security-Policy        | Score for the `Security-Policy` check                   |
| hoppr:scorecard:check:Signed-Releases        | Score for the `Signed-Releases` check                   |
| hoppr:scorecard:check:Token-Permissions      | Score for the `Token-Permissions` check                 |
| hoppr:scorecard:check:Vulnerabilities        | Score for the `Vulnerabilities` check                   |
| hoppr:scorecard:check:Webhooks               | Score for the `Webhooks` check                          |

For descriptions of all the checks performed by Scorecard, see [this table](https://github.com/ossf/scorecard#scorecard-checks).
