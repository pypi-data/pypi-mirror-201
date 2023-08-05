# Upgrading

Onionprobe adopts the [Semantic Versioning 2.0.0][], which means that any major
version might have breaking changes on previous installations.

The [ChangeLog][] file contains the list of main changes from version to version, including
breaking changes.

The following subsections documents other upgrade procedures, such as database updates.

[Semantic Versioning 2.0.2]: https://semver.org/spec/v2.0.0.html
[ChangeLog]: https://gitlab.torproject.org/tpo/onion-services/onionprobe/-/blob/main/ChangeLog.md

## Standalone monitoring node

Upgrade procedures for the [standalone monitoring node](standalone.md).

[PostgreSQL]: https://postgresql.org

### PostgreSQL database

This procedure is based on the [tianon/docker-postgres-upgrade][]
approach[^docker-postgres-upgrade] and needs to be done whenever Onionprobe is
upgraded to a new [postgres image][] version:

### Stop the monitoring node

Just run

    docker compose down

### Run the upgrade script

This handy script may do all the heavy lifting for you:

    ./scripts/upgrade-postgresql-database

By default it searches for the `onionprobe_postgres` service containers, but
you can pass the name of your custom container as the optional command line
parameter:

    ./scripts/upgrade-postgresql-database <service-container-name>

As a safeguard measure, the script does not remove it's working directory and
also makes a backup of the old PostgreSQL data. You can manually remove those
later after checking that the upgrade procedure works. Just follow the script
output for instructions or check it's source code.

### Start the monitoring node

Simply start the standalone monitoring node again after the upgrade procedure:

    make run-containers

[tianon/docker-postgres-upgrade]: https://github.com/tianon/docker-postgres-upgrade
[tpo/onion-services/onionprobe#70]: https://gitlab.torproject.org/tpo/onion-services/onionprobe/-/issues/70
[postgres image]: https://hub.docker.com/_/postgres
[^docker-postgres-upgrade]: See [tpo/onion-services/onionprobe#70][] for more information.
